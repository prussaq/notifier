import json
import os

from dotenv import load_dotenv

from ..utils.os_utils import reqenv

VAULT_DIR = reqenv('VAULT_DIR')

vaults = {
    "firebase": {
        "service_account": None,
        "creds": None
    }
}


def init():
    load_dotenv(os.path.join(VAULT_DIR, '.env'))

    with open(f"{VAULT_DIR}/firebase/service_account.json") as f:
        vaults['firebase']['service_account'] = json.load(f)

    with open(f"{VAULT_DIR}/firebase/creds.json") as f:
        vaults['firebase']['creds'] = json.load(f)


init()