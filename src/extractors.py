import requests
import logging
import pandas as pd
from constants import BASE_FILE_DIR, LOGS_DIR
from datetime import datetime


log_file_path = LOGS_DIR / "extractors.log"
logging.basicConfig(filename=log_file_path, encoding="utf-8", level=logging.DEBUG)
log = logging.getLogger()


class UrlExtractor:
    file_path_crib = (
        "{category}/{year}-{month:02d}/{category}-{day:02d}-{month:02d}-{year}.csv"
    )

    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    def extract(self, date_str: str) -> str:
        """Extract data from url, stores it on file_path and return the csv path

        Args:
            date_str (str): Run date with yyyy-mm-dd format

        Returns:
            str: csv final path
        """
        log.info(f"Extracting file {self.name}")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        file_path = self.file_path_crib.format(
            category=self.name, year=date.year, month=date.month, day=date.day
        )
        museo_path = BASE_FILE_DIR / file_path
        # If there's no parent directory, this will throw FileNotFoundError.
        museo_path.parent.mkdir(parents=True, exist_ok=True)

        r = requests.get(self.url)
        r.encoding = "utf-8"

        log.info(f"Storing file {museo_path}")
        # Save file
        with open(museo_path, "w") as f_out:
            f_out.write(r.text)
        log.info(f"File stored successfully")

        return museo_path

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforming the raw data and returns it on a dataframe

        Args:
            df (pd.DataFrame): The dataframe that I want to apply the transformation to

        Returns:
            pd.DataFrame: The transformed dataframe
        """
        # Map the columns as the statement says
        renamed_columns = {
            "Cod_Loc": "cod_localidad",
            "IdProvincia": "id_provincia",
            "IdDepartamento": "id_departamento",
            "Provincia": "provincia",
            "Categoría": "categoria",
            "Domicilio": "domicilio",
            "CP": "código postal",
            "Localidad": "localidad",
            "Nombre": "nombre",
            "Domicilio": "domicilio",
            "Teléfono": "telefono",
            "Mail": "mail",
            "Web": "web",
        }

        df = df.rename(columns=renamed_columns)

        columns_list = [
            "cod_localidad",
            "id_provincia",
            "id_departamento",
            "categoria",
            "provincia",
            "localidad",
            "nombre",
            # "domicilio",
            "código postal",
            "telefono",
            "mail",
            "web",
        ]

        # breakpoint()
        # Taking only the necessary columns
        return df[columns_list]


class MuseoExtractor(UrlExtractor):
    def transfrom(self, df: pd.DataFrame) -> pd.DataFrame:
        renamed_columns = {
            "Cod_Loc": "cod_localidad",
            "IdProvincia": "id_provincia",
            "IdDepartamento": "id_departamento",
            "categoria": "categoria",
            "direccion": "domicilio",
            "CP": "código postal",
            "telefono": "número de teléfono",
            "Mail": "mail",
            "Web": "web",
        }

        df = df.rename(columns=renamed_columns)

        columns_list = [
            "cod_localidad",
            "id_provincia",
            "id_departamento",
            "categoria",
            "domicilio",
            "código postal",
            "número de teléfono",
            "mail",
            "web",
        ]

        return df[columns_list]
