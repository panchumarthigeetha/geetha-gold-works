from __future__ import annotations

import json
import os
import secrets
import uuid
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    jsonify,
    request,
    send_from_directory,
    session,
)
from werkzeug.utils import secure_filename

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
UPLOAD_DIR = os.path.join(BASE, "uploads", "catalogues")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
CATALOGUE_FILE = os.path.join(DATA_DIR, "catalogues.json")
FOLDERS_FILE = os.path.join(DATA_DIR, "folders.json")
ADMIN_FILE = os.path.join(DATA_DIR, "admin.json")
PUBLIC_URL_FILE = os.path.join(DATA_DIR, "public-url.txt")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

if not os.path.exists(ADMIN_FILE):
    with open(ADMIN_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"username": "admin", "password": "geetha123"},
            f,
            indent=2,
        )

for path, default in ((ORDERS_FILE, []), (CATALOGUE_FILE, []), (FOLDERS_FILE, [])):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def admin_credentials():
    return load_json(ADMIN_FILE)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return jsonify({"error": "Unauthorized"}), 401
        return fn(*args, **kwargs)

    return wrapper


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
def home():
    return send_from_directory(BASE, "index.html")


@app.get("/admin")
def admin_page():
    return send_from_directory(BASE, "admin.html")


@app.post("/api/login")
def login():
    body = request.get_json(silent=True) or {}
    creds = admin_credentials()
    username = str(body.get("username", "")).strip()
    password = str(body.get("password", ""))

    if secrets.compare_digest(username, creds["username"]) and secrets.compare_digest(
        password, creds["password"]
    ):
        session["admin"] = True
        return jsonify({"ok": True})

    return jsonify({"error": "Invalid username or password"}), 401


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.get("/api/me")
def me():
    return jsonify({"admin": bool(session.get("admin"))})


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "Geetha Gold Works"})


@app.get("/api/public-url")
def public_url():
    if os.path.exists(PUBLIC_URL_FILE):
        with open(PUBLIC_URL_FILE, encoding="utf-8") as f:
            url = f.read().strip()
        if url:
            return jsonify({"url": url, "website": f"{url}/", "admin": f"{url}/admin"})
    return jsonify({"url": None, "website": None, "admin": None})


