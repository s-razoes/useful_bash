from datetime import datetime
import socket
from telenotify import user_interaction
import html
import time

localPort   = 20001
token = '#TOKEN#'
localIP     = "0.0.0.0"
bufferSize  = 1024

TIME_THRESHOLD = 10

bot_to_notify = "#BOT_NAME#"

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print(f"UDP server up and listening on port {localPort}")
allowed_IPs = []
last_msg_ip = None
last_msg_time = time.time()
# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = bytesAddressPair[0].decode('utf-8').strip()
    address = str(bytesAddressPair[1]).strip()
    ip_address = str(bytesAddressPair[1][0]).strip()
    if message == '':
        message = f"Empty message from: {address}"
        continue
    #breakpoint()
    if message.startswith(token) or ip_address in allowed_IPs:
        if ip_address not in allowed_IPs:
            allowed_IPs.append(ip_address)
            print(f'Adding:{ip_address}')
        if message.startswith(token):
            message = message[len(token):].strip()
        if message == '':
            print(f"{now} {address}: Token only")
            continue #it was just the token
        message = html.escape(message)
        if "127.0.0.1" == ip_address:
            #send message to bot
            message = f'<code>{message}</code>'
        else:
            notification = f'{ip_address} - UDP: <code>{message}</code>'
            if last_msg_ip != ip_address:
                last_msg_ip = ip_address                
            else:
                if (time.time() - last_msg_time)<TIME_THRESHOLD:
                    notification = f'<code>{message}</code>'
        last_msg_time = time.time()
        user_interaction.send_notification(notification,bot_name=bot_to_notify,parse_mode='HTML')
        print(f"{now} {address}:{message}")
    else:
        print(f"{now}-FAILED-{address}:{message}")
        continue
