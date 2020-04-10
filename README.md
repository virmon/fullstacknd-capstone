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

## Endpoints

### Actor
### GET all actors

```bash
{
    "actors": [
        {
            "genres": "[Fantasy]",
            "id": 1,
            "name": "Dana",
            "role": "Supporting Actor"
        }
    ],
    "success": true
}
```

### GET actor by id

```bash
{
    "actor": {
        "genres": "[Fantasy]",
        "id": 1,
        "name": "Dana",
        "role": "Supporting Actor"
    },
    "success": true
}
```

### POST add actor

```bash
{
    "actor": {
        "genres": "[Fantasy, Romance]",
        "id": 2,
        "name": "Andy",
        "role": "Lead Actor"
    },
    "success": true
}
```

### PATCH actor

```bash
{
    "success": true,
    "updated": 2
}
```

### DELETE actor

```bash
{
    "deleted": 2,
    "success": true
}
```