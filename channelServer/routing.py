from django.urls import path

from channelServer.consumers import WSConsumer

ws_urlpatterns = [
    path('ws/connect/', WSConsumer.as_asgi())
]