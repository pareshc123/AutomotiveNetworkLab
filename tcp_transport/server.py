import socket

from utility.logger import create_logger
from tcp_transport.socket_helper import receive_exactly
from protocol.message import encode_message, decode_message, parse_payload_length

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

        # Set a timeout to avoid infinite waiting period and blocking of python thread
        self.connection_socket.settimeout(5.0)

        logger.info("Client connected from %s:%s", client_address[0], client_address[1])

        # Parse Header
        logger.debug("Extracting Header")
        header = receive_exactly(self.connection_socket, 4)
        logger.debug("Header: %r",header)

        # Get the payload length from header
        payload_length = parse_payload_length(header)
        logger.debug(f"Payload Length: {payload_length}")

        # Receive the payload
        logger.debug("Extracting payload")
        payload = receive_exactly(self.connection_socket, payload_length)
        logger.debug(f"Payload: {payload}")
        
        # Decode UTF-8 payload bytes into a Python string
        message = decode_message(payload)

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
    except TimeoutError:
        logger.warning(
            "Receive timeout while waiting for an application frame from the connected client"
        )

    except ConnectionResetError as error:
        logger.error(
            "Connection reset by peer while receiving an application frame: %s",
            error,
        )

    except ConnectionError as error:
        logger.warning(
            "Peer closed the TCP connection before the complete application frame was received: %s",
            error,
        )

    except OSError as error:
        logger.error("Socket error: %s", error)

    finally:
        server.close()
