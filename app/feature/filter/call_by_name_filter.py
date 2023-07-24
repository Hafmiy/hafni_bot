from aiogram.filters import Filter
from aiogram.types import Message

BOT_NAME = "аврам"


class CallByNameFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        return message.text.lower().startswith(BOT_NAME.lower())
