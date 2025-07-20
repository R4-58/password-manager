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

For app:

customtkinter: GUI components

sqlite3: Local database

cryptography: Encryption using Fernet

bcrypt: Secure master password hashing

pyperclip: Clipboard copy for passwords
   
For demo website:

Flask : Web server framework 

Jinja2 Tempaltes : HTML + dynamic data

static/style.css : Custom styles for website

template/home.html : Home page UI

app.py : Flask app logic

2_requirements.text : install project dependencies for website

Download Buttons : Platform based app links

url_for() (JINJA func) : Auto generate resource paths 

onclick="alerts(...)" : Temporary "comming soon " alerts

Render Deployment : Free Live Hosting 

I have used Render to deploy my demo Website for testing and all some times maybe 

the server will be inactive 😅 bec of free trail but after 3 seconds the srever will be active 
