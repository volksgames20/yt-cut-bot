import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! 👋 Aku bot download YouTube potongan.\n\n"
        "📝 Cara pakai:\n"
        "Kirim pesan dengan format:\n"
        "<link YouTube> <menit mulai> <menit selesai>\n\n"
        "✅ Contoh:\nhttps://youtube.com/watch?v=xxx 6:00 7:00"
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split()

    if len(parts) != 3:
        await update.message.reply_text(
            "❌ Format salah!\n\n"
            "✅ Contoh:\nhttps://youtube.com/watch?v=xxx 6:00 7:00"
        )
        return

    url, start_time, end_time = parts

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❌ Link YouTube tidak valid!")
        return

    await update.message.reply_text("⏳ Sedang proses... Tunggu ya!")

    output_file = "output.mp4"

    try:
        cmd = [
            "yt-dlp",
            "--download-sections", f"*{start_time}-{end_time}",
            "--force-keyframes-at-cuts",
            "-f", "best[height<=480]",
            "-o", output_file,
            url
        ]
        subprocess.run(cmd, check=True, timeout=120)

        with open(output_file, "rb") as f:
            await update.message.reply_video(f, caption=f"✅ Potongan {start_time} - {end_time}")

        os.remove(output_file)

    except Exception as e:
        await update.message.reply_text(f"❌ Gagal: {str(e)}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
app.run_polling()
