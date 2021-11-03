from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('process', views.process_analysis, name="iniciar_analise"),
    path('cancel', views.cancel_analysis, name="cancelar_analise"),
]
