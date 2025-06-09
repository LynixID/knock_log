import socket

LISTEN_PORT = 9999

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", LISTEN_PORT))
    server_socket.listen(1)
    print(f"Menunggu koneksi di port {LISTEN_PORT}...")

    conn, addr = server_socket.accept()
    print(f"Koneksi dari {addr}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("LOG:", data.decode().strip())
    except Exception as e:
        print("Error saat terima log:", e)
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    main()
