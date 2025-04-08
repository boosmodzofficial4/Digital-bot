import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

API_TOKEN = '7656706051:AAEZTYWiffUFzAvyDkG2MmfH3Ktx0l_CblE'
bot = telebot.TeleBot(API_TOKEN)

ADMIN_ID = 7665158009
CHANNELS = ['-1001963974161']  # Demo private channel
BUTTON_LIST = [
    {'name': 'VIP Movies', 'link': 'https://t.me/+xWhqm7Sh-u5jYTg1'},
]

user_ids = set()
autodelete_seconds = 3600  # Default 1 hour auto-delete time

# /start command for admin
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != ADMIN_ID:
        return
    commands = """
✅ Available Commands:

/start - Show this command list
/postlist - Post button list to all channels
/addbutton Name Link - Add a new button
/showbuttons - Show all buttons
/setdelete seconds - Set auto-delete time (in seconds)
/broadcast Your message here - Send message to all joined users
"""
    bot.reply_to(message, commands)

# Auto-approve join request (placeholder)
@bot.chat_join_request_handler(func=lambda r: True)
def approve_join_request(request):
    bot.approve_chat_join_request(request.chat.id, request.from_user.id)
    if request.from_user.id not in user_ids:
        user_ids.add(request.from_user.id)
        send_welcome(request.from_user.id)

# Welcome message
def send_welcome(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔥 JOIN THIS VIP CHANNEL FAST 👇", url='https://t.me/+xWhqm7Sh-u5jYTg1'))
    text = """🔥 WELCOME OUR CHANNEL 🔥

☠ OFFICIAL [VIP] TELEGRAM CHANNEL ☠

💋-NEW ADULT 18+ GAMES XNXX
💳RESSO+SPOTIFY+NETFLIX
✅ -HACKING FILES AND VIDEOS
📷 SECRET MOD APPS FOR YOU
🛡️-DIRECT PREMIUM+APPS UPLOAD"""
    bot.send_message(user_id, text, reply_markup=markup)

# Post the button list
@bot.message_handler(commands=['postlist'])
def post_list(message):
    if message.from_user.id != ADMIN_ID:
        return
    markup = InlineKeyboardMarkup()
    for btn in BUTTON_LIST:
        markup.add(InlineKeyboardButton(btn['name'], url=btn['link']))
    text = "🔥 EXPLORE OUR PREMIUM CHANNELS 🔥"
    for ch in CHANNELS:
        sent = bot.send_message(ch, text, reply_markup=markup)
        time.sleep(autodelete_seconds)
        try:
            bot.delete_message(ch, sent.message_id)
        except:
            pass

# Add a new button
@bot.message_handler(commands=['addbutton'])
def add_button(message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split(' ', 2)
    if len(parts) < 3:
        bot.reply_to(message, "Use format: /addbutton ButtonName Link")
        return
    BUTTON_LIST.append({'name': parts[1], 'link': parts[2]})
    bot.reply_to(message, "✅ Button added.")

# Show button list to admin
@bot.message_handler(commands=['showbuttons'])
def show_buttons(message):
    if message.from_user.id != ADMIN_ID:
        return
    text = "\n".join([f"{i+1}. {btn['name']}" for i, btn in enumerate(BUTTON_LIST)])
    bot.reply_to(message, text or "No buttons added.")

# Change auto-delete time
@bot.message_handler(commands=['setdelete'])
def set_delete_time(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        global autodelete_seconds
        autodelete_seconds = int(message.text.split()[1])
        bot.reply_to(message, f"✅ Auto-delete set to {autodelete_seconds} sec.")
    except:
        bot.reply_to(message, "Use format: /setdelete 3600")

# Broadcast to all users
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text.replace('/broadcast', '').strip()
    if not text:
        bot.reply_to(message, "Usage: /broadcast Your message here")
        return
    success = 0
    for uid in user_ids:
        try:
            bot.send_message(uid, text)
            success += 1
        except:
            pass
    bot.reply_to(message, f"✅ Broadcast sent to {success} users.")

print("Bot is running...")
bot.infinity_polling()
