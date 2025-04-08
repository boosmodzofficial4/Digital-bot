import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

API_TOKEN = '7656706051:AAEZTYWiffUFzAvyDkG2MmfH3Ktx0l_CblE'  # Updated Token
bot = telebot.TeleBot(API_TOKEN)

ADMIN_ID = 7665158009  # Updated Admin ID
CHANNELS = ['-1001234567890']  # Demo channel, बाद में बदल सकते हैं
BUTTON_LIST = [
    {'name': 'VIP Movies', 'link': 'https://t.me/+xWhqm7Sh-u5jYTg1'},
]

user_ids = set()
autodelete_seconds = 3600  # Default auto-delete time in seconds

# Auto-approve (अगर Telegram API allow करे future में)
@bot.channel_post_handler(func=lambda m: True, content_types=['new_chat_members'])
def welcome_user(message):
    for user in message.new_chat_members:
        if user.id not in user_ids:
            user_ids.add(user.id)
            send_welcome(user.id)

def send_welcome(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔥 JOIN THIS VIP  CHANNEL FAST👇", url='https://t.me/+xWhqm7Sh-u5jYTg1'))
    text = """🔥 WELCOME OUR CHANNEL 🔥

☠ OFFICIAL [VIP] TELEGRAM CHANNEL ☠

💋-NEW ADULT 18+ GAMES XNXX 
💳RESSO+SPOTIFY+NETFLIX 
✅ -HACKING FILES AND VIDEOS
📷 SECRET MOD APPS  FOR YOU
🛡️-DIRECT PREMIUM+APPS UPLOAD"""
    bot.send_message(user_id, text, reply_markup=markup)

@bot.message_handler(commands=['postlist'])
def post_list(message):
    if message.from_user.id != ADMIN_ID:
        return
    markup = InlineKeyboardMarkup()
    for btn in BUTTON_LIST:
        markup.add(InlineKeyboardButton(btn['name'], url=btn['link']))
    text = "🔥 WELCOME TO OUR NETWORK 🔥\n\nExplore Premium & Secret Channels Below!"
    for ch in CHANNELS:
        msg = bot.send_message(ch, text, reply_markup=markup)
        time.sleep(autodelete_seconds)
        bot.delete_message(ch, msg.message_id)

@bot.message_handler(commands=['addbutton'])
def add_button(message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split(' ', 2)
    if len(parts) < 3:
        bot.reply_to(message, "Format: /addbutton ButtonName Link")
        return
    BUTTON_LIST.append({'name': parts[1], 'link': parts[2]})
    bot.reply_to(message, "Button added.")

@bot.message_handler(commands=['setdelete'])
def set_delete_time(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        global autodelete_seconds
        autodelete_seconds = int(message.text.split()[1])
        bot.reply_to(message, f"Auto-delete time set to {autodelete_seconds} seconds.")
    except:
        bot.reply_to(message, "Usage: /setdelete 3600")

@bot.message_handler(commands=['showbuttons'])
def show_buttons(message):
    if message.from_user.id != ADMIN_ID:
        return
    text = "\n".join([f"{i+1}. {btn['name']} → {btn['link']}" for i, btn in enumerate(BUTTON_LIST)])
    bot.reply_to(message, text or "No buttons yet.")

print("Bot is running...")
bot.infinity_polling()
