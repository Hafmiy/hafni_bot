from aiogram.types import Message

from app.config.const_config import AppConst


async def handle_voice(message: Message,):
    if message.from_user.id == AppConst.SUNSHINE_ID and not message.forward_sender_name:
        await __forward_sunshine(message)


async def __forward_sunshine(message: Message):
    await message.forward(AppConst.FORWARD_SUNSHINE_TO)
