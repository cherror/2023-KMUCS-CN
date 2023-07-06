import socket
import datetime
import os

def send_response(client_socket, response):
    client_socket.sendall(response.encode())

def read_file(path):
    try:
        with open(path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return None

def generate_html(content):
    html = f'''
    <html>
    <head>
        <title>Server Response</title>
    </head>
    <body>
        <h1>{content}</h1>
    </body>
    </html>
    '''
    return html

def handle_request(client_socket, request):
    request_lines = request.split('\r\n')
    method, path, _ = request_lines[0].split()

    if method == 'GET':
        if path == '/':
            content = 'Hello, World!'
            response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\nDate: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\r\n\r\n{content}'
        else:
            file_content = read_file(path[1:])  # Remove leading '/'
            if file_content is not None:
                content = generate_html(file_content)
                response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\nDate: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\r\n\r\n{content}'
            else:
                response = 'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n'
    elif method == 'POST':
        content_length = None
        for line in request_lines:
            if line.startswith('Content-Length:'):
                content_length = int(line.split()[1])
                break
        
        if content_length is None:
            response = 'HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n'
        else:
            body = request.split('\r\n\r\n')[1]
            if len(body) == content_length:
                response = f'HTTP/1.1 201 Created\r\nLocation: /new-resource\r\nContent-Length: 0\r\nDate: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\r\n'
            else:
                response = 'HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n'
    elif method == 'PUT':
        content_length = None
        for line in request_lines:
            if line.startswith('Content-Length:'):
                content_length = int(line.split()[1])
                break
        
        if content_length is None:
            response = 'HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n'
        else:
            body = request.split('\r\n\r\n')[1]
            if len(body) == content_length:
                response = f'HTTP/1.1 200 OK\r\nContent-Length: 0\r\nDate: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\r\n'
            else:
                response = 'HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n'
    elif method == 'HEAD':
        if path == '/':
            content = ''
            response = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nDate: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\r\n\r\n'
        else:
            file_content = read_file(path[1:])  # Remove leading '/'
            if file_content is not None:
                content = ''
                response = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nDate: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\r\n\r\n'
            else:
                response = 'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n'
    else:
        response = 'HTTP/1.1 501 Not Implemented\r\nContent-Length: 0\r\n'

    send_response(client_socket, response)

# 서버 소켓을 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 주소와 포트 번호를 설정
server_address = ('localhost', 9010)

# 서버 소켓을 지정된 주소와 포트에 바인딩
server_socket.bind(server_address)

# 클라이언트의 연결 대기
server_socket.listen(1)

print('서버가 시작되었습니다. 클라이언트의 연결을 기다립니다...')

while True:
    # 클라이언트의 연결 수락
    client_socket, client_address = server_socket.accept()
    print('클라이언트가 연결되었습니다:', client_address)

    # 클라이언트로부터 데이터를 수신
    data = client_socket.recv(1024).decode()

    # 수신된 데이터를 처리
    handle_request(client_socket, data)

    # 클라이언트와의 연결 종료
    client_socket.close()

# 서버 소켓 종료
server_socket.close()
