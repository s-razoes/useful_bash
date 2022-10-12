from datetime import datetime
import socket
from telenotify import user_interaction
import html

localPort   = 20001

localIP     = "0.0.0.0"
bufferSize  = 1024

bot_to_notify = "BOT_NAME"

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print(f"UDP server up and listening on port {localPort}")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode('utf-8').strip()
    address = str(bytesAddressPair[1]).strip()
    if message == '':
        message = f"Empty message from: {address}"
        continue
    message = html.escape(message)
    if "'127.0.0.1'" in address:
        #send message to bot
        message = f'<code>{message}</code>'
    else:
        message = f'{address}: <code>{message}</code>'
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{now}:{message}")
    user_interaction.send_notification(message,bot_name=bot_to_notify,parse_mode='HTML')
    print(f"{address} : {message}")

