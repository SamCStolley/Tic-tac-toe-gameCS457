import socket
import threading
import json
import logging

# Setup logging configuration
logging.basicConfig(
    filename='server.log',        # Log file name
    level=logging.INFO,           # Log level (can be DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Server parameters
HOST = '127.0.0.1'
PORT = 65432

# Global list to track connected clients
clients = []

# Function to broadcast a message to all clients
def broadcast(message, sender_conn=None):
    for client in clients:
        conn, addr = client
        if conn != sender_conn:  # Don't send the message to the sender itself
            conn.sendall(message)

# Function to handle client messages and game protocol
def handle_client(conn, addr):
    logging.info(f"New connection from {addr}")
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append((conn, addr))

    waiting = True  # Initial state: waiting room

    while waiting:
        try:
            message = conn.recv(1024).decode('utf-8')
            if not message:
                break

            # Parse the incoming message (expected in JSON format)
            try:
                msg_obj = json.loads(message)
                msg_type = msg_obj.get("type")
                msg_data = msg_obj.get("data")

                logging.info(f"Message from {addr}: Type={msg_type}, Data={msg_data}")

                if msg_type == "join":
                    conn.send(json.dumps({"response": "You have joined the game lobby."}).encode('utf-8'))
                    logging.info(f"{addr} joined the game lobby.")
                    waiting = False  # Transition to the game when joined

                elif msg_type == "chat":
                    broadcast_msg = json.dumps({"type": "chat", "from": str(addr), "message": msg_data})
                    broadcast(broadcast_msg.encode('utf-8'), conn)
                    logging.info(f"{addr} sent a chat message: {msg_data}")

                elif msg_type == "move":
                    # This would normally handle a move in the game
                    conn.send(json.dumps({"response": f"Move registered: {msg_data}"}).encode('utf-8'))
                    logging.info(f"{addr} made a move: {msg_data}")

                elif msg_type == "quit":
                    conn.send(json.dumps({"response": "You have disconnected."}).encode('utf-8'))
                    logging.info(f"{addr} quit the game.")
                    break

                else:
                    conn.send(json.dumps({"response": "Unknown command. Please try again."}).encode('utf-8'))
                    logging.warning(f"Unknown command from {addr}: {msg_type}")

            except json.JSONDecodeError:
                conn.send(json.dumps({"response": "Invalid message format. Expected JSON."}).encode('utf-8'))
                logging.error(f"Invalid message format received from {addr}.")

        except ConnectionResetError:
            logging.error(f"Connection with {addr} was reset unexpectedly.")
            print(f"[ERROR] Connection with {addr} was reset unexpectedly.")
            break
        except Exception as e:
            logging.error(f"Error occurred with {addr}: {e}")
            print(f"[ERROR] {e}")
            break

    # Cleanup on disconnection
    conn.close()
    clients.remove((conn, addr))
    logging.info(f"{addr} disconnected.")
    print(f"[DISCONNECTION] {addr} disconnected.")

# Main function to start the server
def start_server():
    logging.info("Starting the server.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    logging.info(f"Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        logging.info(f"New thread started for {addr}. Active connections: {threading.active_count() - 1}")
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
