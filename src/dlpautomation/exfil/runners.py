from exfil.aws.exfil import ExfilS3
from exfil.dns.exfil import ExfilDNS
from exfil.email.exfil import exfilEmail
from exfil.ftp.exfil import exfilFTP
from exfil.git.exfil import exfiltrate_to_github
from exfil.http_advanced.graphql.exfil import ExfilGraphQL
from exfil.http_advanced.grpc.exfil import ExfilGRPC
from exfil.http_advanced.websocket.exfil import ExfilWebSocket
from exfil.http_standard.exfil import ExfilHTTP
from exfil.icmp.exfil import exfilICMP
from exfil.rpc.exfil import exfilRPC
from exfil.ssh.exfil import exfilSSH
from exfil.tcp.exfil import ExfilTCP
from exfil.udp.exfil import exfilUDP
import logging

# can be file or data testcases
def run_dns(config, testcase, location, file = False, port=53):
    logging.debug("Running run_dns(location = %s, file = %s)" % (location, file))
    ret = []
    if "server" in config["exfil"]["dns"] and isinstance(config["exfil"]["dns"]["server"], str):
        server = config["exfil"]["dns"]["server"]
        logging.debug("DNS server specified in config file: %s" % server)
        if location == "*":
            logging.debug("Running DNS exfiltration for all locations")
            ret.append({
                "method": "DNS",
                "location": "TXT",
                "testcase": testcase,
                "ret": ExfilDNS(server, "TXT", testcase, file, port)
            })
            logging.debug("Finished TXT DNS exfiltration")
            ret.append({
                "method": "DNS",
                "location": "A",
                "testcase": testcase,
                "ret": ExfilDNS(server, "A", testcase, file, port)
            })
            logging.debug("Finished A DNS exfiltration")
            ret.append({
                "method": "DNS",
                "location": "AAAA",
                "testcase": testcase,
                "ret": ExfilDNS(server, "AAAA", testcase, file, port)
            })
            logging.debug("Finished AAAA DNS exfiltration")
            return ret
        elif location == "A":
            logging.debug("Running A DNS exfiltration")
            ret.append({
                "method": "DNS",
                "location": "A",
                "testcase": testcase,
                "ret": ExfilDNS(server, "A", testcase, file, port)
            })
            logging.debug("Finished A DNS exfiltration")
        elif location == "AAAA":
            logging.debug("Running AAAA DNS exfiltration")
            ret.append({
                "method": "DNS",
                "location": "AAAA",
                "testcase": testcase,
                "ret": ExfilDNS(server, "AAAA", testcase, file, port)
            })
            logging.debug("Finished AAAA DNS exfiltration")
        elif location == "TXT":
            logging.debug("Running TXT DNS exfiltration")
            ret.append({
                "method": "DNS",
                "location": "TXt",
                "testcase": testcase,
                "ret": ExfilDNS(server, "TXT", testcase, file, port)
            })
            logging.debug("Finished TXT DNS exfiltration")
        else:
            logging.warning("Invalid DNS location specified. Skipping DNS Exfiltration.")
            print("[-] Invalid DNS location specified. Skipping DNS Exfiltration.")

        logging.debug("run_dns returning")
        return ret
    else:
        logging.warning("DNS server not specified in config file. Skipping DNS Exfiltration.")
        print("[-] DNS server not specified in config file. Skipping DNS Exfiltration.")
        return ret

