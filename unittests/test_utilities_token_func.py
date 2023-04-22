import pytest

from utilities.token_func import encode_token, decode_token


def test_encode_token():
    user_id = 1
    token = encode_token(user_id)
    assert decode_token(token) == user_id


def test_decode_token():
    assert decode_token(encode_token(1)) == 1


if __name__ == '__main__':
    pytest.main(['-v'])
