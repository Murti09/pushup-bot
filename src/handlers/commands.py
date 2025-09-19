from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hallo, ich bin Mr. PushUp! Schreibe mir deine Liegestütze')
