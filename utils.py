# utils.py
import os, sys, random, string, hashlib, subprocess
from datetime import datetime
from shutil import copy2
from tkinter import messagebox

UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB by default (adjusted in main if required)
ALLOWED_UPLOAD_EXT = {'.pdf'}

def gen_tr_id():
    t = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    r = ''.join(random.choices(string.digits, k=4))
    return f"TX{t}{r}"

def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()

def filesize_ok(path, limit_bytes=MAX_UPLOAD_BYTES):
    try:
        return os.path.getsize(path) <= limit_bytes
    except Exception:
        return False

def open_file_with_default(path):
    try:
        if sys.platform.startswith('win'):
            os.startfile(path)
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
    except Exception:
        pass

def save_uploaded_file_for_user(user_id: int, src_path: str):
    """Copies file locally to uploads/user_{id}/timestamp_filename and returns path or None."""
    fname = os.path.basename(src_path)
    try:
        dest_dir = os.path.join(UPLOAD_DIR, f"user_{user_id}")
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, f"{int(datetime.utcnow().timestamp())}_{fname}")
        copy2(src_path, dest_path)
        return dest_path
    except Exception as e:
        messagebox.showerror("Upload error", str(e)); return None
