import redis

from yaml_config import YamlConfig

# https://realpython.com/python-redis/
# https://redis-py.readthedocs.io/en/stable/commands.html


class TestRedis:
    def test_connection(self):
        config = YamlConfig().read()
        redis_client = redis.StrictRedis(host=config['redis']['host'],
                                         port=config['redis']['port'],
                                         db=0,
                                         username=config['redis']['login'],
                                         password=config['redis']['password'])
        answer = redis_client.ping()
        redis_client.close()
        assert answer is True

    def test_read_write_delete(self):
        config = YamlConfig().read()
        redis_client = redis.StrictRedis(host=config['redis']['host'],
                                         port=config['redis']['port'],
                                         db=0,
                                         username=config['redis']['login'],
                                         password=config['redis']['password'])
        redis_client.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})
        exists = redis_client.exists("Bahamas")
        answer = redis_client.get("Bahamas").decode('utf-8')
        redis_client.delete("Bahamas")
        exists_after_del = redis_client.exists("Bahamas")
        redis_client.close()
        assert exists == 1
        assert answer == "Nassau"
        assert exists_after_del == 0
