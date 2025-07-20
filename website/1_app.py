import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = "securevault_key"

# 🔐 Encryption key setup
if not os.path.exists("secret.key"):
    with open("secret.key", "wb") as f:
        f.write(Fernet.generate_key())

fernet = Fernet(open("secret.key", "rb").read())

# 📦 SQLite DB setup
conn = sqlite3.connect("vault.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT,
        username TEXT,
        password TEXT
    )
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
""")
conn.close()


# 🔐 Routes
@app.route('/')
def index():
    return redirect(url_for('login'))
    return render_template("3_login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("vault.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template("3_login.html", error="Invalid username or password")

    return render_template("3_login.html")



@app.route('/register')
def register():
    return render_template("2_register.html")


@app.route('/register', methods=['POST'])
def do_register():
    u = request.form['username']
    p = request.form['password']
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('index'))

    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("SELECT * FROM vault")
    data = c.fetchall()
    conn.close()
    return render_template("4_home.html", data=data)
@app.route('/settings')
def settings():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template("7_settings.html")


@app.route('/add', methods=['POST'])
def add_entry():
    site = request.form['site']
    username = request.form['username']
    password = fernet.encrypt(request.form['password'].encode()).decode()

    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("INSERT INTO vault (site, username, password) VALUES (?, ?, ?)", (site, username, password))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


@app.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute("DELETE FROM vault WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
