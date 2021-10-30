from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from core.models import AnalyticalReview
from core.steps import requestUrl
from core.steps import summarizer
from core.steps import  estructurer

from socketServer.views import sockets_connected
from socketServer.views import disconnect



# lista de políticas de privacidade em análise
policies_under_analysis_review = []



# 
# método POST para análise de política de privacidade
# 
@api_view(['POST', ])
def process_analysis(request):
    # Verifica se contêm o parametro "url" e "id" no corpo da requisição
    if "url" in request.data and "id" in request.data:
        if request.method == 'POST':

            # instância da resposta do endpoint
            data = {}

            # verificação se id informado foi gerado pelo sistema
            if request.data['id'] not in sockets_connected:
                data["error"] = "Identificação de solicitação informada não corresponde a uma identificação do sistema"
                return Response(data=data)

            # criação da esturutura para análise
            policy_under_analysis = AnalyticalReview()
            policy_under_analysis.id = request.data['id']

            # incluindo a análise na lista de políticas em análise
            policies_under_analysis_review.append(policy_under_analysis)
            del policy_under_analysis

            # verifica se análise foi cancelada antes da próxima etapa 
            if(get_cancel_status(request.data['id'])):
                remove_policy_under_analysis(request.data['id'])
                return Response("")

            # etapa de extração de texto bruto do PDF ou HTML
            data['politica_generica'], text = requestUrl.text_extractor(request.data['url'], request.data['id'])

            # verificação se texto não é política de privacidade e retorno
            if text == "Sistema considerou o documento como não sendo uma política de privacidade":
                data["error"] = text
                return Response(data = data, status = status.HTTP_400_BAD_REQUEST)
            
            # verifica se análise foi cancelada antes da próxima etapa 
            if(get_cancel_status(request.data['id'])):
                remove_policy_under_analysis(request.data['id'])
                return Response("")
            
            # etapa de sumarização do texto bruto
            data = summarizer.summarizer_text(text, data)
            del text

            # verifica se análise foi cancelada antes da próxima etapa 
            if(get_cancel_status(request.data['id'])):
                remove_policy_under_analysis(request.data['id'])
                return Response("")
        
            # etapa de sinalização do texto sumarizado
            data = estructurer.sinalize(data)

            remove_policy_under_analysis(request.data['id'])
            
            # retorno de resposta
            return Response(data)
    else:
        #formatação de mensagem de erro
        message_complement = ("'id'" if ("id" not in request.data) else "") + ("'url'" if ("url" not in request.data) else "")
        message_complement = (message_complement[0: 4] + " e " + message_complement[4:]) if len(message_complement) > 6 else message_complement

        data = {}
        data["error"] = "Falta do parâmetro " + message_complement + " no corpo da requisição"
        return Response(data = data, status = status.HTTP_400_BAD_REQUEST)



#
# método para remover definitivamente política de privacidade em análise em processamento
#
def remove_policy_under_analysis(review_id):
    # recupera index pelo id informado
    policy_index = next((i for i, policy in enumerate(policies_under_analysis_review) if policy.id == review_id), -1)

    # verifica se o id informado existe
    if(policy_index != -1):
        # caso sim, remove o arquivo criado e da lista de políticas em análise
        requestUrl.remove_file(review_id + '.pdf')
        policies_under_analysis_review.pop(policy_index)

        # desconectar socket
        disconnect(review_id)


#
#
#
def get_cancel_status(review_id):
    # recupera index pelo id informado
    policy_review = next((p for p in policies_under_analysis_review if p.id == review_id), -1)

    return policy_review.cancel



# 
# método POST para solicitar cancelamento de análise de política de privacidade
# 
@api_view(['POST', ])
def cancel_analysis(request):
    # Verifica se contêm o parametro "id" no corpo da requisição
    if "id" in request.data:
        if request.method == 'POST':

            # recupera index pelo id informado
            policy_index = next((i for i, policy in enumerate(policies_under_analysis_review) if policy.id == request.data['id']), -1)

            # verifica se o id informado existe
            if(policy_index != -1):
                # caso sim, seta como cancelado na lista de políticas de privacidade em análise
                policies_under_analysis_review[policy_index].cancel = True

            # TODO verificar o retorno
            return Response(True)
    else:
        data = {}
        data["error"] = "Falta do parâmetro 'id' no corpo da requisição"
        return Response(data = data, status = status.HTTP_400_BAD_REQUEST)       