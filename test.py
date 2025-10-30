# telegram_test.py
import telebot

BOT_TOKEN = "8449942039:AAHTy7w5n-7nqj6b4ZXp4PUJkiHATWbM_4k" 
CHANNEL_ID = -1003241456559  

bot = telebot.TeleBot(BOT_TOKEN)

try:
    bot.send_message(CHANNEL_ID, "✅ Telegram test message successful!")
    print("Message sent successfully!")
except Exception as e:
    print("Failed to send message:", e)
