import logging
import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک دانلود مستقیم بفرست تا فایل رو برات بفرستم.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    try:
        await update.message.reply_text("در حال دانلود فایل...")

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            filename = url.split("/")[-1]
            with open(filename, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)

            await update.message.reply_text("آپلود فایل در تلگرام...")
            with open(filename, "rb") as f:
                await update.message.reply_document(f)

            os.remove(filename)
        else:
            await update.message.reply_text("نتونستم فایل رو دریافت کنم 😕")

    except Exception as e:
        await update.message.reply_text(f"خطا: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()