# Geetha Gold Works

Public website for Geetha Gold Works — handcrafted gold jewellery, custom designs, repairs, and an admin panel for orders and catalogues.

## Continue on another laptop

1. Clone: https://github.com/panchumarthigeetha/geetha-gold-works
2. Read **[CONTINUE-HERE.md](CONTINUE-HERE.md)** — full handoff from the Cursor chat
3. In Cursor, say: *Read CONTINUE-HERE.md and continue from there.*

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Open:
- Website: http://127.0.0.1:5500/
- Admin: http://127.0.0.1:5500/admin

Default admin login (change after first run):
- Username: `admin`
- Password: set in `data/admin.json` (see `data/admin.example.json`)

## Public link

Double-click `start-public.bat` to create a temporary public URL.
For a permanent address, use `setup-permanent-link.bat` (free ngrok account required).
Keep this computer on while the site is public.
