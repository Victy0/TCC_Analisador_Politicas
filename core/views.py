from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


# Create your views here.
@api_view(['GET', ])
def read_news(request):
    if request.method == 'GET':
        return Response("Hello friend :)")