# can be file or data testcases
def run_email(config, testcase, location, file = False):
    logging.debug("Running run_email(location = %s, file = %s)" % (location, file))
    ret = []
    server = ""
    port = 25
    to = ""
    e_from = "dlp@dlp.com"
    from_password = ""
    tls = False
    if "server" in config["exfil"]["email"] and isinstance(config["exfil"]["email"]["server"], str):
        logging.debug("Email server specified in config file: %s" % config["exfil"]["email"]["server"])
        server = config["exfil"]["email"]["server"]
    else:
        logging.warning("Invalid Email Server specified. Skipping Email Exfiltration.")
        print("[-] Invalid Email Server specified. Skipping Email Exfiltration.")
        return []

    if "port" in config["exfil"]["email"] and isinstance(config["exfil"]["email"]["port"], int):
        logging.debug("Email port specified in config file: %s" % config["exfil"]["email"]["port"])
        port = config["exfil"]["email"]["port"]
    else:
        logging.warning("Invalid Email Port specified. Defaulting to 25.")
        print("[-] Invalid Email Port specified. Defaulting to 25.")

    if "to" in config["exfil"]["email"] and isinstance(config["exfil"]["email"]["to"], str):
        logging.debug("Email To specified in config file: %s" % config["exfil"]["email"]["to"])
        to = config["exfil"]["email"]["to"]
    else:
        logging.warning("Invalid Email To specified. Skipping Email Exfiltration.")
        print("[-] Invalid Email To specified. Skipping Email Exfiltration.")
        return []

    if "from" in config["exfil"]["email"] and isinstance(config["exfil"]["email"]["from"], str):
        logging.debug("Email From specified in config file: %s" % config["exfil"]["email"]["from"])
        e_from = config["exfil"]["email"]["from"]
    else:
        logging.warning("Invalid Email From specified. Defaulting to dlp@dlp.com")
        print("[-] Invalid Email From specified. Defaulting to dlp@dlp.com")

    if "from_password" in config["exfil"]["email"] and isinstance(config["exfil"]["email"]["from_password"], str):
        logging.debug("Email From Password specified in config file: %s" % config["exfil"]["email"]["from_password"])
        from_password = config["exfil"]["email"]["from_password"]
    else:
        logging.warning("Invalid Email From Password specified. Defaulting to no password.")
        print("[-] Invalid Email From Password specified. Defaulting to no password.")

    if "tls" in config["exfil"]["email"] and isinstance(config["exfil"]["email"]["tls"], bool):
        logging.debug("Email TLS specified in config file: %s" % config["exfil"]["email"]["tls"])
        tls = config["exfil"]["email"]["tls"]
    else:
        logging.warning("Invalid Email TLS specified. Defaulting to False.")
        print("[-] Invalid Email TLS specified. Defaulting to False.")

    if location == "*":
        logging.debug("Running Email exfiltration with location = *")
        ret.append({
            "method": "Email",
            "location": "SUBJECT",
            "testcase": testcase,
            "ret": exfilEmail(server, port, to, e_from, from_password, "subject", testcase, tls)
        })
        logging.debug("Finished SUBJECT Email exfiltration")
        ret.append({
            "method": "Email",
            "location": "BODY",
            "testcase": testcase,
            "ret": exfilEmail(server, port, to, e_from, from_password, "body", testcase, tls)
        })
        logging.debug("Finished BODY Email exfiltration")
        if file:
            ret.append({
                "method": "Email",
                "location": "ATTACHMENT",
                "testcase": testcase,
                "ret": exfilEmail(server, port, to, e_from, from_password, "attachment", testcase, tls)
            })
            logging.debug("Finished ATTACHMENT Email exfiltration")
    elif location == "SUBJECT":
        logging.debug("Running SUBJECT Email exfiltration")
        ret.append({
            "method": "Email",
            "location": "SUBJECT",
            "testcase": testcase,
            "ret": exfilEmail(server, port, to, e_from, from_password, "subject", testcase, tls)
        })
        logging.debug("Finished SUBJECT Email exfiltration")
    elif location == "BODY":
        logging.debug("Running BODY Email exfiltration")
        ret.append({
            "method": "Email",
            "location": "BODY",
            "testcase": testcase,
            "ret": exfilEmail(server, port, to, e_from, from_password, "body", testcase, tls)
        })
        logging.debug("Finished BODY Email exfiltration")
    elif location == "ATTACHMENT" and file:
        logging.debug("Running ATTACHMENT Email exfiltration")
        ret.append({
                "method": "Email",
                "location": "ATTACHMENT",
                "testcase": testcase,
                "ret": exfilEmail(server, port, to, e_from, from_password, "attachment", testcase, tls)
            })
        logging.debug("Finished ATTACHMENT Email exfiltration")

    logging.debug("Finished Email exfiltration")
    return ret

