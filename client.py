import socket

def send_request(method, path, body=None):
    # 서버 주소와 포트 번호 설정
    server_address = ('localhost', 9010)

    # 서버에 연결
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    # HTTP 요청 생성
    request_parts = [f'{method} {path} HTTP/1.1', f'Host: localhost']

    # POST나 PUT 메소드인 경우 body를 요청에 추가
    if method in ['POST', 'PUT']:
        if body:
            request_parts.append(f'Content-Length: {len(body)}')
        request_parts.append('Content-Type: text/plain')
    
    request_parts.append('')
    if body:
        request_parts.append(body)

    request = '\r\n'.join(request_parts)

    client_socket.sendall(request.encode())

    # 서버로부터 응답을 수신
    response = client_socket.recv(1024).decode()

    # 수신된 응답을 출력
    print(f'{method} 요청 결과:', response)

    # 서버와의 연결 닫기
    client_socket.close()

# GET method - 200 OK
send_request('GET', '/')

# GET method - 404 Not Found
send_request('GET', '/nonexistent-page')

# HEAD method - 200 OK
send_request('HEAD', '/')

# POST method - 200 OK
post_content = 'This is a POST request.'
send_request('POST', '/new-resource', post_content)

# POST method - 400 Bad Request
send_request('POST', '/new-resource')

# PUT method - 201 Created
put_content = 'This is a PUT request.'
send_request('PUT', '/existing-resource', put_content)

# PUT method - 409 Conflict
send_request('PUT', '/existing-resource', put_content)
