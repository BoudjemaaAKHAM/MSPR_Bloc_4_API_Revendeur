import os
import jwt
import datetime

with open(os.path.join(os.path.dirname(__file__), '.secret.txt'), 'r') as f:
    secret_key = f.read()


def encode_token(user_id):
    """
    Encode a token for a user
    :param user_id
    :return:
    """
    payload = {'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def decode_token(token):
    """
    Decode a token
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        # Le jeton a expiré
        return 1
    except jwt.InvalidTokenError:
        # Le jeton est invalide
        return 2
