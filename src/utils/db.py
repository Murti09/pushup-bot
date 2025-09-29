import sqlite3
from datetime import date

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

    c.execute("""
        CREATE TABLE IF NOT EXISTS pushups_log (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              username TEXT,
              count INTEGER,
              date TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Datenbank wurde initialisert")

def add_pushups(user_id, username, count):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Gesamter Stand aktualisieren
    c.execute("SELECT total FROM pushups WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row:
        new_total = row[0] + count
        c.execute("UPDATE pushups SET total=? WHERE user_id=?", (new_total, user_id))
    else:
        new_total = count
        c.execute("INSERT INTO pushups (user_id, username, total) VALUES (?, ?, ?)", (user_id, username, new_total))

    # Heutigen Log-Eintrag speichern
    today = date.today().isoformat()
    c.execute("SELECT count FROM pushups_log WHERE user_id=? AND date=?", (user_id, today))
    row = c.fetchone()
    if row:
        new_daily = row[0] + count
        c.execute("UPDATE pushups_log SET count=?, username=?, last_count=? WHERE user_id=? AND date=?", 
                  (new_daily, username, count, user_id, today))
    else:
        c.execute("INSERT INTO pushups_log (user_id, username, count, date, last_count) VALUES (?, ?, ?, ?, ?)", 
                  (user_id, username, count, today, count))
    conn.commit()
    conn.close()
    print("add_pushups wurde aufgerufen")

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
    
    today = date.today().isoformat()
    c.execute("SELECT count FROM pushups_log WHERE user_id=? AND date=?", (user_id, today))
    row = c.fetchone()
    if row:
        new_daily = row[0] - count
        if new_daily > 0:
            c.execute("UPDATE pushups_log SET count=? WHERE user_id=? AND date=?", 
                      (new_daily, user_id, today))
        else:
            c.execute("DELETE FROM pushups_log WHERE user_id=? AND date=?", (user_id, today))
    conn.commit()
    conn.close()
    print("delete_pushups wurde aufgerufen")

def get_today_rank():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute("""
        SELECT username, SUM(count) as daily_total
        FROM pushups_log
        WHERE date = ?
        GROUP BY user_id
        ORDER BY daily_total DESC
    """, (today,))
    rows = c.fetchall()
    conn.close()
    return rows

def undo_last_pushups(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    today = date.today().isoformat()
    #Letzten count holen
    c.execute("SELECT last_count FROM pushups_log WHERE user_id=? AND date=?", (user_id, today))
    row = c.fetchone()

    if row and row[0] > 0:
        last_count = row[0]

        # Gesamtstand reduzieren
        c.execute("UPDATE pushups SET total = total - ? WHERE user_id=?", (last_count, user_id))

        # Tagesstand reduzieren
        c.execute("UPDATE pushups_log SET count = count - ?, last_count=0 WHERE user_id=? AND date=?",
                  (last_count, user_id, today))
        
        # Falls auf 0 oder weniger -> löschen
        c.execute("DELETE FROM pushups WHERE user_id=? AND total <= 0", (user_id,))
        c.execute("DELETE FROM pushups_log WHERE user_id=? AND date=? AND count <= 0", (user_id, today))

        conn.commit()
        conn.close()
    else:
        conn.close()
    print("undo_last_pushups wurde aufgerufen")