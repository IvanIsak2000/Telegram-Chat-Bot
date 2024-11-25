import asyncio

import pytz
import logging
from datetime import datetime

import requests
from inspect import stack, getmodule

from utils.config import BOT_KEY, MODERATOR_ID, MY_TIMEZONE


class BotLogger:
    def __init__(self, file: str = 'main.log') -> None:
        """
        Main logging class for a bot.

        Usage:
        1. Import class
        2. Call class with logging file(default, main.log)
        and with log level funcion(info, error, critical)
        """
        frame = stack()[1]
        module = getmodule(frame[0])
        name = module.__file__.split('/')[-1] if module else __name__

        self.logger = logging.getLogger(name)

        if not self.logger.hasHandlers():
            file_handler = logging.FileHandler(file)
            file_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                fmt=f'%(levelname)s - {name} - %(asctime)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.INFO)

        logging.getLogger('aiogram').setLevel(logging.WARNING)

    def formatTime(self, record, datefmt=None):
        """Override built-in function to get time in current location """
        tz = pytz.timezone(MY_TIMEZONE)
        record_time = datetime.fromtimestamp(record.created, tz)
        if datefmt:
            return record_time.strftime(datefmt)
        else:
            return record_time.isoformat()

    async def send_alert(self, text: str) -> None:
        url = f'https://api.telegram.org/bot{BOT_KEY}/sendMessage'
        params = {
            'chat_id': MODERATOR_ID,
            'text': f'Message from bot:\n{text}'}
        requests.post(url, params=params)

    async def info(self, message: str, send_alert: bool = False, extra: dict = None) -> None:
        if send_alert:
            await self.send_alert(text=message)
        self.logger.info(msg=message, extra=extra)

    async def error(self, message: str) -> None:
        self.logger.error(message)
        await self.send_alert(text=message)

    async def critical(self, message: str, extra: dict = None) -> None:
        self.logger.critical(message, extra=extra)
        await self.send_alert(text=f'{message}\nExtra:{extra}')
