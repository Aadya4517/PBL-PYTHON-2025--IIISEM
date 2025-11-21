# auth.py
import os
from typing import List, Optional
from tkinter import Toplevel, Label, Button, Frame, Message
import pyotp as _pyotp_module  # optional import handled in main
from tkinter import messagebox, filedialog
from db import fetchone, fetchall, insert_and_get_id, execute_commit
from utils import gen_tr_id, hash_pin, save_uploaded_file_for_user, filesize_ok, ALLOWED_UPLOAD_EXT
from datetime import datetime

# NOTE: pyotp, qrcode usage is optional and for QR display only. main.py will pass available libs if needed.

# --- user creation & role assignment ---
def register_user(name: str, phone: str, gender: str, roles: List[str], totp_secret: Optional[str]=None) -> Optional[int]:
    q = "INSERT INTO users (name, phone, gender, totp_secret) VALUES (%s,%s,%s,%s)"
    uid = insert_and_get_id(q, (name, phone, gender, totp_secret))
    if not uid: return None
    # assign roles from roles table if exists
    for rn in roles:
        row = fetchone("SELECT role_id FROM roles WHERE role_name=%s LIMIT 1", (rn,))
        if row:
            execute_commit("INSERT INTO user_roles (user_id, role_id, enabled, verified) VALUES (%s,%s,1,1)", (uid, row['role_id']))
    return uid

def find_user_by_phone(phone: str):
    return fetchone("SELECT * FROM users WHERE phone=%s", (phone,))

def set_password_for_phone(phone: str, hashed_pw: str):
    return execute_commit("UPDATE users SET password_hash=%s, phone_verified=1 WHERE phone=%s", (hashed_pw, phone))

# --- TOTP UI helper (main supplies pyotp, qrcode, ImageTk if installed) ---
def show_totp_window(root, name: str, phone: str, secret: str, pyotp=None, qrcode=None, ImageTk=None):
    issuer = "SmartShare"
    user_label = f"{name}_{phone}"
    uri = f"otpauth://totp/{issuer}:{user_label}?secret={secret}&issuer={issuer}"
    top = Toplevel(root)
    top.title("TOTP enrollment")
    top.transient(root)
    try:
        top.grab_set()
    except Exception:
        pass
    Label(top, text="Scan this QR with your Authenticator app OR copy the secret below").pack(pady=8)
    qr_frame = Frame(top)
    qr_frame.pack(padx=10, pady=8)
    if qrcode and ImageTk:
        try:
            img = qrcode.make(uri)
            img.thumbnail((260,260))
            tkimg = ImageTk.PhotoImage(img)
            lbl = Label(qr_frame, image=tkimg)
            lbl.image = tkimg
            lbl.pack()
        except Exception:
            Label(qr_frame, text="(QR generation failed)").pack()
    else:
        Label(qr_frame, text="(QR not available — install qrcode & Pillow for QR)").pack()
    Label(top, text=f"TOTP secret: {secret}").pack(pady=8)
    Message(top, text="Open authenticator app, add account → scan QR or enter secret; then enter the 6-digit TOTP at login.", width=420).pack(padx=10, pady=6)
    Button(top, text="I've saved it", command=lambda: (top.grab_release() if hasattr(top, 'grab_release') else None, top.destroy())).pack(pady=10)
    top.lift(); top.focus_force()
    return top

# --- Upload ID (Graphic Era) ---
def upload_graphic_id_logic(user_id: int, src_path: str, db_update=True):
    fname = os.path.basename(src_path)
    if not any(x in fname.lower() for x in ('geu','graphic','rdlc')):
        messagebox.showerror("Upload failed", "Filename must include GEU / Graphic / RDLC (case-insensitive)")
        return False
    ext = os.path.splitext(fname)[1].lower()
    if ext not in ALLOWED_UPLOAD_EXT:
        messagebox.showerror("Upload failed", "Only PDF files allowed")
        return False
    if not filesize_ok(src_path):
        messagebox.showerror("Upload failed", "File exceeds upload limit")
        return False
    dest = save_uploaded_file_for_user(user_id, src_path)
    if not dest:
        return False
    if db_update:
        ok = execute_commit("UPDATE users SET id_doc_url=%s, id_status='Approved' WHERE user_id=%s", (dest, user_id))
        if ok:
            execute_commit("INSERT INTO verification (user_id, type, status, admin_id, notes) VALUES (%s,%s,%s,%s,%s)",
                           (user_id, 'ID', 'Approved', 0, 'Auto-approved'))
            # enable driver role if present
            execute_commit("""UPDATE user_roles ur JOIN roles r ON ur.role_id=r.role_id
                               SET ur.enabled=1, ur.verified=1
                               WHERE ur.user_id=%s AND r.role_name='Driver'""", (user_id,))
        else:
            return False
    try:
        # attempt to open file locally
        from utils import open_file_with_default
        open_file_with_default(dest)
    except Exception:
        pass
    return True

# --- role utilities for UI display ---
def get_roles_for_user(user_id: int):
    rows = fetchall("""SELECT r.role_name, ur.enabled, ur.verified
                       FROM user_roles ur JOIN roles r ON ur.role_id=r.role_id WHERE ur.user_id=%s""", (user_id,))
    return rows or []

