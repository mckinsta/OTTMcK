import sqlite3

conn = sqlite3.connect("movies.db", check_same_thread=False)
cur = conn.cursor()

# 🧱 TABLE CREATE
cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    part INTEGER,
    file_id TEXT
)
""")

# ⚡ INDEX
cur.execute("CREATE INDEX IF NOT EXISTS idx_name ON movies(name)")
conn.commit()


# 📥 SAVE MOVIE
def add_movie(name, part, file_id):
    name = name.lower().replace(".mp4", "").strip()

    # remove extra spaces / normalize
    if "_" in name:
        name = name.split("_")[0]

    cur.execute(
        "INSERT INTO movies (name, part, file_id) VALUES (?, ?, ?)",
        (name, part, file_id)
    )
    conn.commit()


# 🔍 GET ALL PARTS
def get_parts(name):
    name = name.lower().replace(".mp4", "").strip()
    name = name.split("_")[0]

    cur.execute(
        "SELECT part FROM movies WHERE name LIKE ? ORDER BY part",
        (name + "%",)
    )

    return [row[0] for row in cur.fetchall()]


# 🎬 GET SPECIFIC PART
def get_movie_by_part(name, part):
    name = name.lower().replace(".mp4", "").strip()
    name = name.split("_")[0]

    cur.execute(
        "SELECT file_id FROM movies WHERE name LIKE ? AND part=?",
        (name + "%", part)
    )

    result = cur.fetchone()
    return result[0] if result else None


# 🔎 SEARCH (optional)
def search_movie(query):
    query = f"%{query.lower()}%"

    cur.execute("""
    SELECT name, part, file_id
    FROM movies
    WHERE name LIKE ?
    LIMIT 1
    """, (query,))

    return cur.fetchone()
if __name__ == "__main__":
    print("Bot starting...")
    app.run_polling()
