import logging

logger = logging.getLogger(__name__)


def handle(args):
    if args.handler: 
        args.handler(args)
    else: 
        args.print_help()


def foo(args):
    print('Foo')
