import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 53000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

clients = []
lock = threading.Lock()

def broadcast_message(message, sender_socket):
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except socket.error:
                    # Gestisci errore di connessione
                    print("Errore durante l'invio a un client")
                    clients.remove(client)

def handle_client(client_socket):
    print("Un client si è connesso")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                # Se il messaggio è vuoto, chiudi la connessione
                raise socket.error("Connessione chiusa dal client")
            broadcast_message(message, client_socket)
        except socket.error:
            # Gestisci errore di connessione o ricezione
            print("Connessione chiusa dal client")
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    print(f"Server avviato su {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        client_socket, _ = server_socket.accept()
        with lock:
            clients.append(client_socket)
        # Affidamento della gestione delle comunicazioni post connessione ad un thread per
        # liberare il main thread da busy duty
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
