import json

from django.http import HttpRequest
from telegram import Update

from .bot import dispatcher


def webhook(request: HttpRequest):
    if request.method == "POST":
        update_data = json.loads(request.body)
        dispatcher.process_update(Update.de_json(update_data, dispatcher.bot))
        return ""
    else:
        raise TypeError("Wrong type of request was sent")
