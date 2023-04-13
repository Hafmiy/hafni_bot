from aiogram.filters import Filter
from aiogram.types import Message

from app.filters.superusers import is_superuser


class SuperuserFilter(Filter):
    def __init__(self, superusers: list[int]) -> None:
        self.superusers = superusers

    async def __call__(self, message: Message) -> bool:
        return await is_superuser(message, self.superusers)
