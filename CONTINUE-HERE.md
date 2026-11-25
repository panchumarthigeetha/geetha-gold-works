# Geetha Gold Works — Continue Here

Use this file on **any laptop** to continue building the website.
Open this project in Cursor and tell the AI:  
**“Read CONTINUE-HERE.md and continue from there.”**

---

## 1. Get the project on a new laptop

1. Install [Git](https://git-scm.com/downloads) and [Python](https://www.python.org/downloads/)
2. Open terminal and run:

```bash
git clone https://github.com/panchumarthigeetha/geetha-gold-works.git
cd geetha-gold-works
pip install -r requirements.txt
python app.py
```

3. Open in browser:
   - Website: http://127.0.0.1:5500/
   - Admin: http://127.0.0.1:5500/admin

4. Open the folder in **Cursor** and continue editing.

**GitHub repo:** https://github.com/panchumarthigeetha/geetha-gold-works  
**GitHub user:** `panchumarthigeetha`

---

## 2. Admin login

| Field | Value |
|--------|--------|
| Username | `admin` |
| Password | `geetha123` (or whatever is in `data/admin.json`) |

Change password by editing `data/admin.json` (see `data/admin.example.json`).

Admin sessions are set to **never expire** on localhost (cookie ~100 years). Session secret is stored in `data/secret.key` so restarts do not log you out.

---

## 3. What this project is

A jewellery business website for **Geetha Gold Works** with:

- Public homepage (hero, collections, story, services, testimonials, contact)
- Contact form that saves **orders** and can open WhatsApp
- **Admin panel** to:
  - View / mark orders done
  - Create **folders** (Chains, Necklace, Rings, etc.)
  - Upload catalogue photos into folders
  - See / copy public links
- Folders appear on the public Collections section; customers open a folder to see pieces
- Optional public sharing via Cloudflare tunnel or permanent ngrok domain

Brand name on the site: **Geetha Gold Works** (replaced earlier “Aurelia Goldsmiths”).

---

## 4. Important files

| File | Purpose |
|------|---------|
| `index.html` | Public website |
| `admin.html` | Admin login + orders + folders + catalogues |
| `app.py` | Flask backend (orders, folders, uploads, sessions) |
| `requirements.txt` | Python deps (`flask`) |
| `data/admin.json` | Admin username/password (local, not in git) |
| `data/orders.json` | Customer enquiries |
| `data/folders.json` | Category folders |
| `data/catalogues.json` | Uploaded pieces |
| `data/secret.key` | Session secret (local, not in git) |
| `uploads/catalogues/` | Uploaded images |
| `start-public.bat` | Start temporary public URL |
| `restart-public.bat` | Restart after fixes |
| `setup-permanent-link.bat` | One-time permanent ngrok domain |
| `PUBLIC-LINKS.txt` | Saved public URLs (local) |

---

## 5. How things work (for the next AI / you)

### Run locally
```bash
python app.py
```
Server: `0.0.0.0:5500` (localhost + same Wi‑Fi if firewall allows).

### Admin folders & catalogues
1. Admin → **Catalogues**
2. Add folder name (e.g. Chains, Necklace) + optional cover image
3. Choose folder → upload piece photo + title + description
4. Public site Collections shows folders; click folder to see pieces

### Orders
Customer submits contact form → saved in `data/orders.json` → visible in Admin → **Orders** → mark done. WhatsApp still opens for the customer.

### Public links (temporary)
- Free Cloudflare quick tunnel URL **changes / expires** when PC sleeps or tunnel restarts
- Run `start-public.bat` or `restart-public.bat` for a new link
- Keep the PC **on** while public

### Permanent public link
- Run `setup-permanent-link.bat` once (free ngrok account + static domain)
- Same address after restarts; PC must still be on

### Local network (same Wi‑Fi)
- Example: `http://192.168.x.x:5500/admin`
- Windows Firewall may block; use `open-firewall.bat` as Administrator

---

## 6. Chat history summary (what we already did)

1. Built full goldsmith `index.html` site, then rebranded to **Geetha Gold Works**
2. Added Flask admin: orders + catalogue uploads
3. Made site reachable on LAN, then public via Cloudflare tunnel
4. Added **admin-created folders** (Chains / Necklace style categories)
5. Tried permanent ngrok setup (needs user signup once)
6. Installed Git + GitHub CLI; logged in as `panchumarthigeetha`
7. Pushed code to https://github.com/panchumarthigeetha/geetha-gold-works
8. Made admin sessions unlimited for localhost

Placeholder contact details still used in places: phone `+91 99999 99999`, address “123 Main Street”. Replace with real shop details when ready.

---

## 7. Suggested next tasks

- Replace phone, WhatsApp number, address, Instagram with real details
- Change admin password from `geetha123`
- Add more folders and real product photos
- Finish permanent public domain (`setup-permanent-link.bat`) if you need a stable customer URL
- Deploy to real hosting (Render / Railway / VPS) if you need the site online when the PC is off
- Push latest changes after every important edit:

```bash
git add .
git commit -m "Describe your change"
git push
```

Then on the other laptop:

```bash
git pull
```

---

## 8. Prompt to paste in Cursor on the other laptop

```
Open this Geetha Gold Works project. Read CONTINUE-HERE.md fully.
Continue building from there. Repo: https://github.com/panchumarthigeetha/geetha-gold-works
Admin: admin / geetha123 at http://127.0.0.1:5500/admin
Website: http://127.0.0.1:5500/
```

---

*Last updated from Cursor chat handoff — keep this file updated when you make major changes.*
