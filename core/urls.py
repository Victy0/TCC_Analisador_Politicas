from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('start', views.start_analysis, name="iniciar_analise"),
    path('cancel', views.cancel_analysis, name="cancelar_analise"),
]
