
def encode_message(message: str) -> bytes:
    """
    Convert a Python string into bytes for socket transmission.
    """
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    
    return message.encode("utf-8")

def decode_message(data: bytes) -> str:
    """
    Convert a received sockets bytes back into python string.
    """
    if not isinstance(data, bytes):
        raise TypeError("Received data must by bytes")    
    
    return data.decode("utf-8")
