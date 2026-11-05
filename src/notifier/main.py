#!/usr/bin/env python3

import logging
import traceback
import sys
import os
from datetime import datetime

RUN_ID = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}_{os.getpid()}"    # DATE-TIME_PID

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(MAIN_DIR))
DATA_DIR = os.path.join(ROOT_DIR, "data")

from .cli.parser import parse_args
from .cli.handlers import handle
from .infra import config, output
from .infra import logging as app_logging
from .models.outputs import Error

logger = logging.getLogger(__name__)


def init(args):
    output.init(args)
    config.init(args)
    app_logging.init()


def run():
    args = parse_args()
    init(args)
    output.write(f"Notifier started ({RUN_ID})")
    handle(args)


def cleanup():
    output.close()


def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr, flush=True)
        return 130
    except Exception as e:
        output.emergency(Error(f"Application failed: {e}\n{traceback.format_exc()}"), flush=True)

        if app_logging.initialized:
            logger.exception("Application failed: %s", e)

        return 1
    finally:
        try:
            cleanup()
        except Exception as e:
            output.emergency(Error(f"Cleanup failed: {e}\n{traceback.format_exc()}"), flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())