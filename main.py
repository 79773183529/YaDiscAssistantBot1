import asyncio
import logging

import emoji
from aiogram import Bot
from aiogram.types import BotCommand

from common import register_handlers_common
from send_photo import register_handlers_send_photo

from bot import bot, dp

logging.basicConfig(level=logging.INFO)


async def main():
    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_send_photo(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/send", description=f"{emoji.emojize(':magnifying_glass_tilted_left:')} Send"
                                                f" a photo"),
        BotCommand(command="/cancel", description=f"{emoji.emojize(':chequered_flag:')} Cancel the current action")
    ]
    await bot.set_my_commands(commands)


if __name__ == '__main__':
    asyncio.run(main())
