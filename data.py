import sqlite3

def init():
    with sqlite3.connect('vault.db') as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS vault(
                site TEXT PRIMARY KEY,
                username TEXT,
                password TEXT
            )
        """)
        conn.commit()

def save(site, user, pwd):
    init()
    with sqlite3.connect('vault.db') as conn:
        c = conn.cursor()
        c.execute("REPLACE INTO vault (site, username, password) VALUES (?, ?, ?)", (site, user, pwd))
        conn.commit()

def fetch_all():
    init()
    with sqlite3.connect("vault.db") as conn:
        return conn.cursor().execute("SELECT * FROM vault").fetchall()

def delete(site):
    with sqlite3.connect("vault.db") as conn:
        conn.cursor().execute("DELETE FROM vault WHERE site = ?", (site,))
        conn.commit()

def update(site, user, new_pwd):
    with sqlite3.connect("vault.db") as conn:
        conn.cursor().execute("UPDATE vault SET username = ?, password = ? WHERE site = ?", (user, new_pwd, site))
        conn.commit()
