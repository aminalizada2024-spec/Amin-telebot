import os
import threading
import time
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)

# تابعی که به پیام‌ها پاسخ می‌دهد
def echo(update, context):
    user_message = update.message.text
    update.message.reply_text(user_message)

# راه‌اندازی dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# مسیر وب‌هوک که تلگرام پیام‌ها را به اینجا می‌فرستد
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# یک تابع که هر 5 دقیقه یک بار به خودش درخواست می‌زند تا بیدار بماند
def keep_alive():
    my_url = "https://amin-telebot-1.onrender.com/webhook"
    while True:
        time.sleep(300)  # 5 دقیقه
        try:
            requests.get(my_url)
            print("Keep-alive ping sent")
        except:
            print("Ping failed")

# اجرای thread نگهدارنده در پس‌زمینه
threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
