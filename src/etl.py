from constants import BASE_FILE_DIR, LOGS_DIR
from cfg import museos_ds, biblios_ds
import pandas as pd
import click
import logging
from extractors import MuseoExtractor, UrlExtractor
from loaders import (
    SizeByCategoryLoader,
    SizeBySourceLoader,
    SizeByCatProvLoader,
)

log_file_path = LOGS_DIR / "etl.log"
logging.basicConfig(filename=log_file_path, encoding="utf-8", level=logging.DEBUG)
log = logging.getLogger()

extractors_dict = {
    "museos": MuseoExtractor(museos_ds["name"], museos_ds["url"]),
    "biblios": UrlExtractor(biblios_ds["name"], biblios_ds["url"]),
    # "cines": UrlExtractor(cines_ds["name"], cines_ds["url"]),
}


def extract_raws(date_str: str) -> list[str]:
    """Run extractors

    Args:
        date_str (str): Run date with yyyy-mm-dd format

    Returns:
        list[str]: list of stored data file paths
    """
    file_paths = dict()
    for name, extractor in extractors_dict.items():
        file_path = extractor.extract(date_str)
        file_paths[name] = file_path
    return file_paths


def merge_raw(file_paths: list[str], out_file_path: str) -> str:
    """Merge raw data and stores it in out_file_path

    Args:
        file_paths (list[str]): list of raw data path
        out_file_path (str): final merge csv path

    Returns:
        str: _description_
    """
    dfs_transformed = list()
    for name, extractor in extractors_dict.items():
        df = pd.read_csv(file_paths[name])
        df_transformed = extractor.transform(df)
        dfs_transformed.append(df_transformed)
    pd.concat(dfs_transformed, axis=0).to_csv(out_file_path)
    return out_file_path


@click.command()
@click.option("--date", help="Run date with yyyy-mm-dd format")
def run_pipeline(date: str) -> None:
    """Run the pipeline

    Args:
        date (str): Job date with yyyy-mm-dd format
    """

    # Extract
    log.info("Extracting data")
    file_paths = extract_raws(date)

    # Transform
    merge_path = BASE_FILE_DIR / "merge_df_{date}.csv"
    merge_raw(file_paths, merge_path)

    # Load
    log.info("Loading data")
    SizeByCategoryLoader().load_table(merge_path)
    SizeBySourceLoader().load_table(file_paths)
    SizeByCatProvLoader().load_table(merge_path)
    log.info("Data loaded successfully")


if __name__ == "__main__":
    run_pipeline()
