import socket
import time
import select

IP = '192.168.1.52'
PORT = 8222

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))

server_socket.listen(10)
print("server up!")

socket_list = [server_socket]

clients = {}
audiences = {}

while True:
    read_socket, write_socket, exception_socket = select.select(
        socket_list, socket_list, socket_list)
    print('read', read_socket)
    print('write', write_socket)
    for s in read_socket:
        if s == server_socket:
            client_socket, address = server_socket.accept()
            if client_socket:
                # client_socket.send(bytes("welcome!", 'utf-8'))
                socket_list.append(client_socket)
                print("Connection Established from {}".format(address))
    print('read', read_socket)
    print('write', write_socket)
    for s in read_socket:
        if s not in clients.values():
            username = None
            try:
                username = s.recv(1024).decode('utf-8')
            except IOError:
                continue
            if username:
                if username in clients:
                    s.send(bytes('error1', 'utf-8'))
                if username not in clients:
                    s.send(bytes('accept1', 'utf-8'))
                    clients[username] = s
                    names = ''
                    for name in list(clients.keys()):
                        names += name + ' '
                    s.send(bytes(names, 'utf-8'))
                    print(clients)
                    print(audiences)
        else:
            message = None
            try:
                message = s.recv(1024).decode('utf-8')
            except IOError:
                continue
            if message:
                if message.startswith('adnc'):
                    audience = message[4:]
                    if audience in audiences:
                        s.send(bytes('error2', 'utf-8'))
                        message = None
                    else:
                        s.send(bytes('accept2', 'utf-8'))
                        audiences[s] = audience
                        audiences[audience] = s
                        message = None
                if message:
                    print(message)
                    if not message:
                        socket_list.remove(s)
                    clients[audiences[s]].send(bytes(list(clients.keys())[list(clients.values()).index(s)] + ': ' +
                                                     message + '\n', 'utf-8'))

    for s in exception_socket:
        socket_list.remove(s)
        del clients[s]
        del audiences[audiences[s]]
        del audiences[s]

    time.sleep(1)
    # print(socket_list)
# server_socket.close()
