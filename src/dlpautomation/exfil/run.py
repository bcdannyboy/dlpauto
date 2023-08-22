import logging

from exfil.runners import run_dns, run_email, run_git, run_graphql, run_grpc, run_http, run_icmp, run_rpc, run_s3, run_ssh, run_tcp, run_udp, run_websockets

async def runExfil(config, data):
    logging.debug("Running runExfil()")
    all_data_test_cases = []
    for encoding_scheme in data["data"]:
        for testcasedata in data["data"][encoding_scheme]:
            tcd = testcasedata["data"]
            all_data_test_cases.extend(tcd)

    results = []
    data_results = 0
    file_results = 0
    logging.info("Running exfil tests for " + str(len(all_data_test_cases)) + " data test cases")
    print("[.] Running exfil tests for " + str(len(all_data_test_cases)) + " data test cases")
    for testcase in all_data_test_cases:
        if "dns" in config["exfil"]:
            location = "TXT"
            port = 53
            if "location" in config["exfil"]["dns"] and config["exfil"]["dns"]["location"].upper() in ["A", "TXT", "AAAA", "*"]:
                location = config["exfil"]["dns"]["location"].upper()
            if "port" in config["exfil"]["dns"] and config["exfil"]["dns"]["port"] != "" and config["exfil"]["dns"]["port"] != None and isinstance(config["exfil"]["dns"]["port"], int) and config["exfil"]["dns"]["port"] > 0 and config["exfil"]["dns"]["port"] < 65535:
                port = config["exfil"]["dns"]["port"]
            logging.debug("Running DNS exfil test for data test case, location = " + location)
            ret = run_dns(config, testcase, location, port=port)
            logging.debug("Finished running DNS exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "email" in config["exfil"]:
            location = "body"
            if "location" in config["exfil"]["email"] and config["exfil"]["email"]["location"].upper() in ["A", "TXT", "AAAA", "*"]:
                location = config["exfil"]["email"]["location"].upper()
            logging.debug("Running Email exfil test for data test case, location = " + location)
            ret = run_email(config, testcase, location)
            logging.debug("Finished running Email exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "git" in config["exfil"]:
            logging.debug("Running Git exfil test for data test case")
            ret = run_git(config, testcase)
            logging.debug("Finished running Git exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "s3" in config["exfil"]:
            logging.debug("Running s3 exfil test for data test case")
            ret = run_s3(config, testcase)
            logging.debug("Finished running s3 exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "graphql" in config["exfil"]:
            logging.debug("Running GraphQL exfil test for data test case")
            ret = run_graphql(config, testcase)
            logging.debug("Finished running GraphQL exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "websockets" in config["exfil"]:
            logging.debug("Running Websockets exfil test for data test case")
            ret = await run_websockets(config, testcase)
            logging.debug("Finished running Websockets exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "grpc" in config["exfil"]:
            logging.debug("Running gRPC exfil test for data test case")
            ret = run_grpc(config, testcase)
            logging.debug("Finished running gRPC exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "http" in config["exfil"]:
            logging.debug("Running HTTP exfil test for data test case")
            ret = run_http(config, testcase)
            logging.debug("Finished running HTTP exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "icmp" in config["exfil"]:
            logging.debug("Running ICMP exfil test for data test case")
            ret = run_icmp(config, testcase)
            logging.debug("Finished running ICMP exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "rpc" in config["exfil"]:
            logging.debug("Running RPC exfil test for data test case")
            ret = run_rpc(config, testcase)
            logging.debug("Finished running RPC exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "ssh" in config["exfil"]:
            logging.debug("Running SSH exfil test for data test case")
            ret = run_ssh(config, testcase)
            logging.debug("Finished running SSH exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "tcp" in config["exfil"]:
            logging.debug("Running TCP exfil test for data test case")
            ret = run_tcp(config, testcase)
            logging.debug("Finished running TCP exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "udp" in config["exfil"]:
            logging.debug("Running UDP exfil test for data test case")
            ret = run_udp(config, testcase)
            logging.debug("Finished running UDP exfil test for data test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

    data_results = len(results)
    logging.info("Finished running exfil tests for " + str(len(all_data_test_cases)) + " data test cases. Got " + str(data_results) + " results.")
    print("[+] Finished running exfil tests for " + str(len(all_data_test_cases)) + " data test cases. Got " + str(data_results) + " results.")

    logging.info("Running exfil tests for " + str(len(data["files"])) + " file test cases")
    print("[.] Running exfil tests for " + str(len(data["files"])) + " file test cases")
    for testcase in data["files"]:
        if "dns" in config["exfil"]:
            location = "TXT"
            port = 53
            if "location" in config["exfil"]["dns"] and config["exfil"]["dns"]["location"].upper() in ["A", "TXT", "AAAA", "*"]:
                location = config["exfil"]["dns"]["location"].upper()

            if "port" in config["exfil"]["dns"] and isinstance(config["exfil"]["dns"]["port"], int) and config["exfil"]["dns"]["port"] > 0 and config["exfil"]["dns"]["port"] < 65536:
                port = config["exfil"]["dns"]["port"]

            logging.debug("Running DNS exfil test for " + testcase["type"] + " file test case, location = " + location)
            ret = run_dns(config, testcase["path"], location, file=True, port=port)
            logging.debug("Finished running DNS exfil test for " + testcase["type"] + " file test case, location = " + location + ". Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "ftp" in config["exfil"]:
            logging.debug("Running FTP exfil test for " + testcase["type"] + " file test case")
            ret = run_tcp(config, testcase["path"])
            logging.debug("Finished running FTP exfil test for " + testcase["type"] + " file test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "email" in config["exfil"]:
            logging.debug("Running email exfil test for " + testcase["type"] + " file test case")
            ret = run_email(config, testcase["path"], "attachment", file=True)
            logging.debug("Finished running email exfil test for " + testcase["type"] + " file test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "git" in config["exfil"]:
            logging.debug("Running Git exfil test for " + testcase["type"] + " file test case")
            ret = run_git(config, testcase["path"], file=True)
            logging.debug("Finished running Git exfil test for " + testcase["type"] + " file test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "s3" in config["exfil"]:
            logging.debug("Running s3 exfil test for " + testcase["type"] + " file test case")
            ret = run_s3(config, testcase["path"], file=True)
            logging.debug("Finished running s3 exfil test for " + testcase["type"] + " file test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "graphql" in config["exfil"]:
            logging.debug("Running GraphQL exfil test for " + testcase["type"] + " file test case")
            ret = run_graphql(config, testcase["path"], file=True)
            logging.debug("Finished running GraphQL exfil test for " + testcase["type"] + " file test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "websockets" in config["exfil"]:
            logging.debug("Running WebSockets exfil test for " + testcase["type"] + " file test case")
            ret = await run_websockets(config, testcase["path"], file=True)
            logging.debug("Finished running WebSockets exfil test for " + testcase["type"] + " file test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "grpc" in config["exfil"]:
            logging.debug("Running gRPC exfil test for " + testcase["type"] + " file test case")
            ret = run_grpc(config, testcase["path"], file=True)
            logging.debug("Finished running gRPC exfil test for " + testcase["type"] + " file test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "rpc" in config["exfil"]:
            logging.debug("Running RPC exfil test for " + testcase["type"] + " file test case")
            ret = run_rpc(config, testcase["path"], file=True)
            logging.debug("Finished running RPC exfil test for " + testcase["type"] + " file test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

        if "ssh" in config["exfil"]:
            logging.debug("Running SSH exfil test for " + testcase["type"] + " file test case")
            ret = run_ssh(config, testcase["path"], file=True)
            logging.debug("Finished running SSH exfil test for " + testcase["type"] + " file test case. Got " + str(len(ret)) + " results")
            results.extend(ret)

    file_results = len(results) - data_results
    logging.info("Finished running exfil tests for " + str(len(data["files"])) + " file test cases. Got " + str(file_results) + " results.")
    print("[+] Finished running exfil tests for " + str(len(data["files"])) + " file test cases. Got " + str(file_results) + " results.")
    logging.info("Finished running exfil tests for " + str(len(all_data_test_cases) + len(data["files"])) + " test cases. Got " + str(len(results)) + " results.")
    print("[+] Finished running exfil tests for " + str(len(all_data_test_cases) + len(data["files"])) + " test cases. Got " + str(len(results)) + " results.")
    return results

