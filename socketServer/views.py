import os
import socketio

async_mode = None
basedir = os.path.dirname(os.path.realpath(__file__))

# instanciar servidor socket io
sio = socketio.Server(async_mode=async_mode, cors_allowed_origins='*')
thread = None

# lista de sockets
sockets_connected = []

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
    sockets_connected.append(sid)
    print("Socket conectado: " + sid)
    
    # mensagem de conexão desnecessário, pois pode recuperar do id do próprio socket
    # deixando para caso seja necessário para outro sistema intregado posteriormente
    sio.emit('connect', {'id': sid}, room = sid)

#
# método para desconectar
#
@sio.event
def disconnect(sid):
    sockets_connected.remove(sid)
    print('Socket desconectado: ' + sid)

#
# método de envio de mensagem
#
@sio.event
def message_event(sid, message):
    sio.emit('mensagem', {'data': message}, room = sid)

#
# método para envio de mensagem em broadcast
#
@sio.event
def broadcast_message_event(sid, message):
    sio.emit('nome_do_evento', {'data': message})

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