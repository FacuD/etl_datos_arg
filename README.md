# Challenge Data Analytics Python 🐍

## Prerequisites

### Poetry

Poetry helps you declare, manage and install dependencies of Python projects, ensuring you have the right stack everywhere.
You need to install poetry with `pip install poetry`.
How to use poetry is explained in the [documentation](https://python-poetry.org/docs/).
I exported all the necesary dependencies to a `requeriments.txt` file, so you can install them with `pip install -r requeriments.txt` if you don't want to use poetry. Although I recommend you to use poetry, [here](https://dev.to/vadimkolobanov/poetry-vs-pip-or-how-to-forget-forever-requirementstxt-cheat-sheet-for-beginners-33h1) you have some reasons why.

## Data reaserch

On this [notebook](notebooks/data%20exploratory.ipynb) you have all the data research I did to understand the data and the problem.

## Setup the database

To set up the database you need to run the following commands:

```docker
docker run --name challenge_datos_argentina -v my_dbdata:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=data_analytics -d postgres
```

To query the database you can do

```docker
docker exec -it challenge_datos_argentina psql -U postgres -d data_analytics
```

### Create the tables

You can create the database tables with the following command:

```python
python src/create_tables.py
```

This script will run all the files in the `src/sql` folder.

### Run the ETL

To run the ETL you need to run the following command:

```python
python src/etl.py --date run_date
```

Where `run_date` is the date you want to run the ETL for. The format is `YYYY-MM-DD`.
