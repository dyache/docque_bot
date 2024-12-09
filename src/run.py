from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiohttp import ClientSession
from dotenv import load_dotenv
from aiogram.filters import CommandStart
import aiohttp
load_dotenv()
TOKEN = getenv('TOKEN')
API_KEY = getenv('API_KEY')

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command_handler(message: Message)-> None:
    headers = {'TG-API-KEY': API_KEY}
    user_id = message.from_user.id
    username = message.from_user.username  
    payload = { "user_id" : user_id,  "username" : username }
    async with ClientSession() as session:
        async with aiohttp.session.post( 'https://api.b33db57e.nip.io/student/', json=payload) as response:
            if response.status == 200:
                print(response.body())
                reply = await response.json()
                await message.answer(f"Добро пожаловать, {username}!\nВы добавлены в очередь.\nВаш номер: {reply.get('queue_number')}")
            else:
                await message.answer("Ошибка: не удалось зарегистрироваться в очереди. Попробуйте позже.")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
