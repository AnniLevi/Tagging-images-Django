# First Django Project

### A project for storing a collection of images and allowing users to tag them


## Description
Back-end (REST API) developed using Python 3, Django REST Framework.
Application implements authorization (JWT token), splitting of users into groups of privileges.
Users, according to the privilege level, can add collections of images, as well as tag them.
Users with the highest level of privileges can receive statistical information about the frequency of image tagging
and the most common tags.

- GET type endpoints are cached and results are provided using pagination
- All endpoints are covered with tests
- Project contains swagger documentation and endpoint for health checking
- Project is placed in a docker container managed by a docker compose file, in order to easy set up the application in production


## Prerequisites
- Docker
- GitLab Runner

## Usage
Start the docker containers

> docker-compose up -d --build

User privilege groups must be created.
Each newly registered user will have the lowest privilege level

> python manage.py creategroups

Swagger documentation:

> /swagger/

Admin interface:

> /admin/


## Endpoints

### auth
- POST api/auth/register/
```
request:
{
    "username",
    "first_name",
    "last_name",
    "email",
    "password"
}

response (code 201):
{
    "username",
    "first_name",
    "last_name",
    "email",
    "password",
    "token"
}
```

- POST api/auth/token/
```
request:
{
    "username",
    "password"
}

response (code 200):
{
    "refresh",
    "access"
}
```

- POST api/auth/token/refresh/
```
request:
{
    "refresh"
}

response (code 200):
{
    "refresh",
    "access"
}
```

- POST api/auth/token/verify/
```
request:
{
    "token"
}

response (code 200):
{
    "token"
}
```


### images

- GET api/images/
```
query params: tagged=true/false

response (code 200):
[
    {
        "id",
        "name",
        "img",
        "user_id",
        "created_at",
        "tags":
        [
            {
                "id",
                "tag",
                "img_id",
                "user_id",
                "created_at"
            },
        ]
    },
]
```

- POST api/images/
```
request:
{
    "name",
    "img"
}

response (code 201):
{
    "id",
    "name",
    "img",
    "user_id",
    "created_at",
    "tags"
}
```

- POST api/images/zip-upload/
```
request:
{
    "zip_archive"
}

response (code 201):
{
    "ok": true
}
```

- GET api/images/tags/
```
response (code 200):
[
    {
        "id",
        "tag",
        "img_id",
        "user_id",
        "created_at"
    },
]
```

- POST api/images/tags/
```
request:
{
    "tag",
    "img_id"
}

response (code 201):
{
    "id",
    "tag",
    "img_id",
    "user_id",
    "created_at"
}
```

- GET api/images/common-tags/
```
response (code 200):
[
    {
        "id",
        "img_name",
        "tag",
        "tags_count"
    },
]
```

- GET api/images/most-tagged/
```
response (code 200):
[
    {
        "id",
        "tags_count"
        "img_name",
    },
]
```
