import pytest

from validators.validator_email import ValidatorEmail


class TestValidatorEmail:
    def test_simple_email(self):
        ValidatorEmail("test@test.ru")

    def test_invalid_email(self):
        with pytest.raises(Exception):
            ValidatorEmail("text.ru")
