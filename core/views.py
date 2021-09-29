from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from core.steps import hello
from core.steps import summarizer

# Create your views here.
@api_view(['GET', ])
def read_news(request):
    if request.method == 'GET':
        text = hello.helloFriend()
        return Response(summarizer.sumarizationText(text))