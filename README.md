# Restaurants API

## Requirements

You need `python 3.12` or superior and you need to have installed `poetry`. You can install poetry using the following command:

```bash
pip install poetry
```

If you want to have your local MongoDB database you will need to have installed `docker` and `docker compose`. If you are in windows you can install docker desktop [here](https://docs.docker.com/desktop/install/windows-install/) or if you are using linux you can install see the instructions for any linux distro [here](https://docs.docker.com/engine/install/). You can use any mongo provider changing the environment variable.

## Environment variables

You need all the following environment variables inside a .env file:

```env
MONGO_URL=
DATABASE_NAME=
ALGORITHM=HS256
SECRET_KEY=
ENVIRONMENT=
```

ENVIRONMENT must be 'testing' or 'production'. Use 'testing' for running pytests or local api.
Given that we only want to use 1 algorithm it is only allowed to use HS256. The variables is added for completness.

## Setup

After installing poetry you will be able to run the following commands:

```bash
poetry install --no-root # Install the virtual environment
```

If you want to use your local docker MongoDB database you should run `docker compose up` in other terminal. Now you need to set the following environment variable:

```env
MONGO_URL=mongodb://root:testing_local_database@localhost:27017/
```

## Start

To start the API you can run:

```bash
poetry shell # Activate virtual environment
fastpi dev main.py # Run the api
```

The default port is 8000. You can now go to the [local docs](localhost:8000/docs) and use the API.

## Swagger docs

You can authorize any request made inside Swagger docs using the **Authorize** button at top right of the page. You need to provide the authorization token (JWT) and swagger docs will automatically attach this tokent to **Authorization** header in the next requests.

You can generate JWT's using the endpoint `auth/login`. Remember that the token has a **lifespan of 20 min**.

## Reset database

> [!WARNING]
> The following command will delete the database and populate with the data inside scripts/seed_data.py.

You can populate the databse using:

```bash
python scripts/reset_database.py # Run this from the project root
```

## Testing

Before runing the tests you need to change the ENVIRONMENT variable to be 'testing'. You excecute the tests running in root folder:

```bash
pytest
```

Currently there are 10 available tests:
![imagen](https://github.com/judasaca/restaurant_api/assets/48933463/6668bb3c-eab2-4526-a491-7bc7380a6416)
