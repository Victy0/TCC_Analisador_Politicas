from django.shortcuts import render
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


from core.steps import requestUrl
from core.steps import summarizer

from models import AnalyticalReview

# criação da lista de políticas de privacidade em análise
analytical_review_list = []

# criação da lista  de id de análises canceladas
cancel_review_list = []

# 
# método POST para solicitar análise de política de privacidade
# 
@api_view(['POST', ])
def request_url(request):
    if request.method == 'POST':

        # criação do id para 
        analytical_review = AnalyticalReview()
        analytical_review.id = datetime.now().strftime("%S.%f")

        # incluindo a análise na lista de políticas em análise
        analytical_review_list.append(analytical_review)

        # etapa de extração de texto bruto do PDF ou HTML
        text = requestUrl.textExtractor(request.data['url'], analytical_review.id)

        return Response(summarizer.summarizerText(text))
