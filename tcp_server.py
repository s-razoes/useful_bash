from telenotify import user_interaction
import socket
import html
from datetime import datetime

port = 5003

bot_to_notify = "BOT_NAME"

host = "0.0.0.0"

server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together

while True:
    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        conn.settimeout(1)
        try:
            data = conn.recv(1024).decode("utf-8").strip()
            message = html.escape(data)
            if "127.0.0.1" in address:
                #send message to bot
                message = f'<code>{message}</code>'
            else:
                message = f'{address}: <code>{message}</code>'
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{now}:{message}")
            user_interaction.send_notification(message,bot_name=bot_to_notify,parse_mode='HTML')
        except Exception as e:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"error:{now} - {e}")
            conn.close()
            break
        
        print("from connected user: " + str(data))
        break

    conn.close()  # close the connection

