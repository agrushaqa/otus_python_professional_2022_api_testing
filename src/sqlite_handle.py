from src.sqlite_wrapper import sqlite_send_request
from src.yaml_config import YamlConfig


class ScoringSqlite:
    def __init__(self, connection, table_name):
        self.connection = connection
        self.table_name = table_name
        config = YamlConfig().read()
        self.key_max_length = config['sqlite']['max_key_length']
        self.value_max_length = config['sqlite']['value_max_length']

    def get(self, redis_key):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT VALUE FROM {self.table_name} WHERE "
                       f"KEY = '{redis_key}';")
        result = cursor.fetchone()
        cursor.close()
        if result:
            if len(result) > 0:
                return result[0]
        return result

    def db_create_table(self):
        sqlite_send_request(
            self.connection,
            f'CREATE TABLE IF NOT EXISTS "{self.table_name}" '
            f"(ID INTEGER PRIMARY KEY AUTOINCREMENT,"
            f" KEY CHAR({self.key_max_length}),"
            f" VALUE CHAR({self.value_max_length}))",
        )

    def set(self, redis_key, redis_value):
        sqlite_send_request(
            self.connection,
            f'INSERT INTO "{self.table_name}"' f" (KEY, VALUE) VALUES (?, ?)",
            (redis_key, redis_value),
        )
        self.connection.commit()
