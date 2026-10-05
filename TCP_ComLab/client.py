import socket

from utility.logger import create_logger
from protocol.message import encode_message, decode_message

logger = create_logger("TCP-Client")


class ClientSocket:

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.client_socket = None

    def create_socket(self):

        # Ask the OS to create an IPv4 TCP socket
        self.client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

    def start(self):
        
        # Ask the OS to establish a TCP connection
        logger.info("Connecting to %s:%s", self.ip_address, self.port)
        self.client_socket.connect(
            (self.ip_address, self.port)
        )
        logger.info("TCP connection established")

        message = "TCP Communication Client ..."

        # Encode Message
        network_data = encode_message(message)

        # Give application bytes to the socket
        self.client_socket.sendall(network_data)
        logger.info("Message sent: %s", message)

        # Wait for up to 1024 bytes from the server
        received_data = self.client_socket.recv(1024)
        response = decode_message(received_data)

        logger.info("Response recieved: %s", response)

    def close(self):

        if self.client_socket is not None:
            self.client_socket.close()
            self.client_socket = None

            logger.info("Client socket closed")


if __name__ == "__main__":

    client = ClientSocket("127.0.0.1", 5000)

    try:
        client.create_socket()
        client.start()

    except ConnectionRefusedError:
        logger.error("Connection refused. Is the server running?")

    except OSError as error:
        logger.error("Socket error: %s", error)

    finally:
        client.close()