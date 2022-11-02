import pytest

from validators.validator_phone import ValidatorPhone


class TestValidatorEmail:
    def test_simple_email_str(self):
        ValidatorPhone("71234567890")

    def test_simple_email_int(self):
        ValidatorPhone(71234567890)

    def test_invalid_email_long(self):
        with pytest.raises(Exception):
            ValidatorPhone(712345678902)

    def test_invalid_email_short(self):
        with pytest.raises(Exception):
            ValidatorPhone(7123456789)

    def test_invalid_first_number(self):
        with pytest.raises(Exception):
            ValidatorPhone(81234567890)
