import redis

from src.yaml_config import YamlConfig

# https://redis-py.readthedocs.io/en/stable/commands.html


def fill_redis(data: dict):
    config = YamlConfig().read()
    redis_client = redis.StrictRedis(host=config['redis']['host'],
                                     port=config['redis']['port'],
                                     db=0,
                                     username=config['redis']['login'],
                                     password=config['redis']['password'])
    redis_client.mset(data)
    redis_client.close()


if __name__ == "__main__":
    fill_redis({"i:1": 5})
    fill_redis({"i:2": 0})
    fill_redis({"i:3": 25})
