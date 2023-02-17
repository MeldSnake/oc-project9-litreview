# LitReview

Site de diffusion et de requete de diffusion de commentaire sur des livres et autres oeuvres.

## Description

Ce projet ecris avec le framework django permets a different utilisateur d'interragir entre eux dans le but d'obtenir des commentaires sur des oeuvres.

Ecris en python, et avec l'aide du [framework django](https://www.djangoproject.com/), le serveur realisé genere les pages html de son cote et les redistribues a l'utilisateur connecté.

Les utilisateurs doivent ce [connecter](https://localhost:8000/login/) au site via l'interface ou [creer un nouveau compte](https://localhost:8000/register/).

Chaque utilisateur dispose d'un flux de requetes/commentaires representant leurs requetes/commentaires ou ceux d'autre utilisateur auquels ils sont souscris ou ayant repondus a leurs demande de commentaire.

Ils peuvent aussi s'abonner au flux de requetes/commentaires d'autres utilisateurs.

## Utilisation

1. Cloner le repository git ou telecharger l'archive du repository.
2. (opt) Creer et activer un environement viruel
    - Linux/MacOS
        ```shell
        > python -m venv .venv
        > source .venv/Scripts/activate
        ```
    - Windows (cmd)
        ```shell
        > python -m venv .venv
        > .venv/Scripts/activate.bat
        ```
    - Windows (poweshell)
        ```shell
        > python -m venv .venv
        > & .venv/Scripts/activate.ps1
        ```

3. Installer les dependances necessaires au projet
    ```shell
    (venv)> python -m pip install -r requirements.txt
    ```
4. Lancer le serveur
    ```shell
    (venv)> python manage.py runserver
    ```
5. Dans le navigateur de votre choix allez à l'address du serveur HTTP http://localhost:8000/

## Connexion

Une serie d'utilisateur deja existant sont integrer a la base de donnée par defaut.
Chaqu'un de ces utilisateurs utilise le meme mot de passe: `password`

1. admin
2. jean_jean
3. darth_vador
4. marco_polo

L'utilisateur admin peut aussi acceder a la page d'administration [/admin](http://localhost:800/admin/)