# can only be file testcases
def run_ftp(config, testcase):
    logging.debug("running run_ftp")
    ret = []
    server = ""
    directory = ""
    username = "anonymous"
    password = ""
    tls = False

    if "server" in config["exfil"]["ftp"] and isinstance(config["exfil"]["ftp"]["server"], str):
        logging.debug("FTP server specified in config file: %s" % config["exfil"]["ftp"]["server"])
        server = config["exfil"]["ftp"]["server"]
    else:
        logging.warning("Invalid FTP Server specified. Skipping FTP Exfiltration.")
        print("[-] Invalid FTP Server specified. Skipping FTP Exfiltration.")
        return []

    if "directory" in config["exfil"]["ftp"] and isinstance(config["exfil"]["ftp"]["directory"], str):
        logging.debug("FTP directory specified in config file: %s" % config["exfil"]["ftp"]["directory"])
        directory = config["exfil"]["ftp"]["directory"]
    else:
        logging.warning("Invalid FTP Directory specified. Defaulting to /")
        print("[-] Invalid FTP Directory specified. Defaulting to /")
        return []

    if "username" in config["exfil"]["ftp"] and isinstance(config["exfil"]["ftp"]["username"], str):
        logging.debug("FTP username specified in config file: %s" % config["exfil"]["ftp"]["username"])
        username = config["exfil"]["ftp"]["username"]
    else:
        logging.warning("Invalid FTP Username specified. Defaulting to 'anonymous'.")
        print("[-] Invalid FTP Username specified. Defaulting to 'anonymous'.")

    if "password" in config["exfil"]["ftp"] and isinstance(config["exfil"]["ftp"]["password"], str):
        logging.debug("FTP password specified in config file: %s" % config["exfil"]["ftp"]["password"])
        password = config["exfil"]["ftp"]["password"]
    else:
        logging.warning("Invalid FTP Password specified. Defaulting to no password.")
        print("[-] Invalid FTP Password specified. Defaulting to no password.")

    if "tls" in config["exfil"]["ftp"] and isinstance(config["exfil"]["ftp"]["tls"], bool):
        logging.debug("FTP TLS specified in config file: %s" % config["exfil"]["ftp"]["tls"])
        tls = config["exfil"]["ftp"]["tls"]
    else:
        logging.warning("Invalid FTP TLS specified. Defaulting to False.")
        print("[-] Invalid FTP TLS specified. Defaulting to False.")

    ret.append({
        "method": "FTP",
        "location": directory,
        "testcase": testcase,
        "ret": exfilFTP(server, directory, testcase, tls, username, password)
    })

    logging.debug("Finished FTP exfiltration")
    return ret

# can be file or data testcase
def run_git(config, testcase, file = False):
    logging.debug("running run_git(file=%s)" % str(file))
    ret = []
    token = []
    owner = []
    repo = []
    path = []

    if "token" in config["exfil"]["git"] and isinstance(config["exfil"]["git"]["token"], str):
        logging.debug("Git token specified in config file: %s" % config["exfil"]["git"]["token"])
        token = config["exfil"]["git"]["token"]
    else:
        logging.warning("Invalid Git Token specified. Skipping Git Exfiltration.")
        print("[-] Invalid Git Token specified. Skipping Git Exfiltration.")
        return []

    if "owner" in config["exfil"]["git"] and isinstance(config["exfil"]["git"]["owner"], str):
        logging.debug("Git owner specified in config file: %s" % config["exfil"]["git"]["owner"])
        owner = config["exfil"]["git"]["owner"]
    else:
        logging.warning("Invalid Git Owner specified. Skipping Git Exfiltration.")
        print("[-] Invalid Git Owner specified. Skipping Git Exfiltration.")
        return []

    if "repo" in config["exfil"]["git"] and isinstance(config["exfil"]["git"]["repo"], str):
        logging.debug("Git repo specified in config file: %s" % config["exfil"]["git"]["repo"])
        repo = config["exfil"]["git"]["repo"]
    else:
        logging.warning("Invalid Git Repo specified. Skipping Git Exfiltration.")
        print("[-] Invalid Git Repo specified. Skipping Git Exfiltration.")
        return []

    if "path" in config["exfil"]["git"] and isinstance(config["exfil"]["git"]["path"], str):
        logging.debug("Git path specified in config file: %s" % config["exfil"]["git"]["path"])
        path = config["exfil"]["git"]["path"]
    else:
        logging.warning("Invalid Git Path specified. Skipping Git Exfiltration.")
        print("[-] Invalid Git Path specified. Skipping Git Exfiltration.")
        return []

    ret.append({
        "method": "FTP",
        "location": repo + ":" + path,
        "testcase": testcase,
        "ret": exfiltrate_to_github(token, owner, repo, path, testcase, file)
    })

    logging.debug("Finished Git exfiltration")
    return ret

