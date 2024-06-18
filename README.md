# Flask JWT Auth

# How to start

0. Clone the project

```cmd
git clone <path_to_project>.git
```

1. Create .env file based on .env_example

2. Start Docker services
``` cmd
docker-compose up --build
```

3. Run migrations

3.1. Connect to `front-ml`
```commandline
docker ps -a

docker exec -it <container_id> /bin/bash
```

3.2. Run migrations
``` bash
conda activate flask-ml

export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

4. (Optional) Stop services
``` cmd
docker-compose down
```



[![Build Status](https://travis-ci.org/realpython/flask-jwt-auth.svg?branch=master)](https://travis-ci.org/realpython/flask-jwt-auth)

## Want to learn how to build this project?

Check out the [blog post](https://realpython.com/blog/python/token-based-authentication-with-flask/).

## Want to use this project?

### Basics

1. Fork/Clone
1. Activate a virtualenv
1. Install the requirements

### Set Environment Variables

Update *project/server/config.py*, and then run:

```sh
$ export APP_SETTINGS="project.server.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.server.config.ProductionConfig"
```

Set a SECRET_KEY:

```sh
$ export SECRET_KEY="change_me"
```

### Create DB

Create the databases in `psql`:

```sh
$ psql
# create database flask_jwt_auth
# create database flask_jwt_auth_test
# \q
```

Create the tables and run the migrations:

```sh
$ flask create_db
$ flask db init
$ flask db migrate
$ flask db upgrade
```

### Run the Application

```sh
$ flask run
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

> Want to specify a different port?

> ```sh
> $ python app.py runserver -h 0.0.0.0 -p 8080
> ```

### Testing

Without coverage:

```sh
$ python app.py test
```

With coverage:

```sh
$ python app.py cov
```
