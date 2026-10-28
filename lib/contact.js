'use strict';

/*
  Contact form back end, shared by the Vercel function (api/contact.js) and the Express
  server (server/index.js). Everything private comes from environment variables:

    CONTACT_TO       who receives the messages (falls back to contactTo in site.config.json)
    Email delivery, choose ONE:
      RESEND_API_KEY   a Resend API key (https://resend.com), plus optional CONTACT_FROM
      SMTP_USER + SMTP_PASS (+ SMTP_HOST, SMTP_PORT, SMTP_SECURE)   e.g. Gmail with an App Password
    CONTACT_FROM     sender shown on the email (defaults to SMTP_USER, or Resend's test sender)
    CONTACT_SUBJECT_PREFIX, CONTACT_RATE_MAX, CONTACT_RATE_WINDOW_MIN, CONTACT_MIN_FILL_MS
*/

let fileConfig = {};
try {
  fileConfig = require('../site.config.json');
} catch (e) {
  /* optional file */
}

const EMAIL_RE = /^[^\s@<>"',;:\\]+@[^\s@<>"',;:\\]+\.[^\s@<>"',;:\\]{2,}$/;

const TOPICS = {
  briefing: 'Requesting a briefing',
  border: 'Border perimeter defense',
  'counter-uav': 'Counter-UAV protection',
  maritime: 'Coastal and maritime security',
  recon: 'Analysis and recon planning',
  partnership: 'A partnership',
  careers: 'Careers',
  press: 'Press',
  security: 'A security disclosure',
  other: 'Something else'
};

function env(name, fallback) {
  const v = process.env[name];
  return v === undefined || v === '' ? fallback : String(v).trim();
}

function settings() {
  const smtpUser = env('SMTP_USER', '');
  const gmail = /@(gmail|googlemail)\.com$/i.test(smtpUser);
  const smtpHost = env('SMTP_HOST', gmail ? 'smtp.gmail.com' : '');
  const smtpPort = parseInt(env('SMTP_PORT', gmail ? '465' : '587'), 10);
  return {
    to: env('CONTACT_TO', fileConfig.contactTo || ''),
    from: env('CONTACT_FROM', ''),
    prefix: env('CONTACT_SUBJECT_PREFIX', 'Traversion Dynamics'),
    resendKey: env('RESEND_API_KEY', ''),
    smtp: {
      host: smtpHost,
      port: smtpPort,
      secure: /^(1|true|yes|on)$/i.test(env('SMTP_SECURE', smtpPort === 465 ? 'true' : 'false')),
      user: smtpUser,
      pass: env('SMTP_PASS', '')
    },
    rateMax: parseInt(env('CONTACT_RATE_MAX', '5'), 10),
    rateWindowMs: parseInt(env('CONTACT_RATE_WINDOW_MIN', '60'), 10) * 60 * 1000,
    minFillMs: parseInt(env('CONTACT_MIN_FILL_MS', '1500'), 10)
  };
}

/* single line: no control characters, so nothing can break out of a header */
function oneLine(v) {
  return String(v == null ? '' : v).replace(/[\u0000-\u001F\u007F\u2028\u2029]+/g, ' ').replace(/\s+/g, ' ').trim();
}

/* multi-line text: keep line breaks and tabs, drop other control characters */
function multiLine(v) {
  return String(v == null ? '' : v)
    .replace(/\r\n?/g, '\n')
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F\u2028\u2029]/g, '')
    .trim();
}

function validate(body) {
  const errors = {};
  const b = body && typeof body === 'object' ? body : {};
  const data = {
    name: oneLine(b.name),
    email: oneLine(b.email),
    organization: oneLine(b.organization),
    role: oneLine(b.role),
    topic: oneLine(b.topic),
    message: multiLine(b.message)
  };
  if (data.name.length < 2 || data.name.length > 100) errors.name = 'Please enter your name.';
  if (data.email.length > 254 || !EMAIL_RE.test(data.email)) errors.email = 'Please enter a valid email address.';
  if (data.organization.length > 120) errors.organization = 'Please keep this under 120 characters.';
  if (data.role.length > 120) errors.role = 'Please keep this under 120 characters.';
  if (!Object.prototype.hasOwnProperty.call(TOPICS, data.topic)) errors.topic = 'Please choose a topic.';
  if (data.message.length < 10) errors.message = 'Please write at least a short message (10 characters).';
  else if (data.message.length > 5000) errors.message = 'Please keep the message under 5000 characters.';
  if (b.consent !== true) errors.consent = 'Please confirm so we can reply to you.';
  return { errors, data };
}

