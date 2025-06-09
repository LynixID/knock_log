import socket
import subprocess
import time

TARGET_IP = "192.168.161.43"   # Ganti dengan IP device penerima log
TARGET_PORT = 9999             # Port socket penerima

def get_knock_logs():
    try:
        result = subprocess.run(
            ["dmesg"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        lines = result.stdout.splitlines()
        knock_lines = [line for line in lines if "KNOCK" in line]
        return knock_lines
    except Exception as e:
        print("Gagal ambil dmesg:", e)
        return []

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Menghubungi {TARGET_IP}:{TARGET_PORT} ...")
    try:
        sock.connect((TARGET_IP, TARGET_PORT))
        print("Terhubung. Kirim log...")

        sent_lines = set()
        while True:
            logs = get_knock_logs()
            new_lines = [line for line in logs if line not in sent_lines]

            for line in new_lines:
                try:
                    sock.sendall((line + "\n").encode())
                    sent_lines.add(line)
                    print("Kirim:", line)
                except Exception as e:
                    print("Gagal kirim:", e)
                    break

            time.sleep(2)

    except Exception as conn_err:
        print("Gagal koneksi:", conn_err)
    finally:
        sock.close()

if __name__ == "__main__":
    main()