@app.post("/api/orders")
def create_order():
    body = request.get_json(silent=True) or {}
    name = str(body.get("name", "")).strip()
    phone = str(body.get("phone", "")).strip()
    email = str(body.get("email", "")).strip()
    message = str(body.get("message", "")).strip()

    if not name or not phone or not message:
        return jsonify({"error": "Name, phone and message are required"}), 400

    orders = load_json(ORDERS_FILE)
    order = {
        "id": str(uuid.uuid4()),
        "name": name,
        "phone": phone,
        "email": email,
        "message": message,
        "status": "new",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    orders.insert(0, order)
    save_json(ORDERS_FILE, orders)
    return jsonify(order), 201


@app.get("/api/orders")
@login_required
def list_orders():
    return jsonify(load_json(ORDERS_FILE))


@app.patch("/api/orders/<order_id>")
@login_required
def update_order(order_id):
    body = request.get_json(silent=True) or {}
    status = str(body.get("status", "")).strip()
    if status not in {"new", "done"}:
        return jsonify({"error": "Invalid status"}), 400

    orders = load_json(ORDERS_FILE)
    for order in orders:
        if order["id"] == order_id:
            order["status"] = status
            save_json(ORDERS_FILE, orders)
            return jsonify(order)

    return jsonify({"error": "Order not found"}), 404


@app.get("/api/folders")
def list_folders():
    folders = load_json(FOLDERS_FILE)
    items = load_json(CATALOGUE_FILE)
    for folder in folders:
        folder_items = [item for item in items if item.get("folder_id") == folder["id"]]
        folder["count"] = len(folder_items)
        if not folder.get("image") and folder_items:
            folder["image"] = folder_items[0].get("image")
    return jsonify(folders)


@app.post("/api/folders")
@login_required
def create_folder():
    name = str(request.form.get("name", "")).strip()
    description = str(request.form.get("description", "")).strip()
    image = request.files.get("image")

    if not name:
        return jsonify({"error": "Folder name is required"}), 400

    folders = load_json(FOLDERS_FILE)
    if any(folder["name"].lower() == name.lower() for folder in folders):
        return jsonify({"error": "A folder with this name already exists"}), 400

    cover = ""
    if image and image.filename:
        if not allowed_file(image.filename):
            return jsonify({"error": "Use a JPG, PNG, WEBP or GIF image"}), 400
        ext = image.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        image.save(os.path.join(UPLOAD_DIR, filename))
        cover = f"/uploads/catalogues/{filename}"

    folder = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "image": cover,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    folders.append(folder)
    save_json(FOLDERS_FILE, folders)
    return jsonify(folder), 201


@app.delete("/api/folders/<folder_id>")
@login_required
def delete_folder(folder_id):
    folders = load_json(FOLDERS_FILE)
    match = next((folder for folder in folders if folder["id"] == folder_id), None)
    if not match:
        return jsonify({"error": "Folder not found"}), 404

    items = load_json(CATALOGUE_FILE)
    for item in items:
        if item.get("folder_id") == folder_id:
            item["folder_id"] = None
    save_json(CATALOGUE_FILE, items)

    if match.get("image"):
        filename = os.path.basename(match["image"])
        filepath = os.path.join(UPLOAD_DIR, filename)
        used_elsewhere = any(item.get("image") == match["image"] for item in items)
        if filename and os.path.exists(filepath) and not used_elsewhere:
            os.remove(filepath)

    folders = [folder for folder in folders if folder["id"] != folder_id]
    save_json(FOLDERS_FILE, folders)
    return jsonify({"ok": True})


@app.get("/api/catalogues")
def list_catalogues():
    items = load_json(CATALOGUE_FILE)
    folder_id = str(request.args.get("folder_id", "")).strip()
    if folder_id:
        items = [item for item in items if item.get("folder_id") == folder_id]
    return jsonify(items)


@app.post("/api/catalogues")
@login_required
def create_catalogue():
    title = str(request.form.get("title", "")).strip()
    description = str(request.form.get("description", "")).strip()
    folder_id = str(request.form.get("folder_id", "")).strip()
    image = request.files.get("image")

    if not title:
        return jsonify({"error": "Title is required"}), 400
    if not folder_id:
        return jsonify({"error": "Choose a folder first"}), 400
    if not image or not image.filename:
        return jsonify({"error": "Image is required"}), 400
    if not allowed_file(image.filename):
        return jsonify({"error": "Use a JPG, PNG, WEBP or GIF image"}), 400

    folders = load_json(FOLDERS_FILE)
    if not any(folder["id"] == folder_id for folder in folders):
        return jsonify({"error": "Folder not found"}), 400

    ext = image.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    image.save(os.path.join(UPLOAD_DIR, filename))

    items = load_json(CATALOGUE_FILE)
    item = {
        "id": str(uuid.uuid4()),
        "folder_id": folder_id,
        "title": title,
        "description": description,
        "image": f"/uploads/catalogues/{filename}",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    items.insert(0, item)
    save_json(CATALOGUE_FILE, items)
    return jsonify(item), 201


@app.delete("/api/catalogues/<item_id>")
@login_required
def delete_catalogue(item_id):
    items = load_json(CATALOGUE_FILE)
    match = next((item for item in items if item["id"] == item_id), None)
    if not match:
        return jsonify({"error": "Catalogue item not found"}), 404

    filename = os.path.basename(match.get("image", ""))
    filepath = os.path.join(UPLOAD_DIR, filename)
    if filename and os.path.exists(filepath):
        os.remove(filepath)

    items = [item for item in items if item["id"] != item_id]
    save_json(CATALOGUE_FILE, items)
    return jsonify({"ok": True})


@app.get("/uploads/catalogues/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, secure_filename(filename))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=False)
