from telegram import Update
from telegram.ext import ContextTypes
from utils.db import delete_pushups, add_pushups
from utils.responses import show_rank
from config import GROUP_CHAT_ID, TEST_USER_ID

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hallo, ich bin Mr. PushUp! Schreibe mir deine Liegestütze')

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name

    if update.effective_chat.id not in [GROUP_CHAT_ID, TEST_USER_ID]:
        await update.message.reply_text("Du bist kein Teilnehmer!")
        return
    
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("Bitte gib die Anzahl an, z.B. /delete 10")
        return
    
    count = int(context.args[0])
    new_total = delete_pushups(user_id, count)
    await update.message.reply_text(f"{count} Liegestütze für {username} gelöscht.\n"
                                    f"Aktueller Stand: {new_total}")

async def rank_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_rank(update, context)

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    username = update.effective_chat.first_name

    if update.effective_chat.id not in [GROUP_CHAT_ID, TEST_USER_ID]:
        await update.message.reply_text("Du bist kein Teilnehmer!")
        return
    
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("Bitte gib die Anzahl an, z.B. /add 10")
        return
    
    count = int(context.args[0])
    new_total = add_pushups(user_id, username, count)
    await update.message.reply_text(f"{count} Liegestütze für {username} hinzugefügt.\n"
                                    f"Aktueller Stand: {new_total}")