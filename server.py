import socket
import threading
import json
import logging

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Prompt the user for host and port at startup
HOST = input("Enter the host address (e.g., 127.0.0.1): ").strip()
PORT = int(input("Enter the port number (e.g., 65432): ").strip())

clients = []
game_board = [" " for _ in range(9)]
current_turn = 0  # Tracks whose turn it is (0 for Player 1, 1 for Player 2)

# Broadcast a message to all clients
def broadcast(message):
    for conn, _ in clients:
        conn.sendall(message)

# Check for win or draw conditions
def check_game_status():
    win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]
    for a, b, c in win_combinations:
        if game_board[a] == game_board[b] == game_board[c] != " ":
            return game_board[a]  # Return the winning symbol
    if " " not in game_board:
        return "Draw"
    return None

# Handle client moves and game updates
def handle_client(conn, player_id):
    global current_turn, game_board
    conn.send(json.dumps({"player_id": player_id}).encode('utf-8'))

    # Start the game once two players are connected
    if len(clients) == 2:
        broadcast(json.dumps({"type": "start_game", "current_turn": current_turn}).encode('utf-8'))

    while True:
        try:
            message = conn.recv(1024).decode('utf-8').strip()
            if not message:
                break
            
            msg_obj = json.loads(message)
            msg_type = msg_obj.get("type")
            msg_data = msg_obj.get("data")

            if msg_type == "move" and int(player_id) == current_turn:
                move = int(msg_data)
                if game_board[move] == " ":
                    game_board[move] = "X" if current_turn == 0 else "O"
                    winner = check_game_status()

                    if winner:
                        broadcast(json.dumps({"type": "game_over", "winner": winner, "board": game_board}).encode('utf-8'))
                        game_board = [" " for _ in range(9)]  # Reset the board
                    else:
                        # Switch turns and update the board for both players
                        current_turn = 1 - current_turn
                        broadcast(json.dumps({"type": "update", "board": game_board, "current_turn": current_turn}).encode('utf-8'))
                else:
                    conn.send(json.dumps({"type": "error", "message": "Invalid move"}).encode('utf-8'))

        except (ConnectionResetError, json.JSONDecodeError):
            break

    conn.close()
    clients.remove((conn, player_id))

# Start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        player_id = len(clients)  # Assign player_id based on connection order (0, then 1)
        clients.append((conn, player_id))
        thread = threading.Thread(target=handle_client, args=(conn, player_id))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
