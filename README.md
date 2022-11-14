# First Django Project

### A project for storing a collection of images and allowing users to tag them


## Description
Back-end (REST API) developed using Python 3, Django REST Framework.
Application with authorization (JWT token), splitting of users into groups of privileges. Users, according to the privilege level, can add collections of images, as well as tag them. Users with the highest level of privileges can receive statistical information about the frequency of image tagging and the most common tags.

- GET type endpoints are cached and results are provided using pagination
- All endpoints are covered with tests
- Project contains swagger documentation and endpoint for health checking
- Project is placed in a docker container managed by a docker compose file, in order to easy set up the application in production


## Prerequisites
- Docker

## Usage
Start the docker containers
```
docker-compose up -d --build
```

User privilege groups must be created.
Each newly registered user will have the lowest privilege level
```
python manage.py creategroups
```
