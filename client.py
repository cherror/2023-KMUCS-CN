import socket

# 서버 주소와 포트 번호 설정
server_address = ('localhost', 9010)

# 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# HTTP GET 요청
request = 'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n'
client_socket.sendall(request.encode())

# 서버로부터 응답을 수신
response = client_socket.recv(1024).decode()

# 수신된 응답을 출력
print('서버 응답:', response)

# 서버와의 연결 닫기
client_socket.close()
