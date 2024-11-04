import socket
import threading
import json
import logging

# Setup logging configuration
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

HOST = '0.0.0.0'
PORT = 65432

clients = [] 
game_state = [['' for _ in range(3)] for _ in range(3)]  
current_turn = 0  
player_ids = {}  
player_count = 0  

def broadcast(message, sender_conn=None):
    """Broadcast a message to all clients except the sender."""
    for client_conn, _ in clients:
        if client_conn != sender_conn:  
            try:
                client_conn.sendall(message)
            except Exception as e:
                logging.error(f"Error broadcasting to a client: {e}")

def broadcast_game_state():
    """Send the current game state to all connected clients."""
    state = {
        "type": "game_state",
        "board": game_state,
        "current_turn": current_turn,
    }
    message = json.dumps(state).encode('utf-8')
    broadcast(message)

def handle_client(conn, addr):
    global current_turn, player_count
    player_id = player_count  
    player_ids[conn] = player_id
    player_count += 1

    clients.append((conn, addr))
    
    conn.send(json.dumps({"type": "player_id", "player_id": player_id}).encode('utf-8'))
    logging.info(f"Player {player_id} ({addr}) connected.")
    print(f"[NEW CONNECTION] Player {player_id} connected from {addr}.")

    try:
        while True:
            message = conn.recv(1024).decode('utf-8')
            if not message:
                break
            msg_obj = json.loads(message)
            msg_type = msg_obj.get("type")
            msg_data = msg_obj.get("data")

            if msg_type == "join":
                
                conn.send(json.dumps({"type": "game_state", "board": game_state, "current_turn": current_turn}).encode('utf-8'))

            elif msg_type == "move" and player_id == current_turn:
                
                x, y = msg_data.get("x"), msg_data.get("y")
                if game_state[x][y] == '':
                    game_state[x][y] = 'X' if player_id == 0 else 'O'
                    current_turn = (current_turn + 1) % 2  
                    broadcast_game_state()
                else:
                    conn.send(json.dumps({"response": "Invalid move. Cell already occupied."}).encode('utf-8'))
                
            elif msg_type == "chat":
                broadcast_msg = json.dumps({"type": "chat", "from": f"Player {player_id}", "message": msg_data})
                broadcast(broadcast_msg.encode('utf-8'), conn)
                logging.info(f"Player {player_id} sent a chat message: {msg_data}")

            elif msg_type == "quit":
                conn.send(json.dumps({"response": "You have disconnected."}).encode('utf-8'))
                logging.info(f"Player {player_id} quit the game.")
                break

            else:
                conn.send(json.dumps({"response": "Unknown command or not your turn."}).encode('utf-8'))
                logging.warning(f"Unknown command from Player {player_id} or action not allowed.")
    except json.JSONDecodeError:
        conn.send(json.dumps({"response": "Invalid message format. Expected JSON."}).encode('utf-8'))
        logging.error(f"Invalid message format received from {addr}.")
    except ConnectionResetError:
        logging.error(f"Connection with {addr} was reset unexpectedly.")
        print(f"[ERROR] Connection with {addr} was reset unexpectedly.")
    except Exception as e:
        logging.error(f"Error occurred with {addr}: {e}")
        print(f"[ERROR] {e}")
    finally:
        # Cleanup on disconnection
        conn.close()
        clients.remove((conn, addr))
        del player_ids[conn]
        logging.info(f"Player {player_id} ({addr}) disconnected.")
        print(f"[DISCONNECTION] Player {player_id} disconnected from {addr}.")

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
