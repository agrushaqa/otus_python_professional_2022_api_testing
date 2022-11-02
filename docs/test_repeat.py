from repeat import repeat

from redis_store import RedisStore


class TestRepeat:
    def test_repeat(self):
        with RedisStore() as store:
            store.cache_set("test1", "12345", 5)
            assert "12345" == repeat(store.cache_get, 4, 2, "test1")