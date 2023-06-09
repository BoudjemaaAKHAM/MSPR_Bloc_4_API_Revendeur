"""
MSPR 4 - Revendeur API
"""

import requests
import logging
import uvicorn
from email.header import Header
from functools import wraps
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from urllib.parse import unquote
from services.qr_code_generator import generate_qr_code
from services.mail_sender import send_email
from database.database import Db
from utilities.token_func import encode_token, decode_token
from utilities.utils import is_valid_email

# api produits
API_PRODUCT = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products"

API_PREFIX = "/api/v1"

# Partie sécurité
token_auth_scheme = HTTPBearer()

description = """
Documentation de l'API Revendeur du projet MSPR 4. 🚀

## Products

 - The user will be able to **read products** if he has a valid token.

url: /api/v1/products

call the api with curl:
```shell
curl -X 'GET' \
  'http://localhost:82/api/v1/products' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer put_token_here'
```

- The user will be able to get a **product by id** if he has a valid token.

url: /api/v1/products/{product_id}

call the api with curl:
```shell
curl -X 'GET' \
    'http://localhost:82/api/v1/products/1' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer put_token_here'
```

- The user will be able to get a **product stock by id** if he has a valid token.

url: /api/v1/products/{product_id}/stock

call the api with curl:
```shell
curl -X 'GET' \
    'http://localhost:82/api/v1/products/1/stock' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer put_token_here'
```

## Users

You will be able to **create / delete / update users** if you have the admin rights

- The admin will be able to **create a user** if he has the correct rights.

**description:**s
when this api is called, the user will be created and an email will be sent to the user with a qr code containing the token.



url: /api/v1/create-user/{user_id}/{user_email}

call the api with curl:
```shell
curl -X 'POST' \
    'http://localhost:82/api/v1/create-user/1/boudjemaa.akham@epsi.fr' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer admin'
```

- The admin will be able to **delete a user** if he has the correct rights.

url: /api/v1/delete-user/{user_id}

call the api with curl:
```shell
curl -X 'DELETE' \
    'http://localhost:82/api/v1/delete-user/1' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer admin'
```

- The admin will be able to **update a user** if he has the correct rights.

url: /api/v1/update-user/{user_id}

call the api with curl:
```shell
curl -X 'PUT' \
    'http://localhost:82/api/v1/update-user/1' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer admin'
```

"""

tags_metadata = [
    {
        "name": "Products",
        "description": "Manage products.",
    },
    {
        "name": "Users",
        "description": "Manage users.",
    }
]

app = FastAPI(
    title="MSPR Bloc 4",
    description=description,
    version="1.0.0",
    license_info={
        "name": "Apache 2.0",
        "src": "./LICENSE.txt",
    },
    openapi_tags=tags_metadata
)

db = Db('data/database', clear=False)
db.__enter__()
db.create_tables()


@app.on_event("shutdown")
def shutdown_event():
    db.__exit__(None, None, None)


def admin_required(func):
    """
    Decorator to check if the user is admin
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get('token') or Header(None)
        if not token:
            raise HTTPException(status_code=401, detail='Token is missing')
        if token.credentials != "admin":
            raise HTTPException(status_code=403, detail='You are not admin')

        return func(*args, **kwargs)

    return wrapper


def token_required(func):
    """
    Decorator to check if the token is valid
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get('token') or Header(None)
        if not token:
            raise HTTPException(status_code=401, detail='Token is missing')
        # TODO: a verifier si ça empeche pas les autres api de rester connecté
        # if token.credentials == "admin":
        #    return func(*args, **kwargs)
        token_decoded = decode_token(token.credentials)
        if token_decoded == 1:
            raise HTTPException(status_code=401, detail='Token has expired')
        elif token_decoded == 2:
            raise HTTPException(status_code=401, detail='Token is not valid')
        if db.get_user_by_email(token_decoded) is False:
            raise HTTPException(status_code=403,
                                detail='User has been deleted and has no rights to access this resource')
        return func(*args, **kwargs)

    return wrapper


# route principale
@app.get("/")
def root():
    return {"message": "Welcome to the MSPR API"}


# Products routes


@app.get(f"{API_PREFIX}/products", tags=["Products"])
@token_required
def get_products(token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Get all products
    :param token:
    :return: json response
    """
    response = requests.get(API_PRODUCT)
    return response.json()


@app.get(f"{API_PREFIX}/products/{{product_id}}", tags=["Products"])
@token_required
def get_product(product_id: int, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Get a product by id
    :param product_id:
    :param token:
    :return: json response
    """
    response = requests.get(API_PRODUCT + "/" + str(product_id))
    if type(response.json()) == dict:
        return response.json()
    else:
        return {"status": "error", "message": "Product not found"}


@app.get(f"{API_PREFIX}/products/{{product_id}}/stock", tags=["Products"])
@token_required
def get_product_stock(product_id: int, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Get a product stock by id
    :param product_id:
    :param token:
    :return: json response
    """
    response = requests.get(API_PRODUCT + "/" + str(product_id))
    if type(response.json()) == dict:
        return response.json()["stock"]
    else:
        return {"status": "error", "message": "Product not found"}


@app.post(f"{API_PREFIX}/create-user/{{user_id}}/{{user_email}}", tags=["Users"])
@admin_required
def create_user(user_id: int, user_email: str, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Create a user
    :param user_id:
    :param user_email:
    :param token:
    :return:
    """

    if not is_valid_email(user_email):
        return {"status": "error", "message": "Invalid email format"}
    try:
        decoded_email = unquote(user_email)
        token = encode_token(decoded_email)
        if db.insert_user(user_id, decoded_email, token) is False:
            return {"status": "error", "message": f"User with id {user_id} already exists on the database"}
        generate_qr_code(token, "", "qrcode")
        send_email(decoded_email, "./qrcode.png")
        return {"status": "success",
                "message": f"User with id {user_id} has been created. Check your email for the QR code"}
    except Exception as e:
        return {"status": "error", "message": e.__repr__()}


@app.delete(f"{API_PREFIX}/delete-user/{{user_id}}", tags=["Users"])
@admin_required
def delete_user(user_id: int, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Delete a user
    :param user_id:
    :param token:
    :return:
    """
    try:
        if db.delete_user(user_id) is False:
            return {"status": "error", "message": f"User with id {user_id} does not exist on the database"}
        return {"status": "success", "message": f"User with id {user_id} has been deleted"}
    except Exception as e:
        return {"status": "error", "message": e.__repr__()}


@app.put(f"{API_PREFIX}/update-user/{{user_id}}", tags=["Users"])
@admin_required
def update_user(user_id: int, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Update a user
    :param user_id:
    :param token:
    :return:
    """
    # update the user information
    # modify the token on the database

    return {"status": "success"}


if __name__ == "__main__":
    # logging.basicConfig(filename='server.log', level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=82, log_level="debug", access_log=True)
    # uvicorn.run(app)
