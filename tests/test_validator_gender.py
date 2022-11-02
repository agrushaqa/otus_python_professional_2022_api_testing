import pytest

from validators.validator_gender import ValidatorGender
from yaml_config import YamlConfig


class TestValidatorGender:
    def test_simple_gender_0(self):
        config = YamlConfig().read()
        ValidatorGender(config['gender']['unknown'])

    def test_simple_gender_1(self):
        config = YamlConfig().read()
        ValidatorGender(config['gender']['male'])

    def test_simple_gender_2(self):
        config = YamlConfig().read()
        ValidatorGender(config['gender']['female'])

    def test_invalid_gender_not_number(self):
        with pytest.raises(Exception):
            ValidatorGender("M")

    def test_invalid_gender_more_then_3(self):
        with pytest.raises(Exception):
            ValidatorGender("0")
