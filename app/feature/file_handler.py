import gc
import os
import shutil
from pathlib import Path

import requests
from PIL import Image
from aiogram import types, Bot
from moviepy.editor import VideoFileClip
from pyrlottie import convSingleLottie, LottieFile

from app.feature.exceptions.exceptions import UserInputException
from app.models.config.main import Paths


class FileHandler:
    def __init__(self, message: types.Message, bot: Bot):
        self.message = message
        self.bot = bot
        temp_path = get_paths().temp_path
        temp_path.mkdir(exist_ok=True)
        self._temp_dir = temp_path / str(message.message_id)
        self._temp_dir.mkdir(exist_ok=True)
        self._temp_image = self._temp_dir / 'orig'
        self._temp_video = self._temp_dir / 'origVideo'
        self._video_export = self._temp_dir / 'u_kota_umerla_mama.mp4'
        self._temp_frames_path = self._temp_dir / 'frames'

    def get_img_path(self):
        return self._temp_image

    def get_export_video_path(self):
        return self._video_export

    def get_frames_path(self):
        return self._temp_frames_path

    def set_gif_temp(self):
        self._temp_video = self._temp_video.with_suffix('.gif')

    def set_mp4_temp(self):
        self._temp_video = self._temp_video.with_suffix('.mp4')

    async def download_video(self) -> VideoFileClip:
        self.set_mp4_temp()
        file_id = None
        if self.message.video:
            file_id = self.message.video.file_id
        elif self.message.video_note:
            file_id = self.message.video_note.file_id
        elif self.message.animation:
            file_id = self.message.animation.file_id
        elif self.message.document:
            file_id = self.message.document.file_id
        elif self.message.sticker:
            if self.message.sticker.is_video:
                file_id = self.message.sticker.file_id
            else:
                self.set_gif_temp()
                await self._download_video_by_id(self.message.sticker.file_id)
                file = LottieFile(self._temp_video.as_posix())
                await convSingleLottie(file, {'v.gif'}, backgroundColour='FFFFFF')
        elif self.message.text:
            r = requests.get(self.message.text, stream=True, headers={'User-agent': 'Mozilla/5.0'})
            self._temp_video.touch(exist_ok=True)
            with self._temp_video.open('wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                f.close()
        else:
            raise UserInputException(
                '(◡ ω ◡) Неподходящее медиа в реплайчике. Должно быть видео или гифочка(не тикток)))')
        if file_id:
            await self._download_video_by_id(file_id)
        return VideoFileClip(self._temp_video.as_posix())

    async def download_image(self) -> str:
        if self.message.sticker:
            await self._download_image_by_id(self.message.sticker.file_id)
            image = Image.open(self._temp_image).convert("RGBA")
            new_image = Image.new("RGBA", image.size, "WHITE")
            new_image.paste(image, (0, 0), image)
            new_image.convert('RGB').save(self._temp_image, "JPEG")
        elif self.message.photo:
            await self._download_image_by_id(self.message.photo[-1].file_id)
        elif self.message.document:
            await self._download_image_by_id(self.message.document.file_id)
        elif self.message.text:
            r = requests.get(self.message.text, stream=True, headers={'User-agent': 'Mozilla/5.0'})
            with self._temp_image.open() as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                f.close()
        else:
            raise UserInputException('(◡ ω ◡) Неподходящее медиа в реплайчике. Должна быть картиночка или стикер))')
        return self._temp_image.as_posix()

    def split_video_into_frames(self, video):
        fps = video.fps
        self._temp_frames_path.mkdir(parents=True, exist_ok=True)
        frame_array_list = []
        for frame_index in range(1, int(video.duration * fps) + 1):
            try:
                frame_array = video.get_frame(frame_index / fps)
                path = (self.get_frames_path() / str(frame_index)).with_suffix('.jpg').as_posix()
                Image.fromarray(frame_array).save(path)
                frame_array_list.append(path)
            except UserWarning:
                pass
        return frame_array_list

    def dispose(self):
        shutil.rmtree(self._temp_dir, True)
        gc.collect()

    async def _download_video_by_id(self, file_id):
        file = await self.bot.get_file(file_id)
        await self.bot.download_file(file.file_path, self._temp_video.as_posix())

    async def _download_image_by_id(self, file_id):
        file = await self.bot.get_file(file_id)
        await self.bot.download_file(file.file_path, self._temp_image.as_posix())


def get_paths() -> Paths:
    if path := os.getenv("BOT_PATH"):
        return Paths(Path(path))
    return Paths(Path(__file__).parent.parent.parent)
