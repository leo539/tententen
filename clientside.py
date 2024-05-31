import socket
import pyaudio
import threading
import tkinter as tk
from tkinter import simpledialog

# Audio Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Server Configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

contacts = [("Recipient1", "127.0.0.1", 6000), ("Recipient2", "127.0.0.1", 6001)]

def send_audio(recipient_ip, recipient_port):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    client_socket.sendall(recipient_ip.encode('utf-8'))
    client_socket.sendall(str(recipient_port).encode('utf-8'))

    try:
        print("Recording and sending audio...")
        while talk_button_pressed:
            data = stream.read(CHUNK)
            client_socket.sendall(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()

def start_talking():
    global talk_button_pressed
    talk_button_pressed = True
    selected_contact = contacts_listbox.curselection()
    if selected_contact:
        recipient_name, recipient_ip, recipient_port = contacts[selected_contact[0]]
        threading.Thread(target=send_audio, args=(recipient_ip, recipient_port)).start()

def stop_talking():
    global talk_button_pressed
    talk_button_pressed = False

app = tk.Tk()
app.title("Audio Messenger")

contacts_listbox = tk.Listbox(app)
for contact in contacts:
    contacts_listbox.insert(tk.END, contact[0])
contacts_listbox.pack()

talk_button_pressed = False
talk_button = tk.Button(app, text="Talk", command=start_talking)
talk_button.pack()

stop_button = tk.Button(app, text="Stop", command=stop_talking)
stop_button.pack()

app.mainloop()
