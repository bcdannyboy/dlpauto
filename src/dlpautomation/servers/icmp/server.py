import os
import socket
import struct
import threading
import ping3
import logging

class ICMPServer(threading.Thread):
    def __init__(self):
        logging.debug("ICMP Server running ICMPServer.__init__()")
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        s = self.create_icmp_socket()
        logging.info("ICMP server running...")
        print("[+] ICMP server...")
        try:
            while True:
                packet, addr = self.receive_icmp_request(s)
                self.send_icmp_reply(s, packet, addr)
        except Exception as e:
            logging.error(f"ICMP Server error: {e}")
            s.close()
        except KeyboardInterrupt:
            logging.info("ICMP Server shutting down...")
            print("[!] ICMP Server shutting down...")
            s.close()

    def create_icmp_socket(self):
        logging.debug("ICMP Server running ICMPServer.create_icmp_socket()")
        icmp = socket.getprotobyname('icmp')
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        logging.debug("ICMP Server running ICMPServer.create_icmp_socket() - socket created")
        return s

    def receive_icmp_request(self, s):
        logging.debug("ICMP Server running ICMPServer.receive_icmp_request()")
        packet, addr = s.recvfrom(4096)
        logging.debug("ICMP Server running ICMPServer.receive_icmp_request() - packet received")
        return packet, addr

    def send_icmp_reply(self, s, packet, addr):
        logging.debug("ICMP Server running ICMPServer.send_icmp_reply()")
        icmp_header = packet[20:28]
        icmp_type, code, chksum, id, seq = struct.unpack('BBHHH', icmp_header)

        icmp_type = 0
        icmp_checksum = 0
        data = packet[28:]

        icmp_packet = struct.pack('BBHHH', icmp_type, code, icmp_checksum, id, seq)
        icmp_packet += data

        icmp_checksum = ping3.checksum(icmp_packet)

        icmp_packet = struct.pack('BBHHH', icmp_type, code, icmp_checksum, id, seq)
        icmp_packet += data

        logging.debug("ICMP Server running ICMPServer.send_icmp_reply() - sending packet")
        s.sendto(icmp_packet, addr)
