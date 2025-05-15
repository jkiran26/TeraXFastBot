import logging
import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send me a Terabox link and I'll send you the video directly.")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    if "terabox.com" not in message and "teraboxapp.com" not in message:
        await update.message.reply_text("❌ Please send a valid Terabox link.")
        return

    try:
        # Show 🚀 animation
        loading_msg = await update.message.reply_text("🚀")

        # Step 1: Fetch page
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(message, headers=headers, timeout=15)
        response.raise_for_status()

        # Step 2: Parse download link
        soup = BeautifulSoup(response.text, 'html.parser')
        download_url = None
        for tag in soup.find_all('a'):
            href = tag.get('href')
            if href and "download.terabox.com" in href:
                download_url = href
                break

        if not download_url:
            await loading_msg.edit_text("❌ Could not find a downloadable file.")
            return

        # Step 3: Download file
        video_data = requests.get(download_url, stream=True, timeout=30)
        video_data.raise_for_status()

        file_size = int(video_data.headers.get("Content-Length", 0))
        if file_size > 2 * 1024 * 1024 * 1024:
            await loading_msg.edit_text("❌ File too large. Telegram bots support only files up to 2 GB.")
            return

        file_name = download_url.split("/")[-1]
        with open(file_name, "wb") as f:
            for chunk in video_data.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # Step 4: Send video
        with open(file_name, "rb") as video:
            await update.message.reply_video(video)

        await loading_msg.delete()
        os.remove(file_name)

    except requests.exceptions.Timeout:
        await update.message.reply_text("❌ Failed to download. Terabox is not responding right now.")
    except Exception as e:
        logging.error(str(e))
        await update.message.reply_text("❌ Something went wrong while processing the file.")

# Main entry
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running with webhook...")

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=f"https://<teraxfastbot.up.railway.app/{BOT_TOKEN}"
    )

