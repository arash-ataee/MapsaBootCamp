import socket
import time
import select

IP = 'localhost'
PORT = 8218

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((IP, PORT))

server_socket.listen(10)
print("server up!")

socket_list = [server_socket]

clients = {}
audiences = {}


while True:
    read_socket, write_socket, exception_socket = select.select(
        socket_list, [], socket_list)
    for s in read_socket:
        if s == server_socket:
            client_socket, address = server_socket.accept()
            if client_socket:
                # client_socket.send(bytes("welcome!", 'utf-8'))
                socket_list.append(client_socket)
                username = client_socket.recv(1024).decode('utf-8')
                print(username)
                while username in clients:
                    client_socket.send(bytes('error1'))
                    username = client_socket.recv(1024)
                client_socket.send(bytes('accepted1', 'utf-8'))
                clients[username] = client_socket
                print("Connection Established from {}".format(address))
                audience = None
                while not audience:
                    try:
                        while not audience:
                            audience = client_socket.recv(1024).decode('utf-8')
                    except IOError as e:
                        pass
                    if audience not in clients:
                        client_socket.send(bytes('error2', 'utf-8'))
                        audience = None
                client_socket.send(bytes('error2', 'utf-8'))

                audiences[client_socket] = audience
                audiences[audience] = client_socket
                continue


        else:
            message = s.recv(1024)
            print(message)
            if not message:
                socket_list.remove(s)
                del clients[s]
                continue
            audiences[audiences[s]].send(message)
    for s in exception_socket:
        socket_list.remove(s)
        del clients[s]
        del audiences[s]
        del audiences[audiences[s]]
    # print(socket_list)
# server_socket.close()
