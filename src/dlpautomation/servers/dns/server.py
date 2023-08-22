import threading
from dnslib import DNSRecord, RR, dns, DNSHeader
import logging
import socketserver
from utils.strings import convert_string_to_ascii_representation, string_to_ipv6

class EchoResolver:
    def handle(self, data, addr, server):
        logging.debug("Got a DNS request, running EchoResolver.handle()")

        print("Raw data received: ", data)  # Print the raw data received

        try:
            request = DNSRecord.parse(data)
        except Exception as e:
            print("Error parsing DNS request: ", e)
            # Create a DNS response with the raw data in the TXT record
            response = DNSRecord(DNSHeader(id=12345, qr=1, aa=1, ra=1, rcode=1))  # Use a random id
            response.add_answer(RR(rname="error", rtype=dns.QTYPE.TXT, rdata=dns.TXT("Raw data: " + str(data)), ttl=60))
            return response.pack()

        print("Parsed DNS request: ", request)  # Print the parsed DNS request

        q = request.q
        rdata = None

        logging.debug("DNS Query Type: %s" % q.qtype)
        logging.debug("DNS Query Name: %s" % q.qname)
        if dns.QTYPE[q.qtype] == "A":
            rdata = dns.A("127.0.0.1")  # Return a dummy A record
        elif dns.QTYPE[q.qtype] == "AAAA":
            rdata = dns.AAAA("::1")  # Return a dummy AAAA record
        elif dns.QTYPE[q.qtype] == "TXT":
            rdata = dns.TXT(str(q.qname))
        else:
            logging.warning(f"Unhandled query type: {dns.QTYPE[q.qtype]} - {q.qtype}")
            response = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1, rcode=4))  # rcode=4 indicates "Not Implemented"
            return response.pack()

        # Create a new response object
        response = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
        # Add the answer to the response
        response.add_answer(RR(rname=q.qname, rtype=q.qtype, rdata=rdata, ttl=60))

        logging.debug("DNS handle returning response")
        return response.pack()

class ThreadedDNSServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

class ThreadedDNSRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.debug("running ThreadedDNSRequestHandler.handle()")
        data = self.request[0].strip()
        socket = self.request[1]
        resolver = self.server.resolver
        response = resolver.handle(data, self.client_address, self.server)
        logging.debug("DBS response sending over socket")
        socket.sendto(response, self.client_address)

class ThreadedDNSProxy(threading.Thread):
    def __init__(self, resolver, server="localhost", port=53):
        logging.debug("running ThreadedDNSProxy(resolver=%s, server=%s, port=%d)" % (resolver, server, port))
        threading.Thread.__init__(self)
        self.daemon = True
        self.server = ThreadedDNSServer((server, port), ThreadedDNSRequestHandler)
        self.server.resolver = resolver

    def run(self):
        logging.info("Starting DNS server...")
        print("[+] Starting DNS server...")
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logging.info("Stopping DNS server...")
            print("[!] Stopping DNS server...")
            self.server.shutdown()
            self.server.server_close()