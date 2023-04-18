import calendar
import random
import re
from datetime import datetime, timedelta

import pytz
from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import ContentType
from aiogram.types import FSInputFile
from aiogram.types import Message
from moviepy.editor import *

from app.feature import file_handler, media
from app.feature.exceptions.exceptions import BotLogicException, UserInputException
from app.feature.untils.mime_util import *

members = ["Ферал","Реноме","Хафний","Славик","Мунстик","Зирич","Тексер","Заец","Кот","Тигр","Пинки","Импрувед","Плюхен","Дарккипер","Сергей Блинов","Суса","Алриша","Настася","Влад","Перламутра","Джон","Юм","Ламун","Лиса","Саншаин","Виталик","Вуф","Допельгангер","Арти","Френк","Жирон","Ворки","Пушкарина","Антонидас","Саендра","Анидакс","Висперс","Аняняша","Курама","Мира","Лирали","Светич","Импрувед","Никита","Яхени"]
wow_class_spec = {"Вар" : ["Прот", "Фури", "Армс"], "Пал": ["Прот", "Ретри", "Холи"],"Хант" : ["БМ", "ММ", "Допель"],"Шаман" : ["Енх", "Элем", "Рестор"],"Маг" : ["Фаер", "Фрост", "Аркан"],"Варлок" : ["Демон", "Дестр", "Аффлик"] ,"Монк" : ["Брю", "ВВ", "МВ"] ,"Друид" : ["Сова", "Медвед", "Пень", "Вуфёнак"],"ДК" : ["Фрост", "Анхоли", "Блад"] ,"ДХ" : ["Хавок", "Венженс"],"Дракарис": ["ДД", "Хил"]}

tanks = ["Вар Прот", "Пал Прот", "Монк Брю", "Друид Медвед", "ДК Блуд","ДХ Венженс",]
dds = {"Вар" : ["Фури", "Армс"], "Пал": ["Ретри",],"Хант" : ["БМ", "ММ", "Допель"],"Шаман" : ["Енх", "Элем",],"Маг" : ["Фаер", "Фрост", "Аркан"],"Варлок" : ["Демон", "Дестр", "Аффлик"] ,"Монк" : ["ВВ",] ,"Друид" : ["Сова", "Вуфёнак"],"ДК" : ["Фрост", "Анхоли",] ,"ДХ" : ["Хавок",],"Дракарис": ["ДД"]}
healers = ["Пал Холи","Шаман Рестор","Монк МВ","Друид Пень","Дракарис Хил"]


async def delete(message: Message):
    await message.reply_to_message.delete()


async def create_mplus(message: Message):
    already_in_party = set()
    result = ''

    def _roll_member():
        while True:
            _member = random.choice(members)
            if _member not in already_in_party:
                already_in_party.add(_member)
                return _member

    result += 'Танк: ' + _roll_member() + " - " + random.choice(tanks) + "\n"
    result += 'Хил: ' + _roll_member() + " - " + random.choice(healers) + "\n"
    result += 'ДД:\n'
    for i in range(3):
        classes = list(dds.keys())
        clas = random.choice(classes)
        spec = random.choice(dds[clas])
        result += _roll_member() + " - " + clas + " " + spec + "\n"
    await message.reply(result)


async def create_raid(message: Message):
    already_in_raid = set()
    result = 'Танки:\n'
    for i in range(2):
        while True:
            member = random.choice(members)
            if member not in already_in_raid:
                already_in_raid.add(member)
                break
        result += member + " - " + random.choice(tanks) + "\n"

    result += '\nХилы:\n'
    for i in range(4):
        while True:
            member = random.choice(members)
            if member not in already_in_raid:
                already_in_raid.add(member)
                break
        result += member + " - " + random.choice(healers) + "\n"

    result += '\nДД:\n'
    for i in range(14):
        while True:
            if i == 13 and "Реноме" not in already_in_raid:
                member = "Реноме"
                break
            member = random.choice(members)
            if member not in already_in_raid:
                already_in_raid.add(member)
                break
        classes = list(dds.keys())
        clas = random.choice(classes)
        spec = random.choice(dds[clas])
        result += member + " - " + clas + " " + spec + "\n"
    return await message.reply(result)


async def roll_main(message: Message, command: CommandObject):
    precision = command.args
    if not precision:
        classes = list(wow_class_spec.keys())
        clas = random.choice(classes)
        spec = random.choice(wow_class_spec[clas])
        return await message.reply(clas + " " + spec)
    if precision == '1':
        classes = list(wow_class_spec.keys())
        clas = random.choice(classes)
        return await message.reply(clas)


