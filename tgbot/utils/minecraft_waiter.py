from time import sleep
from socket import timeout

from mcipc import query

from app.settings import TGBOT_SETTINGS
from utils import setup_logger

logger = setup_logger(__name__)


class McWaiter:
    mc_client = query.Client(
        TGBOT_SETTINGS.get("MC_HOST"), TGBOT_SETTINGS.get("MC_PORT"), timeout=1
    )
    tries = 0

    def wait(self):
        while self.tries < TGBOT_SETTINGS.get("MC_CONNECTION_TRIES"):
            try:
                self.tries += 1
                logger.info(f"Tries accepted {self.tries}")
                self.mc_client.connect()
                res = self.mc_client.stats()
                self.mc_client.disconnect()
                return res

            except timeout:
                if self.tries >= TGBOT_SETTINGS.get("MC_CONNECTION_TRIES"):
                    self.mc_client.disconnect()
                    raise timeout
                sleep(TGBOT_SETTINGS.get("MC_CONNECTION_WAIT"))
