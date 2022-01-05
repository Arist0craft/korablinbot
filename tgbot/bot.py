import sys

import telegram as tg
from telegram.ext import CommandHandler, Dispatcher, Updater

from app.settings import DEBUG, TGBOT_SETTINGS
from .handlers import *
from utils import setup_logger


logger = setup_logger(__name__)
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
    dispatcher: Dispatcher = setup_dispatcher(Dispatcher(bot, None, 0))

    webhook_url = (
        TGBOT_SETTINGS.get("HOST")
        if TGBOT_SETTINGS.get("HOST")[-1] == "/"
        else TGBOT_SETTINGS.get("HOST") + "/"
    )
    webhook_url += TGBOT_SETTINGS.get("TOKEN") + "/" + "webhook/"
    logger.debug(f"Setting webhook to {webhook_url}")
    if bot.set_webhook(webhook_url):
        logger.info("Webhook successfully set")
    else:
        logger.error("Wasn't set")
