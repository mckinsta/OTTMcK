import sqlite3

conn = sqlite3.connect("movies.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    name TEXT,
    part INTEGER,
    file_id TEXT
)
""")

conn.commit()


def add_movie(name, part, file_id):
    name = name.lower().strip().replace(".mp4","")
    cur.execute("INSERT INTO movies VALUES (?, ?, ?)", (name, part, file_id))
    conn.commit()


def get_parts(name):
    name = name.lower().strip()
    cur.execute("SELECT part FROM movies WHERE name=?", (name,))
    return [i[0] for i in cur.fetchall()]


def get_movie(name, part):
    name = name.lower().strip()
    cur.execute("SELECT file_id FROM movies WHERE name=? AND part=?", (name, part))
    data = cur.fetchone()
    return data[0] if data else None
