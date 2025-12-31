import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

last_user_id = None

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Напиши сообщение, и администратор тебе ответит.")

@dp.message(F.from_user.id != ADMIN_ID)
async def from_user(message: Message):
    global last_user_id
    last_user_id = message.from_user.id
    await bot.send_message(ADMIN_ID, f"📩 Сообщение от {message.from_user.id}:\n{message.text}")
    await message.answer("Сообщение отправлено администратору ✅")

@dp.message(F.from_user.id == ADMIN_ID)
async def from_admin(message: Message):
    if not last_user_id:
        await message.answer("❌ Пока некому отвечать")
        return
    await bot.send_message(last_user_id, message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())