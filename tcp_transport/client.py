import socket

from utility.logger import create_logger
from tcp_transport.socket_helper import receive_exactly
from protocol.message import encode_message, decode_message, parse_payload_length

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

        # Parse Header
        logger.debug("Extracting Header")
        header = receive_exactly(self.client_socket, 4)
        logger.debug("Header: %r", header)

        # Get the payload length from header
        payload_length = parse_payload_length(header)
        logger.debug(f"Payload Length: {payload_length}")

        # Receive the payload
        logger.debug("Extracting payload")
        payload_response = receive_exactly(self.client_socket, payload_length)
        logger.debug(f"Payload: {payload_response}")

        # Decode UTF-8 payload bytes into a Python string
        response = decode_message(payload_response)

        logger.info("Response received: %s", response)

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

    except ConnectionRefusedError as error:
        logger.error(
            "Connection to %s:%s refused; is the server running? %s",
            client.ip_address,
            client.port,
            error,
        )

    except OSError as error:
        if type(error) is ConnectionError:
            logger.warning(
                "Peer closed the TCP connection before the complete response frame "
                "was received: %s",
                error,
            )
        else:
            logger.error("Socket error: %s", error)

    finally:
        client.close()
