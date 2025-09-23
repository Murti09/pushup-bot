from telegram import Update
from telegram.ext import ContextTypes
from utils.db import init_db, add_pushups, get_all_pushups
from config import GROUP_CHAT_ID, TEST_USER_ID

init_db() # Datenbank beim Start initialisieren

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name
    text = update.message.text.lower()

    chat_type = update.effective_chat.type
    group_name = update.effective_chat.title if chat_type in ["group", "supergroup"] else "Privatchat"

    print(f"{username} ({user_id}) in {group_name}: {text}")
    
    if update.effective_chat.id != GROUP_CHAT_ID and update.effective_chat.id != TEST_USER_ID:
        await update.message.reply_text("Du bist kein Teilnehmer!")
        return

    if not text.isdigit():
        if "nicht" in text or "kein bock" in text or "keine lust" in text:
            await update.message.reply_text("Zu schwach was?")
        elif "schwer" in text or "anstrengend" in text:
            await update.message.reply_text("Nur die Harten kommen in den Garten!")
        elif "geschafft" in text or "fertig" in text:
            await update.message.reply_text("Starke Leistung! Weiter so!")
        elif "hallo" in text or "hi" in text or "hey" in text:
            await update.message.reply_text(f"Hallo {username}!")
        return
    
    count = int(text)
    add_pushups(user_id, username, count)

    # Übersicht aller Teilnehmer
    all_pushups = get_all_pushups()
    msg = "Aktueller Stand:\n"
    for i, (name, total) in enumerate(all_pushups):
        if i == 0:
            msg += f"{i+1}. 🏆{name}: {total}\n"
        else:
            msg += f"{i+1}. {name}: {total}\n"

    await update.message.reply_text(msg)