import logging

import firebase_admin
from firebase_admin import credentials, messaging

from notifier.infra import output
from notifier.utils.dict_utils import reqv
from notifier.infra.vault import vaults

logger = logging.getLogger(__name__)


def send(title: str, body: str):
    if not firebase_admin._apps:
        firebase_admin.initialize_app(
            credentials.Certificate(vaults['firebase']['service_account'])
        )

    message = messaging.Message(
        fid=vaults['firebase']['creds']['fid'],
        data={
            "title": title,
            "body": body,
        },
    )
    msg_id = messaging.send(message)

    logger.info(f"Push notification sent with message ID: {msg_id}")
    output.write("Push notification sent")
