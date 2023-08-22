import asyncio
import logging
import websockets
import hashlib
import threading

async def exfil(websocket, path):
    data = await websocket.recv()
    logging.debug("websocket server running exfil() - received data")

    # Calculate the hash of the data
    data_hash = hashlib.sha256(data.encode()).hexdigest()

    await websocket.send(data_hash)
    logging.debug("websocket server running exfil() - sent data_hash")

def start_server():
    logging.debug("websocket server running start_server()")
    return websockets.serve(exfil, "0.0.0.0", 8765)

def initWebsocketServer():
    logging.info("Starting websocket server...")
    print("[+] running websocket server...")
    asyncio.set_event_loop(asyncio.new_event_loop())
    server = start_server()
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
    logging.info("Stopping websocket server...")
    print("[!] websocket server stopped...")
