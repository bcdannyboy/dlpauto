import socket
import logging

# exfiltrate data over a TCP socket, returns true once the data is echoed back from the server
def ExfilTCP(ip, port, data):
    logging.debug("Using TCP exfiltration")
    if isinstance(data, list):
        logging.debug("data is a list, converting to string")
        data = ','.join(data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Convert port to integer
    port = int(port)

    server_address = (ip, port)
    sock.connect(server_address)
    logging.debug(f'Made TCP Connection to {ip} on port {port}')

    good_echo = False
    try:
        message = bytes(data, 'utf-8')  # Convert string to bytes
        logging.debug(f'Sending data to {ip} on port {port} over TCP')
        sock.sendall(message)

        amt_received = 0
        amt_expected = len(message)
        recv_data = b""  # Initialize as bytes

        while amt_received < amt_expected:
            data = sock.recv(4096)
            amt_received += len(data)
            logging.debug(f'Received data from {ip} on port {port} over TCP')
            recv_data += data  # Concatenate bytes

        if recv_data == message:
            logging.debug(f'Got echo from {ip} on port {port} over TCP')
            good_echo = True
        else:
            logging.debug(f'Got bad echo from {ip} on port {port} over TCP')

        logging.debug(f'Closing TCP connection to {ip} on port {port}')
        sock.close()
    except Exception as e:
        logging.error(f"Failed to send or receive TCP message: {e}")
        return {
            "good": False,
            "recv": None,
            "err": f"Failed to send or receive TCP message: {e}"
        }

    logging.debug("TCP exfiltration successful!")
    return {
        "good": good_echo,
        "recv": recv_data.decode('utf-8'),  # Convert received bytes to string
        "err": None
    }
