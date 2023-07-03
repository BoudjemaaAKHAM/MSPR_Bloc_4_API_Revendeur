# Pour le test OWASP nous allons vérifier certains de ces tests sur notre application API. 

 
 

## 1 - Dans un premier temps nous allons commencer avec le test OWASP N°5 

 
 

Ce test concerne le manque d'accès et de contrôle 

 
 

Pour cela nous allons tester à partir du DOM pour voir si on peut modifier des éléments : 

 
 

Nous allons tester à partir de la création d'un User sur l'API de Webshopapi.  

     

Pour cela nous ferons des tests à partir du swager de fast api. 

 
 
 

![img.png](imgs/ow00.png) 

     

 
 

On va manipuler par le biais de l'inspection du DOM les éléments d'autorisations 

 
 
 

![img.png](imgs/ow02.png) 

 
 

     

qui correspond à cette partie du code visible sur le DOM 

 
 
 

![img.png](imgs/ow03.png) 

 
 
 

Si on modifie le code sur le DOM en supprimant tout le code concernant le bouton comme l'image ci-dessous 

 
 
 

![img.png](imgs/ow05.png) 

 
 
 

Le résultat est toujours une erreur 403 sur la non-autorisation 

 
 
 

![img.png](imgs/ow06.png) 

 
 
 
 

Si on accède au formulaire pour l'identification par le mot de passe  

 
 
 

![img.png](imgs/ow01.png) 

 
 
 

on pourra observer que dans l'input du formulaire nous ne pouvons pas modifier les autorisations 

 
 
 
 

Conclusion je pense que nous respectons le point N°5 du référentiel OWASP 

 
 
 
 

## 2 - Test Owasp n°6. 

 l'objectif du test dans un premier temps concerne l'oublie de mettre en place de système de sécurité par manque de temps. Le second point est sur l'hardening de la partie serveur.


Pour constater si nous avons fait un oubli lors de la rédaction du code source sur la sécurité nous allons ouvrir le code source de notre page "``localhost:81/docs``" de notre Framework ``fastapi``  

 
 
 
 

![img.png](imgs/ow08.png) 

 
 
 

En tapant sur internet ``Ctrl+u``  

 
 
 

![img.png](imgs/ow07.png) 

 
 



Conclusion : nous avons passé ce test n°6 dans un premier temps parce que nous avons pris en compte et mis en place un système de sécurité. Mais aussi car le Framework ``fastapi`` a pris en charge la page source html que l'on peut voir ci-dessus et on constate que l'on n'a pas accès à grand-chose à part le liens css l'icône et un fichier javascript concernant la licence d'utilisation. 

Pour la partie serveur nous ne somme pas parfait neanmoins nous avons mis en place un TLS (Transport Layer Security) SSL (Secure Sockets Layer).

 

 
