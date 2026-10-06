from TCP_ComLab.socket_helper import receive_exactly

def encode_message(message: str) -> bytes:
    """
    Convert a Python string into bytes for socket transmission.
    """
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    

    # UTF-encoding
    payload = message.encode("utf-8")

    # get the length of the message
    payload_len = len(payload)

    # convert the length to bytes
    header = payload_len.to_bytes(4, "big")

    # insert the header length to message
    frame = header + message

    return frame

def decode_message(data: bytes) -> str:
    """
    Convert a received sockets bytes back into python string.
    """
    if not isinstance(data, bytes):
        raise TypeError("Received data must by bytes")    
    
    return data.decode("utf-8")


def parse_payload_length(header: bytes) -> int:
    """
    Convert a 4-byte big-endian header into the payload length.
    """

    if not isinstance(header, bytes):
        raise TypeError("Header must be in bytes")
    
    if len(header) != 4:
        raise ValueError("Header must be exactly 4 bytes")
    
    payload_length = int.from_bytes(header, "big")

    return payload_length
