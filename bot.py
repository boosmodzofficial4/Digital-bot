import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ChatJoinRequestHandler
import json
import os

API_TOKEN = '7320159726:AAESYR2n1EGC9f1VFVnwlPv1sKRrjZ_4gpo'
ADMIN_ID = 7665158009

ACCEPTED_USERS_FILE = 'accepted_users.json'
BUTTONS_FILE = 'buttons.json'

WELCOME_TEXT = """🔥 WELCOME OUR CHANNEL 🔥  
☠ OFFICIAL [VIP] TELEGRAM CHANNEL ☠  
...  
🔥 JOIN THIS VIP  CHANNEL FAST👇"""

def load_json(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

async def join_request_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        request: ChatJoinRequest = update.chat_join_request
        await context.bot.approve_chat_join_request(chat_id=request.chat.id, user_id=request.from_user.id)
        await context.bot.send_message(chat_id=request.from_user.id, text=WELCOME_TEXT, reply_markup=make_buttons())
        users = load_json(ACCEPTED_USERS_FILE)
        if request.from_user.id not in users:
            users.append(request.from_user.id)
            save_json(ACCEPTED_USERS_FILE, users)
    except Exception as e:
        print("Error in join request:", e)

def make_buttons():
    buttons = load_json(BUTTONS_FILE)
    keyboard = []
    for btn in buttons:
        keyboard.append([InlineKeyboardButton(btn['name'], url=btn['link'])])
    return InlineKeyboardMarkup(keyboard) if keyboard else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        text = (
            "✅ Bot Command Menu:\n"
            "/start - Show this help\n"
            "/AutoAcceptedUsers - Total accepted users\n"
            "/broadcast <message> - Send message to all users\n"
            "/addbutton - Add new button\n"
            "/showbuttons - Show saved buttons"
        )
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("You are not admin.")

async def show_accepted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_json(ACCEPTED_USERS_FILE)
    await update.message.reply_text(f"Total Auto-Accepted Users: {len(users)}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    msg = ' '.join(context.args)
    if not msg:
        await update.message.reply_text("Use: /broadcast your_message")
        return

    users = load_json(ACCEPTED_USERS_FILE)
    success = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=msg)
            success += 1
        except:
            continue
    await update.message.reply_text(f"Broadcast sent to {success} users.")

async def addbutton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        await update.message.reply_text("Send button name and link like:\nName | https://t.me/yourchannel")
        context.user_data['waiting_for_button'] = True
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_button'):
        try:
            name, link = update.message.text.split("|")
            name = name.strip()
            link = link.strip()
            buttons = load_json(BUTTONS_FILE)
            buttons.append({'name': name, 'link': link})
            save_json(BUTTONS_FILE, buttons)
            await update.message.reply_text(f"✅ Button saved: {name}")
            context.user_data['waiting_for_button'] = False
        except:
            await update.message.reply_text("Wrong format. Use:\nName | https://t.me/yourchannel")

async def showbuttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = load_json(BUTTONS_FILE)
    if not buttons:
        await update.message.reply_text("No buttons saved.")
    else:
        msg = "Saved Buttons:\n\n"
        for b in buttons:
            msg += f"- {b['name']}\n"
        await update.message.reply_text(msg)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(API_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(join_request_handler))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("AutoAcceptedUsers", show_accepted))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("addbutton", addbutton))
    app.add_handler(CommandHandler("showbuttons", showbuttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
