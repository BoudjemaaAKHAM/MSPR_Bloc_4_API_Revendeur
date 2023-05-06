import pytest

from services.qr_code_generator import generate_qr_code


def test_generate_qr_code():
    generate_qr_code('test', './unittests/', 'test')
    assert True


if __name__ == '__main__':
    pytest.main(['-v'])
