# Requirements
Install virtualenv for python 3

Set environment variable to specify database connection:
export DATABASE_URL=postgresql://user:password@host/database

e.g. export DATABASE_URL=postgresql://harvest:harvest@localhost/harvest


# Starting web service
From a terminal and at the project folder (i.e. service), execute the following commands:

    virtualenv --python=python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

## With Flask
    python api.py

## With Gunicorn

Create `gunicorn_conf.py` (see `gunicorn_conf.example.py`) and start the server:

    gunicorn -c gunicorn_conf.py wsgi:app

The web service will run by default at http://localhost:3000

Example to get CLUs (CLU):

    GET http://localhost:3000/api/CLUs/665516

Example to create a user (users):

    POST http://localhost:3000/api/users
    {
        "email": "user@example.com",
        "first_name": "user",
        "last_name" : "example"
    }

Example to create a user field:

    POST http://localhost:3000/api/user-field

    {"user_id": "user@example.com", "clu": "665516", "clu_name": "Field-1"}
