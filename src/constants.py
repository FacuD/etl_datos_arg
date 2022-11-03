from pathlib import Path

# Where I'm gonna place all the .csv files
BASE_FILE_DIR = Path("/tmp")
ROOT_DIR = Path()
SQL_DIR = (ROOT_DIR / "sql").resolve()
LOGS_DIR = (ROOT_DIR / "logs").resolve()

RAW_TABLE_NAME = "raw"
# CINE_INSIGHTS_TABLE_NAME = "cine_insights"
SOURCE_SIZE_TABLE_NAME = "size_by_datasource"
CATEGORY_COUNT_TABLE_NAME = "size_by_category"
PROV_CAT_COUNT_TABLE_NAME = "size_by_datasource"

TABLES_NAMES = [
    RAW_TABLE_NAME,
    # CINE_INSIGHTS_TABLE_NAME,
    SOURCE_SIZE_TABLE_NAME,
    CATEGORY_COUNT_TABLE_NAME,
    PROV_CAT_COUNT_TABLE_NAME,
]
