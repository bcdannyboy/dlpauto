import base64
import requests
import json
import logging
import urllib3

from utils.strings import can_encode_latin1
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# exfil data over HTTP
# possible methods: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
# possible data locations: url parameter, url query variable, header, body, cookies
def ExfilHTTP(url, httpmethod, location, data):
    logging.debug("Using HTTP exfiltration")
    if isinstance(data, list):
        if location in ["urlparam", "urlquery", "header", "cookies"]:
            logging.debug("data is a list, converting to string")
            data = ','.join(data).replace("\n","<>")
        else:
            logging.debug("data is a list, converting to newline separated string")
            data = ' - '.join(data).replace("\n","<>")
    else:
        data = str(data).replace("\n","<>")

    # Requests library forces data to be within the latin-1 range but a string representation of some of our encodings can lead to unicode, etc.
    # so here we check if the data can be encoded as latin-1 and if not we encode it as utf-8 and convert it to a hex string representation of the data bytes
    if not can_encode_latin1(data):
        data_bytes = data.encode('utf-8')
        data = ''.join(f'0x{b:02X}' for b in data_bytes)

    method = httpmethod.upper()
    location = location.lower()

    supported_methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
    if method not in supported_methods:
        logging.error(f"Unsupported method: {method}. Method must be one of {json.dumps(supported_methods)}")
        raise ValueError(f"Unsupported method: {method}. Method must be one of {json.dumps(supported_methods)}")

    url_params, headers, data_param, cookies = None, None, None, None
    if location == "urlparam":
        logging.debug("Using url parameter")
        url = f"{url}/{data}"
    elif location == "urlquery":
        logging.debug("Using url query variable")
        url_params = {"dlpexfil": data}
    elif location == "header":
        logging.debug("Using header")
        headers = {"dlpexfil": data}
    elif location == "body":
        logging.debug("Using body")
        data_param = data
    elif location == "cookies":
        logging.debug("Using cookies")
        cookies = {"dlpexfil": data}
    else:
        logging.error(f"Unsupported location: {location}. location must be one of 'urlparam', 'urlquery', 'header', 'body' or 'cookies'")
        raise ValueError(f"Unsupported location: {location}. location must be one of 'urlparam', 'urlquery', 'header', 'body' or 'cookies'")

    try:
        response = requests.request(method, url + "/dlp/dlptest/" + location, params=url_params, headers=headers, data=data_param, cookies=cookies, verify=False)
    except UnicodeEncodeError:
        print(f"Error encoding data: {data} to {url}/dlp/dlptest/{location}")
        raise

    logging.debug("Done exfiltrating over HTTP")
    return response