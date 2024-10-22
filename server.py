import socket  # network communication
import threading  # handling messages
import os  # interacting with file paths and sizes


def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')  # receives a message of max 1024 bytes and decodes it
        if message == 'FILE':
            file_name = client_socket.recv(1024).decode('utf-8')  # receiving the filename
            file_size = int(client_socket.recv(1024).decode('utf-8'))  # receving the file size
            with open(file_name, 'wb') as file:
                data = client_socket.recv(file_size)
                file.write(data)  # opens a new file on the server and writes the data to it
            print(f"Received file: {file_name}")
        else:
            print(f"Client: {message}")


def send_message(client_socket):
    while True:
        message = input("Enter message or type 'sendfile' to send a file: ")
        if message == 'sendfile':
            client_socket.send('FILE'.encode('utf-8'))  # sending a file command
            file_path = input("Enter file path to send: ")
            file_name = os.path.basename(file_path)  # setting the file name
            file_size = os.path.getsize(file_path)  # setting the file size
            client_socket.send(file_name.encode('utf-8'))  # sending the file name
            client_socket.send(str(file_size).encode('utf-8'))  # sending the file size
            with open(file_path, 'rb') as file:  # reading the file in binary mode
                client_socket.send(file.read())  # sending file to client
            print("File successfully sent")
        else:
            client_socket.send(message.encode('utf-8'))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a socket
server.bind(('0.0.0.0', 12345))  # binding the server to 12345
server.listen(1)  # having the server listen for any messages
print("Server listening on port 12345....")

client_socket, addr = server.accept()  # accepting connection with client
print(f"Connection established with {addr}")

received_thread = threading.Thread(target=handle_client, args=(client_socket,))  # starting a new thread to handle client messages
received_thread.start()

send_thread = threading.Thread(target=send_message, args=(client_socket,))  # starting a new thread to send messages to the client
send_thread.start()