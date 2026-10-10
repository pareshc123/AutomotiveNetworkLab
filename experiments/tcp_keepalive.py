"""
Experiment: TCP Keep-Alive

Demonstrates how Linux sends TCP keep-alive probes when a connection
is idle, without Python sending or receiving application data.

Run:
    python3 -m experiments.tcp_keepalive

Configuration (client socket):
    SO_KEEPALIVE  = 1   # Enable TCP keep-alive
    TCP_KEEPIDLE  = 10  # First probe after 10 seconds idle
    TCP_KEEPINTVL = 3   # Interval between unanswered probes
    TCP_KEEPCNT   = 3   # Maximum unanswered probes

Experiment:
    1. Establish a TCP connection on localhost.
    2. Enable keep-alive on the client socket.
    3. Keep the connection idle for 35 seconds.
    4. Linux sends keep-alive probes; the server TCP stack sends ACKs.
    5. Close the connection normally.

Wireshark:
    Interface: lo
    Display filter: tcp.port == <server_port>
    Keep-alive filter:
        tcp.analysis.keep_alive || tcp.analysis.keep_alive_ack

Expected:
    - TCP handshake (SYN, SYN/ACK, ACK).
    - Keep-alive probes approximately every 10 seconds.
    - Server ACKs each probe without application involvement.
    - No application payload is exchanged.
    - Normal TCP connection closure (FIN).

Note:
    TCP_KEEPINTVL and TCP_KEEPCNT matter when probes go unanswered.
    This experiment demonstrates a healthy, responsive TCP connection.
"""

import socket
import sys
import time

from utility.logger import create_logger


logger = create_logger("tcp_keepalive")


def run_experiment() -> None:
    """Hold an established connection idle while Linux handles keep-alive."""
    if sys.platform != "linux":
        raise RuntimeError("This experiment requires the Linux TCP socket options.")

    # Context managers close every socket on normal exit, errors, and Ctrl+C.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        # Port 0 asks the kernel to assign an available local port.
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        server_address = listener.getsockname()
        logger.info("Listening on %s:%s", *server_address)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            # Linux completes the handshake and queues the connection for accept;
            # the server application does not need a thread to call accept first.
            client.connect(server_address)
            server_connection, peer_address = listener.accept()
            with server_connection:
                logger.info(
                    "Connected client %s:%s -> server %s:%s",
                    *peer_address,
                    *server_address,
                )

                # Python passes configuration to the kernel; it does not build
                # TCP probes. SOL_SOCKET selects socket-level options, while
                # IPPROTO_TCP selects options specific to the TCP protocol.
                client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
                client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
                client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)

                logger.info(
                    "Client options: SO_KEEPALIVE=%s, TCP_KEEPIDLE=%s s, "
                    "TCP_KEEPINTVL=%s s, TCP_KEEPCNT=%s",
                    client.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE),
                    client.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE),
                    client.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL),
                    client.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT),
                )
                logger.info("Keeping both endpoints idle for 35 seconds; capture on lo.")

                # sleep() pauses Python, not Linux TCP processing. No send() or
                # recv() is needed for kernel-generated probes or acknowledgments.
                time.sleep(35)

    logger.info("Experiment complete; all sockets closed.")


if __name__ == "__main__":
    run_experiment()
