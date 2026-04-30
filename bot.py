from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from db import add_movie, get_parts

TOKEN = "8716119355:AAGKHNCEAbpaYbVQAYSJzt0oioDlsshtfSk"


# 📥 SAVE MOVIE
async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    file_id = None
    file_name = "movie"

    if msg.video:
        file_id = msg.video.file_id
        file_name = msg.video.file_name or "movie"

    elif msg.document:
        file_id = msg.document.file_id
        file_name = msg.document.file_name or "movie"

    if not file_id:
        return

    file_name = file_name.lower().replace(".mp4","").strip()

    if "_" in file_name:
        name, part = file_name.rsplit("_",1)
        part = int(part)
    else:
        name = file_name
        part = 1

    add_movie(name, part, file_id)

    await msg.reply_text(f"✔ Saved: {name} Part {part}")


# 🔍 SEARCH TEST
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.lower().strip()

    parts = get_parts(name)

    if not parts:
        await update.message.reply_text("❌ Movie नाही सापडली")
    else:
        await update.message.reply_text(f"Parts: {parts}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, save))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

print("Bot running 🚀")
app.run_polling()
