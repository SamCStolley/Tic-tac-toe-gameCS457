import socket

# Server connection parameters
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f"[CONNECTED] Connected to server at {HOST}:{PORT}")
        
        while True:
            message = input("Enter message to send (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            
            client.send(message.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(f"[SERVER RESPONSE] {response}")

    except ConnectionRefusedError:
        print("[ERROR] Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.close()
        print("[DISCONNECTED] Connection closed.")

if __name__ == "__main__":
    start_client()
