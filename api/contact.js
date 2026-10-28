'use strict';

/* Vercel serverless function: POST /api/contact. The logic lives in lib/contact.js. */
const { handleContact } = require('../lib/contact');

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Method not allowed.' });
  }
  if (!String(req.headers['content-type'] || '').toLowerCase().includes('application/json')) {
    return res.status(415).json({ ok: false, error: 'Unsupported content type.' });
  }
  if (parseInt(req.headers['content-length'] || '0', 10) > 16 * 1024) {
    return res.status(413).json({ ok: false, error: 'Message too large.' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body);
    } catch (e) {
      return res.status(400).json({ ok: false, error: 'Invalid request.' });
    }
  }

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || (req.socket && req.socket.remoteAddress) || '';
  const result = await handleContact({ body, origin: req.headers.origin, host: req.headers.host, ip });
  return res.status(result.status).json(result.json);
};
