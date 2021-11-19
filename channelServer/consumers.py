import json
import random
import random
import string
import time

from channels.generic.websocket import AsyncJsonWebsocketConsumer


# lista de sockets que não iniciaram processamento
sockets_connected_awaiting = []


#
# método para remover socket da lista de sockets que não iniciaram processamento
#
def remove_sockets_connected_awaiting(socket_id):
    # remoção do id da lista de sockets
    sockets_connected_awaiting.remove(socket_id)



#
# método para adicionar socket na lista de sockets que não iniciaram processamento
#
def add_sockets_connected_awaiting(socket_id):
    # inclusão do id da lista de sockets
    sockets_connected_awaiting.append(socket_id)
    
    
    
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
            'message': 'Pode iniciar processamento'
        }))

    # desconectar WebSocket
    async def disconnect(self, sw_id):
        await self.channel_layer.group_discard(sw_id, self.channel_name)
        print(sw_id + ": WEBSOCKET DESCONECTADO")

    # Enviar mensagem para grupo
    async def send_data(self, event):
        # enviar mensagem para WebSocket
        await self.send(text_data=json.dumps({
            'message': event['text']
        }))