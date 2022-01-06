import json

from django.http import HttpRequest, JsonResponse

from .bot import process_update
from app.settings import USE_CELERY
from utils import setup_logger

logger = setup_logger(__name__, with_function=True)


def webhook(request: HttpRequest):
    logger.info("Request accepted")
    if request.method == "POST":
        if USE_CELERY:
            logger.info("Add task to Celery Queue")
            process_update.delay(json.loads(request.body))
        else:
            logger.info("Processing update")
            process_update(json.loads(request.body))

        logger.info("Send response to Telegram")
        return JsonResponse({"ok": "POST request processed"})
    else:
        logger.warning("Request type wasn't POST, smth wrong")
        raise TypeError("Wrong type of request was sent")
