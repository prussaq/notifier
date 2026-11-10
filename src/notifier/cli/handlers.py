import logging

logger = logging.getLogger(__name__)


def handle(args):
    if args.handler: 
        args.handler(args)
    else: 
        args.print_help()


def push(args):
    from notifier.services import pusher

    pusher.send(args.title, args.body)


def email(args):
    ...