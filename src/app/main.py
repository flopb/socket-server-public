#!/usr/bin/env python
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect, Namespace

from flask_cors import CORS

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "eventlet"

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, async_mode=async_mode, engineio_logger=False, origins='*', cors_allowed_origins="*")

app.config['CORS_SUPPORTS_CREDENTIALS'] = True
CORS(app, resources={r"/*": {"origins": "*"}}, automatic_options=True)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/send')
def send():
    message = request.args.get("msg")
    room = request.args.get("room")
    session['receive_count'] = session.get('receive_count', 0) + 1
    socketio.emit('my_response',
                  {'data': message, 'count': session['receive_count']},
                  room=room)
    return "ok"


@socketio.on('notification', namespace='/')
def notification(message):
    emit('notification', message, room=message['room'])

@socketio.on('command', namespace='/')
def command(payload):
    emit('command', payload, room=payload['room'])

@socketio.on('my_event', namespace='/')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': 1})



@socketio.on('leave', namespace='/')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])

@socketio.on('disconnect_request', namespace='/')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('my_ping', namespace='/')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/')
def test_connect():
    global thread
    emit('my_response', {'data': 'Connected', 'count': 0})
    emit('command', {'command': 'fireEvent', 'args': {"eventname": "SIOConnected", "eventdata": {}}})


@socketio.on('disconnect', namespace='/')
def test_disconnect():
    print('Client disconnected', request.sid)




if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
