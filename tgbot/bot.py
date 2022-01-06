import sys
from logging import Logger

from celery.utils.log import get_task_logger
import telegram as tg
from telegram.ext import CommandHandler, Dispatcher, Updater

from app.settings import DEBUG, TGBOT_SETTINGS
from app.celery import app
from .handlers import start_server, stop_server
from utils import setup_logger


task_logger: Logger = get_task_logger(__name__)
logger: Logger = setup_logger(__name__)
if DEBUG:
    logger.setLevel("DEBUG")


handlers = [
    {
        "type": CommandHandler,
        "command": "start_server",
        "callback": start_server,
        "description": "Запуск сервера Майна",
    },
    {
        "type": CommandHandler,
        "command": "stop_server",
        "callback": stop_server,
        "description": "Остановка сервера Майна",
    },
]


def setup_bot() -> tg.Bot:
    logger.info("Start setup bot")
    tgbot: tg.Bot = tg.Bot(token=TGBOT_SETTINGS.get("TOKEN"))
    try:
        logger.info("Checking API Token")
        tgbot.get_me()
        logger.info("Token checking success")

        logger.info("Deleting BOT Commands")
        if not tgbot.delete_my_commands():
            raise tg.error.BadRequest("Commands weren't deleted, bad request")

        logger.info("Setting BOT Commands")
        if not tgbot.set_my_commands(
            [
                tg.BotCommand(h["command"], h["description"])
                for h in handlers
                if h["type"] == CommandHandler
            ]
        ):
            raise tg.error.BadRequest("Commands weren't set, bad request")
        return tgbot

    except tg.error.Unauthorized as err:
        logger.exception(err)
        sys.exit(1)

    except tg.error.BadRequest as err:
        logger.exception(err)
        sys.exit(1)


def setup_dispatcher(dp: Dispatcher) -> Dispatcher:
    [dp.add_handler(h["type"](h["command"], h["callback"])) for h in handlers]
    return dp


def run_polling():
    if not TGBOT_SETTINGS.get("DEBUG"):
        raise ValueError("Don't use pooling mode in production")
    updater = Updater(TGBOT_SETTINGS.get("TOKEN"), use_context=True)
    setup_dispatcher(updater.dispatcher)
    logger.info("Running polling mode")
    updater.start_polling()
    updater.idle()


if not TGBOT_SETTINGS.get("DEBUG"):
    bot: tg.Bot = setup_bot()
    dispatcher: Dispatcher = setup_dispatcher(Dispatcher(bot, None, 1))

    @app.task(ignore_result=True)
    def process_update(update_data: dict):
        task_logger.info("Handling update")
        dispatcher.process_update(tg.Update.de_json(update_data, dispatcher.bot))
