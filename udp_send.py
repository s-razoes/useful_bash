import socket
import argparse


parser = argparse.ArgumentParser(description='Send a message via UDP.')
parser.add_argument('server', help='server address')
parser.add_argument('port', help='server post')
parser.add_argument('text', help='The text to send')
        
args = parser.parse_args()

if args.text =='' or args.server =='' or args.port=='':
    print("All arguments are mandatory")
    quit(1)

bytesToSend         = str.encode(args.text)
serverAddressPort   = (args.server, int(args.port))
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
#msgFromServer = UDPClientSocket.recvfrom(bufferSize)
#msg = "Message from Server {}".format(msgFromServer[0])
#print(msg)
