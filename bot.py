import os
import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatInviteLink
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler, ChatJoinRequestHandler

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

approved_users = set()
custom_buttons = []

WELCOME_TEXT = """🔥 WELCOME OUR CHANNEL 🔥  
☠ OFFICIAL [VIP] TELEGRAM CHANNEL ☠  
🔥 JOIN THIS VIP CHANNEL FAST👇"""

WELCOME_BUTTONS = [
    {"name": "VIP 1", "url": "https://t.me/+rRE7PGogVh5lM2Y1"}
]

def start(update: Update, context: CallbackContext):
    if update.effective_user.id == ADMIN_ID:
        commands = [
            "/AutoAcceptedUsers - Total auto-accepted users",
            "/broadcast <msg> - Send msg to all",
            "/addbutton - Add new VIP button",
            "/postlist - Send buttons to all channels",
            "/setdelete <sec> - Auto-delete time",
            "/setautopost <sec> - Auto-post time",
            "/showbuttons - Show saved button list"
        ]
        update.message.reply_text("Available Commands:\n" + "\n".join(commands))

def join_request(update: Update, context: CallbackContext):
    try:
        user_id = update.chat_join_request.from_user.id
        chat_id = update.chat_join_request.chat.id
        context.bot.approve_chat_join_request(chat_id, user_id)
        approved_users.add(user_id)

        buttons = [InlineKeyboardButton(btn["name"], url=btn["url"]) for btn in WELCOME_BUTTONS]
        reply_markup = InlineKeyboardMarkup.from_column(buttons)

        context.bot.send_message(
            chat_id=user_id,
            text=WELCOME_TEXT,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Join request error: {e}")

def auto_users(update: Update, context: CallbackContext):
    update.message.reply_text(f"Total Auto-Accepted Users: {len(approved_users)}")

def broadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return

    msg = update.message.text.split(' ', 1)
    if len(msg) < 2:
        update.message.reply_text("Usage: /broadcast your_message")
        return

    message = msg[1]
    count = 0
    for uid in approved_users:
        try:
            context.bot.send_message(chat_id=uid, text=message)
            count += 1
        except:
            continue
    update.message.reply_text(f"Broadcast sent to {count} users.")

def add_button(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        parts = update.message.text.split(" ", 2)
        if len(parts) < 3:
            update.message.reply_text("Usage: /addbutton <Button Name> <URL>")
            return
        name, url = parts[1], parts[2]
        custom_buttons.append({"name": name, "url": url})
        update.message.reply_text(f"Button added: {name}")
    except:
        update.message.reply_text("Failed to add button.")

def post_list(update: Update, context: CallbackContext):
    buttons = [InlineKeyboardButton(btn["name"], url=btn["url"]) for btn in custom_buttons]
    markup = InlineKeyboardMarkup.from_column(buttons)
    update.message.reply_text("VIP Channels:", reply_markup=markup)

def show_buttons(update: Update, context: CallbackContext):
    text = "\n".join([f"{btn['name']} → {btn['url']}" for btn in custom_buttons])
    update.message.reply_text("Saved Buttons:\n" + text)

def main():
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("AutoAcceptedUsers", auto_users))
    dp.add_handler(CommandHandler("broadcast", broadcast))
    dp.add_handler(CommandHandler("addbutton", add_button))
    dp.add_handler(CommandHandler("postlist", post_list))
    dp.add_handler(CommandHandler("showbuttons", show_buttons))
    dp.add_handler(ChatJoinRequestHandler(join_request))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
