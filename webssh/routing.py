from django.urls import path
from .websocket import WebSSH
from batch.websocket_layer import Cmd

websocket_urlpatterns = [
    path('webssh/', WebSSH),
    path('cmd/', Cmd),
]