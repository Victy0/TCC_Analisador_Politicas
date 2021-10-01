from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from core.steps import requestUrl
from core.steps import summarizer

# Create your views here.
@api_view(['POST', ])
def request_url(request):
    if request.method == 'POST':
        text = requestUrl.textExtractor(request.data['url'])
        return Response(summarizer.summarizerText(text))