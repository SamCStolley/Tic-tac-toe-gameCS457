import socket
import threading
import json
import logging

# Configure logging
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

HOST = input("Enter the host address (e.g., 127.0.0.1): ").strip()
PORT = int(input("Enter the port number (e.g., 65432): ").strip())

clients = []
game_board = [" " for _ in range(9)]
current_turn = 0  # Tracks whose turn it is (0 for Player 1, 1 for Player 2)
win_counts = [0, 0]  # Tracks wins for Player 1 and Player 2
tie_count = 0  # Tracks the number of ties

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

# Reset the game
def reset_game():
    global game_board, current_turn
    game_board = [" " for _ in range(9)]
    current_turn = 0

# Handle client moves and game updates
def handle_client(conn, player_id):
    global current_turn, game_board, win_counts, tie_count
    conn.send(json.dumps({"player_id": player_id}).encode('utf-8'))
    logging.info(f"Player {player_id} joined the game.")

    if len(clients) == 2:
        broadcast(json.dumps({"type": "start_game", "current_turn": current_turn}).encode('utf-8'))
        logging.info("Game started between Player 0 and Player 1.")

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
                    logging.info(f"Player {player_id} made a move at position {move}.")
                    winner = check_game_status()

                    if winner:
                        if winner == "Draw":
                            tie_count += 1
                            logging.info("The game ended in a draw.")
                            broadcast(json.dumps({
                                "type": "game_over",
                                "winner": "Draw",
                                "board": game_board,
                                "win_counts": win_counts,
                                "tie_count": tie_count
                            }).encode('utf-8'))
                        else:
                            winning_player = 0 if winner == "X" else 1
                            win_counts[winning_player] += 1
                            logging.info(f"Player {winning_player} won the game.")
                            broadcast(json.dumps({
                                "type": "game_over",
                                "winner": winning_player,
                                "board": game_board,
                                "win_counts": win_counts,
                                "tie_count": tie_count
                            }).encode('utf-8'))
                        
                        reset_game()
                        broadcast(json.dumps({"type": "reset_game", "current_turn": current_turn}).encode('utf-8'))
                    else:
                        current_turn = 1 - current_turn
                        broadcast(json.dumps({
                            "type": "update",
                            "board": game_board,
                            "current_turn": current_turn
                        }).encode('utf-8'))
                else:
                    logging.warning(f"Player {player_id} attempted an invalid move at position {move}.")
                    conn.send(json.dumps({"type": "error", "message": "Invalid move"}).encode('utf-8'))

        except (ConnectionResetError, json.JSONDecodeError) as e:
            logging.error(f"Error with Player {player_id}: {e}")
            break

    # Handle client disconnection
    conn.close()
    clients.remove((conn, player_id))
    logging.info(f"Player {player_id} disconnected.")

    if len(clients) == 1:
        # Handle remaining player: reset game and treat disconnect as a tie
        tie_count += 1
        logging.info("Opponent disconnected. Game reset as a tie.")
        reset_game()
        current_turn = 0  # Remaining player always starts new games
        remaining_conn, remaining_player_id = clients[0]
        remaining_conn.send(json.dumps({
            "type": "player_disconnect",
            "tie_count": tie_count,
            "board": game_board
        }).encode('utf-8'))
    elif len(clients) == 0:
        reset_game()

# Start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    logging.info(f"Server started, listening on {HOST}:{PORT}")
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        player_id = len(clients)  # Assign player_id based on connection order (0, then 1)
        clients.append((conn, player_id))
        logging.info(f"Player {player_id} connected from {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, player_id))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
