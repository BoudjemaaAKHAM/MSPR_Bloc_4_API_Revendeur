import os
import jwt
import datetime

with open(os.path.join(os.path.dirname(__file__), '.secret.txt'), 'r') as f:
    secret_key = f.read()


def encode_token(user_email):
    """
    Encode a token for a user
    :param user_email
    :return:
    """
    payload = {'user_email': user_email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)}
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
        return payload['user_email']
    except jwt.ExpiredSignatureError:
        # Le jeton a expiré
        return None
    except jwt.InvalidTokenError:
        # Le jeton est invalide
        return None


def token_is_valid(token):
    """
    Check if a token is valid
    :param token:
    :return:
    """
    user_id = decode_token(token)
    return user_id is not None
