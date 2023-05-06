import pytest

from utilities.utils import is_valid_email


def test_is_valid_email():
    assert is_valid_email('email') is False
    assert is_valid_email('email@') is False
    assert is_valid_email('email@domain') is False
    assert is_valid_email('email@domain.') is False
    assert is_valid_email('email@domain.com') is True


if __name__ == '__main__':
    pytest.main(['-v'])
