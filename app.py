import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

def echo(update, context):
    user_message = update.message.text
    update.message.reply_text(user_message)

dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

if __name__ == '__main__':
    app.run()
