const express = require('express');
const rateLimit = require('express-rate-limit');
const { Readable } = require('stream');
const path = require('path');

const app = express();
app.set('trust proxy', 1); // Railway sits behind a proxy

// Send the old subdomain and www to the main domain (permanent redirect for SEO)
const MAIN = 'saatik.site';
const OLD = ['saatiktokvideodownloader.hassanwebdev.site', 'www.saatik.site'];
app.use((req, res, next) => {
  if (OLD.includes(req.hostname)) return res.redirect(301, 'https://' + MAIN + req.originalUrl);
  next();
});
app.use(express.static(path.join(__dirname, 'public'), { extensions: ['html'] }));
app.use('/api', rateLimit({ windowMs: 60000, limit: 20, standardHeaders: true, legacyHeaders: false }));

const API = 'https://www.tikwm.com/api/?hd=1&url=';
const ALLOWED = /(^|\.)(tikwm\.com|tiktokcdn\.com|tiktokcdn-us\.com|muscdn\.com)$/;
const abs = p => (!p ? null : p.startsWith('http') ? p : 'https://www.tikwm.com' + p);

function isTikTok(v) {
  try {
    const u = new URL(v);
    return ['http:', 'https:'].includes(u.protocol) && /(^|\.)tiktok\.com$/.test(u.hostname);
  } catch { return false; }
}

// Only fetch from known media hosts (prevents the server being used as an open proxy)
async function safeFetch(url, hops = 0) {
  const u = new URL(url);
  if (u.protocol !== 'https:' || !ALLOWED.test(u.hostname)) throw new Error('blocked host');
  const r = await fetch(u, { redirect: 'manual', signal: AbortSignal.timeout(30000) });
  const loc = r.headers.get('location');
  if (r.status >= 300 && r.status < 400 && loc && hops < 3) return safeFetch(new URL(loc, u).href, hops + 1);
  return r;
}

app.get('/api/info', async (req, res) => {
  const url = String(req.query.url || '').trim();
  if (!isTikTok(url)) return res.status(400).json({ error: 'Paste a valid TikTok link.' });
  try {
    const r = await fetch(API + encodeURIComponent(url), { signal: AbortSignal.timeout(15000) });
    const d = (await r.json()).data;
    const images = d && Array.isArray(d.images) ? d.images.map(abs).filter(Boolean) : [];
    if (!d || (!d.play && !images.length)) return res.status(404).json({ error: 'Post not found. It may be private or removed.' });
    res.json({
      title: d.title || 'TikTok video',
      author: (d.author && (d.author.nickname || d.author.unique_id)) || '',
      cover: abs(d.cover),
      duration: d.duration || 0,
      images,
      video: images.length ? null : abs(d.play),
      hd: images.length ? null : abs(d.hdplay),
      music: abs(d.music)
    });
  } catch {
    res.status(502).json({ error: 'The service is busy. Try again in a moment.' });
  }
});

app.get('/api/download', async (req, res) => {
  try {
    const r = await safeFetch(String(req.query.u || ''));
    if (!r.ok || !r.body) return res.status(502).send('Download failed. Go back and try again.');
    let ext = ['mp3', 'jpg'].includes(req.query.e) ? req.query.e : 'mp4';
    const name = String(req.query.n || 'tiktok').replace(/[^\w\- ]+/g, '').trim().slice(0, 60) || 'tiktok';
    let type = ext === 'mp3' ? 'audio/mpeg' : ext === 'jpg' ? (r.headers.get('content-type') || 'image/jpeg') : 'video/mp4';
    if (ext === 'jpg') {
      if (/webp/.test(type)) ext = 'webp';
      else if (/png/.test(type)) ext = 'png';
      else if (!/^image\//.test(type)) type = 'image/jpeg';
    }
    res.setHeader('Content-Type', type);
    res.setHeader('Content-Disposition', `attachment; filename="${name}.${ext}"`);
    const len = r.headers.get('content-length');
    if (len) res.setHeader('Content-Length', len);
    res.on('close', () => { try { r.body.cancel(); } catch {} });
    Readable.fromWeb(r.body).pipe(res);
  } catch {
    if (!res.headersSent) res.status(400).send('Bad link.');
  }
});

app.listen(process.env.PORT || 3000, () => console.log('Running'));
