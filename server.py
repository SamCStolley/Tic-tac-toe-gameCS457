import socket
import threading

# Server parameters
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

# Function to handle client connections
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        try:
            # Receiving a message from the client
            message = conn.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[{addr}] {message}")
            # Sending back the same message (echo)
            conn.send(f"Server received: {message}".encode('utf-8'))
        except ConnectionResetError:
            print(f"[ERROR] Connection with {addr} was reset unexpectedly.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            break

    conn.close()
    print(f"[DISCONNECTION] {addr} disconnected.")

# Main function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()  # Accept client connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
