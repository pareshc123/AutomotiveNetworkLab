def receive_exactly(sock, n):
    received_data = b""
    while len(received_data) < n:

        remaining = n - len(received_data)

        chunk = sock.recv(remaining)

        if chunk == b"":
            raise ConnectionError("Connection closed before all expected bytes were received")

        received_data += chunk

    return received_data
