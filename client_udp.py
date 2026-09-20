import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = ('localhost', 9092)

print('UDP клиент')

while True:
    msg = input('UDP: ')
    if msg == 'exit':
        break
    sock.sendto(msg.encode(), server)
    sock.settimeout(2)
    try:
        data, _ = sock.recvfrom(1024)
        print(f'Ответ: {data.decode()}')
    except socket.timeout:
        print('Нет ответа (UDP сервер не запущен?)')

sock.close()