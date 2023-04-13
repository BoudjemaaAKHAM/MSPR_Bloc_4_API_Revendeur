import requests
import logging
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# api mise à disposition dans le sujet
# api produits
API_PRODUCT = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products"

# Partie sécurité à tester
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

description = """
Documentation des APIs du projet MSPR 4. 🚀

## Products

You will be able to **read products**.

"""

tags_metadata = [
    {
        "name": "products",
        "description": "Manage products.",
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


# fonction pour tester la sécurité d'une api mais n'est pas testé maintenant


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# route principale


@app.get("/")
def read_root():
    """
    Root path
    """
    return {"Hello": "World"}


# routes produits


@app.get("/products", tags=["products"])
def get_products():
    """
    Get all products
    """
    response = requests.get(API_PRODUCT)
    return response.json()


@app.get("/products/{product_id}", tags=["products"])
def get_product(product_id: int):
    """
    Get a product by id
    """
    response = requests.get(API_PRODUCT + "/" + str(product_id))
    return response.json()


@app.post("/create-user/{user_email}", tags=["users"])
def create_user(user_email: str):
    """
    Create a user
    """
    # je génère une clé d'authentification que je pourrais utiliser ensuite pour autoriser l'utilisateur à utiliser l'api
    # je stocke la clé dans la base de données sqlite et j'envoie un mail à l'utilisateur avec le qr code
    # le token étant stocké dans la base de données, je peux l'utiliser pour vérifier l'authentification de l'utilisateur prochainement
    # retourner un code 200 si tout s'est bien passé
    # retourne un autre code si erreur

    return {"status": "success"}


if __name__ == "__main__":
    # logging.basicConfig(filename='server.log', level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=82, log_level="debug", access_log=True)
    # uvicorn.run(app)
