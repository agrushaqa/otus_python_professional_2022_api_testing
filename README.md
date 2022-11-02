Scoring API Tests: дописываем тесты к предыдущему ДЗ


## Запуск 

# Запуск
## логи в консоли
python.exe api.py
## логи в файле
python.exe api.py --log debug.txt
## insomnia & postman
### online_score
post запрос 
http://localhost:8080/method

    {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": {"phone": "79175002040", "email": "stupnikov@otus.ru"}, "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95"}

где token вычисляется следующим образом
для admin:
````
    token = hashlib.sha512((datetime.datetime.now()
                        .strftime("%Y%m%d%H")
                        + Config().admin_salt).encode('utf-8')).hexdigest()

````
в остальных случаях 
````
    account = "horns&hoofs"
    login = "h&f"
    msg = account + login \
          + Config().salt
    empty_token = hashlib.sha512(msg.encode('utf-8')).hexdigest()
````
### clients_interests
http://localhost:8080/method
    ```{"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": {"client_ids": [1, 2, 3], "date": "02.03.2021"}, "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95"}```

ответ
    ```{
        "response": {
            "1": 5,
            "2": 0,
            "3": 25
        },
        "code": 200
    }```

для того, чтобы score выводился нужно предварительно его заполнить
запустив файл redis_fill_data.py

https://pytest-cov.readthedocs.io/en/latest/reporting.html
https://github.com/pytest-dev/pytest-cov

# redis
## запуск
redis-server /etc/redis/6379.conf

## /etc/redis/6379.conf

port              6379
daemonize         yes
save              60 1
bind              127.0.0.1 192.168.0.142
tcp-keepalive     300
dbfilename        dump.rdb
dir               ./
rdbcompression    yes
protected-mode    no


## Проверка того, что redis запущен
pgrep redis-server
## Проверка связи 
telnet 192.168.0.142 6379
отправить команду 
PING
должен прийти ответ PONG


# подключение 
    redis-cli -h 192.168.0.142 -p 6379 --user gav --pass <password>
или
    redis-cli -h 127.0.0.1 -p 6379
AUTH gav <password>

## Создание пользователя
ACL SETUSER gav on >password allkeys +@all
где password нужно изменить на пароль для этого пользователя
(Придумайте его. Он должен содержать латинские буквы и цифры)
    
**Этот пароль нужно указать в файле src\config\config.yml. В поле password**

после перезагрузки данные пользователя теряются.
https://redis.io/commands/acl-setuser/
https://redis.io/docs/manual/security/acl/

# Узнать настройки пользователя
ACL GETUSER gav

# Узнать под кем подключен
ACL WHOAMI

# Проверить соединение
    PING
должен прийти ответ PONG
https://realpython.com/python-redis/

# Задать значение через redis-cli
MSET "Croatia" "Zagreb"

## Redis benchmark
    redis-benchmark -q -n 100000
https://redis.io/docs/management/optimization/benchmarks/

# Конфигурирование:
Установить python 3.11

Установить pip
https://bootstrap.pypa.io/get-pip.py.

# requirements.txt
## create
pip freeze > requirements.txt
## use
pip install -r requirements.txt

    py get-pip.py

# code style
## isort
python -m pip install isort
### run 
isort .
## mypy
python -m pip install mypy
### run 
mypy .
## flake8
python -m pip install flake8
### run
flake8
## parameterized
python -m pip install mock
pip install pytest
pip install pytest-cov
# redis
python -m pip install redis
python -m pip install types-redis
# request
python -m pip install requests
python -m pip install types-requests

# yaml
python -m pip install pyyaml
python -m pip install types-PyYAML

# логирование
python -m pip install loguru
https://pypi.org/project/loguru/

# profiler
python -m pip install -U memory_profiler
python -m pip install matplotlib
https://pypi.org/project/memory-profiler/
https://stackoverflow.com/questions/43927799/why-close-a-cursor-for-sqlite3-in-python
## run
mprof run -T 0.01 .\test_redis_store.py
## show result
mprof plot

## Запуск тестов:
pytest в папке с README.md
или
pytest tests/test_yaml_config.py

## Задание:
Задание: 
```
протестировать HTTP API сервиса скоринга. Шаблон уже есть в test.py,само API реализовывалось в прошлой части ДЗ.
1.
Необходимо разработать модульные тесты, как минимум, на все типы полей и 
функциональные тесты на систему. Разрешается пользоваться любым тестовым 
фреймворком: unittest, nosetests, pytest.
2.
Обязательно необходимо реализовать через декоратор функционал запуска кейса 
с разными тест-векторами (Либо, в качестве альтернативы, сделать тоже самое 
через фикстуры в pytest). 
Если берете готовый cases, то его надо допилить так, чтобы при падении теста 
было ясно какой кейс упал.
@cases([
{"account": "horns&hoofs", "login": "h&f", "method": "online_score", {"account": "horns&hoofs", "login": "h&f", "method": "online_score", {"account": "horns&hoofs", "login": "admin", "method": "online_score" ])
def test_bad_auth(self, request):
...
3.
store, который был захардкожен в None, наконец обретает смысл! Нужно 
реализовать в store.py общение с любым клиент-серверным key-value хранилищем 
(tarantool, memcache, redis, etc.) согласно интерфейсу заданному в 
обновленном scoring.py. Обращение к хранилищу не должно падать из-за 
разорванного соединения (т.е. store должен пытаться переподключаться N раз 
прежде чем сдаться) и запросы не должны залипать (нужно использовать 
timeout'ы где возможно).
У store есть отдельно
get
и
cache_get
. В реальной системы, аналогом которой является API из ДЗ, есть отдельный кеш 
и отдельный key-value storage. Методы названы по-разному, чтобы показать что 
есть разница. В данном случае, внутри можно реализовать это и как хождение в одно и
то же хранилище. Важно то, как это будет протестировано с учетом разных 
требований для разных функций.
4.
Естественно нужно протестировать этот новый функционал. Обратите внимание, 
функции
get_score
не важна доступность store'а, она использует его как кэш и, следовательно, 
должна работать даже если store сгорел в верхних слоях атмосферы.
get_interests
использует store как персистентное хранилище и если со store'ом что-то 
случилось может отдавать только ошибки.
5.
Структура тестов
https://realpython.com/python-testing/#writing-integration-tests
Цель задания: 
применить знания по тестированию, полученные на занятии. В результате 
получится прокачать навык дизайна тест-кейсов, разработки модульных и 
функциональных тестов, создания mock'ов.
Критерии успеха: задание
обязательно
, критерием успеха является работающий согласно заданию код, для которого 
проверено соответствие pep8, написана минимальная документация с примерами запуска, в README, например. Далее
успешность определяется code review.
```
# Замечание 
## 
В задаче для метода online_score было сказано
    Контекст
    в словарь контекста должна прописываться запись "has" - список полей,
    которые были не пустые для данного запроса
я не понял откуда берётся этот список полей поэтому сейчас ответ выдаётся в виде

    {
        "response": {
            "score": 3.0,
            "non_empty_params": [
                "email",
                "phone"
            ]
        },
        "code": 200
    }

то есть я добавил дополнительный параметр non_empty_params для выполнения 
этого условия
## ACL SAVE
выдаёт ошибку
(error) ERR This Redis instance is not configured to use an ACL file. You may want to specify users via the ACL SETUSER command and then issue a CONFIG REWRITE (assuming you have a Redis configuration file set) in order to store users in the Redis configuration.

## redis CONFIG REWRITE
192.168.0.142:6379> CONFIG REWRITE
(error) ERR Rewriting config file: Permission denied
выдача прав и отключение selinux не помогло

## redis supervised systemd
если в конфиг добавить supervised systemd,
то появится предупреждение
    systemd supervision requested or auto-detected, but Redis is compiled without libsystemd support!

