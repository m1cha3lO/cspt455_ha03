import socket  # network communication
import threading  # handling messages
import os  # interacting with file paths and sizes


def handle_server(server_socket):
    while True:
        message = server_socket.recv(1024).decode('utf-8')  # receives a message of max 1024 bytes and decodes it
        if message == 'FILE':
            file_name = server_socket.recv(1024).decode('utf-8')  # receiving the filename
            file_size = int(server_socket.recv(1024).decode('utf-8'))  # receving the file size
            with open(file_name, 'wb') as file:
                data = server_socket.recv(file_size)
                file.write(data)  # opens a new file on the client and writes the data to it
            print(f"Received file: {file_name}")
        else:
            print(f"Server: {message}")


def send_message(server_socket):
    while True:
        message = input("Enter message or type 'sendfile' to send a file: ")
        if message == 'sendfile':
            server_socket.send('FILE'.encode('utf-8'))  # sending a file command
            file_path = input("Enter file path to send: ")
            file_name = os.path.basename(file_path)  # setting the file name
            file_size = os.path.getsize(file_path)  # setting the file size
            server_socket.send(file_name.encode('utf-8'))  # sending the file name
            server_socket.send(str(file_size).encode('utf-8'))  # sending the file size
            with open(file_path, 'rb') as file:  # reading the file in binary mode
                server_socket.send(file.read())  # sending file to client
            print("File successfully sent")
        else:
            server_socket.send(message.encode('utf-8'))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a socket
server_socket.connect(('127.0.0.1', 12345))  # binding the server to 12345
print("Successfully connected to the server")

received_thread = threading.Thread(target=handle_server, args=(server_socket,))  # starting a new thread to handle server messages
received_thread.start()
send_thread = threading.Thread(target=send_message, args=(server_socket,))  # starting a new thread to send messages to the server
send_thread.start()