# can be file or data testcase
def run_graphql(config, testcase, file = False):
    logging.debug("running run_graphql(file=%s)" % str(file))
    ret = []
    url = ""
    if "url" in config["exfil"]["graphql"] and isinstance(config["exfil"]["graphql"]["url"], str):
        logging.debug("GraphQL URL specified in config file: %s" % config["exfil"]["graphql"]["url"])
        url = config["exfil"]["graphql"]["url"]
    else:
        logging.warning("Invalid GraphQL URL specified. Skipping GraphQL Exfiltration.")
        print("[-] Invalid GraphQL URL specified. Skipping GraphQL Exfiltration.")
        return []

    ret.append({
        "method": "GraphQL",
        "location": url,
        "testcase": testcase,
        "ret": ExfilGraphQL(url, testcase, file)
    })

    logging.debug("Finished GraphQL exfiltration")
    return ret

# can be file or data testcase
async def run_websockets(config, testcase, file = False):
    logging.debug("running run_websockets(file=%s)" % str(file))
    ret = []
    url = ""
    if "url" in config["exfil"]["websockets"] and isinstance(config["exfil"]["websockets"]["url"], str):
        logging.debug("websockets URL specified in config file: %s" % config["exfil"]["websockets"]["url"])
        url = config["exfil"]["websockets"]["url"]
        if not url.startswith(('ws://', 'wss://')):
            logging.debug("WebSocket URI scheme missing. Prepending ws:// to the URL.")
            url = 'ws://' + url
    else:
        logging.warning("Invalid websockets URL specified. Skipping websockets Exfiltration.")
        print("[-] Invalid websockets URL specified. Skipping websockets Exfiltration.")
        return []

    ret.append({
        "method": "WebSockets",
        "location": url,
        "testcase": testcase,
        "ret": await ExfilWebSocket(url, testcase, file)
    })

    logging.debug("Finished WebSockets exfiltration")
    return ret


# can be file or data testcase
def run_grpc(config, testcase, file = False):
    logging.debug("running run_grpc(file=%s)" % str(file))
    ret = []
    server = ""
    port = ""
    if "server" in config["exfil"]["grpc"] and isinstance(config["exfil"]["grpc"]["server"], str):
        logging.debug("gRPC Server specified in config file: %s" % config["exfil"]["grpc"]["server"])
        server = config["exfil"]["grpc"]["server"]
    else:
        logging.warning("Invalid gRPC Server specified. Skipping gRPC Exfiltration.")
        print("[-] Invalid gRPC Server specified. Skipping gRPC Exfiltration.")
        return []

    if "port" in config["exfil"]["grpc"] and isinstance(config["exfil"]["grpc"]["port"], str):
        logging.debug("gRPC Port specified in config file: %s" % config["exfil"]["grpc"]["port"])
        port = config["exfil"]["grpc"]["port"]
    else:
        logging.warning("Invalid gRPC Port specified. Skipping gRPC Exfiltration.")
        print("[-] Invalid gRPC Port specified. Skipping gRPC Exfiltration.")
        return []

    ret.append({
        "method": "gRPC",
        "location": server + ":" + port,
        "testcase": testcase,
        "ret": ExfilGRPC(server, port, testcase, file)
    })

    logging.debug("Finished gRPC exfiltration")
    return ret

