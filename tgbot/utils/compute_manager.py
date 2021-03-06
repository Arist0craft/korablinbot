import configparser
import logging
from pathlib import Path

from oci import wait_until
from oci.config import validate_config
from oci.core import ComputeClient
from oci.exceptions import ServiceError

from app.settings import OCI_SETTING

START = "START"
SOFTSTOP = "SOFTSTOP"


class ComputeEngineManager:
    client: ComputeClient
    instance_id: str

    def __init__(self, config: dict):
        validate_config(config)
        self.client = ComputeClient(config)
        instance_id = config.get("instance_id")
        if self.get_instance(instance_id):
            self.instance_id = instance_id

    def get_instance(self, instance_id):
        try:
            response = self.client.get_instance(instance_id)
            return response

        except ServiceError as err:
            logging.exception(err)
            raise err

    @classmethod
    def from_config(
        cls, config_path: Path, section="DEFAULT"
    ) -> "ComputeEngineManager":
        if not (config_path.exists() and config_path.is_file()):
            raise ValueError("Config file doesn't exists")

        parser = configparser.ConfigParser()
        parser.read(config_path)
        config = dict(parser.items(section))
        config["key_file"] = (
            Path(config_path).resolve().parent / config["key_file"]
        ).absolute()
        return cls(config)

    def start_instance(self):
        try:
            self.client.instance_action(instance_id=self.instance_id, action=START)
            response = wait_until(
                self.client,
                self.get_instance(self.instance_id),
                "lifecycle_state",
                "RUNNING",
            )
            return response

        except ServiceError as err:
            raise err

    def stop_instance(self):
        try:
            self.client.instance_action(instance_id=self.instance_id, action=SOFTSTOP)
            response = wait_until(
                self.client,
                self.get_instance(self.instance_id),
                "lifecycle_state",
                "STOPPED",
            )
            return response

        except ServiceError as err:
            raise err


compute_client = ComputeEngineManager(OCI_SETTING)
