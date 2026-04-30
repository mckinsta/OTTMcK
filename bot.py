import os
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ================= TOKEN (Railway ENV) =================
TOKEN = os.getenv("BOT_TOKEN")

# ================= DATABASE =================
conn = sqlite3.connect("movies.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    part INTEGER DEFAULT 1,
    file_id TEXT
)
""")

cur.execute("CREATE INDEX IF NOT EXISTS idx_name ON movies(name)")
conn.commit()

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Movie Bot Ready!\n\n"
        "📌 Forward video → auto save\n"
        "📌 /get movie_name → send movie"
    )

# ================= SAVE MOVIE =================
async def save_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if not msg.video:
        return

    file_id = msg.video.file_id
    caption = msg.caption or "unknown"

    parts = caption.rsplit(" ", 1)

    if len(parts) == 2 and parts[1].isdigit():
        name = parts[0].lower()
        part = int(parts[1])
    else:
        name = caption.lower()
        part = 1

    cur.execute(
        "INSERT INTO movies (name, part, file_id) VALUES (?, ?, ?)",
        (name, part, file_id)
    )
    conn.commit()

    await msg.reply_text(f"✅ Saved: {name} Part {part}")

# ================= GET MOVIE =================
async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /get movie_name")
        return

    name = " ".join(context.args).lower()

    cur.execute("SELECT file_id FROM movies WHERE name=?", (name,))
    result = cur.fetchone()

    if result:
        await update.message.reply_video(result[0])
    else:
        await update.message.reply_text("❌ Movie not found")

# ================= MAIN =================
if __name__ == "__main__":
    if not TOKEN:
        print("❌ BOT_TOKEN missing in environment variables")
        exit()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get", get_movie))

    # forward video handler
    app.add_handler(MessageHandler(filters.VIDEO, save_movie))

    print("🚀 Bot starting...")
    app.run_polling()
