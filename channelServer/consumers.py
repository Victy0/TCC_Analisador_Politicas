import json
import random
import random
import string
import time

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



# recuperar camada do channel
channel_layer = get_channel_layer()



# lista de sockets que não iniciaram processamento
sockets_connected_awaiting = []


#
# método para remover WebSocket da lista de sockets que não iniciaram processamento
#
def remove_sockets_connected_awaiting(sw_id, delete_ws):
    # remoção do id da lista de sockets
    if(sw_id in sockets_connected_awaiting):
        sockets_connected_awaiting.remove(sw_id)
    
    if delete_ws:
        disconnect_ws(sw_id)



#
# método para adicionar WebSocket na lista de sockets que não iniciaram processamento
#
def add_sockets_connected_awaiting(sw_id):
    # inclusão do id da lista de sockets
    sockets_connected_awaiting.append(sw_id)
    
    
    
#
# método para desconectar WebSocket
#
def disconnect_ws(sw_id):
    async_to_sync(channel_layer.group_discard)(sw_id, sw_id)
    
    
    
#
# classe de consumo do web socket
#
class WSConsumer(AsyncJsonWebsocketConsumer):
    # conectar WebSocket
    async def connect(self):
        # criação id
        sw_id = random.choice(string.ascii_letters) + str(round(time.time() * 1000)) + random.choice(string.ascii_letters)
        
        # inclusão em grupo (por hora grupo com apenas 1 id)
        await self.channel_layer.group_add(sw_id, self.channel_name)

        # conectar 
        await self.accept()
        print(sw_id + ": WEBSOCKET CONECTADO")
        
        # incluir WebSocket na lista de conectados e aguardando
        sockets_connected_awaiting.append(sw_id)
        
        # enviar mensagem indicando que está pronto para que seja chamada a API de processamento
        await self.send(text_data = json.dumps({
            'message': 'Pode iniciar processamento',
            'id': sw_id
        }))

    # desconectar WebSocket
    async def disconnect(self, sw_id):
        print(str(sw_id) + ": WEBSOCKET DESCONECTADO")

    # Enviar mensagem para grupo
    async def send_value_porcentage(self, event):
        # enviar mensagem para WebSocket
        await self.send(text_data=json.dumps({
            'message': "Atualização do processamento",
            'value': event['message']
        }))