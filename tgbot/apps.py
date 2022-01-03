import os

from django.apps import AppConfig


class TgBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tgbot"

    bot_token = os.environ["BOT_TOKEN"]
