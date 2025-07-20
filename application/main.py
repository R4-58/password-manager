# main.py
"""
main.py – SecureVault GUI Password Manager
"""

try:
    import customtkinter as ctk
    from tkinter import messagebox
except ModuleNotFoundError as exc:
    raise ImportError(
        "customtkinter or tkinter is not installed. Please ensure tkinter is available in your environment."
    ) from exc

import os
from cryptography.fernet import Fernet
import pyperclip
import data
import auth

# Load or generate the encryption key
if not os.path.exists("secret.key"):
    with open("secret.key", "wb") as f:
        f.write(Fernet.generate_key())

with open("secret.key", "rb") as key_file:
    fernet = Fernet(key_file.read())

# App UI
def show_main_app():
    app = ctk.CTk()
    app.title("SecureVault")
    app.geometry("720x500")
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    sidebar = ctk.CTkFrame(app, width=150)
    sidebar.pack(side="left", fill="y")
    main_area = ctk.CTkFrame(app)
    main_area.pack(side="right", expand=True, fill="both")

    def clear_main():
        for widget in main_area.winfo_children():
            widget.destroy()

    def generate_password():
        import string, random
        chars = string.ascii_letters + string.digits + string.punctuation
        pwd = ''.join(random.choices(chars, k=16))
        pwd_entry.delete(0, 'end')
        pwd_entry.insert(0, pwd)
        pyperclip.copy(pwd)

    def check_strength(pwd):
        import re
        score = sum(bool(re.search(r, pwd)) for r in [r"[a-z]", r"[A-Z]", r"\d", r"\W"])
        if len(pwd) >= 8: score += 1
        status = ["Weak", "Moderate", "Strong"][(score - 2) if score > 1 else 0]
        color = ["red", "orange", "green"][(score - 2) if score > 1 else 0]
        strength.configure(text=status, text_color=color)

    def add_page():
        clear_main()
        ctk.CTkLabel(main_area, text="Add Password", font=("Segoe UI", 20)).pack(pady=10)
        global site_entry, user_entry, pwd_entry, strength

        site_entry = ctk.CTkEntry(main_area, placeholder_text="Website")
        user_entry = ctk.CTkEntry(main_area, placeholder_text="Username")
        pwd_entry = ctk.CTkEntry(main_area, placeholder_text="Password", show="*")

        site_entry.pack(pady=5)
        user_entry.pack(pady=5)
        pwd_entry.pack(pady=5)
        pwd_entry.bind("<KeyRelease>", lambda e: check_strength(pwd_entry.get()))

        strength = ctk.CTkLabel(main_area, text="")
        strength.pack()

        ctk.CTkButton(main_area, text="Generate", command=generate_password).pack(pady=5)

        def save():
            encrypted = fernet.encrypt(pwd_entry.get().encode()).decode()
            data.save(site_entry.get(), user_entry.get(), encrypted)
            messagebox.showinfo("Success", "Password saved")
            add_page()

        ctk.CTkButton(main_area, text="Save", command=save).pack(pady=10)

    def view_page():
        clear_main()
        ctk.CTkLabel(main_area, text="Saved Passwords", font=("Segoe UI", 20)).pack(pady=10)
        for site, user, encrypted in data.fetch_all():
            pwd = fernet.decrypt(encrypted.encode()).decode()
            frame = ctk.CTkFrame(main_area)
            frame.pack(pady=4, padx=10, fill="x")
        ctk.CTkLabel(frame, text=f"{site} | {user} | {pwd}", anchor="w").pack(side="left", fill="x", expand=True)
        ctk.CTkButton(frame, text="Edit", command=lambda s=site: edit_entry(s), width=40).pack(side="right")
        ctk.CTkButton(frame, text="Del", command=lambda s=site: delete_entry(s), width=40).pack(side="right", padx=5)

    def delete_entry(site):
        data.delete(site)
        view_page()

    def edit_entry(site):
        clear_main()
        site_data = data.fetch(site)
        user, pwd = site_data[1], fernet.decrypt(site_data[2].encode()).decode()
        ctk.CTkLabel(main_area, text=f"Edit: {site}", font=("Segoe UI", 20)).pack(pady=10)
        new_user = ctk.CTkEntry(main_area)
        new_pwd = ctk.CTkEntry(main_area)

        new_user.insert(0, user)
        new_pwd.insert(0, pwd)

        new_user.pack(pady=5)
        new_pwd.pack(pady=5)

        def update():
            encrypted = fernet.encrypt(new_pwd.get().encode()).decode()
            data.update(site, new_user.get(), encrypted)
            view_page()

        ctk.CTkButton(main_area, text="Update", command=update).pack(pady=10)

    def settings_page():
        clear_main()
        ctk.CTkLabel(main_area, text="Settings", font=("Segoe UI", 20)).pack(pady=10)
        ctk.CTkButton(main_area, text="Dark Mode", command=lambda: ctk.set_appearance_mode("Dark")).pack(pady=5)
        ctk.CTkButton(main_area, text="Light Mode", command=lambda: ctk.set_appearance_mode("Light")).pack(pady=5)

    # Sidebar buttons with icons
    ctk.CTkButton(sidebar, text="➕ Add", command=add_page).pack(pady=10, fill="x")
    ctk.CTkButton(sidebar, text="📁 View", command=view_page).pack(pady=10, fill="x")
    ctk.CTkButton(sidebar, text="⚙️ Settings", command=settings_page).pack(pady=10, fill="x")

    add_page()
    app.mainloop()

# --- Login Screen ---
def login():
    window = ctk.CTk()
    window.title("Login")
    window.geometry("300x200")

    ctk.CTkLabel(window, text="Master Password", font=("Segoe UI", 16)).pack(pady=20)
    entry = ctk.CTkEntry(window, show="*")
    entry.pack(pady=10)

    def verify():
        if auth.verify_master(entry.get()):
            window.destroy()
            show_main_app()
        else:
            messagebox.showerror("Error", "Incorrect password")

    ctk.CTkButton(window, text="Login", command=verify).pack(pady=10)

    if not auth.master_exists():
        ctk.CTkLabel(window, text="Set Master Password:").pack(pady=5)
        ctk.CTkButton(window, text="Create", command=lambda: auth.set_master(entry.get())).pack(pady=5)

    window.mainloop()

login()