async def roll_things(message: Message, command: CommandObject):
    if not message.reply_to_message:
        things = command.args.split(" ")
    else:
        things = message.reply_to_message.text.split(" ")
    return await message.reply(random.choice(things))


async def roll_member(message: Message):
    member = random.choice(members)
    await message.reply(member)


async def get_sup_timer(message: Message):
    interval = 12600
    active_sup = 11700
    date_time = datetime.today().astimezone(pytz.timezone('UTC'))
    now = calendar.timegm(date_time.timetuple())
    feast_start = 1668985200
    to_next_sup = interval - divmod(now - feast_start, interval)[1]
    if to_next_sup > active_sup:
        await message.reply('Суп прямо сейчас, до конца ' + str(timedelta(seconds=to_next_sup - active_sup)))
    else:
        await message.reply('Суп через ' + str(timedelta(seconds=to_next_sup)))


async def convert(message: Message, bot: Bot):
    await video_check(message.reply_to_message, bot, media.convert)


async def auto_convert(message: Message, bot: Bot):
    try:
        if is_video_link(message.text) and not is_mp4_link(message.text):
            await video_check(message, bot, media.convert)
    except:
        pass


async def mirror(message: Message, bot: Bot):
    await hybrid_check(message.reply_to_message, bot, media.mirror_image)


async def cut_tik_tok(message: Message, command: CommandObject, bot: Bot):
    args_string = command.args
    if not args_string:
        await video_check(message.reply_to_message, bot, media.cut_video,)
    else:
        try:
            args = args_string.split(' ')
            reg_exp = r'^([0-9]?[0-9]):[0-9][0-9]$'
            if len(args) == 2:
                from_t = args[0]
                to_t = args[1]
                if not re.match(reg_exp, from_t) and re.match(reg_exp, to_t):
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            raise UserInputException(
                '(//ω//) нужны параметры в форматике /cutt 0:00(времечко начала) 1:20(сколько секундочек отрезать)')
        await video_check(message.reply_to_message, bot, media.cut_video, args={'from_t': from_t, 'to_t': to_t})


async def reverse(message: Message, bot: Bot):
    await video_check(message.reply_to_message, bot, media.reverse_video)


async def circle(message: Message, bot: Bot):
    await video_check(message.reply_to_message, bot, media.circle_video)


async def kekpuk(message: Message, bot: Bot):
    await hybrid_check(message.reply_to_message, bot, media.left_flip)
    await hybrid_check(message.reply_to_message, bot, media.right_flip)


async def pukkek(message: Message, bot: Bot):
    await hybrid_check(message.reply_to_message, bot, media.top_flip)
    await hybrid_check(message.reply_to_message, bot, media.bottom_flip)


async def mirroring(message: Message, bot: Bot, command: CommandObject):
    func = media.left_flip if '/lmirr' in command.command else media.right_flip
    await hybrid_check(message.reply_to_message, bot, func)


async def implode(message: Message, bot: Bot, command: CommandObject):
    coeff_str = command.args
    if not coeff_str:
        coeff_float = 0.5
    else:
        try:
            coeff_float = 1 - 1 / float(coeff_str)
        except ValueError:
            raise UserInputException('(￣ ￣|||) нужен коэффициентик впучиванья))')
    await hybrid_check(message.reply_to_message, bot, media.implode, {'coeff': coeff_float})


async def explode(message: Message, bot: Bot, command: CommandObject):
    coeff_str = command.args
    if not coeff_str:
        coeff_float = -0.5
    else:
        try:
            coeff_float = -1 + 1/float(coeff_str)
        except ValueError:
            raise UserInputException('(￣ ￣|||) нужен коэффициентик пученья)')
    await hybrid_check(message.reply_to_message, bot, media.implode, {'coeff': coeff_float})


async def swirl(message: Message, bot: Bot, command: CommandObject):
    coeff_str = command.args
    if not coeff_str:
        coeff_float = 60
    else:
        try:
            coeff_float = float(coeff_str) * 360 / 100
        except ValueError:
            raise UserInputException('(￣ ￣|||) нужен коэффициентик крутки)')
    await hybrid_check(message.reply_to_message, bot, media.swirl, {'coeff': coeff_float})


