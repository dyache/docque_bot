import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('TOKEN')
API_KEY = getenv('API_KEY')

dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)

@dp.message(commands=["start"])
async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username  
    
    payload = {"user_id": user_id, "username": username}

    async with ClientSession() as session:
        try:
            async with session.post(API_KEY, json=payload) as response:
                if response.status == 200:
                    reply = await response.json()
                    await message.answer(f"Добро пожаловать, {username}!\nВы добавлены в очередь.\nВаш номер: {reply.get('queue_number')}")
                else:
                    await message.answer("Ошибка: не удалось зарегистрироваться в очереди. Попробуйте позже.")
        except Exception as e:
            logging.error(f"Ошибка при запросе к серверу: {e}")
            await message.answer("Произошла ошибка при подключении к серверу.")

async def main():
    dp.include_router(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())