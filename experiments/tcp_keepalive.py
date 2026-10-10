

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
