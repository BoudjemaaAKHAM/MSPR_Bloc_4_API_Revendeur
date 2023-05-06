## Documentation utilisateur

### Prérequis

- Python 3.10    https://www.python.org/downloads/
- git            https://git-scm.com/downloads
- Docker         https://docs.docker.com/get-docker/
- Kubernetes     https://kubernetes.io/fr/docs/tasks/tools/install-kubectl/

### Installation

Voir le fichier [README.md](../README.md)

### Utilisation de l'application en local :

1 - Une fois l'application lancée, les routes de l'API et la documentation sont disponibles à l'adresse suivante :

http://localhost:82/docs

Vous devriez voir la documentation de l'API.
![img.png](imgs/img.png)

Note : le port 82 est configuré uniquement pour l'environnement de développement. Une fois l'application déployée en
production, le port 444 sera utilisé.

2 - Pour tester l'API, il faut d'abord créer un utilisateur en utilisant la route :

http://localhost:82/api/v1/create-user/{user_id}/{user_email}

Vous devez remplacer {user_id} et {user_email} par les valeurs de votre choix. Il faut utiliser une adresse email
valide.

Le token à utiliser est : admin

