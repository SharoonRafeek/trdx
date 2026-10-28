'use strict';

const path = require('path');
const fs = require('fs');
const express = require('express');
const helmet = require('helmet');
const compression = require('compression');

const config = require('./config');
const { handleContact } = require('../lib/contact');

const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const app = express();

app.disable('x-powered-by');
app.set('trust proxy', config.trustProxy);

/* ---------- one canonical hostname, HTTPS (opt-in via CANONICAL_REDIRECT) ---------- */
const SITE_HOST = (() => {
  try {
    return new URL(config.siteUrl).host;
  } catch (e) {
    return '';
  }
})();

app.use((req, res, next) => {
  if (config.canonicalRedirect && SITE_HOST && req.path !== '/healthz') {
    const wrongHost = req.get('host') !== SITE_HOST;
    const wrongProto = config.siteUrl.startsWith('https:') && req.protocol !== 'https';
    if (wrongHost || wrongProto) return res.redirect(301, config.siteUrl + req.originalUrl);
  }
  next();
});

app.get('/healthz', (req, res) => res.type('text').send('ok'));

app.use(compression());

/* ---------- security headers ---------- */
app.use(
  helmet({
    contentSecurityPolicy: {
      useDefaults: false,
      directives: {
        'default-src': ["'self'"],
        'script-src': ["'self'"],
        'style-src': ["'self'"],
        'img-src': ["'self'", 'data:'],
        'font-src': ["'self'"],
        'connect-src': ["'self'"],
        'media-src': ["'self'"],
        'object-src': ["'none'"],
        'base-uri': ["'self'"],
        'form-action': ["'self'"],
        'frame-ancestors': ["'none'"],
        ...(config.isProd ? { 'upgrade-insecure-requests': [] } : {})
      }
    },
    crossOriginEmbedderPolicy: false,
    hsts: config.isProd ? { maxAge: 63072000, includeSubDomains: true, preload: false } : false,
    referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
  })
);

app.use((req, res, next) => {
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), payment=(), usb=()');
  next();
});

/* ---------- HTML pages (SITE_URL is injected from the environment) ---------- */
const PAGES = {
  '/': 'index.html',
  '/index.html': 'index.html',
  '/missions': 'missions.html',
  '/missions.html': 'missions.html',
  '/contact': 'contact.html',
  '/contact.html': 'contact.html',
  '/privacy': 'privacy.html',
  '/privacy.html': 'privacy.html'
};

const pageCache = new Map();
function renderPage(file) {
  if (config.isProd && pageCache.has(file)) return pageCache.get(file);
  const html = fs
    .readFileSync(path.join(PUBLIC_DIR, file), 'utf8')
    .replace(/%%SITE_URL%%/g, config.siteUrl)
    .replace(/%%CONTACT_TO%%/g, config.contactTo);
  if (config.isProd) pageCache.set(file, html);
  return html;
}

function sendPage(res, file, status) {
  res
    .status(status || 200)
    .set('Cache-Control', 'no-cache')
    .type('html')
    .send(renderPage(file));
}

Object.keys(PAGES).forEach((route) => {
  app.get(route, (req, res) => sendPage(res, PAGES[route]));
});

/* ---------- robots.txt and sitemap.xml, built from SITE_URL ---------- */
app.get('/robots.txt', (req, res) => {
  res.type('text/plain').send('User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: ' + config.siteUrl + '/sitemap.xml\n');
});

const SITEMAP = [
  { loc: '/', file: 'index.html', priority: '1.0', freq: 'weekly', image: '/images/og-image.png' },
  { loc: '/missions.html', file: 'missions.html', priority: '0.8', freq: 'monthly' },
  { loc: '/contact.html', file: 'contact.html', priority: '0.6', freq: 'yearly' },
  { loc: '/privacy.html', file: 'privacy.html', priority: '0.2', freq: 'yearly' }
];

app.get('/sitemap.xml', (req, res) => {
  const items = SITEMAP.map((u) => {
    let mod = '';
    try {
      mod = fs.statSync(path.join(PUBLIC_DIR, u.file)).mtime.toISOString().slice(0, 10);
    } catch (e) {
      /* no lastmod if the file is missing */
    }
    return (
      '  <url>\n    <loc>' + config.siteUrl + u.loc + '</loc>\n' +
      (mod ? '    <lastmod>' + mod + '</lastmod>\n' : '') +
      '    <changefreq>' + u.freq + '</changefreq>\n    <priority>' + u.priority + '</priority>\n' +
      (u.image ? '    <image:image><image:loc>' + config.siteUrl + u.image + '</image:loc></image:image>\n' : '') +
      '  </url>'
    );
  });
  res.type('application/xml').send(
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' +
      items.join('\n') + '\n</urlset>\n'
  );
});

/* ---------- static assets (dotfiles are never served) ---------- */
app.use(
  express.static(PUBLIC_DIR, {
    index: false,
    dotfiles: 'deny',
    extensions: false,
    maxAge: config.isProd ? '7d' : 0,
    setHeaders(res, filePath) {
      if (/\.(woff2)$/.test(filePath)) res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
      if (/\.html$/.test(filePath)) res.setHeader('Cache-Control', 'no-cache');
    }
  })
);

/* ---------- contact API (same handler as the Vercel function in api/contact.js) ---------- */
app.post(
  '/api/contact',
  (req, res, next) => {
    if (!req.is('application/json')) return res.status(415).json({ ok: false, error: 'Unsupported content type.' });
    next();
  },
  express.json({ limit: '16kb', strict: true }),
  async (req, res) => {
    res.set('Cache-Control', 'no-store');
    const result = await handleContact({ body: req.body, origin: req.get('origin'), host: req.get('host'), ip: req.ip });
    res.status(result.status).json(result.json);
  }
);
app.all('/api/*', (req, res) => res.status(404).json({ ok: false, error: 'Not found.' }));

/* ---------- 404 and error handling ---------- */
app.use((req, res) => {
  if (req.accepts('html')) return sendPage(res, '404.html', 404);
  res.status(404).type('text').send('Not found');
});

// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  if (err && err.type === 'entity.too.large') return res.status(413).json({ ok: false, error: 'Message too large.' });
  if (err && (err.type === 'entity.parse.failed' || err instanceof SyntaxError)) {
    return res.status(400).json({ ok: false, error: 'Invalid request.' });
  }
  console.error('[server] error:', err && err.message);
  res.status(500).type('text').send('Server error');
});

if (require.main === module) {
  app.listen(config.port, () => {
    console.log('Traversion site listening on port ' + config.port + ' (' + config.env + ')');
    if (!process.env.RESEND_API_KEY && !(process.env.SMTP_USER && process.env.SMTP_PASS)) {
      console.warn('[warn] No RESEND_API_KEY or SMTP_USER/SMTP_PASS set: the contact form will return an error.');
    }
    if (config.isProd && /localhost/.test(config.siteUrl)) {
      console.warn('[warn] SITE_URL is not set: canonical URLs and the sitemap will point at localhost.');
    }
  });
}

module.exports = app;
