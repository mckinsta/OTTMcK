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

cur.execute("CREATE INDEX IF NOT EXISTS idx_name ON movies(name)")
conn.commit()

# ================= CLEAN NAME =================
def clean_name(name):
    return name.lower().strip().replace(".mp4", "")

# ================= ADD MOVIE =================
def add_movie(name, part, file_id):
    name = clean_name(name)

    cur.execute(
        "INSERT INTO movies (name, part, file_id) VALUES (?, ?, ?)",
        (name, part, file_id)
    )
    conn.commit()

# ================= GET PARTS =================
def get_parts(name):
    name = clean_name(name)

    cur.execute("SELECT part FROM movies WHERE name=?", (name,))
    return [i[0] for i in cur.fetchall()]

# ================= GET MOVIE =================
def get_movie(name, part):
    name = clean_name(name)

    cur.execute(
        "SELECT file_id FROM movies WHERE name=? AND part=?",
        (name, part)
    )

    data = cur.fetchone()
    return data[0] if data else None
