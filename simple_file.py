import socket

HOST = 'localhost'
PORT = 12345
server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(server_address)

print(f"Server listening on {server_address}")

while True:
    data, address = sock.recvfrom(4096)
    print(f"Received message: {data} from {address}")

    if data:
        sent = sock.sendto(b'Hello from UDP server!', address)
        print(f"Sent {sent} bytes back to {address}")
