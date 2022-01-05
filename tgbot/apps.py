import os

from django.apps import AppConfig

if mc_port := os.environ.get("MC_PORT"):
    mc_port = int(mc_port)


class TgBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tgbot"

    bot_token: str = os.environ["BOT_TOKEN"]
    debug: bool = os.environ.get("DEBUG_BOT", True)
    mc_host: str = os.environ.get("MC_HOST")
    mc_port: int = mc_port
