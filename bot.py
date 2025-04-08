import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
import json
import os
from datetime import datetime, timedelta

API_TOKEN = '7320159726:AAESYR2n1EGC9f1VFVnwlPv1sKRrjZ_4gpo'
ADMIN_IDS = [7665158009, 7656706051, 7644302009]

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

accepted_users = set()
button_list = []
auto_delete_time = 60
auto_post_interval = None
target_channels = ['-1001963974161']
welcome_message = """🔥 WELCOME OUR CHANNEL 🔥  
☠ OFFICIAL [VIP] TELEGRAM CHANNEL ☠  
...  
🔥 JOIN THIS VIP  CHANNEL FAST👇"""

# Save & load button data
def save_buttons():
    with open('buttons.json', 'w') as f:
        json.dump(button_list, f)

def load_buttons():
    global button_list
    if os.path.exists('buttons.json'):
        with open('buttons.json', 'r') as f:
            button_list = json.load(f)

# Save & load accepted user data
def save_users():
    with open('users.json', 'w') as f:
        json.dump(list(accepted_users), f)

def load_users():
    global accepted_users
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            accepted_users = set(json.load(f))
            @dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        cmds = [
            "/addbutton - नया बटन जोड़ें",
            "/showbuttons - सभी बटन लिस्ट देखें",
            "/postlist - सभी चैनलों में बटन लिस्ट भेजें",
            "/setdelete <seconds> - auto-delete टाइम सेट करें",
            "/setautopost <seconds> - auto-post टाइम सेट करें",
            "/AutoAcceptedUsers - auto-accepted यूज़र्स की गिनती",
            "/broadcast <message> - सभी यूज़र्स को मैसेज भेजें"
        ]
        await message.reply("\n".join(cmds))

@dp.message_handler(commands=['addbutton'])
async def add_button(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        try:
            parts = message.text.split(' ', 2)
            name, url = parts[1], parts[2]
            button_list.append({'name': name, 'url': url})
            save_buttons()
            await message.reply(f"✅ बटन '{name}' जोड़ा गया।")
        except:
            await message.reply("❌ Format: /addbutton <name> <url>")

@dp.message_handler(commands=['showbuttons'])
async def show_buttons(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        text = "\n".join([f"{i+1}. {b['name']}" for i, b in enumerate(button_list)])
        await message.reply(text or "कोई बटन नहीं है।")

@dp.message_handler(commands=['postlist'])
async def post_buttons(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        kb = InlineKeyboardMarkup(row_width=2)
        for btn in button_list:
            kb.add(InlineKeyboardButton(btn['name'], url=btn['url']))
        for cid in target_channels:
            msg = await bot.send_message(cid, "👇 VIP चैनल्स की लिस्ट 👇", reply_markup=kb)
            await asyncio.sleep(1)
            await asyncio.sleep(auto_delete_time)
            await msg.delete()

@dp.message_handler(commands=['setdelete'])
async def set_delete(message: types.Message):
    global auto_delete_time
    if message.from_user.id in ADMIN_IDS:
        try:
            auto_delete_time = int(message.text.split()[1])
            await message.reply(f"✅ Auto-delete time set to {auto_delete_time} sec.")
        except:
            await message.reply("❌ Format: /setdelete <seconds>")

@dp.message_handler(commands=['setautopost'])
async def set_autopost(message: types.Message):
    global auto_post_interval
    if message.from_user.id in ADMIN_IDS:
        try:
            sec = int(message.text.split()[1])
            auto_post_interval = sec
            await message.reply(f"✅ Auto-post time set to {sec} sec.")
        except:
            await message.reply("❌ Format: /setautopost <seconds>")

async def auto_post_job():
    while True:
        if auto_post_interval:
            await post_buttons(types.Message(chat=types.Chat(id=ADMIN_IDS[0], type="private"), from_user=types.User(id=ADMIN_IDS[0], is_bot=False), message_id=0))
        await asyncio.sleep(auto_post_interval or 5)

@dp.message_handler(commands=['AutoAcceptedUsers'])
async def show_accepted(message: types.Message):
    await message.reply(f"✅ Total Auto-Accepted Users: {len(accepted_users)}")

@dp.message_handler(commands=['broadcast'])
async def broadcast_msg(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        text = message.text.replace('/broadcast ', '')
        count = 0
        for uid in accepted_users:
            try:
                await bot.send_message(uid, text)
                count += 1
            except:
                pass
        await message.reply(f"✅ Broadcast sent to {count} users.")

@dp.chat_join_request_handler()
async def join_handler(update: types.ChatJoinRequest):
    try:
        await bot.approve_chat_join_request(update.chat.id, update.from_user.id)
        accepted_users.add(update.from_user.id)
        save_users()
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton("VIP Channel", url=button_list[0]['url'] if button_list else "https://t.me"))
        await bot.send_message(update.from_user.id, welcome_message, reply_markup=kb)
    except:
        pass

if __name__ == '__main__':
    load_buttons()
    load_users()
    loop = asyncio.get_event_loop()
    loop.create_task(auto_post_job())
    executor.start_polling(dp, skip_updates=True)
