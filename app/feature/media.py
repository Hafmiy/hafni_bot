from enum import Enum

from PIL import Image
from aiogram import Bot
from aiogram.types import ContentType, Message
from aiogram.types import FSInputFile
from moviepy.editor import *
from wand.image import Image as wImage

from app.feature import file_handler
from app.feature.exceptions.exceptions import BotLogicException


class Directions(Enum):
    LEFT = 0,
    RIGHT = 1,
    TOP = 2,
    BOTTOM = 3


async def left_flip(image_path: str, export_path: str):
    return await __flip_vertical(Directions.LEFT, Image.open(image_path), export_path)


async def right_flip(image_path: str, export_path: str):
    return await __flip_vertical(Directions.RIGHT, Image.open(image_path), export_path)


async def top_flip(image_path: str, export_path: str):
    return await __flip_horizontal(Directions.TOP, Image.open(image_path), export_path)


async def bottom_flip(image_path: str, export_path: str):
    return await __flip_horizontal(Directions.BOTTOM, Image.open(image_path), export_path)


async def mirror_image(image_path: str, export_path: str):
    image = Image.open(image_path)
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    image.save(export_path, 'jpeg')
    image.close()


async def __flip_horizontal(direction: Directions, image: Image, path: str):
    if direction is Directions.TOP:
        top_part = image.crop((0, 0, image.size[0], image.size[1] / 2))
        bottom_part = top_part.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        bottom_part = image.crop((0, image.size[1] / 2, image.size[0], image.size[1]))
        top_part = bottom_part.transpose(Image.FLIP_TOP_BOTTOM)
    result = Image.new('RGB', (image.size[0], image.size[1]), (255, 255, 255))
    result.paste(top_part, (0, 0))
    result.paste(bottom_part, (0, int(image.size[1]/2)))
    result.save(path, 'jpeg')
    image.close()
    result.close()


async def __flip_vertical(direction: Directions, image: Image, path: str, ):
    if direction is Directions.LEFT:
        left_part = image.crop((0, 0, image.size[0] / 2, image.size[1]))
        right_part = left_part.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        right_part = image.crop((image.size[0] / 2, 0, image.size[0], image.size[1]))
        left_part = right_part.transpose(Image.FLIP_LEFT_RIGHT)
    result = Image.new('RGB', (2 * right_part.size[0], right_part.size[1]), (255, 255, 255))
    result.paste(left_part, (0, 0))
    result.paste(right_part, (right_part.size[0], 0))
    result.save(path, 'jpeg')
    image.close()
    result.close()


async def convert(message: Message, bot: Bot):
    try:
        fh = file_handler.FileHandler(message, bot)
    except BotLogicException as exp:
        raise exp
    with await fh.download_video() as video:
        fps = video.fps
        if message.content_type is ContentType.TEXT:
            video.write_videofile(fh.get_export_video_path(), fps=fps)
        else:
            video.without_audio().write_videofile(fh.get_export_video_path(), fps=fps)
        video.close()
        await message.reply_animation(FSInputFile(fh.get_export_video_path()))
        fh.dispose()


async def cut_video(message: Message, bot: Bot, **args: dict):
    try:
        fh = file_handler.FileHandler(message, bot)
    except BotLogicException as exp:
        raise exp
    with await fh.download_video() as video:
        fps = video.fps
        if 'from_t' in args:
            video = video.subclip(args['from_t'], args['to_t'])
        else:
            if video.duration > 4:
                video = video.subclip(0, video.duration - 4)
        video.write_videofile(fh.get_export_video_path(), fps=fps)
        video.close()
        await message.reply_video(FSInputFile(fh.get_export_video_path()))
        fh.dispose()


async def circle_video(message: Message, bot: Bot):
    try:
        fh = file_handler.FileHandler(message, bot)
    except BotLogicException as exp:
        raise exp
    with await fh.download_video() as video:
        frames_path = fh.split_video_into_frames(video)
        fps = video.fps
        video.close()
        reversed_frame_path = frames_path.copy()
        reversed_frame_path.reverse()
        frames_path.extend(reversed_frame_path)
        clip = ImageSequenceClip(frames_path, fps=fps)
        clip.write_videofile(fh.get_export_video_path(), fps=fps)
        clip.close()
        await message.reply_animation(FSInputFile(fh.get_export_video_path()))
        fh.dispose()


async def reverse_video(message: Message, bot: Bot):
    try:
        fh = file_handler.FileHandler(message, bot)
    except BotLogicException as exp:
        raise exp
    with await fh.download_video() as video:
        frames_path = fh.split_video_into_frames(video)
        fps = video.fps
        video.close()
        frames_path.reverse()
        clip = ImageSequenceClip(frames_path, fps=fps)
        clip.write_videofile(fh.get_export_video_path(), fps=fps)
        clip.close()
        await message.reply_animation(FSInputFile(fh.get_export_video_path()))
        fh.dispose()


async def speed_fx_video(message: Message, bot: Bot, **args: dict):
    coeff = args['coeff']
    try:
        fh = file_handler.FileHandler(message, bot)
    except BotLogicException as exp:
        raise exp
    with await fh.download_video() as video:
        result = video.fx(vfx.speedx, coeff)
        result.write_videofile(fh.get_export_video_path(),)
        result.close()
        await message.reply_animation(FSInputFile(fh.get_export_video_path()))
        fh.dispose()


async def implode(image_path: str, export_path: str, **args: dict):
    image = wImage(filename=image_path)
    image.implode(args['coeff'])
    image.save(filename=export_path)


async def swirl(image_path: str, export_path: str, **args: dict):
    image = wImage(filename=image_path)
    image.swirl(args['coeff'])
    image.save(filename=export_path)