# can only be a data testcase. TODO: add file support
def run_http(config, testcase):
    logging.debug("running run_http()")
    ret = []
    url = ""
    method = "GET"
    location = "urlparam"
    http_port = 80
    https_port = 443

    if "url" in config["exfil"]["http"] and isinstance(config["exfil"]["http"]["url"], str):
        logging.debug("HTTP URL specified in config file: %s" % config["exfil"]["http"]["url"])
        url = config["exfil"]["http"]["url"]
    else:
        logging.warning("Invalid HTTP URL specified. Skipping HTTP Exfiltration.")
        print("[-] Invalid HTTP URL specified. Skipping HTTP Exfiltration.")
        return []

    if "http_port" in config["exfil"]["http"] and isinstance(config["exfil"]["http"]["http_port"], int):
        logging.debug("HTTP Port specified in config file: %s" % config["exfil"]["http"]["http_port"])
        http_port = config["exfil"]["http"]["http_port"]
    else:
        logging.warning("Invalid HTTP Port specified. Defaulting to 80.")

    if "https_port" in config["exfil"]["http"] and isinstance(config["exfil"]["http"]["https_port"], int):
        logging.debug("HTTPS Port specified in config file: %s" % config["exfil"]["http"]["https_port"])
        https_port = config["exfil"]["http"]["https_port"]
    else:
        logging.warning("Invalid HTTPS Port specified. Defaulting to 443.")

    if "method" in config["exfil"]["http"] and isinstance(config["exfil"]["http"]["method"], str):
        if config["exfil"]["http"]["method"].upper() in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "*"]:
            logging.debug("HTTP Method specified in config file: %s" % config["exfil"]["http"]["method"])
            method = config["exfil"]["http"]["method"].upper()
        else:
            logging.warning("Invalid HTTP Method specified. Defaulting to GET.")
            print("[-] Invalid HTTP Method specified. Defaulting to GET.")
    else:
        logging.warning("Invalid HTTP Method specified. Defaulting to GET.")
        print("[-] Invalid HTTP Method specified. Defaulting to GET.")

    if "location" in config["exfil"]["http"] and isinstance(config["exfil"]["http"]["location"], str):
        if config["exfil"]["http"]["location"].lower() in ["urlparam", "urlquery", "header", "body", "cookies", "*"]:
            logging.debug("HTTP Location specified in config file: %s" % config["exfil"]["http"]["location"])
            location = config["exfil"]["http"]["location"].lower()
        else:
            logging.warning("Invalid HTTP Location specified. Defaulting to urlparam.")
            print("[-] Invalid HTTP Location specified. Defaulting to urlparam.")
    else:
        logging.warning("Invalid HTTP Location specified. Defaulting to urlparam.")
        print("[-] Invalid HTTP Location specified. Defaulting to urlparam.")

    if method == "*" and location == "*":
        logging.debug("HTTP Method and Location are both *. Running all combinations.")
        for meth in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
            for loc in ["urlparam", "urlquery", "header", "body", "cookies"]:
                logging.debug("Running HTTP exfiltration for method %s and location %s" % (meth, loc))
                ret.append({
                    "method": "HTTP",
                    "location": "http://" + meth + " " + url + ":" + str(http_port) + " - " + loc,
                    "testcase": testcase,
                    "ret": ExfilHTTP("http://" + url + ":" + str(http_port) , meth, loc, testcase)
                })
                ret.append({
                    "method": "HTTPS",
                    "location": "https://" + meth + " " + url + ":" + str(https_port) + " - " + loc,
                    "testcase": testcase,
                    "ret": ExfilHTTP("https://" + url + ":" + str(https_port), meth, loc, testcase)
                })
                logging.debug("Finished HTTP exfiltration for method %s and location %s" % (meth, loc))
    elif method == "*" and location != "*":
        logging.debug("HTTP Method is * and Location is not *. Running all methods.")
        for meth in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
            logging.debug("Running HTTP exfiltration for method %s and location %s" % (meth, location))
            ret.append({
                "method": "HTTP",
                "location": "http://" + meth + " " + url + ":" + str(http_port) + " - " + location,
                "testcase": testcase,
                "ret": ExfilHTTP("http://" + url + ":" + str(http_port) , meth, location, testcase)
            })
            ret.append({
                "method": "HTTPS",
                "location": "https://" + meth + " " + url + ":" + str(https_port) + " - " + loc,
                "testcase": testcase,
                "ret": ExfilHTTP("https://" + url + ":" + str(https_port), meth, loc, testcase)
            })
            logging.debug("Finished HTTP exfiltration for method %s and location %s" % (meth, location))
    elif method != "*" and location == "*":
        logging.debug("HTTP Method is not * and Location is *. Running all locations.")
        for loc in ["urlparam", "urlquery", "header", "body", "cookies"]:
            logging.debug("Running HTTP exfiltration for method %s and location %s" % (method, loc))
            ret.append({
                "method": "HTTP",
                "location": "http://" + method + " " + url + ":" + str(http_port) + " - " + loc,
                "testcase": testcase,
                "ret": ExfilHTTP("http://" + url + ":" + str(http_port) , method, loc, testcase)
            })
            ret.append({
                "method": "HTTPS",
                "location": "https://" + meth + " " + url + ":" + str(https_port) + " - " + loc,
                "testcase": testcase,
                "ret": ExfilHTTP("https://" + url + ":" + str(https_port), meth, loc, testcase)
            })
            logging.debug("Finished HTTP exfiltration for method %s and location %s" % (method, loc))
    else:
        logging.debug("HTTP Method and Location are both specified. Running specified method and location.")
        ret.append({
                "method": "HTTP",
                "location": "http://" + method + " " + url + ":" + str(http_port) + " - " + location,
                "testcase": testcase,
                "ret": ExfilHTTP("http://" + url + ":" + str(http_port) , method, location, testcase)
            })
        ret.append({
                "method": "HTTP",
                "location": "https://" + method + " " + url + ":" + str(https_port) + " - " + location,
                "testcase": testcase,
                "ret": ExfilHTTP("https://" + url + ":" + str(https_port), method, location, testcase)
            })
        logging.debug("Finished HTTP exfiltration for method %s and location %s" % (method, location))

    logging.debug("Finished HTTP exfiltration")
    return ret

