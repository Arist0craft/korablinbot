from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import webhook


urlpatterns = [
    path("webhook/", csrf_exempt(webhook)),
]
