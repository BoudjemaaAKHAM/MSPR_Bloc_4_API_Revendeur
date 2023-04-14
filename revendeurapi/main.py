import requests
import logging
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from urllib.parse import unquote
from services.qr_code_generator import generate_qr_code
from services.mail_sender import send_email
from database.database import Db
from utilities.token_func import encode_token
from utilities.utils import is_valid_email

# api produits
API_PRODUCT = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products"

# Partie sécurité à tester
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

description = """
Documentation des APIs du projet MSPR 4. 🚀

## Products

You will be able to **read products**.

## Users

You will be able to **create / delete / update users** if you have the admin rights

"""

tags_metadata = [
    {
        "name": "products",
        "description": "Manage products.",
    },
    {
        "name": "users",
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

db = Db("../data/database", clear=False)
db.create_tables()


# fonction pour tester la sécurité d'une api mais n'est pas testé maintenant


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# routes produits


@app.get("/products", tags=["products"])
def get_products():
    """
    Get all products
    :return:
    """
    response = requests.get(API_PRODUCT)
    return response.json()


@app.get("/products/{product_id}", tags=["products"])
def get_product(product_id: int):
    """
    Get a product by id
    :param product_id:
    :return:
    """
    response = requests.get(API_PRODUCT + "/" + str(product_id))
    return response.json()


@app.get("/products/{product_id}/stock", tags=["products"])
def get_product_stock(product_id: int):
    """
    Get a product stock by id
    :param product_id:
    :return:
    """
    response = requests.get(API_PRODUCT + "/" + str(product_id))
    return response.json()["stock"]


@app.post("/create-user/{user_id}/{user_email}", tags=["users"])
def create_user(user_id: int, user_email: str):
    """
    Create a user
    :param user_id:
    :param user_email:
    :return:
    """
    # je génère une clé d'authentification que je pourrais utiliser ensuite pour autoriser l'utilisateur à utiliser l'api
    # je stocke la clé dans la base de données sqlite et j'envoie un mail à l'utilisateur avec le qr code
    # le token étant stocké dans la base de données, je peux l'utiliser pour vérifier l'authentification de l'utilisateur prochainement
    # retourner un code 200 si tout s'est bien passé
    # retourne un autre code si erreur

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


@app.delete("/delete-user/{user_id}", tags=["users"])
def delete_user(user_id: int):
    """
    Delete a user
    :param user_id:
    :return:
    """
    try:
        if db.delete_user(user_id) is False:
            return {"status": "error", "message": f"User with id {user_id} does not exist on the database"}
        return {"status": "success", "message": f"User with id {user_id} has been deleted"}
    except Exception as e:
        return {"status": "error", "message": e.__repr__()}


@app.put("/update-user/{user_id}", tags=["users"])
def update_user(user_id: int):
    """
    Update a user
    :param user_id:
    :return:
    """
    # update the user information
    # modify the token from the database

    return {"status": "success"}


if __name__ == "__main__":
    # logging.basicConfig(filename='server.log', level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=82, log_level="debug", access_log=True)
    # uvicorn.run(app)
