import random
import re
from aiogram import Bot
from aiogram.types import Message

from app.feature import media, video_check
from app.feature.utils.mime_util import *

BOT_NAME = "аврам"
CHOICE_TAG = 'или'


async def handle_text(message: Message, superuser: bool, bot: Bot, ):
    if superuser:
        await __auto_convert(message, bot)
    await __roll_text(message)


async def __roll_text(message: Message):
    if message.text:
        text = message.text.lower()
        if CHOICE_TAG in text and text.startswith(BOT_NAME):
            answer = await __roll_or(message.text)
            if answer:
                return await message.reply(answer)


async def __roll_or(text: str):
    words = re.sub(r'[^\w\s]+', '', text).split()
    choice_idx = words.index(CHOICE_TAG)
    if choice_idx == 1 and choice_idx < len(words) - 1:
        return
    return random.choice([words[choice_idx - 1], words[choice_idx + 1]])


async def __auto_convert(message: Message, bot: Bot, ):
    try:
        if is_video_link(message.text) and not is_mp4_link(message.text):
            await video_check(message, bot, media.convert)
    except:
        pass
