import os
import jwt
import datetime


def encode_token(user_id):
    """
    Encode a token for a user
    :param user_id
    :return:
    """
    if os.path.exists(os.path.join(os.path.dirname(__file__), '.secret.txt')):
        with open(os.path.join(os.path.dirname(__file__), '.secret.txt'), 'r') as f:
            secret_key = f.read()

    payload = {'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=60)}
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def decode_token(token):
    """
    Decode a token
    :param token:
    :return:
    """
    try:
        if os.path.exists(os.path.join(os.path.dirname(__file__), '.secret.txt')):
            with open(os.path.join(os.path.dirname(__file__), '.secret.txt'), 'r') as f:
                secret_key = f.read()
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        # Le jeton a expiré
        return 1
    except jwt.InvalidTokenError:
        # Le jeton est invalide
        return 2
