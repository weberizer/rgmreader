# Deploy Guide — Crisp RGM site

You have a single-folder static site. Here's the full path from "files on my laptop" to "live at my custom domain."

Total time: ~30–60 minutes (most of it waiting for DNS to propagate).

---

## Step 1 — Buy a domain (5 min)

Pick a registrar. I recommend **Cloudflare Registrar** (cheapest at near-cost pricing, no markup, free WHOIS privacy). Alternative: Namecheap.

1. Go to https://dash.cloudflare.com → "Domain Registration" → "Register Domains"
2. Search for the domain you want (e.g. `crisprgm.com`, `yourname-rgm.com`)
3. Buy it ($10–$15/yr typical)

You don't have to do anything else here yet — we'll come back to DNS in Step 4.

---

## Step 2 — Set up GitHub repo (10 min)

If you don't have a GitHub account, create one at https://github.com first.

**Option A — through the web UI (easiest, no command line):**

1. Go to https://github.com/new
2. Repository name: `rgm-site` (or anything you want — it'll be in your URL only if you skip a custom domain)
3. Set to **Public** (required for free GitHub Pages)
4. Check "Add a README file"
5. Create repository
6. Click "Add file" → "Upload files"
7. Drag in the contents of this folder:
   - `index.html`
   - `404.html`
   - `CNAME`
   - `.nojekyll`
8. Commit changes

**Option B — through Git command line (if you're comfortable):**

```bash
cd "/Users/machine/Documents/Claude/Projects/RGM modelling"
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/rgm-site.git
git push -u origin main
```

---

## Step 3 — Enable GitHub Pages (2 min)

1. In your repo, click **Settings** (top right)
2. In the left sidebar, click **Pages**
3. Under "Build and deployment" → "Source": choose **Deploy from a branch**
4. Branch: **main** / folder: **/ (root)** → **Save**
5. Wait ~1 minute. Refresh the Pages settings page. You'll see a green ✓ and a URL like `https://YOUR-USERNAME.github.io/rgm-site/`

**Your site is now live at that URL.** You can stop here if you don't want a custom domain.

---

## Step 4 — Connect your custom domain (10 min + DNS wait)

### 4a. Edit the CNAME file

Open the `CNAME` file in your repo (click it in GitHub → pencil icon) and replace `YOUR-DOMAIN.com` with your actual domain (no `https://`, no trailing slash, no `www`):

```
crisprgm.com
```

Commit.

### 4b. Add DNS records at your registrar

Go to your registrar's DNS settings (Cloudflare: select your domain → DNS → Records).

Add **four A records** pointing the apex domain (`@`) to GitHub Pages' IPs:

| Type | Name | Value           | Proxy (if Cloudflare) |
|------|------|-----------------|----------------------|
| A    | @    | 185.199.108.153 | DNS only (gray cloud)|
| A    | @    | 185.199.109.153 | DNS only             |
| A    | @    | 185.199.110.153 | DNS only             |
| A    | @    | 185.199.111.153 | DNS only             |

Add **one CNAME record** for the `www` subdomain:

| Type  | Name | Value                       |
|-------|------|-----------------------------|
| CNAME | www  | YOUR-USERNAME.github.io     |

> Note: If you're using Cloudflare, set the proxy to **DNS only** (gray cloud) at first. You can turn it on (orange cloud) later once everything works, but it complicates the HTTPS handshake during initial setup.

### 4c. Configure the domain in GitHub Pages

Back in your repo → Settings → Pages:

1. Under "Custom domain", type your domain (e.g. `crisprgm.com`) → Save
2. Wait for the DNS check (can take 1 minute to a few hours)
3. Once it's green, check the **Enforce HTTPS** box (it might take an hour to become available)

### 4d. Wait for DNS to propagate

DNS changes can take anywhere from 5 minutes to 24 hours. Usually it's under an hour. Check propagation: https://dnschecker.org

When it's done, https://your-domain.com loads your site.

---

## Step 5 — Hook up the contact form (5 min)

The site has a contact form pointing to a Formspree placeholder. To make it actually deliver emails:

1. Sign up free at https://formspree.io
2. Create a new form (pick your email as the destination)
3. Copy the form endpoint (looks like `https://formspree.io/f/abc123xyz`)
4. In `index.html`, find `YOUR_FORMSPREE_ID` and replace the full URL with your endpoint
5. Commit. Form now delivers to your email.

Free tier: 50 submissions/month, which is plenty for a portfolio site.

---

## Step 6 — Hook up analytics (optional, 5 min)

The site is pre-wired for **GoatCounter** (free, privacy-friendly, no cookies, no consent banner needed):

1. Sign up at https://goatcounter.com → pick a subdomain (e.g. `crisprgm`)
2. In `index.html`, find the commented analytics block in `<head>`
3. Uncomment it and replace `YOUR-SUBDOMAIN` with your GoatCounter subdomain
4. Commit. You'll see visits at `https://crisprgm.goatcounter.com`

Alternatives if you prefer: **Plausible** ($9/mo, similar privacy) or **Google Analytics 4** (free, intrusive).

---

## Step 7 — Update OG image (optional, polish)

Social shares show a generic preview right now. To get a custom one:

1. Create a 1200×630px PNG with your branding (Canva, Figma)
2. Upload it to your repo as `og.png`
3. In `index.html`, find `og.png` URL references and replace `YOUR-DOMAIN.com` with your actual domain

Test how shares look: https://www.opengraph.xyz

---

## Updating the site later

Edit any file in GitHub (pencil icon → save) and the site updates in ~30 seconds. Or push from your terminal:

```bash
cd "/Users/machine/Documents/Claude/Projects/RGM modelling"
# edit index.html
git add index.html
git commit -m "update copy"
git push
```

---

## Troubleshooting

**Site shows "404" or "There isn't a GitHub Pages site here"**
→ Wait 2 more minutes. First deployment takes a moment. Refresh Settings → Pages to confirm the URL is generated.

**Custom domain shows "DNS check failed"**
→ DNS hasn't propagated yet. Wait, then retry. Use `dig YOUR-DOMAIN.com` or https://dnschecker.org to confirm A records are visible globally.

**Site loads on custom domain but HTTPS shows "Not Secure"**
→ GitHub provisions the SSL cert after DNS is verified. Takes up to an hour. Once "Enforce HTTPS" is enabled and green, it's good.

**Fonts don't load / charts don't render**
→ Check browser console. Likely a Content Security Policy issue or you're behind a corporate firewall blocking cloudflare.com or googleapis.com.

---

That's it. Once you're live, share the URL and start collecting feedback.
