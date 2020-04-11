# Fullstack Nanodegree Capstone Project

## Getting Started

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Setup environment

```bash
export FLASK_APP=app.py
```

### Start server

```bash
flask run --reload
```

### Run Test

## run test_app.py
```bash
dropdb casting
createdb casting
psql casting < movie.psql
python test_app.py
```

## run fullstacknd-capstone.postman_collection.json or open in Postman (make sure the server is running)
```bash
dropdb casting
createdb casting
psql casting < movie.psql
newman run fullstacknd-capstone.postman_collection.json
```

### Roles
 - Casting Assistant: view only
 - Casting Director: view, create and modify actors; modify movie
 - Executive Producer: view, create and modify actors; create and modify movie

## Endpoints

### Actor
### GET all actors

```bash
{
    "actors": [
        {
            "age": 30,
            "gender": "male",
            "id": 1,
            "name": "James"
        },
        {
            "age": 25,
            "gender": "female",
            "id": 2,
            "name": "Dana"
        },
        {
            "age": 30,
            "gender": "male",
            "id": 4,
            "name": "Andy"
        }
    ],
    "success": true
}
```

### GET actor by id

```bash
{
    "actor": {
        "age": 30,
        "gender": "male",
        "id": 1,
        "name": "James"
    },
    "success": true
}
```

### POST add actor

```bash
{
    "actor": {
        "age": 25,
        "gender": "female",
        "id": 5,
        "name": "Dana"
    },
    "success": true
}
```

### PATCH actor

```bash
{
    "success": true
}
```

### DELETE actor

```bash
{
    "success": true
}
```

### Movie
### GET all movies

```bash
{
    "movies": [
        {
            "id": 1,
            "release_date": "Sat, 01 Jun 2013 00:00:00 GMT",
            "title": "Space Hound"
        },
        {
            "id": 3,
            "release_date": "Fri, 01 Jan 2021 00:00:00 GMT",
            "title": "Space Ranger"
        }
    ],
    "success": true
}
```

### GET movie by id

```bash
{
    "movie": {
        "id": 4,
        "release_date": "Sat, 01 Jan 2022 00:00:00 GMT",
        "title": "Space Hound"
    },
    "success": true
}
```

### POST add movie

```bash
{
    "movie": {
        "id": 2,
        "release_date": "Mon, 01 Jun 2020 00:00:00 GMT",
        "title": "Amazing Show"
    },
    "success": true
}
```

### PATCH movie

```bash
{
    "success": true
}
```

### DELETE movie

```bash
{
    "success": true
}
```