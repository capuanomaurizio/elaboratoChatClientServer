import socket
import threading
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 53000

def receive_messages(client_socket):
    while True:
        try:
            # Ricezione dei messaggi dal server
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                raise socket.error("Connessione chiusa dal server")
            print(message)
        except socket.error:
            print("Connessione chiusa")
            client_socket.close()
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Enstabilishment della connessione
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Sei connesso alla chatroom ospitata da {SERVER_HOST}:{SERVER_PORT}")
        print("Per terminare la comunicazione, scrivere 'esci'")
    except socket.error:
        print("Errore durante la connessione al server")
        sys.exit(1)

    # Affidamento della gestione delle comunicazioni post connessione ad un thread per
    # liberare il main thread da busy duty
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    print("I messaggi che invierai saranno visibili agli altri client connessi")
    # Loop per la gestione dell'invio dei messaggi
    while True:
        message = input()
        if message.lower() == 'esci':
            break
        try:
            # Invio del messaggio al server che lo inoltrera' poi agli altri client
            client_socket.sendall(message.encode('utf-8'))
        except socket.error:
            print("Errore durante l'invio del messaggio")
            client_socket.close()
            break
        
    # Chisura la connessione
    client_socket.close()

if __name__ == "__main__":
    start_client()
