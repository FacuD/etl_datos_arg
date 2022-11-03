from unicodedata import category
from sqlalchemy import create_engine
from cfg import DB_CONNSTR
import pandas as pd
from constants import (
    SOURCE_SIZE_TABLE_NAME,
    CATEGORY_COUNT_TABLE_NAME,
    PROV_CAT_COUNT_TABLE_NAME,
)

engine = create_engine(DB_CONNSTR)


class BaseLoader:
    def load_table(self, df: pd.DataFrame) -> None:
        df.to_sql(self.table_name, con=engine, index=False, if_exists="replace")


class SizeByCategoryLoader(BaseLoader):
    table_name = CATEGORY_COUNT_TABLE_NAME

    def load_table(self, file_path: str):
        df = pd.read_csv(file_path)
        df_transformed = df.groupby(["categoria"], as_index=False).size()
        return super().load_table(df_transformed)


class SizeBySourceLoader(BaseLoader):
    table_name = SOURCE_SIZE_TABLE_NAME

    def load_table(self, file_paths: str):
        lst = list()
        for name, file_path in file_paths.items():
            df = pd.read_csv(file_path)
            lst.append({"source": name, "count": df.size})

        df_source_size = pd.DataFrame(lst)
        return super().load_table(df_source_size)


class SizeByCatProvLoader(BaseLoader):
    table_name = PROV_CAT_COUNT_TABLE_NAME

    def load_table(self, file_path: str):
        df = pd.read_csv(file_path)
        df_size_by_prov_cat = df.groupby(
            ["categoria", "provincia"], as_index=False
        ).size()

        return super().load_table(df_size_by_prov_cat)
