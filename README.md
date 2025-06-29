# password-manager
🔐 Password Manager App – Description
This project is a graphical password manager built using Python’s CustomTkinter for a modern interface. It securely stores user credentials in an SQLite database, protected with Fernet encryption from the cryptography library. The app includes the following features:

🎯 Features:
🔑 Master Password Authentication

On first use, the user sets a master password.

On later runs, login is required.

Passwords are securely hashed using bcrypt.

🧠 Custom UI with Tabs and Theme Switching

Built using CustomTkinter for a sleek dark/light UI.

Sidebar navigation for Add, View, and Settings.

🔐 Secure Password Storage

Passwords are encrypted with a symmetric Fernet key.

All data is stored locally in a SQLite database.

🧰 Password Generator with One-Click Copy

Built-in generator creates secure random passwords.

Auto-copies the password to clipboard using pyperclip.

📊 Password Strength Checker

Live feedback for password strength based on complexity.

✏️ Edit and 🗑️ Delete Saved Entries

Update or remove credentials for any website.

🎨 Settings Panel

Easily switch between Light and Dark themes.

🗃️ Technologies Used:
customtkinter: GUI components

sqlite3: Local database

cryptography: Encryption using Fernet

bcrypt: Secure master password hashing

pyperclip: Clipboard copy for passwords