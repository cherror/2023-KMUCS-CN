import socket

# 서버 소켓을 생성합니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 주소와 포트 번호를 설정합니다.
server_address = ('localhost', 9010)

# 서버 소켓을 지정된 주소와 포트에 바인딩합니다.
server_socket.bind(server_address)

# 클라이언트의 연결을 기다립니다.
server_socket.listen(1)

print('서버가 시작되었습니다. 클라이언트의 연결을 기다립니다...')

while True:
    # 클라이언트의 연결을 수락합니다.
    client_socket, client_address = server_socket.accept()
    print('클라이언트가 연결되었습니다:', client_address)

    # 클라이언트로부터 데이터를 수신합니다.
    data = client_socket.recv(1024).decode()

    # 수신된 데이터를 처리합니다.
    # TODO: 요청에 따라 적절한 응답을 구성합니다.

    # 클라이언트에 응답을 전송합니다.
    response = 'HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello World!'
    client_socket.sendall(response.encode())

    # 클라이언트와의 연결을 닫습니다.
    client_socket.close()

# 서버 소켓을 닫습니다.
server_socket.close()
