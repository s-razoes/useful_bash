import socket
import user_interaction

#port is high for low priviledge user
localPort   = 20001
#this address is for all IPv4 addresses, if you only want local change it to 127.0.0.1
localIP     = "0.0.0.0"
bufferSize  = 1024

bytesToSend         = str.encode(msgFromServer)
 
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode('utf-8')
    address = str(bytesAddressPair[1])
    if "'127.0.0.1'" in address:
        #send message to bot
        user_interaction.send_notification(message)
    else:
        user_interaction.send_notification(f'UDP: {message}')
    print(f"{address} : {message}")
