import pytest

from validators.validator_client_ids import ValidatorClientIds


class TestValidatorClientIds:
    def test_dict(self):
        with pytest.raises(Exception):
            ValidatorClientIds({1: 2})

    def test_list_str_as_number(self):
        with pytest.raises(Exception):
            ValidatorClientIds(["1", "2"])

    def test_list(self):
        ValidatorClientIds([1, 2])

    def test_tuple(self):
        with pytest.raises(Exception):
            ValidatorClientIds((1, 2))

    def test_empty(self):
        ValidatorClientIds([])

    def test_invalid_client_ids_number(self):
        with pytest.raises(Exception):
            ValidatorClientIds(56)

    def test_invalid_client_ids_str(self):
        with pytest.raises(Exception):
            ValidatorClientIds("M")
