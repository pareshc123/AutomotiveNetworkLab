"""
Experiment: TCP abortive close using SO_LINGER.

Purpose:
    Demonstrate how Linux can reset an established TCP
    connection instead of closing it gracefully.

Expected server behavior:
    recv() raises ConnectionResetError.

Expected Wireshark:
    SYN -> SYN/ACK -> ACK -> RST/ACK

Run:
    python3 -m experiments.tcp_abortive_close

Start tcp_transport.server before running this experiment.
"""

import struct
import socket


def run_experiment():

    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0),)
        - socket.SOL_SOCKET — Configure an option at the socket level.
        - socket.SO_LINGER — Select the linger option, which affects close behavior.
        - struct.pack("ii", 1, 0) — Convert two Python integers into the binary representation
           expected by the Linux socket API.
        - 1 — Enable linger.
        - 0 — Set the linger timeout to zero.
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("127.0.0.1", 5000))

        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_LINGER,
            struct.pack("ii", 1, 0),
        )


if __name__ == "__main__":
    run_experiment()
