# Créé par leo.braconnier, le 31/05/2024 en Python 3.7
import socket
import pyaudio
import threading

# Audio Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Client Configuration
RECEIVE_IP = '127.0.0.1'
RECEIVE_PORT = 6000

def receive_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((RECEIVE_IP, RECEIVE_PORT))
    server_socket.listen(1)
    print(f"Listening for audio on {RECEIVE_IP}:{RECEIVE_PORT}")

    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    try:
        while True:
            data = client_socket.recv(CHUNK)
            if not data:
                break
            stream.write(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    receive_audio()

