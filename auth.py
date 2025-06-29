import sqlite3
import bcrypt

def master_exists():
    with sqlite3.connect('vault.db') as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS master(
            id INTEGER PRIMARY KEY,
            hash TEXT
            )
            """)
        result = c.execute("SELECT hash FROM master WHERE id = 1").fetchone()
        return result is not None

def set_master(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with sqlite3.connect('vault.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM master")
        c.execute("INSERT INTO master (id, hash) VALUES (?, ?)", (1, hashed.decode()))
        conn.commit()

def verify_master(password):
    with sqlite3.connect("vault.db") as conn:
        c = conn.cursor()
        result = c.execute("SELECT hash FROM master WHERE id = 1").fetchone()
        if result:
            return bcrypt.checkpw(password.encode(), result[0].encode())
        return False




