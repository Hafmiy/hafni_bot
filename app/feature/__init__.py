from functools import partial

from aiogram import Router, F
from aiogram.filters import Command, Filter

from app.feature.feature import *
from app.feature.filter.superuser_filter import SuperuserFilter, SuperuserPassFilter
from app.feature.raw_text_hanler import handle_text


def setup_feature_dispatchers(router: Router, superusers: list[int]):
    router.message.register(roll, Command(commands=['roll'],))
    router.message.register(roll_main, Command(commands=['roll_main']))
    router.message.register(create_mplus, Command(commands=['create_mplus'],))
    router.message.register(roll_things, Command(commands=['roll_things']))
    router.message.register(roll_member, Command(commands=['roll_member']))
    router.message.register(convert, Command(commands=['convert']))
    router.message.register(mirror, Command(commands=['mirror']))
    router.message.register(cut_tik_tok, Command(commands=['cutt']))
    router.message.register(reverse, Command(commands=['reverse']))
    router.message.register(circle, Command(commands=['circle']))
    router.message.register(kekpuk, Command(commands=['kekpuk']))
    router.message.register(pukkek, Command(commands=['pukkek']))
    router.message.register(mirroring, Command(commands=['lmirr', 'rmirr']))
    router.message.register(implode, Command(commands=['implode']))
    router.message.register(explode, Command(commands=['explode']))
    router.message.register(swirl, Command(commands=['swirl']))
    router.message.register(fast_video, Command(commands=['fast']))
    router.message.register(slow_video, Command(commands=['slow']))
    router.message.register(delete, Command(commands=['d']), SuperuserFilter(superusers))
    router.message.register(create_raid, Command(commands=['create_raid']), SuperuserFilter(superusers))
    router.message.register(handle_text, SuperuserPassFilter(superusers), F.text)

