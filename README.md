# twitter-clone
[![](https://github.com/ShadabS05/final_project/workflows/tests/badge.svg)](https://github.com/ShadabS05/final_project/actions?query=workflow%3Atests)


This is a twitter clone that uses the following tech stack:

1.Python
2.Flask
3.Docker
3.HTML/CSS
4.Jinga2
5.PostgreSQL
6.Nginx
7.Gunicorn

This twitter clone has 6 pages.

- Home
    - Default page, loads in most recent messages with 20 tweets per page.
- Search Message
    - Has a textbook that is used to search through all messages that are within the searchbar.
- Login
    - A user can login with a valid username and password, grants access to create message feature.
- Create User
    - A user can create an account with a new username and with a password.
- Create Message
    - A user can "post" a message online.
- Logout
    - A user can logout (deletes cookies).

In the future, there will be more functionality to add images, user account profiles, and more. Furthermore, there will be more updates to the websites style!

## Prerequisites

Make sure you have docker / docker compose installed. Afterwards, you can clone this repository.

## Setup Instructions

After you have cloned this repository, you need the following files:

1. .end.dev

```
FLASK_APP=project/__init__.py
FLASK_DEBUG=1
DATABASE_URL=postgresql://{your username}:{your password}@db:5432/{your dev db name}
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
APP_FOLDER=/usr/src/app
```

2. .end.prod

```
FLASK_APP=project/__init__.py
FLASK_DEBUG=0
DATABASE_URL=postgresql://{your username}:{your password}@db:5432/{your prod db name}
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
APP_FOLDER=/home/app/web
```

3. .env.prod.db

```
POSTGRES_USER={your username}
POSTGRES_PASSWORD={your password}
POSTGRES_DB={your prod db name}
```

Afterwards, edit the `docker-compose.yml` file so that it uses your username and password for the db. Now, we can use docker compose to start building!

## Building

Before we build, we must ensure that port forwarding is enabled.This allows us to run our flask application locally. The default for production is `1486`. Once port forwarding is enabled, run the following commands in order:

```
$ docker compose down -v
```

This command allows us to bring down any open, pre-existing containers and volumes.

Next run the following commands:

```
$ docker compose -f docker-compose.prod.yml up -d --build
$ docker compose -f docker-compose.prod.yml exec web python manage.py create_db
```

The first command builds a new image and spins the containers. The next command creates the table where images will be stored. Once you are finished, you can run the first command in this section to spin down your containers.

## Results

To see your local flask application, you want to go to the following link in firefox:

`localhost:PORT/upload`.

PORT depends on your first number in your portforwarding. From here, you can browse and upload your image.

To see your image, go to the following link: 

`localhost:PORT/upload/FILENAME`.

 If there are any issues, please let me know!
