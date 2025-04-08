import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, ChatJoinRequestHandler
)

TOKEN = "7656706051:AAEZTYWiffUFzAvyDkG2MmfH3Ktx0l_CblE"
ADMIN_ID = 7665158009
CHANNEL_IDS = [-1001963974161]  # Add more channels here
accepted_users = set()
button_list = []
auto_post_seconds = 3600
auto_post_task = None

# Auto-accept
async def join_request_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.chat_join_request.approve()
    user_id = update.chat_join_request.from_user.id
    accepted_users.add(user_id)
    if button_list:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(name, url=url)] for name, url in button_list])
        await context.bot.send_message(chat_id=user_id, text="Welcome!", reply_markup=keyboard)
    else:
        await context.bot.send_message(chat_id=user_id, text="Welcome!")
        # /AutoAcceptedUsers
async def show_accepted_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(f"Total accepted users: {len(accepted_users)}")

# /broadcast
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    message = ' '.join(context.args)
    count = 0
    for user_id in accepted_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            count += 1
        except:
            pass
    await update.message.reply_text(f"Broadcast sent to {count} users.")

# /addbutton <name> <url>
async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /addbutton <name> <url>")
        return
    name = context.args[0]
    url = context.args[1]
    button_list.append((name, url))
    await update.message.reply_text(f"Button '{name}' added.")

# /showbuttons
async def show_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not button_list:
        await update.message.reply_text("No buttons saved.")
        return
    reply = "\n".join([f"{i+1}. {btn[0]}" for i, btn in enumerate(button_list)])
    await update.message.reply_text(reply)
    # Auto-post
async def auto_post(context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(name, url=url)] for name, url in button_list])
    for channel_id in CHANNEL_IDS:
        msg = await context.bot.send_message(chat_id=channel_id, text="VIP Access", reply_markup=keyboard)
        await asyncio.sleep(5)
        await context.bot.delete_message(chat_id=channel_id, message_id=msg.message_id)

# /setautopost <seconds>
async def set_auto_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global auto_post_seconds, auto_post_task
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        auto_post_seconds = int(context.args[0])
        if auto_post_task:
            auto_post_task.cancel()
        auto_post_task = context.application.create_task(repeat_auto_post(context))
        await update.message.reply_text(f"Auto-post every {auto_post_seconds} seconds.")
    except:
        await update.message.reply_text("Usage: /setautopost <seconds>")

async def repeat_auto_post(context: ContextTypes.DEFAULT_TYPE):
    while True:
        await auto_post(context)
        await asyncio.sleep(auto_post_seconds)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        commands = [
            "/AutoAcceptedUsers",
            "/broadcast <message>",
            "/addbutton <name> <url>",
            "/showbuttons",
            "/setautopost <seconds>"
        ]
        await update.message.reply_text("Available commands:\n" + "\n".join(commands))

# Main
async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(join_request_handler))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("AutoAcceptedUsers", show_accepted_users))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("addbutton", add_button))
    app.add_handler(CommandHandler("showbuttons", show_buttons))
    app.add_handler(CommandHandler("setautopost", set_auto_post))

    print("Bot running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
