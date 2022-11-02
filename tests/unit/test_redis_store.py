import time

from redis_store import RedisStore
from sqlite_wrapper import sqlite_send_request


class TestRedisStore:
    def test_mysql_table_exists(self):
        with RedisStore() as store:
            conn = store.connection
            result = sqlite_send_request(
                conn,
                "SELECT EXISTS (SELECT name FROM sqlite_schema "
                "WHERE type='table' AND name='redis' )",)
            assert result.fetchone()[0] == 1

    def test_read_write(self):
        with RedisStore() as store:
            store.write_to_redis("test1", "12345", 5)
            assert "12345" == store.get("test1")

    def test_read_write_period(self):
        with RedisStore() as store:
            store.write_to_redis("test1", "12345", 5)
            assert "12345" == store.get("test1")
            time.sleep(6)
            assert store.get("test1") is None

    def test_read_write_cached(self):
        with RedisStore() as store:
            store.cache_set("test1", "12345", 5)
            assert "12345" == store.cache_get("test1")
