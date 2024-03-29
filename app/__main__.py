import logging
import os
from pathlib import Path

from aiogram import Dispatcher, Bot
from sqlalchemy.orm import close_all_sessions

from app.config import load_config
from app.config.logging_config import setup_logging
from app.handlers import setup_handlers
from app.models.config.main import Paths

logger = logging.getLogger(__name__)

version = '1.0.6'


def main():
    paths = get_paths()

    setup_logging(paths)
    config = load_config(paths)

    dp = Dispatcher()
    # setup_middlewares(dp, create_pool(config.db), config.bot)
    setup_handlers(dp, config.bot)
    bot = Bot(
        token=config.bot.token,
        parse_mode="HTML",
        session=config.bot.create_session(),
    )

    logger.info("started")
    logger.info(f"version {version}")
    try:
        dp.run_polling(bot)
    finally:
        close_all_sessions()
        logger.info("stopped")


def get_paths() -> Paths:
    if path := os.getenv("BOT_PATH"):
        return Paths(Path(path))
    return Paths(Path(__file__).parent.parent)


if __name__ == '__main__':
    main()
