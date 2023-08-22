import asyncio
import json
from threading import Thread
from utils.strings import rand_string, byte_to_string
from exfil.run import runExfil
from servers.grpc.server import ThreadedGRPCServer
from utils.config import parseConfig
from utils.generate import generateFakeData
from servers.websockets.server import initWebsocketServer
from servers.graphql.server import initGQLServer
from servers.http.httpserver import HTTPServer
from servers.dns.server import ThreadedDNSProxy, EchoResolver
from servers.icmp.server import ICMPServer
from servers.tcp.server import TCPServer
from servers.udp.server import UDPServer
import argparse
from wonderwords import RandomWord
import datetime
import logging

def main(server=False, config="", verbose=False):
    logname = "dlpexfil_client_" + rand_string(6) + ".log"
    if server:
        logname = "dlpexfil_server_" + rand_string(6) + ".log"

    if verbose:
        print("[+] Verbose logging enabled")
        logging.basicConfig(filename=logname, filemode='w+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    else:
        print("[+] Standard logging enabled")
        logging.basicConfig(filename=logname, filemode='w+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    if server:
        # TODO: add configuration options for custom server ports / ssl certs
        print("[+] Starting in server mode")
        logging.info("Starting in server mode")
        print("[.] Parsing configuration file")
        logging.info("Parsing configuration file")
        configOrErr = parseConfig(config, server=True)
        if isinstance(configOrErr, str):
            logging.error("Failed to parse server configuration file: " + configOrErr)
            print("Failed to parse server configuration file: " + configOrErr)
            exit(-1)

        config = configOrErr

        server = []

        if "http" in config and config["http"]:
            logging.info("Starting HTTP Server on port 8000")
            print("[+] Starting HTTP Server on port 8000")
            http_server = HTTPServer()
            server.append(http_server)

        if "https" in config and config["https"]:
            logging.info("Starting HTTPS Server on port 8443")
            print("[+] Starting HTTPS Server on port 8443")
            http_server = HTTPServer(port=8443, use_https=True)
            server.append(http_server)

        if "dns" in config and config["dns"]:
            logging.info("Starting DNS Server on port 54")
            print("[+] Starting DNS Server on port 54")
            dns_resolver = EchoResolver()
            dns_server = ThreadedDNSProxy(dns_resolver, server="0.0.0.0", port=54)
            server.append(dns_server)

        if "icmp" in config and config["icmp"]:
            logging.info("Starting ICMP Server")
            print("[+] Starting ICMP Server")
            icmp_server = ICMPServer()
            server.append(icmp_server)

        if "tcp" in config and config["tcp"]:
            logging.info("Starting TCP Server on port 9000")
            print("[+] Starting TCP Server on port 9000")
            tcp_server = TCPServer(host="0.0.0.0", port=9000)
            server.append(tcp_server)

        if "udp" in config and config["udp"]:
            logging.info("Starting UDP Server on port 9001")
            print("[+] Starting UDP Server on port 9001")
            udp_server = UDPServer(host="0.0.0.0", port=9001)
            server.append(udp_server)

        if "graphql" in config and config["graphql"]:
            logging.info("Starting GraphQL Server on port 8081")
            print("[+] Starting GraphQL Server on port 8081")
            gql_server = Thread(target=initGQLServer)
            server.append(gql_server)

        if "websocket" in config and config["websocket"]:
            logging.info("Starting Websocket Server on port 8765")
            print("[+] Starting Websocket Server on port 8765")
            websocket_server = Thread(target=initWebsocketServer)
            server.append(websocket_server)

        if "grpc" in config and config["grpc"]:
            logging.info("Starting GRPC Server on port 50051")
            print("[+] Starting GRPC Server on port 50051")
            grpc_server = ThreadedGRPCServer()
            server.append(grpc_server)

        for s in server:
            logging.debug("Starting one of the servers...")
            s.start()

        logging.info("All servers started. Client can now connect.")
        print("[+] All servers started. Client can now connect.")

        for s in server:
            logging.debug("Joining one of the server threads...")
            s.join()

        logging.info("All servers joined main thread. Goodbye!")
        print("[!] All servers joined main thread. Goodbye!")
        exit(1)
    else:
        # TODO: add configuration option that would allow exfiltration of files with encoded data rather than exclusively plaintext data

        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info("Starting in client mode")
        print("[+] Starting in client mode.")
        adjective = RandomWord()
        noun = RandomWord()
        title_adjective = adjective.word(include_parts_of_speech=["adjectives"])
        title_noun = noun.word(include_parts_of_speech=["nouns"])
        client_title = title_adjective + "_" + title_noun
        logging.info("Client Title: " + client_title)
        print("[+] Client Title: " + client_title)
        logging.info("Parsing configuration file")
        print("[.] Parsing configuration file")
        configOrErr = parseConfig(config)
        if isinstance(configOrErr, str):
            logging.error("Failed to parse client configuration file: " + configOrErr)
            print("Failed to parse client configuration file: " + configOrErr)
            exit(-1)

        config = configOrErr
        logging.info("Generating fake data")
        generated = byte_to_string(generateFakeData(config, client_title))
        j = json.dumps(generated)
        f = open("generated_testcases.json", "w+").write(j)
        logging.info("Generated fake data. Starting exfiltration.")
        exfil_results = asyncio.run(runExfil(config, generated))
        logging.info("Exfiltration complete")

        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        final_object = {
            "title": client_title,
            "start_time": start_time,
            "end_time": end_time,
            "config": config,
            "generated": generated,
            "exfil_results": exfil_results
        }

        fojson = json.dumps(final_object)
        f = open("exfil_results.json", "w+").write(fojson)

if __name__ == "__main__":
    print("DLP Testing Automation")
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', help='Start in server mode')
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument ('-v', action='store_true', help='Verbose logging mode')

    args = parser.parse_args()

    if (args.config == "" or args.config is None):
        print("[!] No configuration file provided. Exiting.")
        exit(0)

    main(server=args.s, config=args.config, verbose=args.v)

