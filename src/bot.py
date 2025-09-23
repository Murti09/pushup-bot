from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.commands import start_command, delete_command, rank_command, add_command
from utils.responses import handle_response
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('delete', delete_command))
    app.add_handler(CommandHandler('rank', rank_command))
    app.add_handler(CommandHandler('add', add_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    app.run_polling()

if __name__ == '__main__':
    print("Bot startet...")
    main()
    print("Bot ist beendet.")
