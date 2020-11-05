# Requirements
Install virtualenv for python 3

Set environment variable to specify database connection:
export DATABASE_URL=postgresql://user:password@host/database

e.g. export DATABASE_URL=postgresql://harvest:harvest@localhost/harvest


# Starting web service
From a terminl and at the project folder (i.e. service), execute the following commands:

    virtualenv --python=python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

## With Flask
    python api.py

## With Gunicorn
    gunicorn -c gunicorn_conf.py wsgi:app

The web service will run by default at http://localhost:5000

If you have issues installing gdal, try the following:

pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==`gdal-config --version`

Example to get CLUs (CLU):

    GET http://localhost:5000/api/CLUs/665516

Example to create a user (users):

    POST http://localhost:5000/api/users

{
"email": "user@example.com",
"firstName":"user",
"lastName" : "example"
}


Example to create a userfield (userfield):

    POST http://localhost:5000/api/userfield

{
"userid": "user@example.com",
"clu":"665516",
"cluname" : "Field-1",
  "lat": "40.025",
  "lon": "-88.275"
}

