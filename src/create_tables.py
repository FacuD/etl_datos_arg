from sqlalchemy import create_engine
from sqlalchemy.sql import text
from constants import SQL_DIR, TABLES_NAMES, LOGS_DIR
from cfg import DB_CONNSTR
import logging

engine = create_engine(DB_CONNSTR)
log_file_path = LOGS_DIR / "create_tables.log"
logging.basicConfig(filename=log_file_path, encoding="utf-8", level=logging.DEBUG)
log = logging.getLogger()


def create_tables():
    """
    Looping over the SQL files in the /sql directory and executing them
    """

    with engine.connect() as connection:
        for file in TABLES_NAMES:
            log.info(f"Creating table => {file}")
            with open(SQL_DIR / f"{file}.sql") as f:
                query = text(f.read())

            connection.execute(f"DROP TABLE IF EXISTS {file}")
            connection.execute(query)
            log.info(f"Table {file} created successfully")


if __name__ == "__main__":
    create_tables()
