import socket
import selectors
from cryptography.fernet import Fernet

KEY = 'SGWXy9pdgbE_MhGFRr3NfxMchblC3Acl9dW-_ogwvYA='
cipher = Fernet(KEY.encode())
selector = selectors.DefaultSelector()
clients = {}
server_running = True


def encrypt(msg):
    return cipher.encrypt(msg.encode())


def decrypt(data):
    return cipher.decrypt(data).decode()


def accept(sock):
    client_sock, addr = sock.accept()
    print(f'Клиент {addr} подключен')
    client_sock.setblocking(False)
    clients[client_sock] = addr
    selector.register(client_sock, selectors.EVENT_READ, read)


def read(client_sock):
    try:
        data = client_sock.recv(4096)
        if not data:
            disconnect(client_sock)
            return

        msg = decrypt(data)
        addr = clients[client_sock]
        print(f'{addr}: {msg}')

        if msg.lower() == 'shutdown':
            print('Сервер выключается...')
            shutdown_server()
            return

        for sock in clients:
            if sock != client_sock:
                sock.sendall(encrypt(f'{addr}: {msg}'))
    except:
        disconnect(client_sock)


def disconnect(client_sock):
    addr = clients.pop(client_sock, None)
    if addr:
        print(f'Клиент {addr} отключен')
        selector.unregister(client_sock)
        client_sock.close()


def shutdown_server():
    global server_running
    server_running = False
    for sock in list(clients.keys()):
        try:
            sock.sendall(encrypt('Сервер выключен'))
        except:
            pass
        disconnect(sock)
    selector.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9095))
    server.listen()
    server.setblocking(False)
    selector.register(server, selectors.EVENT_READ, accept)
    print('Сервер на порту 9095')

    while server_running:
        events = selector.select(timeout=1)
        for key, _ in events:
            key.data(key.fileobj)

    server.close()
    print('Сервер остановлен')


if __name__ == '__main__':
    start_server()