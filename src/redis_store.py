import random
import sqlite3
import time

import redis
from loguru import logger

from src.sqlite_handle import ScoringSqlite
from src.yaml_config import YamlConfig


class RedisStore:
    def __init__(self, sqlite_table_name=None, sqlite_db_name=None):
        self.redis_client = None
        self.connection = None

        config = YamlConfig().read()
        self.redis_attempt_connection = config['redis']['connection_attempts']
        self.redis_timeout = config['redis']['timeout_between_attempts']
        if sqlite_table_name is None:
            self.sqlite_db_name = config['sqlite']['db_name']
        else:
            self.sqlite_db_name = sqlite_db_name

        if sqlite_table_name is None:
            self.sqlite_table_name = config['sqlite']['redis_table']
        else:
            self.sqlite_table_name = sqlite_table_name
        self.db = None

    def __enter__(self):
        config = YamlConfig().read()
        for i in range(self.redis_attempt_connection):
            try:
                self.redis_client = redis.StrictRedis(host=config['redis'][
                    'host'],
                                                      port=config['redis'][
                                                          'port'],
                                                      db=0,
                                                      username=config['redis'][
                                                          'login'],
                                                      password=config['redis'][
                                                          'password'],
                                                      socket_timeout=config[
                                                          'redis'][
                                                          'socket_timeout'],
                                                      #   socket_keepalive=True
                                                      )
                self.redis_client.ping()
                break
            except Exception:
                self.redis_client = None
                time.sleep(self.redis_timeout)
        self.connection = sqlite3.connect(database=self.sqlite_db_name)
        self.db = ScoringSqlite(self.connection,
                                self.sqlite_table_name)
        self.db.db_create_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.redis_client is not None:
            self.redis_client.quit()
        self.connection.close()

    def get(self, key):
        if key is None:
            return None
        if self.redis_client is None:
            raise KeyError("redis_client is None")
        result = self.redis_client.get(key)
        if result is not None:
            return result.decode('utf-8')
        return result

    def write_to_redis(self, key: str, value: str, period=60):
        self.redis_client.set(name=key, value=value, ex=period)

    @staticmethod
    def generate_value():
        interests = ["cars", "pets", "travel", "hi-tech", "sport", "music",
                     "books", "tv", "cinema", "geek", "otus"]
        return random.sample(interests, 2)

    def cache_get(self, key):
        try:
            cache_value = self.get(key)
            logger.info("get value from redis")
            logger.debug(cache_value)
            logger.debug(type(cache_value))
            return cache_value
        except Exception:
            logger.error("exception when get from redis")
            cache_value = self.db.get(key)
            logger.info("get value from sqlite")
            logger.debug(cache_value)
            logger.debug(type(cache_value))
            if not cache_value:
                return None
            return cache_value

    def cache_set(self, key, value, period):
        try:
            logger.info("set value to redis")
            self.write_to_redis(key, value, period)
        except Exception:
            logger.exception("redis exception")
        try:
            logger.info("set value to sqlite")
            self.db.set(key, value)
        except Exception:
            logger.exception("sqlite exception")
