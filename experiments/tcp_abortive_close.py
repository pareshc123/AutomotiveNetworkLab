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