# can only be a data testcase.
def run_icmp(config, testcase):
    logging.debug("running run_icmp()")
    ret = []
    ip = ""
    if "ip" in config["exfil"]["icmp"] and isinstance(config["exfil"]["icmp"]["ip"], str):
        logging.debug("ICMP IP specified in config file: %s" % config["exfil"]["icmp"]["ip"])
        ip = config["exfil"]["icmp"]["ip"]
    else:
        logging.warning("Invalid ICMP IP specified. Skipping ICMP Exfiltration.")
        print("[-] Invalid ICMP IP specified. Skipping ICMP Exfiltration.")
        return []

    ret.append({
        "method": "ICMP",
        "location": ip,
        "testcase": testcase,
        "ret": exfilICMP(ip, testcase)
    })
    logging.debug("Finished ICMP exfiltration")
    return ret

# can be a data or file testcase
def run_rpc(config, testcase, file = False):
    logging.debug("running run_rpc()")
    ret = []
    server = []
    port = []

    if "server" in config["exfil"]["rpc"] and isinstance(config["exfil"]["rpc"]["server"], list):
        logging.debug("RPC Server specified in config file: %s" % config["exfil"]["rpc"]["server"])
        server = config["exfil"]["rpc"]["server"]
    else:
        logging.warning("Invalid RPC Server specified. Skipping RPC Exfiltration.")
        print("[-] Invalid RPC Server specified. Skipping RPC Exfiltration.")
        return []

    if "port" in config["exfil"]["rpc"] and isinstance(config["exfil"]["rpc"]["port"], list):
        logging.debug("RPC Port specified in config file: %s" % config["exfil"]["rpc"]["port"])
        port = config["exfil"]["rpc"]["port"]
    else:
        logging.warning("Invalid RPC Port specified. Skipping RPC Exfiltration.")
        print("[-] Invalid RPC Port specified. Skipping RPC Exfiltration.")
        return []

    ret.append({
        "method": "RPC",
        "location": server + ":" + port,
        "testcase": testcase,
        "ret": exfilRPC(server, port, testcase, file)
    })

    logging.debug("Finished RPC exfiltration")
    return ret

