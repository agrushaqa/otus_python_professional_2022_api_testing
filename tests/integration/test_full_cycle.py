import json
import threading
from http.server import HTTPServer

import requests
from loguru import logger

from api import MainHTTPHandler
from src.redis_fill_data import fill_redis


class TestApi:

    def test_online_score(self):
        with HTTPServer(("localhost", 8095), MainHTTPHandler) as server:
            threading.Thread(target=server.serve_forever).start()
            headers = {'Content-Type': 'application/json',
                       'Content-Length': '278'}
            payload = {"account": "horns&hoofs", "login": "h&f",
                       "method": "online_score",
                       "arguments": {"phone": "79175002040",
                                     "email": "stupnikov@otus.ru"},
                       "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1"
                                "e19d2750a2c03e80dd209a27954dca045e5bb12418e7"
                                "d89b6d718a9e35af34e14e1d5bcd5a08f21fc95"}
            r = requests.post("http://localhost:8095/method",
                              data=json.dumps(payload),
                              headers=headers)
            logger.debug(r.text)
            server.shutdown()
            assert r.text == '{"response": {"score": 3.0' \
                             ', "non_empty_params": ["email", "phone"]},' \
                             ' "code": 200}'

    def test_clients_interests(self):
        fill_redis({"i:1": 5})
        fill_redis({"i:2": 0})
        fill_redis({"i:3": 25})
        with HTTPServer(("localhost", 8095), MainHTTPHandler) as server:
            threading.Thread(target=server.serve_forever).start()
            headers = {'Content-Type': 'application/json',
                       'Content-Length': '276'}
            payload = {"account": "horns&hoofs", "login": "h&f",
                       "method": "clients_interests", "arguments":
                           {"client_ids": [1, 2, 3], "date": "02.03.2021"},
                       "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be"
                                "1e19d2750a2c03e80dd209a27954dca045e5bb12418e"
                                "7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95"}
            r = requests.post("http://localhost:8095/method",
                              data=json.dumps(payload),
                              headers=headers)
            logger.debug(r.text)
            server.shutdown()
            assert r.text == '{"response":' \
                             ' {"1": 5, "2": 0, "3": 25}, "code": 200}'
