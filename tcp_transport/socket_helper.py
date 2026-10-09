def receive_exactly(sock, n):
    """
     Receive exactly `n` bytes from a connected TCP socket.

    TCP delivers an ordered byte stream, so one call to `sock.recv()` may
    return fewer bytes than requested. This function keeps calling `recv()`
    until `n` bytes have been collected.

    Raises:
        ConnectionError: If the peer closes the connection before all expected
            bytes are received.
    """
    received_data = b""
    while len(received_data) < n:

        remaining = n - len(received_data)

        chunk = sock.recv(remaining)

        if chunk == b"":
            raise ConnectionError(
                f"Connection closed after receiving {len(received_data)} of {n} expected bytes"
            )

        received_data += chunk

    return received_data