# can be a data or file testcase
def run_ssh(config, testcase, file = False):
    logging.debug("running run_ssh(file = %s)" % file)
    ret = []
    server = ""
    port = ""
    username = ""
    password = ""

    if "server" in config["exfil"]["ssh"] and isinstance(config["exfil"]["ssh"]["server"], str):
        logging.debug("SSH Server specified in config file: %s" % config["exfil"]["ssh"]["server"])
        server = config["exfil"]["ssh"]["server"]
    else:
        logging.warning("Invalid SSH Server specified. Skipping SSH Exfiltration.")
        print("[-] Invalid SSH Server specified. Skipping SSH Exfiltration.")
        return []

    if "port" in config["exfil"]["ssh"] and isinstance(config["exfil"]["ssh"]["port"], str):
        logging.debug("SSH Port specified in config file: %s" % config["exfil"]["ssh"]["port"])
        port = config["exfil"]["ssh"]["port"]
    else:
        logging.warning("Invalid SSH Port specified. Skipping SSH Exfiltration.")
        print("[-] Invalid SSH Port specified. Skipping SSH Exfiltration.")
        return []

    if "username" in config["exfil"]["ssh"] and isinstance(config["exfil"]["ssh"]["username"], str):
        logging.debug("SSH Username specified in config file: %s" % config["exfil"]["ssh"]["username"])
        username = config["exfil"]["ssh"]["username"]
    else:
        logging.warning("Invalid SSH Username specified. Skipping SSH Exfiltration.")
        print("[-] Invalid SSH Username specified. Skipping SSH Exfiltration.")
        return []

    if "password" in config["exfil"]["ssh"] and isinstance(config["exfil"]["ssh"]["password"], str):
        logging.debug("SSH Password specified in config file: %s" % config["exfil"]["ssh"]["password"])
        password = config["exfil"]["ssh"]["password"]
    else:
        logging.warning("Invalid SSH Password specified. Skipping SSH Exfiltration.")
        print("[-] Invalid SSH Password specified. Skipping SSH Exfiltration.")
        return []

    ret.append({
        "method": "SSH",
        "location": username + ":" + password + "@" + server + ":" + port,
        "testcase": testcase,
        "ret": exfilSSH(server, port, username, password, testcase, file)
    })

    logging.debug("Finished SSH exfiltration")
    return ret

# can only be data testcase. TODO: add file support
def run_tcp(config, testcase):
    logging.debug("running run_tcp()")
    ret = []
    ip = ""
    port = ""

    if "ip" in config["exfil"]["tcp"] and isinstance(config["exfil"]["tcp"]["ip"], str):
        logging.debug("TCP IP specified in config file: %s" % config["exfil"]["tcp"]["ip"])
        ip = config["exfil"]["tcp"]["ip"]
    else:
        logging.warning("Invalid TCP IP specified. Skipping TCP Exfiltration.")
        print("[-] Invalid TCP IP specified. Skipping TCP Exfiltration.")
        return []

    if "port" in config["exfil"]["tcp"] and isinstance(config["exfil"]["tcp"]["port"], str):
        logging.debug("TCP Port specified in config file: %s" % config["exfil"]["tcp"]["port"])
        port = config["exfil"]["tcp"]["port"]
    else:
        logging.warning("Invalid TCP Port specified. Skipping TCP Exfiltration.")
        print("[-] Invalid TCP Port specified. Skipping TCP Exfiltration.")
        return []

    ret.append({
        "method": "TCP",
        "location": ip + ":" + port,
        "testcase": testcase,
        "ret": ExfilTCP(ip, port, testcase),
    })

    logging.debug("Finished TCP exfiltration")
    return ret

