import threading
import time
import grpc
import hashlib

from concurrent import futures
import logging

from servers.grpc import exfil_pb2, exfil_pb2_grpc

class ExfilServiceServicer(exfil_pb2_grpc.ExfilServiceServicer):
    def SendExfilData(self, request, context):
        logging.debug("grpc server running ExfilServiceServicer.SendExfilData()")
        # Calculate the hash of the data
        data_hash = hashlib.sha256(request.data.encode()).hexdigest()

        logging.debug("grpc server returning data_hash = %s" % data_hash)
        return exfil_pb2.ExfilReply(message=data_hash)

class ThreadedGRPCServer(threading.Thread):
    def __init__(self):
        logging.debug("grpc server running ThreadedGRPCServer.__init__()")
        threading.Thread.__init__(self)
        self.daemon = True
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        logging.debug("grpc server running ThreadedGRPCServer.__init__() - adding ExfilServiceServicer")
        exfil_pb2_grpc.add_ExfilServiceServicer_to_server(ExfilServiceServicer(), self.server)
        self.server.add_insecure_port('[::]:50051')

    def run(self):
        logging.info("Starting gRPC server...")
        print("[+] Starting gRPC server...")
        self.server.start()
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            logging.info("Stopping gRPC server...")
            print("[!] Stopping gRPC server...")
            self.server.stop(0)

# To run:
# grpc_server = ThreadedGRPCServer()
# grpc_server.start()
