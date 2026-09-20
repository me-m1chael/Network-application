import socket
import threading
from cryptography.fernet import Fernet

KEY = 'SGWXy9pdgbE_MhGFRr3NfxMchblC3Acl9dW-_ogwvYA='
cipher = Fernet(KEY.encode())

def encrypt(msg):
    return cipher.encrypt(msg.encode())

def decrypt(data):
    return cipher.decrypt(data).decode()

def receive(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            print(f'\n{decrypt(data)}')
            print('Вы: ', end='', flush=True)
        except:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9095))
print('Подключен. exit - выход, shutdown - выключить сервер')

threading.Thread(target=receive, args=(sock,), daemon=True).start()

while True:
    msg = input('Вы: ')
    if msg.lower() == 'exit':
        break
    sock.sendall(encrypt(msg))

sock.close()