from schema import MethodRequest, OnlineScoreRequest
from validators.select_validator import SelectValidator


class TestSelectValidator:
    def test_separate_params_by_group(self):
        schema = OnlineScoreRequest()
        is_group = SelectValidator.separate_params_by_group(schema)
        assert is_group == {'day-gender': ['birthday', 'gender'],
                            'fio': ['first_name', 'last_name'],
                            'phone-email': ['email', 'phone']}

    def test_check_groups(self):
        schema = OnlineScoreRequest()
        request = {"phone": "79175002040", "email": "stupnikov@otus.ru"}
        selector = SelectValidator(request)
        i_group = selector._check_groups(schema, request)
        assert i_group == {'day-gender': False, 'fio': False,
                           'phone-email': True}

    def test_validator_group_parameter(self):
        schema = OnlineScoreRequest()
        request = {"phone": "79175002040", "email": "stupnikov@otus.ru"}
        selector = SelectValidator(request)
        i_group = selector._validator_group_parameter(schema, request)
        assert i_group is True

    def test_validator_nullable_params(self):
        schema = OnlineScoreRequest()
        request = {"phone": "79175002040", "email": "stupnikov@otus.ru"}
        selector = SelectValidator(request)
        selector._validator_nullable_params(schema, request)

    def test_validator_required_params(self):
        schema = MethodRequest()
        request = {'account': 'horns&hoofs', 'login': 'h&f',
                   'method': 'online_score', 'arguments':
                   {'phone': '79175002040',
                    'email': 'stupnikov@otus.ru'},
                   'token': '55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19'
                            'd2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d7'
                            '18a9e35af34e14e1d5bcd5a08f21fc95'}
        selector = SelectValidator(request)
        selector._validator_required_params(schema, request)
