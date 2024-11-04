import socket
import json

HOST = '0.0.0.0'
PORT = 65432

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f"[CONNECTED] Connected to server at {HOST}:{PORT}")

        initial_data = client.recv(1024).decode('utf-8')
        initial_msg = json.loads(initial_data)
        if initial_msg["type"] == "player_id":
            player_id = initial_msg["player_id"]
            print(f"[INFO] You are Player {player_id}")

        while True:

            response = client.recv(1024).decode('utf-8')
            response_obj = json.loads(response)

            if response_obj["type"] == "game_state":

                board = response_obj["board"]
                current_turn = response_obj["current_turn"]
                print("\n[GAME BOARD]")
                for row in board:
                    print(" | ".join(cell or ' ' for cell in row))
                print(f"[TURN INFO] It is Player {current_turn}'s turn.")

            if current_turn == player_id:
                action = input("Enter 'move' or 'quit': ").strip()

                if action == "move":
                    x = int(input("Enter row (0, 1, 2): ").strip())
                    y = int(input("Enter column (0, 1, 2): ").strip())
                    message = json.dumps({"type": "move", "data": {"x": x, "y": y}})
                    client.send(message.encode('utf-8'))

                elif action == "quit":
                    message = json.dumps({"type": "quit", "data": "Player quitting."})
                    client.send(message.encode('utf-8'))
                    break
                else:
                    print("[ERROR] Invalid command.")

            else:
                print(f"[SERVER RESPONSE] {response_obj.get('response')}")

    except ConnectionRefusedError:
        print("[ERROR] Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.close()
        print("[DISCONNECTED] Connection closed.")

if __name__ == "__main__":
    start_client()
