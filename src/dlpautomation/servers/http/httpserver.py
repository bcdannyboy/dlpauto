import http.server
import os
import socketserver
import ssl
import threading
import json
import logging
import urllib.parse
from io import BytesIO

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def process_request(self):
        logging.debug("HTTP Server running CustomHTTPRequestHandler.process_request()")
        content_length = int(self.headers['Content-Length']) if 'Content-Length' in self.headers else 0
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else None
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        logging.debug("Building HTTP response")
        response = {
            'method': self.command,
            'path': self.path,
            'headers': dict(self.headers),
            'query': query_components,
            'body': post_data
        }

        outp = json.dumps(response)
        logging.debug("sending HTTP response")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()  # End headers before writing the response body
        self.wfile.write(outp.encode())

    def do_GET(self):
        logging.debug("HTTP Server running CustomHTTPRequestHandler.do_GET()")
        self.process_request()

    def do_POST(self):
        logging.debug("HTTP Server running CustomHTTPRequestHandler.do_POST()")
        self.process_request()

    def do_PUT(self):
        logging.debug("HTTP Server running CustomHTTPRequestHandler.do_PUT()")
        self.process_request()

    def do_DELETE(self):
        logging.debug("HTTP Server running CustomHTTPRequestHandler.do_DELETE()")
        self.process_request()

    def do_PATCH(self):
        logging.debug("HTTP Server running CustomHTTPRequestHandler.do_PATCH()")
        self.process_request()

    def do_OPTIONS(self):
        logging.debug("HTTP Server running CustomHTTPRequestHandler.do_OPTIONS()")
        self.process_request()

class HTTPServer(threading.Thread):
    def __init__(self, server_class=http.server.HTTPServer, handler_class=CustomHTTPRequestHandler, port=8000, use_https=False):
        logging.debug("HTTP Server running HTTPServer.__init__()")
        threading.Thread.__init__(self)
        self.daemon = True
        self.server_class = server_class
        self.handler_class = handler_class
        self.port = port
        self.use_https = use_https

        if use_https:
            logging.debug("HTTP Server running HTTPServer.__init__() - use_https = True")
            # Get the base directory dynamically
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            logging.debug("HTTP Server running HTTPServer.__init__() - base_dir = %s" % base_dir)
            # Set the paths for the cert and key files
            self.cert_file = os.path.join(base_dir, 'servers/http/ssl/cert.pem')
            self.key_file = os.path.join(base_dir, 'servers/http/ssl/key.pem')
            logging.debug("HTTP Server running HTTPServer.__init__() - cert_file = %s" % self.cert_file)
            logging.debug("HTTP Server running HTTPServer.__init__() - key_file = %s" % self.key_file)
            print(f'[.] Using SSL Cert file: {self.cert_file}')
            print(f'[.] Using SSL Key file: {self.key_file}')


    def run(self):
        logging.info("HTTP/S running...")
        print("[+] HTTP/S running...")
        httpd = self.server_class(('localhost', self.port), self.handler_class)
        if self.use_https:
            logging.info("HTTP/S server using HTTPS")
            httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=self.key_file, certfile=self.cert_file, server_side=True)
        try:
            logging.info("HTTP server serving forever...")
            httpd.serve_forever()
        except KeyboardInterrupt:
            logging.info("Shutting down HTTP/S server...")
            print("[!] Shutting down HTTP/S server...")