import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

accepted_users = set()
welcome_buttons = []

# Join request auto-approve
@dp.chat_join_request_handler()
async def approve_join_request(join_request: types.ChatJoinRequest):
    try:
        await bot.approve_chat_join_request(join_request.chat.id, join_request.from_user.id)
        accepted_users.add(join_request.from_user.id)

        # Welcome message with button
        if welcome_buttons:
            keyboard = InlineKeyboardMarkup(row_width=1)
            for name, url in welcome_buttons:
                keyboard.add(InlineKeyboardButton(text=name, url=url))
            await bot.send_message(join_request.from_user.id,
                "🔥 WELCOME OUR CHANNEL 🔥\n☠ OFFICIAL [VIP] TELEGRAM CHANNEL ☠\n🔥 JOIN THIS VIP  CHANNEL FAST👇",
                reply_markup=keyboard
            )
    except Exception as e:
        print("Error approving user:", e)
        # Command to see total accepted users
@dp.message_handler(commands=["AutoAcceptedUsers"])
async def show_accepted_users_count(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.reply(f"Total Auto-Accepted Users: {len(accepted_users)}")

# Broadcast message
@dp.message_handler(commands=["broadcast"])
async def broadcast_message(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text.split(maxsplit=1)
    if len(text) < 2:
        return await message.reply("Usage: /broadcast your_message")
    
    msg = text[1]
    count = 0
    for user_id in accepted_users:
        try:
            await bot.send_message(user_id, msg)
            count += 1
        except:
            pass
    await message.reply(f"Broadcast sent to {count} users.")

# Add VIP button (name + hidden link)
@dp.message_handler(commands=["addbutton"])
async def add_button(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        _, name, url = message.text.split(maxsplit=2)
        welcome_buttons.append((name, url))
        await message.reply(f"✅ Button added:\nName: {name}")
    except:
        await message.reply("Usage: /addbutton Button_Name https://your-link")

# Start Command - show all commands
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.reply(
            "Welcome Admin! Available Commands:\n"
            "/AutoAcceptedUsers - Total accepted users\n"
            "/broadcast <msg> - Send message to all\n"
            "/addbutton <name> <link> - Add hidden VIP button"
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
