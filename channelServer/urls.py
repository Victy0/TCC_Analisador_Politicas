from django.urls import path
from channelServer import views

app_name = 'channelServer'

urlpatterns = [
    path('manual-inclusion', views.connect_manual, name="add_socket_manual"),
]
