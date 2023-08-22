import threading
import logging
import socket

class UDPServer(threading.Thread):
    def __init__(self, host='localhost', port=9000):
        logging.debug("UDP Server running UDPServer.__init__()")
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.daemon = True  # Corrected here

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((self.host, self.port))
            logging.info("UDP server running...")
            print("[+] UDP server...")
            try:
                while True:
                    data, addr = s.recvfrom(4096)
                    logging.debug(f'UDP server received message from {addr}')
                    if data:
                        sent = s.sendto(data, addr)
                        logging.debug(f'UDP server sent {sent} bytes to {addr}: {data}')
            except KeyboardInterrupt:
                logging.info("UDP Server shutting down...")
                print("[!] Shutting down UDP server...")
            finally:
                logging.info("UDP Server closing...")
                s.close()
