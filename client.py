import socket
import json
import threading
import tkinter as tk
from tkinter import messagebox

client_socket = None
connected = False
player_id = None
current_turn = None
game_board = [" " for _ in range(9)]  # Initial empty 3x3 Tic-Tac-Toe board
tie_count = 0  # Tracks the number of ties
win_count = 0  # Tracks player's wins

# Connect to the server
def connect_to_server(host, port):
    global client_socket, connected
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        connected = True
        threading.Thread(target=receive_messages, daemon=True).start()
        connect_button.config(state=tk.DISABLED)  # Disable connect button after connecting
        disconnect_button.config(state=tk.NORMAL)  # Enable disconnect button
    except ConnectionRefusedError:
        messagebox.showerror("Connection Error", "Could not connect to the server. Please try again.")
        connected = False

# Disconnect from the server
def disconnect_from_server():
    global client_socket, connected
    if connected and client_socket:
        client_socket.close()
        connected = False
    connect_button.config(state=tk.NORMAL)  # Enable connect button
    disconnect_button.config(state=tk.DISABLED)  # Disable disconnect button
    update_status("Disconnected from server.")

# Handle messages from the server
def receive_messages():
    global player_id, current_turn, game_board, tie_count, win_count
    while connected:
        try:
            message = client_socket.recv(1024).decode('utf-8').strip()
            if not message:
                break
            
            for msg in message.split('\n'):
                if msg:
                    msg_obj = json.loads(msg)
                    msg_type = msg_obj.get("type")
                    msg_data = msg_obj.get("data")

                    if "player_id" in msg_obj:
                        player_id = msg_obj["player_id"]
                        update_status(f"Connected as Player {player_id}. Waiting for opponent...")

                    elif msg_type == "start_game":
                        current_turn = msg_obj["current_turn"]
                        update_status("Game started!")
                        if current_turn == player_id:
                            update_status("Your turn!")
                        else:
                            update_status("Waiting for opponent's move...")

                    elif msg_type == "update":
                        game_board = msg_obj["board"]
                        current_turn = msg_obj["current_turn"]
                        update_game_board()
                        if current_turn == player_id:
                            update_status("Your turn!")
                        else:
                            update_status("Waiting for opponent's move...")

                    elif msg_type == "game_over":
                        game_board = msg_obj["board"]
                        update_game_board()
                        winner = msg_obj["winner"]
                        if winner == "Draw":
                            tie_count += 1
                            update_tie_counter()
                            update_status("The game is a draw!")
                        elif winner == player_id:
                            win_count += 1
                            update_win_counter()
                            update_status("You win!")
                        else:
                            update_status("Opponent wins!")
                        reset_game()

                    elif msg_type == "player_disconnect":
                        tie_count += 1  # Treat disconnect as a tie
                        update_tie_counter()
                        update_status("Opponent disconnected. Game reset!")
                        reset_game()

                    elif msg_type == "error":
                        update_status(msg_data["message"])

        except Exception as e:
            print(f"[ERROR] {e}")
            break

# Send messages to the server
def send_message(msg_type, msg_data=""):
    if client_socket:
        message = json.dumps({"type": msg_type, "data": msg_data}) + "\n"
        client_socket.send(message.encode('utf-8'))

# UI updates
def update_status(text):
    status_label.config(text=text)

def update_game_board():
    for i, cell in enumerate(game_board):
        buttons[i].config(text=cell)

def on_button_click(i):
    if current_turn == player_id and game_board[i] == " ":
        send_message("move", str(i))
    else:
        update_status("Not your turn or invalid move!")

def reset_game():
    global game_board
    game_board = [" " for _ in range(9)]
    update_game_board()

def update_tie_counter():
    tie_counter_label.config(text=f"Ties: {tie_count}")

def update_win_counter():
    win_counter_label.config(text=f"Wins: {win_count}")

# UI Setup
root = tk.Tk()
root.title("Tic Tac Toe Client")

frame = tk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

tk.Label(frame, text="Host:").grid(row=0, column=0)
host_entry = tk.Entry(frame)
host_entry.grid(row=0, column=1)

tk.Label(frame, text="Port:").grid(row=1, column=0)
port_entry = tk.Entry(frame)
port_entry.grid(row=1, column=1)

connect_button = tk.Button(frame, text="Connect", command=lambda: connect_to_server(host_entry.get(), int(port_entry.get())))
connect_button.grid(row=2, column=0, pady=10)

disconnect_button = tk.Button(frame, text="Disconnect", command=disconnect_from_server, state=tk.DISABLED)
disconnect_button.grid(row=2, column=1, pady=10)

status_label = tk.Label(root, text="Enter server details and connect.", font=("Arial", 12))
status_label.grid(row=1, column=0, pady=10)

board_frame = tk.Frame(root)
board_frame.grid(row=2, column=0, padx=10, pady=10)

buttons = []
for i in range(9):
    button = tk.Button(board_frame, text=" ", width=5, height=2, font=("Arial", 18), command=lambda i=i: on_button_click(i))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

win_counter_label = tk.Label(root, text="Wins: 0", font=("Arial", 12))
win_counter_label.grid(row=3, column=0, pady=5)

tie_counter_label = tk.Label(root, text="Ties: 0", font=("Arial", 12))
tie_counter_label.grid(row=4, column=0, pady=5)

root.mainloop()
