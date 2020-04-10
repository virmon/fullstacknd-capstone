from models import Actor, Movie, Cast, db

actors = [
    {
        "id": 1,
        "name": "Alvin",
        "genres": ["Action"],
        "role": "Lead actor"
    }, 
    {
        "id": 2,
        "name": "Bella",
        "genres": ["Romance"],
        "role": "Lead actor"
    },
    {
        "id": 3,
        "name": "Cath",
        "genres": ["Action"],
        "role": "Supporting actor"
    }
]

movies = [
    {
        "id": 1,
        "title": "Rising Sun",
        "genres": ["Action"]
    }, 
    {
        "id": 2,
        "title": "Race Track",
        "genres": ["Action"]
    },
    {
        "id": 3,
        "title": "Romantic Film",
        "genres": ["Romance"]
    }
]

casts = [
    {
        "actor_id": 1,
        "movie_id": 1
    }, 
    {
        "actor_id": 2,
        "movie_id": 3
    }, 
    {
        "actor_id": 3,
        "movie_id": 3
    },
    {
        "actor_id": 3,
        "movie_id": 1
    }, 
    {
        "actor_id": 1,
        "movie_id": 3
    }, 
]

for a in actors:
    name = a['name']
    genres = a['genres']
    role = a['role']

    data = Actor(name=name, genres=genres, role=role)
    db.session.add(data)


for m in movies:
    title = m["title"]
    genres = m["genres"]

    data = Movie(title=title, genres=genres)
    db.session.add(data)


for c in casts:
    actor_id = c["actor_id"]
    movie_id = c["movie_id"]

    data = Cast(actor_id=actor_id, movie_id=movie_id)
    db.session.add(data)


db.session.commit()