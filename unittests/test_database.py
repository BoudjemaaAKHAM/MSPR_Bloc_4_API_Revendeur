import pytest

from database.database import Db


@pytest.fixture(scope="module")
def db():
    db = Db('data/database', clear=False)
    db.__enter__()
    db.create_tables()
    yield db
    db.__exit__(None, None, None)


def test_create_tables(db):
    db.create_tables()
    db.cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    assert db.cursor.fetchall() == [('users',)]


def test_delete_tables(db):
    db.create_tables()
    db.delete_tables()
    db.cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    assert db.cursor.fetchall() == []


def test_insert_user(db):
    db.create_tables()
    db.insert_user(1, '', 'token')
    db.cursor.execute('SELECT * FROM users')
    assert db.cursor.fetchall() == [(1, '', 'token')]
    assert db.insert_user(1, '', 'token') is False


def test_get_user(db):
    db.create_tables()
    db.insert_user(1, '', 'token')
    assert db.get_user(1) == (1, '', 'token')
    assert db.get_user(2) is None


def test_get_user_by_email(db):
    db.create_tables()
    db.insert_user(100, 'email', 'token')
    assert db.get_user_by_email('email') == (100, 'email', 'token')
    assert db.get_user_by_email('email2') is False


def test_delete_user(db):
    db.create_tables()
    db.insert_user(1, '', 'token')
    assert db.delete_user(1) is None
    assert db.delete_user(2) is False
    assert db.get_user(1) is None


if __name__ == '__main__':
    pytest.main(['-v'])
