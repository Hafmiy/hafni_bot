from aiogram.filters import Filter, BaseFilter
from aiogram.types import Message


class SuperuserFilter(Filter):
    def __init__(self, superusers: list[int]) -> None:
        self.superusers = superusers

    async def __call__(self, message: Message) -> bool:
        return is_superuser(message, self.superusers)


def is_superuser(message: Message, superusers: list[int]) -> bool:
    return message.from_user.id in superusers


class SuperuserPassFilter(BaseFilter):
    def __init__(self, superusers: list[int]) -> None:
        self.superusers = superusers

    async def __call__(self, message: Message) -> dict:
        return {'superuser': is_superuser(message, self.superusers)}
