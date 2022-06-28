# CodeShare API

An async code sharing API written in FastAPI. Inspired from the Django file system and
and Nest JS.

## Run Locally

### There are two ways of running this project locally

#### Note: The application will run fine with all the default configurations that I have added however you are requested to add your own configurations to the application when running it. Also make sure to add .env file and add configurations according to .ev.example file.

- with Docker (recommended)
- without Docker (not recommended)

Clone the project

```bash
  git clone https://github.com/Neeraj319/codeshare
```

#### With Docker

Go to the project directory

```bash
cd codeshare-back
```

```
sudo docker-compose up --build
```

#### NOTE: make sure to comment out line no 4 and 6 in entrypoint.sh after building the image  

#### Without Docker

- Install poetry: https://python-poetry.org/
- Install postgresql database from: https://www.postgresql.org/download/

```bash
cd codeshare-back
```

install required packages

```bash
poetry lock
poetry install
poetry shell
```

create tables on the database

```
python3 manage.py create_tables
```

start the server

```bash
uvicorn main:app --reload
```

#### For more commands

```
python3 manage.py help
```

##### Visit /docs for the documentation of the API

## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's [code_of_conduct.md](https://github.com/Neeraj319/codeshare/blob/main/code_of_conduct.md).
