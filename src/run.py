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
from aiohttp import ClientSession

load_dotenv()
TOKEN = getenv('TOKEN')
API_KEY = getenv('API_KEY')

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command_handler(message: Message)-> None:
    headers = {'Authorization': f"Bearer {API_KEY}"}
    user_id = message.from_user.id
    payload = { "student_id" : str(user_id) ,  "notify" : True }
    print(payload)
    async with ClientSession() as session:
        async with session.post( 'https://api.b33db57e.nip.io/api/v1/student/', json=payload, headers=headers) as response:
            if response.status == 200:
                reply = await response.json()
                await message.answer(f"Добро пожаловать!")
            else:
                print(response)
                await message.answer("Ошибка: не удалось зарегистрироваться в очереди. Попробуйте позже.")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())