# can only be data testcase. TODO: add file support
def run_udp(config, testcase):
    logging.debug("running run_udp()")
    ret = []
    ip = ""
    port = ""

    if "ip" in config["exfil"]["udp"] and isinstance(config["exfil"]["udp"]["ip"], str):
        logging.debug("UDP IP specified in config file: %s" % config["exfil"]["udp"]["ip"])
        ip = config["exfil"]["udp"]["ip"]
    else:
        logging.warning("Invalid UDP IP specified. Skipping UDP Exfiltration.")
        print("[-] Invalid UDP IP specified. Skipping UDP Exfiltration.")
        return []

    if "port" in config["exfil"]["udp"] and isinstance(config["exfil"]["udp"]["port"], int):
        logging.debug("UDP Port specified in config file: %s" % config["exfil"]["udp"]["port"])
        port = config["exfil"]["udp"]["port"]
    else:
        logging.warning("Invalid UDP Port specified. Skipping UDP Exfiltration.")
        print("[-] Invalid UDP Port specified. Skipping UDP Exfiltration.")
        return []

    ret.append({
        "method": "UDP",
        "location": ip + ":" + str(port),
        "testcase": testcase,
        "ret": exfilUDP(ip, port, testcase),
    })

    logging.debug("Finished UDP exfiltration")
    return ret

# can be both data and file testcase
def run_s3(config, testcase, file = False):
    ret = []
    bucket = ""
    access_key_id = ""
    secret_access_token = ""
    session_token = ""
    username = ""
    password = ""

    if "bucket" in config["exfil"]["s3"] and isinstance(config["exfil"]["s3"]["bucket"], str):
        logging.debug("S3 Bucket specified in config file: %s" % config["exfil"]["s3"]["bucket"])
        bucket = config["exfil"]["s3"]["bucket"]
    else:
        logging.warning("Invalid S3 Bucket specified. Skipping S3 Exfiltration.")
        print("[-] Invalid S3 Bucket specified. Skipping S3 Exfiltration.")
        return []

    if "access_key_id" in config["exfil"]["s3"] and isinstance(config["exfil"]["s3"]["access_key_id"], str):
        logging.debug("S3 Access Key ID specified in config file: %s" % config["exfil"]["s3"]["access_key_id"])
        access_key_id = config["exfil"]["s3"]["access_key_id"]
    else:
        logging.warning("Invalid S3 Access Key ID specified. Defaulting to no access key ID.")
        print("[-] Invalid S3 Access Key ID specified. Defualting to no access key ID.")

    if "secret_access_token" in config["exfil"]["s3"] and isinstance(config["exfil"]["s3"]["secret_access_token"], str):
        logging.debug("S3 Secret Access Token specified in config file: %s" % config["exfil"]["s3"]["secret_access_token"])
        secret_access_token = config["exfil"]["s3"]["secret_access_token"]
    else:
        logging.warning("Invalid S3 Secret Access Token specified. Defaulting to no secret access token.")
        print("[-] Invalid S3 Secret Access Token specified. Defaulting to no secret access token.")

    if "session_token" in config["exfil"]["s3"] and isinstance(config["exfil"]["s3"]["session_token"], str):
        logging.debug("S3 Session Token specified in config file: %s" % config["exfil"]["s3"]["session_token"])
        session_token = config["exfil"]["s3"]["session_token"]
    else:
        logging.warning("Invalid S3 Session Token specified. Defaulting to no session token.")
        print("[-] Invalid S3 Session Token specified. Defaulting to no session token.")

    ret.append({
        "method": "AWS S3",
        "location": bucket,
        "testcase": testcase,
        "ret": ExfilS3(bucket, testcase, file, access_key_id, secret_access_token, session_token, username, password),
    })

    logging.debug("Finished S3 exfiltration")
    return ret