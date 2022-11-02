import redis

from yaml_config import YamlConfig

config = YamlConfig().read()
connection = redis.Redis(host=config['redis']['host'],
                                              port=config['redis']['port'],
                                              db=0,
                                              username=config['redis'][
                                                  'login'],
                                              password=config['redis'][
                                                'password'], socket_connect_timeout=1)
print(connection.ping())
# p = connection.pubsub()
# p.subscribe()
# print(p.check_health())