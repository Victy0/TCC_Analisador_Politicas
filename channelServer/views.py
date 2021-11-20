import json
import random
import random
import string
import time

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from channelServer.consumers import sockets_connected_awaiting



#
# método para conectar manualmente (socket falso) para sistemas que não possuem portabilidade para socket
#
@api_view(['POST', ])
def connect_manual(request):

    data = {}

    # Verifica o tipo do método solicitado
    if request.method == 'POST':

        # criação do id
        sw_id = random.choice(string.ascii_letters) + str(round(time.time() * 1000)) + random.choice(string.ascii_letters)

        # inclusão do id na lista de sockets
        sockets_connected_awaiting.append(sw_id)
        print(sw_id + ": SOCKET MANUAL CONECTADO")

        # retorno de resposta
        data["success"] = True
        data["id"] = sw_id
        return Response(data)
    
    else:
        data["success"] = False
        data["error"] = "A rquisição precisa ser do tipo POST para que seja aceita"
        return Response(data = data, status = status.HTTP_400_BAD_REQUEST)
