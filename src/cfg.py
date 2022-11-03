from decouple import AutoConfig
from constants import ROOT_DIR

config = AutoConfig(search_path=ROOT_DIR)

DB_CONNSTR = config("DB_CONNSTR")
MUSEOS_URL = config("MUSEOS_URL")
BIBLIOS_URL = config("BIBLIOS_URL")

museos_ds = {"name": "museos", "url": MUSEOS_URL}
biblios_ds = {"name": "biblios", "url": BIBLIOS_URL}