function compose(data, cfg) {
  const topic = TOPICS[data.topic];
  const lines = [
    'New message from the Traversion Dynamics website',
    '',
    'Name:         ' + data.name,
    'Email:        ' + data.email
  ];
  if (data.organization) lines.push('Organization: ' + data.organization);
  if (data.role) lines.push('Role:         ' + data.role);
  lines.push('Topic:        ' + topic, '', 'Message:', '', data.message, '', '--', 'Reply to this email to answer ' + data.name + '.');
  return {
    subject: cfg.prefix + ': ' + topic + ' (' + data.name + ')',
    text: lines.join('\n')
  };
}

async function sendViaResend(cfg, data, mail) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + cfg.resendKey, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: cfg.from || 'Traversion Website <onboarding@resend.dev>',
      to: [cfg.to],
      reply_to: data.email,
      subject: mail.subject,
      text: mail.text
    }),
    signal: AbortSignal.timeout(12000)
  });
  if (!res.ok) {
    const err = new Error('Resend responded with HTTP ' + res.status);
    err.code = 'RESEND_' + res.status;
    throw err;
  }
}

async function sendViaSmtp(cfg, data, mail) {
  const nodemailer = require('nodemailer');
  const transport = nodemailer.createTransport({
    host: cfg.smtp.host,
    port: cfg.smtp.port,
    secure: cfg.smtp.secure,
    auth: { user: cfg.smtp.user, pass: cfg.smtp.pass },
    connectionTimeout: 10000,
    greetingTimeout: 10000,
    socketTimeout: 12000
  });
  await transport.sendMail({
    from: cfg.from || cfg.smtp.user,
    to: cfg.to,
    replyTo: data.email,
    subject: mail.subject,
    text: mail.text
  });
}

function mailConfigured(cfg) {
  const hasTransport = Boolean(cfg.resendKey) || Boolean(cfg.smtp.host && cfg.smtp.user && cfg.smtp.pass);
  return EMAIL_RE.test(cfg.to) && hasTransport;
}

/* best-effort rate limit, per server instance. On Vercel each warm function keeps its own
   counter, so for hard limits also enable Vercel Firewall rate limiting on /api/contact. */
const hits = new Map();
function limited(cfg, ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < cfg.rateWindowMs);
  hits.set(ip, list);
  if (hits.size > 5000) hits.clear();
  return list.length >= cfg.rateMax;
}
function record(ip) {
  const list = hits.get(ip) || [];
  list.push(Date.now());
  hits.set(ip, list);
}

function hostOf(url) {
  try {
    return new URL(url).host;
  } catch (e) {
    return '';
  }
}

/* req: { body, origin, host, ip }  ->  { status, json } */
async function handleContact(req) {
  const cfg = settings();

  /* only this website may post to it */
  if (req.origin) {
    const siteHost = hostOf(env('SITE_URL', ''));
    const originHost = hostOf(req.origin);
    if (!originHost || (originHost !== req.host && originHost !== siteHost)) {
      return { status: 403, json: { ok: false, error: 'Forbidden.' } };
    }
  }

  const body = req.body && typeof req.body === 'object' ? req.body : {};

  /* spam traps: a filled honeypot, or a form sent faster than a person could. Bots get a
     normal-looking success so they do not adapt. */
  const tooFast = typeof body.elapsedMs === 'number' && body.elapsedMs >= 0 && body.elapsedMs < cfg.minFillMs;
  if ((typeof body.website === 'string' && body.website !== '') || tooFast) {
    return { status: 200, json: { ok: true } };
  }

  const { errors, data } = validate(body);
  if (Object.keys(errors).length) return { status: 400, json: { ok: false, errors } };

  if (limited(cfg, req.ip || 'unknown')) {
    return { status: 429, json: { ok: false, error: 'Too many messages from this connection. Please try again later.' } };
  }

  if (!mailConfigured(cfg)) {
    console.error('[contact] email is not configured (CONTACT_TO and RESEND_API_KEY or SMTP_USER/SMTP_PASS)');
    return { status: 503, json: { ok: false, error: 'The contact form is not available right now.' } };
  }

  try {
    const mail = compose(data, cfg);
    if (cfg.resendKey) await sendViaResend(cfg, data, mail);
    else await sendViaSmtp(cfg, data, mail);
    record(req.ip || 'unknown');
    return { status: 200, json: { ok: true } };
  } catch (err) {
    /* log the reason only, never the visitor's details */
    console.error('[contact] delivery failed:', (err && (err.code || err.responseCode)) || (err && err.message));
    return { status: 502, json: { ok: false, error: 'We could not send your message right now. Please try again shortly.' } };
  }
}

module.exports = { handleContact, validate, TOPICS };
