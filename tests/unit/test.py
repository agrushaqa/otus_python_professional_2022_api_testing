import datetime
from http import HTTPStatus

import pytest


class TestApi:

    def test_empty_request(self, scenario):
        _, code = scenario.get_response({})
        assert HTTPStatus.UNPROCESSABLE_ENTITY == code

    @pytest.mark.parametrize("request_content", [
        ({"account": "horns&hoofs", "login": "h&f", "method": "online_score",
          "token": "", "arguments": ({})}),
        ({"account": "horns&hoofs", "login": "h&f", "method": "online_score",
          "token": "sdd", "arguments": ({})}),
        ({"account": "horns&hoofs", "login": "admin", "method": "online_score",
          "token": "", "arguments": ({})}),
    ])
    def test_bad_auth(self, request_content, scenario):
        _, code = scenario.get_response(request_content)
        assert HTTPStatus.FORBIDDEN == code

    @pytest.mark.parametrize("request_content", [
        ({"account": "horns&hoofs", "login": "h&f", "method": "online_score"}),
        ({"account": "horns&hoofs", "login": "h&f", "arguments": ({})}),
        ({"account": "horns&hoofs", "method": "online_score",
          "arguments": ({})}),
    ])
    def test_invalid_method_request(self, request_content, scenario):
        scenario.set_valid_auth(request_content)
        response, code = scenario.get_response(request_content)
        assert HTTPStatus.UNPROCESSABLE_ENTITY == code
        assert len(response) > 0

    @pytest.mark.parametrize("arguments", [
        {},
        {"phone": "79175002040"},
        {"phone": "89175002040", "email": "stupnikov@otus.ru"},
        {"phone": "79175002040", "email": "stupnikovotus.ru"},
        {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": -1},
        {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": "1"},
        {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1,
         "birthday": "01.01.1890"},
        {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1,
         "birthday": "XXX"},
        {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1,
         "birthday": "01.01.2000", "first_name": 1},
        {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1,
         "birthday": "01.01.2000",
         "first_name": "s", "last_name": 2},
        {"phone": "79175002040", "birthday": "01.01.2000", "first_name": "s"},
        {"email": "stupnikov@otus.ru", "gender": 1, "last_name": 2},
    ])
    def test_invalid_score_request(self, arguments, scenario):
        request = {"account": "horns&hoofs", "login": "h&f",
                   "method": "online_score", "arguments": arguments}
        scenario.set_valid_auth(request)
        response, code = scenario.get_response(request)
        assert HTTPStatus.UNPROCESSABLE_ENTITY == code, arguments
        assert len(response) > 0

    @pytest.mark.parametrize("arguments",
                             [
                                 ({"phone": 79175002040,
                                   "email": "stupnikov@otus.ru"}),
                                 ({"gender": 1, "birthday": "01.01.2000",
                                   "first_name": "a",
                                   "last_name": "b"}),
                                 ({"gender": 0, "birthday": "01.01.2000"}),
                                 ({"gender": 2, "birthday": "01.01.2000"}),
                                 ({"first_name": "a", "last_name": "b"}),
                                 ({"phone": "79175002040",
                                   "email": "stupnikov@otus.ru",
                                   "gender": 1, "birthday": "01.01.2000",
                                   "first_name": "a", "last_name": "b"}),
                             ]
                             )
    def test_ok_score_request(self, arguments, scenario):
        request = {"account": "horns&hoofs", "login": "h&f",
                   "method": "online_score", "arguments": arguments}
        scenario.set_valid_auth(request)
        response, code = scenario.get_response(request)
        assert HTTPStatus.OK == code, arguments
        score = response.get("score")
        assert isinstance(score, (int, float)) is True, arguments
        assert score >= 0, arguments
        scenario.context["has"] = response.get("non_empty_params")
        assert sorted(scenario.context["has"]) == sorted(arguments.keys())

    def test_ok_score_admin_request(self, scenario):
        arguments = {"phone": "79175002040", "email": "stupnikov@otus.ru"}
        request = {"account": "horns&hoofs", "login": "admin",
                   "method": "online_score", "arguments": arguments}
        scenario.set_valid_auth(request)
        response, code = scenario.get_response(request)
        assert HTTPStatus.OK == code
        score = response.get("score")
        assert score == 42

    @pytest.mark.parametrize("arguments", [
        {},
        {"date": "20.07.2017"},
        {"client_ids": [], "date": "20.07.2017"},
        {"client_ids": {1: 2}, "date": "20.07.2017"},
        {"client_ids": ["1", "2"], "date": "20.07.2017"},
        {"client_ids": [1, 2], "date": "XXX"},
    ])
    def test_invalid_interests_request(self, arguments, scenario):
        request = {"account": "horns&hoofs", "login": "h&f",
                   "method": "clients_interests", "arguments": arguments}
        scenario.set_valid_auth(request)
        response, code = scenario.get_response(request)
        assert HTTPStatus.UNPROCESSABLE_ENTITY == code, arguments
        assert len(response) > 0

    @pytest.mark.parametrize('arguments', [
        {"client_ids": [1, 2, 3],
         "date": datetime.datetime.today().strftime("%d.%m.%Y")},
        {"client_ids": [1, 2], "date": "19.07.2017"},
        {"client_ids": [0]},
    ])
    def test_ok_interests_request(self, arguments, scenario):
        request = {"account": "horns&hoofs", "login": "h&f",
                   "method": "clients_interests", "arguments": arguments}
        scenario.set_valid_auth(request)
        response, code = scenario.get_response(request)
        assert HTTPStatus.OK == code, arguments
        assert len(arguments["client_ids"]) == len(response)
        assert all(v and isinstance(v, list) and
               all(isinstance(i, str) for i in v)
               for v in response.values())
        scenario.context["nclients"] = len(response.values())
        assert scenario.context.get("nclients") == len(arguments["client_ids"])
