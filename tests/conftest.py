import datetime
import hashlib

import pytest

import api
from src.yaml_config import YamlConfig


class TestApiScenario:
    def __init__(self):
        self.context = {}
        self.headers = {}
        self.settings = {}

    def get_response(self, request):
        return api.method_handler({"body": request, "headers": self.headers},
                                  self.context, self.settings)

    @staticmethod
    def set_valid_auth(request):
        config = YamlConfig().read()
        if request.get("login") == config['admin']['login']:
            request["token"] = hashlib.sha512((datetime.datetime.now()
                                              .strftime("%Y%m%d%H")
                                              + config['admin'
                                                       ]['salt']).encode(
                                                       'utf-8')).hexdigest()
        else:
            msg = request.get("account", "") + request.get("login", "") \
                  + config['request']['salt']
            request["token"] = hashlib.sha512(msg.encode('utf-8')).hexdigest()


@pytest.fixture(scope="session")
def scenario():
    scenario = TestApiScenario()
    return scenario


@pytest.fixture(scope="session")
def configfile():
    return r".\src\config\test_config.yml"
