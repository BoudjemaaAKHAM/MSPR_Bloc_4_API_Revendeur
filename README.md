# MSPR_Bloc_4_API_Revendeur .......

Ce repository contient le code source de l'API Revendeur.

### Composition du groupe

- Adel Ould Ouelhadj
- Boudjemaa AKHAM
- Guillaume GAY
- Jean-Daniel SPADAZZI
- Sébastien GLORIES

### Résumé de l'API Revendeur :

L'API Revendeur permet de gérer les utilisateurs de l'application mobile.
Elle permet ensuite d'exposer aux revendeurs authentifiés les informations sur les produits et les stocks.

### Utilisation de l'application :

1- Cloner le repository : (Demander l'accès au repository à l'un des membres du groupe))

```bash
git clone https://github.com/BoudjemaaAKHAM/MSPR_Bloc_4_API_Webshop.git
```

2- Créer un environnement virtuel.

3- Installer localement l'application :

```bash
RUN pip install -e .
```

4- Lancer l'application :

```bash
python -m revendeurapi.main
``` 

5- les routes de l'API et la documentation sont disponibles à l'adresse suivante :
http://localhost:82/docs

### Utilisation de l'application avec Docker :

1- Créer l'image Docker :

```bash
docker build -t revendeur_api -f ./deployment/Dockerfile .
```

2- Lancer l'application :

```bash
docker run -p 444:444 revendeur_api
```

3- les routes de l'API et la documentation sont disponibles à l'adresse suivante :
https://localhost:444/docs

### Push sur DockerHub :

1- Se connecter à DockerHub :

```bash
docker login -username=boudjemaa
```

Saisir le token qui est dans le fichier .dockerhub_token

2- Tagger l'image :

```bash
docker tag revendeur_api boudjemaa/revendeur_api:latest
```

3- Pusher l'image :

```bash
docker push boudjemaa/revendeur_api:latest
```

