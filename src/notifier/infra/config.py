import os
import yaml
from datetime import datetime

from dotenv import load_dotenv

from ..main import RUN_ID, MAIN_DIR
from ..utils.dict_utils import setv, getv, reqv
from ..common.exceptions import ConfigError
from ..infra import output
from ..models.outputs import Warning

CONFIG_DIR = os.path.join(MAIN_DIR, "config")
CONFIG_FILE = "application.yaml"

configs = {}


def init(args):
    global CONFIG_DIR

    config_path = os.getenv('CONFIG_PATH')
    if config_path:
        CONFIG_DIR = os.path.join(CONFIG_DIR, config_path)

    try:
        load_dotenv(os.path.join(CONFIG_DIR, '.env'))
        _init_configs(args)
    except Exception as e:
        raise ConfigError(e)


def _init_configs(args):
    configs.update(_load_config(CONFIG_FILE))

    _override_configs(args)
    _resolve_configs()


def _load_config(file_name):
    config_file = os.path.join(CONFIG_DIR, file_name)
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    if config is None:
        raise ConfigError(f"Config file is empty: {config_file}")

    return config


def _override_configs(args):
    if args.configs: 
        for cfg, val in args.configs.items():
            try: setv(configs, cfg, val, strict=True)
            except Exception as e: 
                output.write(Warning(f"Ignoring unknown config: {cfg}"), flush=True)


def _resolve_configs():
    ...
