import os

import django

from app.settings import TGBOT_SETTINGS
from tgbot.bot import bot
from utils import setup_logger

logger = setup_logger(__name__, debug=TGBOT_SETTINGS.get("DEBUG"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

if __name__ == "__main__":
    webhook_url = (
        TGBOT_SETTINGS.get("HOST")
        if TGBOT_SETTINGS.get("HOST")[-1] == "/"
        else TGBOT_SETTINGS.get("HOST") + "/"
    )
    webhook_url += TGBOT_SETTINGS.get("TOKEN") + "/" + "webhook/"
    logger.info(f"Setting webhook to {webhook_url}")
    if bot.set_webhook(webhook_url, drop_pending_updates=True):
        logger.info("Webhook successfully set")
    else:
        logger.error("Wasn't set")
