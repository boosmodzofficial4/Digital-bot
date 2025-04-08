import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '7320159726:AAESYR2n1EGC9f1VFVnwlPv1sKRrjZ_4gpo'
ADMIN_ID = 7665158009

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Store auto-accepted users
accepted_users = set()

# Default welcome message and button
welcome_message = """🔥 WELCOME OUR CHANNEL 🔥
☠ OFFICIAL [VIP] TELEGRAM CHANNEL ☠

🔥 JOIN THIS VIP CHANNEL FAST 👇"""
welcome_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="VIP CHANNEL", url="https://t.me/yourchannel")]
])

@dp.chat_join_request()
async def handle_join_request(event: types.ChatJoinRequest):
    await asyncio.sleep(1)
    await bot.approve_chat_join_request(event.chat.id, event.from_user.id)
    accepted_users.add(event.from_user.id)
    await bot.send_message(
        chat_id=event.from_user.id,
        text=welcome_message,
        reply_markup=welcome_button
    )

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "<b>Bot Commands:</b>\n"
            "/start - Show this message\n"
            "/AutoAcceptedUsers - Total accepted users\n"
            "/broadcast <message> - Send message to all accepted users\n"
            "/addbutton - Add a new VIP button (coming soon)"
        )
    else:
        await message.answer("Bot is active!")

@dp.message(Command("AutoAcceptedUsers"))
async def cmd_auto_accepted_users(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"Total auto-accepted users: {len(accepted_users)}")

@dp.message(Command("broadcast"))
async def cmd_broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        await message.answer("Please provide a message: /broadcast <your message>")
        return
    count = 0
    for user_id in accepted_users:
        try:
            await bot.send_message(user_id, text)
            count += 1
        except:
            pass
    await message.answer(f"Broadcast sent to {count} users.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))
