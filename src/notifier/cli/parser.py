import argparse

from . import handlers
from .helpers import ConfigKV


def parse_args():
    parser = _build_parser()
    return parser.parse_args()


def _build_parser():
    parser = argparse.ArgumentParser(prog="NOTIFIER", description="Notifier CLI application")
    parser.add_argument("--configs", action=ConfigKV, metavar="KEY=VALUE", help="Temporarily override application configuration parameter using dot-separated keys (e.g. foo.bar=value). Can be specified multiple times. Keys map directly to the configuration structure.")
    parser.add_argument("--json-output", dest="json_output", choices=["file", "stdout"], help="Where to write JSON output: 'file' to write to a file, or 'stdout' to write to standard output.")
    
    subparsers = parser.add_subparsers(title="commands", dest="command", required=True, help='Available commands')

    sync = subparsers.add_parser("foo", help="Foo command")
    sync.set_defaults(handler=handlers.foo)
    
    return parser
