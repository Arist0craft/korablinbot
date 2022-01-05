import os
from time import sleep
from socket import timeout

from mcipc import query

from ..apps import TgBotConfig
from utils import setup_logger

logger = setup_logger(__name__)


class McWaiter:
    mc_client = query.Client(TgBotConfig.mc_host, TgBotConfig.mc_port, timeout=1)
    tries = 0

    def wait(self):
        while self.tries < int(os.environ.get("MC_CONNECTION_TRIES", 10)):
            try:
                self.tries += 1
                logger.info(f"Tries accepted {self.tries}")
                self.mc_client.connect()
                res = self.mc_client.stats()
                self.mc_client.disconnect()
                return res

            except timeout:
                if self.tries >= 11:
                    self.mc_client.disconnect()
                    raise timeout
                sleep(int(os.environ.get("MC_CONNECTION_WAIT", 20)))
