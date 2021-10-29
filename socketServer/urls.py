from django.urls import path
from socketServer import views

app_name = 'socketServer'

urlpatterns = [
    path('manual-inclusion', views.connect_manual, name="add_socket_manual"),
]
