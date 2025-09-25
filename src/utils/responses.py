from telegram import Update
from telegram.ext import ContextTypes
from utils.db import init_db, add_pushups, get_all_pushups, get_today_rank
from config import GROUP_CHAT_ID, TEST_USER_ID
from datetime import date

init_db() # Datenbank beim Start initialisieren

async def build_rank_message() -> str:
    msg = "📊 Push-Up Ranking\n\n"

    # Heutige Ergebnisse
    today_results = get_today_rank()
    msg += f"📅 Heute ({date.today().isoformat()}):\n"
    if today_results:
        for i, (name, total) in enumerate(today_results, start=1):
            msg += f"{i}. {name}: {total}\n"
    else:
        msg += "Noch keine Einträge heute.\n"

    msg += "\n🏆 Gesamter Stand:\n"
    total_results = get_all_pushups()
    for i, (name, total) in enumerate(total_results, start=1):
        if i == 1:
            msg += f"{i}. 🥇 {name}: {total}\n"
        elif i == 2:
            msg += f"{i}. 🥈 {name}: {total}\n"
        elif i == 3:
            msg += f"{i}. 🥉 {name}: {total}\n"
        else:
            msg += f"{i}. {name}: {total}\n"

    return msg

async def show_rank(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    msg = await build_rank_message()
    await update.message.reply_text(msg)

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name
    text = update.message.text.lower()

    chat_type = update.effective_chat.type
    group_name = update.effective_chat.title if chat_type in ["group", "supergroup"] else "Privatchat"

    print(f"{username} ({user_id}) in {group_name}: {text}")
    
    if update.effective_chat.id not in [GROUP_CHAT_ID, TEST_USER_ID]:
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

    await show_rank(update, context)