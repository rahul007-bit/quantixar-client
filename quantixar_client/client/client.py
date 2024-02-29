import requests
import json
from typing import List
from .config import Config
from .types import Payload


class QuantixarClient:
    def __init__(self, host: str = "localhost", port: int = 8954, config: 'Config' = None):
        self.host = host
        self.port = port
        self.config = config if config else Config.default()

    @staticmethod
    def new(host: str, port: int, config: Config) -> 'QuantixarClient':
        return QuantixarClient(host, port, config)

    def new_config(self, config: 'Config') -> None:
        self.config = config

    def get_api(self, endpoint: str) -> str:
        return f"http://{self.host}:{self.port}{endpoint}"

    async def insert(self, value: List[float], payload: Payload) -> None:
        api = self.get_api("/vector")
        body = json.dumps({
            "vectors": value,
            "payload": payload
        })
        response = requests.post(api, data=body)
        return response.text

    def query(self, value: List[float]) -> None:
        api = self.get_api("/vector/search")
        body = json.dumps({"vector": value,"k": 10})
        response = requests.post(api, data=body)
        return response.json()