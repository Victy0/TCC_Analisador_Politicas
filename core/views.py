from django.shortcuts import render
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.steps import requestUrl
from core.steps import summarizer

from core.models import AnalyticalReview

# criação da lista de políticas de privacidade em análise
policies_under_analysis_review = []

# 
# método POST para solicitar análise de política de privacidade
# 
@api_view(['POST', ])
def request_url(request):
    if request.method == 'POST':

        # criação do id para 
        policy_under_analysis = AnalyticalReview()
        policy_under_analysis.id = datetime.now().strftime("%S.%f")

        # incluindo a análise na lista de políticas em análise
        policies_under_analysis_review.append(policy_under_analysis)

        #verifica se análise foi cancelada antes da próxima etapa 
        if(policy_under_analysis.cancel):
            cancel_policy_under_analysis(policy_under_analysis.id)
            return Response("")

        # etapa de extração de texto bruto do PDF ou HTML
        text = requestUrl.textExtractor(request.data['url'], policies_under_analysis_review.id)

        #verifica se análise foi cancelada antes da próxima etapa 
        if(policy_under_analysis.cancel):
            cancel_policy_under_analysis(policy_under_analysis.id)
            return Response("")

        return Response(summarizer.summarizerText(text))

#
# método para cancelar política de privacidade em análise em processamento
#
def cancel_policy_under_analysis(review_id):
    # recupera index pelo id informado
    policy_index = next((p for p in policies_under_analysis_review if p.id == review_id), -1)

    # verfica se o id informado existe
    if(policy_index != -1):
        # caso sim, remove o arquivo criado e da lista de políticas em análise
        requestUrl.removeFile(review_id)
        policies_under_analysis_review.pop(policy_index)


