def receive_exactly(sock, n):
    """
     The function calculates the exact bytes required for the header, data etc
    """
    received_data = b""
    while len(received_data) < n:

        remaining = n - len(received_data)

        chunk = sock.recv(remaining)

        if chunk == b"":
            raise ConnectionError("Connection closed before all expected bytes were received")

        received_data += chunk

    return received_data
