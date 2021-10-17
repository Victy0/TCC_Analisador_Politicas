from django.shortcuts import render
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from core.models import AnalyticalReview
from core.steps import requestUrl
from core.steps import summarizer
from core.steps import  estructurer



# lista de políticas de privacidade em análise
policies_under_analysis_review = []



# 
# método POST para análise de política de privacidade
# 
@api_view(['POST', ])
def start_analysis(request):
    # Verifica se  contem o parametro "url" no corpo da requisição
    if "url" in request.data:
        if request.method == 'POST':

            # criação da esturutura e id da política de privacidade solicitada para análise
            policy_under_analysis = AnalyticalReview()
            policy_under_analysis.id = datetime.now().strftime("%S.%f")

            # incluindo a análise na lista de políticas em análise
            policies_under_analysis_review.append(policy_under_analysis)

            # verifica se análise foi cancelada antes da próxima etapa 
            if(policy_under_analysis.cancel):
                cancel_policy_under_analysis(policy_under_analysis.id)
                return Response("")

            # etapa de extração de texto bruto do PDF ou HTML
            text = requestUrl.textExtractor(request.data['url'], policy_under_analysis.id)
            
            if text == "Documento não é uma politica de privacidade":
                data={}
                data["error"]=text
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            # verifica se análise foi cancelada antes da próxima etapa 
            if(policy_under_analysis.cancel):
                cancel_policy_under_analysis(policy_under_analysis.id)
                return Response("")

            # etapa de sumarização do texto bruto
            text = summarizer.summarizer_text(text)
        
            text = estructurer.Sinalize(text)
            return Response(text)
    else:
        data={}
        data["error"]="Falta do parametro url no corpo da requisição"
        return Response(data=data,status=status.HTTP_400_BAD_REQUEST)



#
# método para cancelar política de privacidade em análise em processamento
#
def cancel_policy_under_analysis(review_id):
    # recupera index pelo id informado
    policy_index = next((p for p in policies_under_analysis_review if p.id == review_id), -1)

    # verifica se o id informado existe
    if(policy_index != -1):
        # caso sim, remove o arquivo criado e da lista de políticas em análise
        requestUrl.removeFile(review_id + '.pdf')
        policies_under_analysis_review.pop(policy_index)




# 
# método POST para análise de política de privacidade
# 
@api_view(['POST', ])
def cancel_analysis(request):
    # Verifica se  contem o parametro "id" no corpo da requisição
    if "id" in request.data:
        if request.method == 'POST':

            # recupera index pelo id informado
            policy_index = next((p for p in policies_under_analysis_review if p.id == request.data['id']), -1)

            # verifica se o id informado existe
            if(policy_index != -1):
                # caso sim, seta como cancelado na lista de políticas de privacidade em análise
                policies_under_analysis_review[policy_index].cancel = True

            # TODO verificar o retorno
            return Response(True)
    else:
        data={}
        data["error"]="Falta do parametro id no corpo da requisição"
        return Response(data=data,status=status.HTTP_400_BAD_REQUEST)       