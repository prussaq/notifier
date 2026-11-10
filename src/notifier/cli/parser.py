import argparse

from . import handlers
from .helpers import ConfigKV


def parse_args():
    parser = _build_parser()
    return parser.parse_args()


def _build_parser():
    parser = argparse.ArgumentParser(prog="notifier", description="Notifier CLI application")
    parser.add_argument("--configs", action=ConfigKV, metavar="KEY=VALUE", help="Temporarily override application configuration parameter using dot-separated keys (e.g. foo.bar=value). Can be specified multiple times. Keys map directly to the configuration structure.")
    parser.add_argument("--json-output", dest="json_output", choices=["file", "stdout"], help="Where to write JSON output: 'file' to write to a file, or 'stdout' to write to standard output.")
    
    subparsers = parser.add_subparsers(title="commands", dest="command", required=True, help='Available commands')

    push = subparsers.add_parser("push", help="Push notifications")
    push.add_argument("--title", required=True, help="Push notification title")
    push.add_argument("--body", required=True, help="Push notification body")
    push.set_defaults(handler=handlers.push)

    email = subparsers.add_parser("email", help="Email notifications")
    email.add_argument("recipient", help="Recipient email address")
    email.add_argument("--subject", required=True, help="Email subject")
    email.add_argument("--body", required=True, help="Email body")
    email.set_defaults(handler=handlers.email)

    return parser