async def roll(message: Message, command: CommandObject):
    max_str = command.args
    if not max_str:
        max_int = 100
    else:
        try:
            max_int = int(max_str)
        except ValueError:
            raise UserInputException('(￣ ￣|||) попытайся роллить циферку))')
    if max_int <= 1:
        raise UserInputException('(￢_￢;) вообще тут должно быть положительное число больше 1...')
    await message.reply('1-'+str(max_int)+': '+str(random.SystemRandom().randint(1, max_int)))


async def fast_video(message: Message, bot: Bot, command: CommandObject):
    coeff_str = command.args
    if not coeff_str:
        coeff_float = 2
    else:
        try:
            coeff_float = float(coeff_str)
        except ValueError:
            raise UserInputException(
                '(￣ ￣|||) нужен коэффициентик ускорения с точечкой в роли десятичного разделителя(примерчик: 1.5))')
    await video_check(message.reply_to_message, bot, media.speed_fx_video, {'coeff': coeff_float})


async def slow_video(message: Message, bot: Bot, command: CommandObject):
    coeff_str = command.args
    if not coeff_str:
        coeff_float = 0.5
    else:
        try:
            coeff_float = 1/float(coeff_str)
        except ValueError:
            raise UserInputException('(￣ ￣|||) нужен коэффициентик замедления с точечкой в роли десятичного разделителя(примерчик: 1.5))')
    await video_check(message.reply_to_message, bot, media.speed_fx_video, {'coeff': coeff_float})


async def hybrid_check(message: Message, bot: Bot, func, args=None):
    if args is None:
        args = {}
    if not message:
        raise UserInputException('(˘ω˘) нет медиа в реплайчике)')
    content_type = message.content_type
    if content_type is ContentType.VIDEO or content_type is ContentType.ANIMATION:
        await video_effect_handler(message, bot, func, args)
        return
    if content_type is ContentType.PHOTO:
        await image_effect_handler(message, bot, func, args)
        return
    if content_type is ContentType.STICKER:
        if message.sticker.is_animated or message.sticker.is_video:
            await video_effect_handler(message, bot, func, args)
            return
        else:
            await image_effect_handler(message, bot, func, args)
            return
    if content_type is ContentType.TEXT:
        if is_video_link(message.text):
            await video_effect_handler(message, bot, func, args)
            return
        if is_image_link(message.text):
            await image_effect_handler(message, bot, func, args)
            return
    if content_type is ContentType.DOCUMENT:
        if is_video_mime(message.document.mime_type):
            await video_effect_handler(message, bot, func, args)
            return
        if is_image_mime(message.document.mime_type):
            await image_effect_handler(message, bot, func, args)
            return


async def video_check(message: Message, bot: Bot, func, args=None):
    if args is None:
        args = {}
    if not message:
        raise UserInputException('(˘ω˘) нет медиа в реплайчике)')
    content_type = message.content_type
    if content_type is ContentType.VIDEO \
            or content_type is ContentType.ANIMATION \
            or (content_type is ContentType.STICKER and (message.sticker.is_animated or message.sticker.is_video)) \
            or (content_type is ContentType.TEXT and is_video_link(message.text)) \
            or (content_type is ContentType.DOCUMENT and is_video_mime(message.document.mime_type)):
        await func(message, bot, **args)
        return
    else:
        raise UserInputException('(´꒳`) в реплйчике не видео))')


async def image_effect_handler(message: Message, bot: Bot, func, args: dict):
    try:
        fh = file_handler.FileHandler(message, bot)
    except BotLogicException as exp:
        raise exp
    try:
        image_path = await fh.download_image()
        await func(image_path, fh.get_img_path(), **args)
        await message.reply_photo(FSInputFile(fh.get_img_path()))
        fh.dispose()
    except Exception as exp:
        fh.dispose()
        raise exp


async def video_effect_handler(message: Message, bot: Bot, func, args: dict):
    try:
        fh = file_handler.FileHandler(message, bot)
    except BotLogicException as exp:
        raise exp
    try:
        with await fh.download_video() as video:
            frames_path = fh.split_video_into_frames(video)
            for i in range(len(frames_path)):
                await func(frames_path[i], frames_path[i], **args)
            fps = video.fps
            video.close()
            clip = ImageSequenceClip(frames_path, fps=fps)
            clip.write_videofile(fh.get_export_video_path(), fps=fps)
            await message.reply_animation(FSInputFile(fh.get_export_video_path()))
            fh.dispose()
    except Exception as exp:
        fh.dispose()
        raise exp
