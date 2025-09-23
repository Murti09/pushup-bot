import sqlite3

DB_FILE = "pushups.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS pushups (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            total INTEGER
        )
    """)
    conn.commit()
    conn.close()
    print("Datenbank wurde initialisert")

def add_pushups(user_id, username, count):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT total FROM pushups WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row:
        new_total = row[0] + count
        c.execute("UPDATE pushups SET total=? WHERE user_id=?", (new_total, user_id))
    else:
        c.execute("INSERT INTO pushups (user_id, username, total) VALUES (?, ?, ?)", (user_id, username, count))
    conn.commit()
    conn.close()
    print("add_pushups wurde aufgerufen")
    return new_total

def get_all_pushups():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username, total FROM pushups ORDER BY total DESC")
    rows = c.fetchall()
    conn.close()
    print("get_all_pushups wurde aufgerufen")
    return rows

def delete_pushups(user_id, count):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE pushups SET total = total - ? WHERE user_id = ?", (count, user_id))
    c.execute("DELETE FROM pushups WHERE user_id = ? AND total <= 0", (user_id,))
    c.execute("SELECT total FROM pushups WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.commit()
    conn.close()
    print("delete_pushups wurde aufgerufen")
    return row[0] if row else 0