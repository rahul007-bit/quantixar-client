import requests
import json
from typing import Dict, List, Union
from .config import Config
from .types import Payload
import time


BatchItem = Dict[str, Union[List[float], Payload]]

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

    async def insert_batch(self, batch: List[List[BatchItem]]) -> None:
        api = self.get_api("/vector")
        body = []
        print(type(batch))
        for i, item in enumerate(batch):
            # {points: [{vectors: [], payload: {}, id:1}]}
            points = []
            print(f"Processing batch {i}")
            for j, point in enumerate(item):
                id = round(time.time() * 1000)
                points.append({
                    "vectors": point["vectors"],
                    "payload": point["payload"],
                    "id": id
                })
        
            body_point = json.dumps({"points": points})
            body.append(body_point)
            result = requests.post(api, data=body_point, headers={"Content-Type": "application/json"})
            print(result.text)
        
        # save to json file
        with open('data.json', 'w') as f:
            json.dump(body, f)
            f.close()
        

    async def insert(self, value: List[float], payload: Payload) -> None:
        api = self.get_api("/vector")
        body = json.dumps({
            "vectors": value,
            "payload": payload
        })
        response = requests.post(api, data=body)
        return response.text

    def query(self, value: List[float], k: int = 10) -> None:
        api = self.get_api("/vector/search")
        body = json.dumps({"vector": value,"k": k})
        response = requests.post(api, data=body)
        return response.json()