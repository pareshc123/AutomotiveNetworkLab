import socket

from utility.logger import create_logger
from protocol.message import encode_message, decode_message

logger = create_logger("TCP-Server")


class ServerSocket:

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.server_socket = None
        self.connection_socket = None

    def create_socket(self):

        # Ask the OS to create an IPv4 TCP socket
        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        logger.debug("Server socket created")

    def start(self):

        # Assign the local IP address and port
        logger.info("Binding socket to %s:%s", self.ip_address, self.port)
        self.server_socket.bind(
            (self.ip_address, self.port)
        )

        # Turn the socket into a listening socket
        self.server_socket.listen()

        logger.info("Server listening on %s:%s", self.ip_address, self.port)

        # Wait for a client connection
        self.connection_socket, client_address = (
            self.server_socket.accept()
        )

        logger.info("Client connected from %s:%s", client_address[0], client_address[1])

        # Wait for up to 1024 bytes from the client
        received_data = self.connection_socket.recv(1024)
        logger.info(f"Raw data received: {received_data}")
        message = decode_message(received_data)

        logger.info("Message received: %s", message)

        response = "TCP Communication Server ..."
        network_data = encode_message(response)

        self.connection_socket.sendall(network_data)
        logger.info("Response sent: %s", response)

    def close(self):

        # Close the connected client socket first
        if self.connection_socket is not None:
            self.connection_socket.close()
            self.connection_socket = None

            logger.info("Connection socket closed")

        # Then close the listening socket
        if self.server_socket is not None:
            self.server_socket.close()
            self.server_socket = None

            logger.info("Server socket closed")


if __name__ == "__main__":

    server = ServerSocket("127.0.0.1", 5000)

    try:
        server.create_socket()
        server.start()

    except OSError as error:
        logger.error("Socket error: %s", error)

    finally:
        server.close()
