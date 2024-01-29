import socket
import ssl

public_ips = ['x.x.x.x']  # replace with your list of public IPs
# enter your own service library
services = {
    '21': 'FTP',
    '25': 'SMTP',
    '80': 'HTTP',
    '443': 'HTTPS'
}

def check_port(ip, port, service):
    try:
        with socket.create_connection((ip, port), timeout=5) as sock:
            if service == 'HTTP':
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                if b"HTTP" in sock.recv(100):
                    print(f'{ip}: Port {port} running HTTP')
            elif service == 'HTTPS':
                context = ssl.create_default_context()  # Using SSLContext
                with context.wrap_socket(sock, server_hostname=ip) as ssock:
                    ssock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    if b"HTTP" in ssock.recv(100):
                        print(f'{ip}: Port {port} running HTTPS')
            elif service == 'SMTP':
                response = sock.recv(100)
                if b"SMTP" in response or b"220" in response:
                    print(f'{ip}: Port {port} running SMTP')
            elif service == 'FTP':
                response = sock.recv(100)
                if b"FTP" in response or b"220" in response:
                    print(f'{ip}: Port {port} running FTP')
            else:
                print(f'{ip}: Port {port} open, service unknown')
    except (socket.timeout, socket.error, ssl.SSLError) as e:
        print(f'{ip}: Port {port} check failed - {e}')

for ip in public_ips:
    for port, service in services.items():
        check_port(ip, int(port), service)
