import datetime
import hashlib
from http import HTTPStatus

from loguru import logger

from src.validators.select_validator import SelectValidator
from src.yaml_config import YamlConfig


class ParseRequest:
    def __init__(self, request):
        self.request = request
        self.method = None
        self.validation_failed_code = HTTPStatus.UNPROCESSABLE_ENTITY
        self.code = None
        self.response = None

    def check_auth(self):
        request = self.request['body']
        logger.info("check_auth. login:")
        logger.info(request.get("login"))
        config = YamlConfig().read()
        if request.get("login") == config['admin']['login']:
            token = hashlib.sha512((datetime.datetime.now()
                                    .strftime("%Y%m%d%H")
                                    + config['admin'
                                             ]['salt']).encode(
                                            'utf-8')).hexdigest()
        else:
            msg = request.get("account", "") + \
                  request.get("login", "") \
                  + config['request']['salt']
            token = hashlib.sha512(msg.encode('utf-8')).hexdigest()
        if token != request.get("token"):
            raise ValueError('invalid token')

    def _get_method(self):
        if 'body' in self.request.keys() is False:
            raise ValueError('body is absent')
        logger.info("request type:")
        logger.info(type(self.request))
        logger.info(self.request)
        logger.info("method:")
        logger.info(self.request['body']['method'])
        if 'method' in self.request['body'].keys() is False:
            raise ValueError('method is absent')
        self.method = self.request['body']['method']

    @logger.catch
    def get(self):
        try:
            self._get_method()
        except Exception as e:
            self.code = self.validation_failed_code
            self.response = str(e)
            return self.response, self.code

        try:
            self.check_auth()
        except Exception:
            self.code = HTTPStatus.FORBIDDEN
            self.response = "invalid credentials"
            return self.response, self.code

        try:
            validator = SelectValidator(self.request)
            info = getattr(validator, self.method)()
        except Exception as e:
            self.code = self.validation_failed_code
            self.response = str(e)
            info = self.response, self.code
        finally:
            return info
