'use strict';

/*
  All configuration comes from environment variables (see .env.example).
  The contact address lives only here; the server writes it into the contact page
  when the page is served, so it is never hard-coded in the files under public/.
*/
require('dotenv').config();

function str(name, fallback) {
  const v = process.env[name];
  return v === undefined || v === '' ? fallback : v.trim();
}

function int(name, fallback) {
  const n = parseInt(process.env[name], 10);
  return Number.isFinite(n) ? n : fallback;
}

function bool(name, fallback) {
  const v = process.env[name];
  if (v === undefined || v === '') return fallback;
  return /^(1|true|yes|on)$/i.test(v.trim());
}

const EMAIL_RE = /^[^\s@<>"',;:\\]+@[^\s@<>"',;:\\]+\.[^\s@<>"',;:\\]{2,}$/;

const env = str('NODE_ENV', 'development');
const isProd = env === 'production';
const contactTo = str('CONTACT_TO', '');

module.exports = {
  env,
  isProd,
  port: int('PORT', 3000),
  siteUrl: str('SITE_URL', 'http://localhost:' + int('PORT', 3000)).replace(/\/+$/, ''),

  /* number of reverse proxies in front of the app (0 = none) */
  trustProxy: int('TRUST_PROXY', 0),

  /* 301-redirect any other hostname (www vs bare, old domains) to SITE_URL.
     Keeps one canonical address for search engines. Turn on once SITE_URL is correct. */
  canonicalRedirect: bool('CANONICAL_REDIRECT', false),

  /* address that the contact page opens an email to (empty if missing or invalid) */
  contactTo: EMAIL_RE.test(contactTo) ? contactTo : ''
};
