import socket
import threading

# Server Configuration
SERVER_IP = '0.0.0.0'
SERVER_PORT = 5000

clients = {}

def handle_client(client_socket):
    try:
        # Receive the recipient's IP and port
        recipient_ip = client_socket.recv(1024).decode('utf-8')
        recipient_port = int(client_socket.recv(1024).decode('utf-8'))

        if (recipient_ip, recipient_port) not in clients:
            clients[(recipient_ip, recipient_port)] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clients[(recipient_ip, recipient_port)].connect((recipient_ip, recipient_port))

        recipient_socket = clients[(recipient_ip, recipient_port)]
        print(f"Connected to recipient at {recipient_ip}:{recipient_port}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            recipient_socket.sendall(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print("Server listening on port", SERVER_PORT)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        client_handler = threading.Thread(
            target=handle_client,
            args=(client_socket,)
        )
        client_handler.start()

if __name__ == "__main__":
    server()
