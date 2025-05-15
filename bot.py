import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

>>>>>>> 22de148e4496a4a8eaea8c7a84db91917c2110e5
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send me a Terabox link and I'll try to download it.")

# Handle messages (Terabox links)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    if "terabox.com" in message or "teraboxapp.com" in message:
        await update.message.reply_text("🔄 Downloading... (feature coming soon!)")
    else:
        await update.message.reply_text("❌ Please send a valid Terabox link.")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
