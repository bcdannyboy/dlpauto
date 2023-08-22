import threading
import logging
import socket

class TCPServer(threading.Thread):
    def __init__(self, host='localhost', port=9000):
        logging.debug("TCP Server running TCPServer.__init__()")
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.daemon = True

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logging.debug("TCP Server running TCPServer.run() - TCP server listening...")

            while True:
                try:
                    conn, addr = s.accept()
                    threading.Thread(target=self.handle_client, args=(conn, addr)).start()
                except Exception as e:
                    logging.error(f"TCP Server error: {e}")
                except KeyboardInterrupt:
                    logging.info("TCP Server shutting down...")
                    break

            logging.info("TCP Server closing...")

    def handle_client(self, conn, addr):
        try:
            with conn:
                logging.debug(f'TCP Connection from {addr}')
                while True:
                    data = conn.recv(4096)
                    if not data:
                        logging.debug(f'TCP Connection from {addr} closed by client')
                        break
                    logging.debug(f'TCP Connection from {addr} received data')
                    logging.debug(f'TCP Connection from {addr} sending data back to client')
                    conn.sendall(data)
        except Exception as e:
            logging.error(f"TCP Server error: {e}")

