import logging
import os
import yaml

def parseConfig(configpath, server=False):
    if not os.path.exists(configpath):
        logging.error(f"The file '{configpath}' does not exist")
        return f"Error: The file '{configpath}' does not exist"
    else:
        try:
            with open(configpath, 'r') as file:
                # Load the YAML file
                data = yaml.safe_load(file)
                logging.debug(f"Loaded YAML file: {configpath}")
        except yaml.YAMLError as exc:
            logging.error(f"Error in YAML file: {exc}")
            return f"Error in YAML file: {exc}"

        # parse in server mode
        if server:
            logging.debug("Parsing in server mode")
            # Check if root key exists
            if "server" not in data:
                logging.error("Missing root key 'server'")
                return "Error: Missing root key 'server'"
            else:
                # Check if all servers are false or missing
                servers = data['server']
                if not any(servers.values()):
                    logging.error("All servers are false or missing")
                    return "Error: All servers are false or missing"
                else:
                    logging.debug("returning server config")
                    return servers
        else:
            # parse in client mode
            logging.debug("Parsing in client mode")
            keys = ["rawdata", "files", "encoding", "exfil"]
            for key in keys:
                if key not in data:
                    logging.error(f"Missing root key '{key}' in client configuration")
                    return f"Error: Missing root key '{key}' in client configuration"
            logging.debug("returning client config")
            return data
