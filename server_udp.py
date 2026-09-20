import socket

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('localhost', 9092))
print('UDP сервер на порту 9092')

while True:
    data, addr = udp_socket.recvfrom(1024)
    print(f'UDP от {addr}: {data.decode()}')
    udp_socket.sendto(f'Эхо: {data.decode()}'.encode(), addr)