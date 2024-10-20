import socket
import json

# Server connection parameters
HOST = '127.0.0.1'
PORT = 65432

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f"[CONNECTED] Connected to server at {HOST}:{PORT}")
        
        while True:
            # Get user input and send a structured message
            action = input("Enter 'join', 'move', 'chat', or 'quit': ").strip()

            if action == "join":
                message = json.dumps({"type": "join", "data": "Requesting to join a game."})

            elif action == "move":
                move = input("Enter your move (e.g., X at 1,1): ")
                message = json.dumps({"type": "move", "data": move})

            elif action == "chat":
                chat_msg = input("Enter your chat message: ")
                message = json.dumps({"type": "chat", "data": chat_msg})

            elif action == "quit":
                message = json.dumps({"type": "quit", "data": "Player quitting."})
                client.send(message.encode('utf-8'))
                break

            else:
                print("[ERROR] Invalid command.")
                continue

            # Send the message to the server
            client.send(message.encode('utf-8'))

            # Receive and print the server's response
            response = client.recv(1024).decode('utf-8')
            response_obj = json.loads(response)
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
