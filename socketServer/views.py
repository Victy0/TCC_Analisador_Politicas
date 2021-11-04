import os
import random
import socketio
import string
import time

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



async_mode = None
basedir = os.path.dirname(os.path.realpath(__file__))

# instanciar servidor socket io
sio = socketio.Server(async_mode=async_mode, cors_allowed_origins='*')
thread = None



# lista de sockets que não iniciaram processamento
sockets_connected_awaiting = []



#
# método de localização de threads (talvez será excluído)
#
def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return ""



#
# thread em background (talvez será excluído)
#
def background_thread():
    # Exemplo de como enviar eventos gerados pelo server para cliente
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('nome_do_evento', {'data': 'Server generated event'}, namespace='/test')



#
# método para conectar
#
@sio.event
def connect(sid, environ):

    # inclusão do id na lista de sockets
    sockets_connected_awaiting.append(sid)
    print("Socket conectado: " + sid)
    
    # mensagem de conexão desnecessário, pois pode recuperar do id do próprio socket
    # deixando para caso seja necessário para outro sistema intregado posteriormente
    sio.emit('connect', {'id': sid}, room = sid)



#
# método para conectar manualmente (socket falso) para sistemas que não possuem portabilidade para socket
#
@api_view(['POST', ])
def connect_manual(request):

    data = {}

    # Verifica o tipo do método solicitado
    if request.method == 'POST':

        # criação do id
        sid = random.choice(string.ascii_letters) + str(round(time.time() * 1000)) + random.choice(string.ascii_letters)

        # inclusão do id na lista de sockets
        sockets_connected_awaiting.append(sid)
        print("Socket manual conectado: " + sid)

        # retorno de resposta
        data["sucess"] = True
        data["id"] = sid
        return Response(data)
    
    else:
        data["sucess"] = False
        data["error"] = "A rquisição precisa ser do tipo POST para que seja aceita"
        return Response(data = data, status = status.HTTP_400_BAD_REQUEST)



#
# método para desconectar socket
#
@sio.event
def disconnect(sid):

    # remoção do id da lista de sockets que não iniciaram processamento se estiver
    if sid in sockets_connected_awaiting:    
        sockets_connected_awaiting.remove(sid)

    print('Socket desconectado: ' + sid)



#
# método para remover socket da lista de sockets que não iniciaram processamento
#
def remove_sockets_connected_awaiting(socket_id):

    # remoção do id da lista de sockets
    sockets_connected_awaiting.remove(socket_id)



#
# método de envio de mensagem
#
@sio.event
def message_event(sid, message):

    # envio de mensagem pelo socket 
    sio.emit('mensagem', {'data': message}, room = sid)



#
# método para envio de mensagem em broadcast
#
@sio.event
def broadcast_message_event(sid, message):

    # envio de mensagem para todos os sockets
    sio.emit('broadcast', {'data': message})

#################################################### daqui para baixo provavel que não será usado na primeira versão ####################################################

#
# método para entrar numa sala (talvez não será usada)
#
@sio.event
def join(sid, message):
    sio.enter_room(sid, message['room'])
    sio.emit('nome_do_evento', {'data': 'Entered room: ' + message['room']}, room=sid)

#
# método para sair de uma sala (talvez não será usada)
#
@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit('nome_do_evento', {'data': 'Left room: ' + message['room']}, room=sid)

#
# método para fechar sala (talvez não será usada)
#
@sio.event
def close_room(sid, message):
    sio.emit('nome_do_evento', {'data': 'Room ' + message['room'] + ' is closing.'}, room=message['room'])
    sio.close_room(message['room'])

#
# método para evento dentro de sala (talvez não será usada)
#
@sio.event
def room_event(sid, message):
    sio.emit('nome_do_evento', {'data': message['data']}, room=message['room'])

#
# método para solicitação de desconexão (talvez não será usada)
#
@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)