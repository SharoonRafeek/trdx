# Traversion Dynamics website

Static pages plus a contact form that emails every message to `shimron.alakkal1804@gmail.com`. On Vercel the form is handled by a serverless function (`api/contact.js`). The receiving address and email password live only in environment variables, never in the pages.

## Deploy on Vercel

1. Push this project to GitHub (never commit `.env`, it is in `.gitignore`).
2. On vercel.com choose Add New > Project, import the repo and leave the detected settings (`vercel.json` sets the build and output folder).
3. Under **Environment Variables** add these (names exactly as written), then deploy:

| Name | Value |
|---|---|
| `SITE_URL` | Your final address, no trailing slash, e.g. `https://traversion.vercel.app` |
| `CONTACT_TO` | `shimron.alakkal1804@gmail.com` (optional: it is also the default in `site.config.json`) |
| `SMTP_USER` | `shimron.alakkal1804@gmail.com` |
| `SMTP_PASS` | A Gmail **App Password** (see below), not your normal password |

4. Open the deployed `/contact.html`, send a test message, and check the inbox (and spam folder the first time).

**Getting a Gmail App Password:** Google Account > Security > turn on 2-Step Verification > App passwords > create one named "Traversion site". Paste the 16 characters (spaces do not matter) into `SMTP_PASS`.

**Alternative: Resend.** Instead of the two `SMTP_` variables, create a key at resend.com and set `RESEND_API_KEY`. Without a verified domain Resend only delivers to the email you signed up with, so sign up with the Gmail address.

After changing environment variables, redeploy from the Deployments tab so they take effect. If the form shows "We could not send your message", the variables are missing or wrong: check Vercel > Project > Logs for a `[contact]` line.

**Spam protection built in:** hidden honeypot field, minimum fill time, same-site check, strict validation, header-injection protection, and a per-instance rate limit. For a hard limit also add a rate-limit rule for `/api/contact` in Vercel > Firewall.

## Run it on your computer

```
npm install
cp .env.example .env      # fill in SMTP_USER and SMTP_PASS
npm start                 # http://localhost:3000
```

## Settings: `site.config.json`

| Key | What it does |
|---|---|
| `contactTo` | Default receiving address if `CONTACT_TO` is not set. |
| `siteUrl` | Public address override for the static build. Usually leave empty. |
| `googleSiteVerification`, `bingSiteVerification` | Tokens from Search Console / Bing Webmaster Tools. |

To change page text, edit `public/` (or `build_pages.py`, which generates the pages, then run `python3 build_pages.py`).

> The GitHub Pages workflow in `.github/workflows/` publishes a static copy that has no server, so the contact form does not work there. Use Vercel (or the Node server) for the live site, or delete that workflow.

## Images and logos

Your photos are already installed in `public/images/`:

| File | Used for |
|---|---|
| `trav-macro.jpg` | Home page hero background (1920x1080) |
| `trav-core.jpg` | T.Core card (server racks) |
| `trav-sense.jpg` | T.Sense card (sensor mast) |
| `trav-sync.jpg` | T.Sync card (comms towers) |
| `trav-pulse.jpg` | T.Pulse card (cinema lens) |

To swap one, replace the file keeping the name (cards are 4:5, about 800x1000). Alt text lives in the `ALT` table of the page generator.

Logos: `logo-mark-light.svg` (header), `logo.svg` (footer tile), `logo-dark.svg` (apple-touch-icon source), `logo-mark.svg` (spare). Favicons: `favicon.svg` plus `public/favicon.ico` (16/32/48) as a fallback.

## Node server (optional)

`npm start` runs the same site and the same `/api/contact` route on a small hardened Express server (`server/`), for any host that runs Node. It reads `SITE_URL`, `CANONICAL_REDIRECT`, `TRUST_PROXY` and the contact variables from the environment (see `.env.example`).

## Search engine optimisation

Built in: one h1 per page, unique keyword-bearing titles and descriptions, canonical and hreflang links, Open Graph and Twitter cards, JSON-LD (Organization, WebSite, WebPage, FAQPage, Service, BreadcrumbList), a visible FAQ that matches the FAQ markup, alt text on every image, a preloaded hero image, a web manifest, `sitemap.xml` and `robots.txt` generated on every build, a styled `noindex` 404 page, fast self-hosted fonts and no third-party requests.

Nothing can guarantee position 1. After you publish:
1. Add the site to Google Search Console and Bing Webmaster Tools, verify it (use the two verification keys above) and submit `/sitemap.xml`.
2. Use a real custom domain. A `github.io` address works but ranks less well for competitive searches.
3. Get real links to the site (LinkedIn company page, Crunchbase, press, partners) and use the exact name "Traversion Dynamics" everywhere. Searches for the name rank first once the site is indexed. Competitive terms such as "border defense" or "counter-UAV" take months and depend on links and content.
4. Keep adding real content (a page per system, case studies, news).

## What is protected

- Strict Content-Security-Policy (no inline scripts or styles), HSTS in production, no framing, no MIME sniffing.
- All fonts, scripts and images are served from your own domain. No third-party requests, no cookies, no analytics.
- The contact endpoint accepts only JSON from this site, limits size, validates every field and never logs message contents. The receiving address and credentials are server-side only.
- Source files, `.env`, `server/` and `node_modules/` are never served.

## Before you launch

- Replace the placeholder copy and have `public/privacy.html` reviewed for your company and country.
- The footer links to Careers and Press open the contact page with that topic preselected. Add real pages when you have them.
- To change page text, edit the HTML in `public/`. Styles are in `public/css/site.css`.

## Fonts

Plus Jakarta Sans (SIL OFL), JetBrains Mono (SIL OFL) and TeX Gyre Adventor (GUST Font License, a free Avant Garde lookalike). Licences are in `public/licenses/`.
