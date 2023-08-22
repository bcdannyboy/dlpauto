import logging
import random
from encoding.encoding import aes_encrypt, ascii_encode, b64_encrypt, base16_encode, base32_encode, binary_encode, caesar_encrypt, fernet_encrypt, hex_encode, reverse_cipher, rot13_encode, url_encode, xor_crypt, zlib_compress
from generators.files import generateEML, generateExcel, generateHTML, generateJSONorYAML, generatePDF, generatePowerPoint, generateText, generateVisio, generateWord, generateXML, generateZIP
from generators.npi import getFakeBank, getFakeCCs, getFakeSSNs
from utils.strings import adjust_string_length


def generateFakeData(config, client_title):
    logging.info("Generating fake data")
    print("[.] Generating Data")
    fake_data = []
    if "fakecc" in config["rawdata"] and isinstance(config["rawdata"]["fakecc"], int) and config["rawdata"]["fakecc"] > 0:
        logging.debug("Generating fake credit card numbers")
        ccamt = config["rawdata"]["fakecc"]
        if "fakecc_justnumber" in config["rawdata"] and isinstance(config["rawdata"]["fakecc_justnumber"], bool) and config["rawdata"]["fakecc_justnumber"]:
            fake_data.append({
                "type": "cc-justnumber",
                "data": getFakeCCs(ccamt, True)
            })
            logging.debug("Generated " + str(ccamt) + " fake credit card numbers with just numbers")
        else:
            logging.debug("no formatting specified, using default formatting")
            fake_data.append({
                "type": "cc",
                "data": getFakeCCs(ccamt, False)
            })
            logging.debug("Generated " + str(ccamt) + " fake credit card numbers with formatting")

    if "fakessn" in config["rawdata"] and isinstance(config["rawdata"]["fakessn"], int) and config["rawdata"]["fakessn"] > 0:
        logging.debug("Generating fake social security numbers")
        ssnamt = config["rawdata"]["fakessn"]
        if "fakessn_seperator" in config["rawdata"] and isinstance(config["rawdata"]["fakessn_seperator"], str):
            fake_data.append({
                "type": "ssn",
                "data": getFakeSSNs(ssnamt, config["rawdata"]["fakessn_seperator"])
            })
            logging.debug("Generated " + str(ssnamt) + " fake social security numbers with seperator '" + config["rawdata"]["fakessn_seperator"] + "'")
        else:
            logging.debug("no seperator specified, using default '-'")
            fake_data.append({
                "type": "ssn",
                "data": getFakeSSNs(ssnamt)
            })
            logging.debug("Generated " + str(ssnamt) + " fake social security numbers with seperator '-'")

    if "fakebank" in config["rawdata"] and isinstance(config["rawdata"]["fakebank"], int) and config["rawdata"]["fakebank"] > 0:
        logging.debug("Generating fake bank account numbers")
        fakebankamt = config["rawdata"]["fakebank"]
        if "fakebank_type" in config["rawdata"] and isinstance(config["rawdata"]["fakebank_type"], str):
            fake_data.append({
                "type": "bank",
                "data": getFakeBank(fakebankamt, config["rawdata"]["fakebank_type"])
            })
            logging.debug("Generated " + str(fakebankamt) + " fake bank account numbers of type '" + config["rawdata"]["fakebank_type"] + "'")
        else:
            logging.debug("no type specified, using default 'swift11'")
            fake_data.append({
                "type": "bank",
                "data": getFakeBank(fakebankamt, "swift11")
            })
            logging.debug("Generated " + str(fakebankamt) + " fake bank account numbers of type 'swift11'")

    total_fake_data = 0
    for d in fake_data:
        total_fake_data += len(d["data"])

    logging.info("Generated " + str(len(fake_data)) + " fake data sets for a total of " + str(total_fake_data) + " data points.")
    print("[+] Generated " + str(len(fake_data)) + " fake data sets for a total of " + str(total_fake_data) + " data points.")

    logging.info("Generating fake files")
    print("[.] Generating Files")
    fake_files = []
    if "word" in config["files"] and isinstance(config["files"]["word"], bool) and config["files"]["word"]:
        logging.debug("Generating fake word documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake word document")
        fake_files.append({
            "type": "word",
            "npi": npi,
            "path": generateWord(client_title, npi)
        })
        logging.debug("Generated fake word document")

    if "excel" in config["files"] and isinstance(config["files"]["excel"], bool) and config["files"]["excel"]:
        logging.debug("Generating fake excel documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake excel document")
        fake_files.append({
            "type": "excel",
            "npi": npi,
            "path": generateExcel(client_title, npi)
        })
        logging.debug("Generated fake excel document")

    if "powerpoint" in config["files"] and isinstance(config["files"]["powerpoint"], bool) and config["files"]["powerpoint"]:
        logging.debug("Generating fake powerpoint documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake powerpoint document")
        fake_files.append({
            "type": "powerpoint",
            "npi": npi,
            "path": generatePowerPoint(client_title, npi)
        })
        logging.debug("Generated fake powerpoint document")

    if "visio" in config["files"] and isinstance(config["files"]["visio"], bool) and config["files"]["visio"]:
        # TODO: Fix visio generation, aspose.diagram doesnt work
        logging.warn("Visio generation is currently broken, skipping")
        # logging.debug("Generating fake visio documents")
        # npi = random.choice(fake_data)
        # logging.debug("Using " + npi["type"] + " data for fake visio document")
        # fake_files.append({
        #     "type": "visio",
        #     "npi": npi,
        #     "path": generateVisio(client_title, npi)
        # })
        # logging.debug("Generated fake visio document")

    if "eml" in config["files"] and isinstance(config["files"]["eml"], bool) and config["files"]["eml"]:
        logging.debug("Generating fake eml documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake eml document")
        fake_files.append({
            "type": "eml_body",
            "npi": npi,
            "path": generateEML(client_title, "body", npi)
        })
        logging.debug("Generated fake eml_body document")
        fake_files.append({
            "type": "eml_subject",
            "npi": npi,
            "path": generateEML(client_title, "subject", npi)
        })
        logging.debug("Generated fake eml_subject document")

    if "eml_attachment" in config["files"] and isinstance(config["files"]["eml_attachment"], bool) and config["files"]["eml_attachment"]:
        logging.debug("Generating fake eml_attachment documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake eml_attachment document")
        attachment_path = generateWord(client_title, npi)
        logging.debug("Generated fake word document for eml_attachment: " + attachment_path)

        fake_files.append({
            "type": "eml_attachment",
            "npi": npi,
            "path": generateEML(client_title, "", npi, attachment_path)
        })
        logging.debug("Generated fake eml_attachment document")

    if "txt" in config["files"] and isinstance(config["files"]["txt"], bool) and config["files"]["txt"]:
        logging.debug("Generating fake txt documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake txt document")
        fake_files.append({
            "type": "txt",
            "npi": npi,
            "path": generateText(client_title, npi)
        })
        logging.debug("Generated fake txt document")

    if "csv" in config["files"] and isinstance(config["files"]["csv"], bool) and config["files"]["csv"]:
        logging.debug("Generating fake csv documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake csv document")
        fake_files.append({
            "type": "csv",
            "npi": npi,
            "path": generateText(client_title, npi, csv=True)
        })
        logging.debug("Generated fake csv document")

    if "badformat" in config["files"] and isinstance(config["files"]["badformat"], bool) and config["files"]["badformat"]:
        logging.debug("Generating fake badformat documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake badformat document")
        fake_files.append({
            "type": "badformat",
            "npi": npi,
            "path": generateText(client_title, npi, bad=True)
        })
        logging.debug("Generated fake badformat document")

    if "json" in config["files"] and isinstance(config["files"]["json"], bool) and config["files"]["json"]:
        logging.debug("Generating fake json documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake json document")
        fake_files.append({
            "type": "json",
            "npi": npi,
            "path": generateJSONorYAML(client_title, npi)
        })
        logging.debug("Generated fake json document")

    if "yaml" in config["files"] and isinstance(config["files"]["yaml"], bool) and config["files"]["yaml"]:
        logging.debug("Generating fake yaml documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake yaml document")
        fake_files.append({
            "type": "yaml",
            "npi": npi,
            "path": generateJSONorYAML(client_title, npi, False)
        })
        logging.debug("Generated fake yaml document")

    if "pdf" in config["files"] and isinstance(config["files"]["pdf"], bool) and config["files"]["pdf"]:
        logging.debug("Generating fake pdf documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake pdf document")
        fake_files.append({
            "type": "pdf",
            "npi": npi,
            "path": generatePDF(client_title, npi)
        })
        logging.debug("Generated fake pdf document")

    if "xml" in config["files"] and isinstance(config["files"]["xml"], bool) and config["files"]["xml"]:
        logging.debug("Generating fake xml documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake xml document")
        fake_files.append({
            "type": "xml",
            "npi": npi,
            "path": generateXML(client_title, npi)
        })
        logging.debug("Generated fake xml document")

    if "html" in config["files"] and isinstance(config["files"]["html"], bool) and config["files"]["html"]:
        logging.debug("Generating fake html documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake html document")
        fake_files.append({
            "type": "html",
            "npi": npi,
            "path": generateHTML(client_title, npi)
        })
        logging.debug("Generated fake html document")

    if "zip" in config["files"] and isinstance(config["files"]["zip"], bool) and config["files"]["zip"]:
        logging.debug("Generating fake zip documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake zip document")
        fake_files.append({
            "type": "zip",
            "npi": npi,
            "path": generateZIP(client_title, npi)
        })
        logging.debug("Generated fake zip document")

    if "protectedzip" in config["files"] and isinstance(config["files"]["protectedzip"], bool) and config["files"]["protectedzip"]:
        logging.debug("Generating fake protectedzip documents with password: " + client_title)
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake protectedzip document")
        fake_files.append({
            "type": "protectedzip",
            "npi": npi,
            "path": generateZIP(client_title, npi, password=client_title)
        })
        logging.debug("Generated fake protectedzip document")

    if "embeddedzip" in config["files"] and isinstance(config["files"]["embeddedzip"], bool) and config["files"]["embeddedzip"]:
        logging.debug("Generating fake embeddedzip documents")
        npi = random.choice(fake_data)
        logging.debug("Using " + npi["type"] + " data for fake embeddedzip document")
        fake_files.append({
            "type": "embeddedzip",
            "npi": npi,
            "path": generateZIP(client_title, npi, embed=True)
        })
        logging.debug("Generated fake embeddedzip document")

    logging.info("Generated " + str(len(fake_files)) + " fake files.")
    print("[+] Generated " + str(len(fake_files)) + " fake files.")

    encoded_data = {
        "plaintext": fake_data,
    }
    encoding_keys = {}

    logging.info("Generating Encoded Datasets")
    print("[.] Generating Encoded Datasets")

    if "xor" in config["encoding"]:
        key = client_title
        if "key" in config["encoding"]["xor"]:
            key = config["encoding"]["xor"]["key"]
        encoding_keys["xor"] = key
        logging.debug("Generating XOR encoded dataset with key: " + key)

        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(xor_crypt(d, key))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["xor"] = ec
        logging.debug("Generated XOR encoded dataset")

    if "b64" in config["encoding"] and isinstance(config["encoding"]["b64"], bool) and config["encoding"]["b64"]:
        logging.debug("Generating Base64 encoded dataset")
        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(b64_encrypt(d))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["b64"] = ec
        logging.debug("Generated Base64 encoded dataset")

    if "url" in config["encoding"] and isinstance(config["encoding"]["url"], bool) and config["encoding"]["url"]:
        logging.debug("Generating URL encoded dataset")
        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(url_encode(d))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["url"] = ec
        logging.debug("Generated URL encoded dataset")

    if "hex" in config["encoding"] and isinstance(config["encoding"]["hex"], bool) and config["encoding"]["hex"]:
        logging.debug("Generating Hex encoded dataset")
        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(hex_encode(d))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["hex"] = ec
        logging.debug("Generated Hex encoded dataset")

    if "rot13" in config["encoding"] and isinstance(config["encoding"]["rot13"], bool) and config["encoding"]["rot13"]:
        logging.debug("Generating Rot13 encoded dataset")
        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(rot13_encode(d))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["rot13"] = ec
        logging.debug("Generated Rot13 encoded dataset")

    if "ascii" in config["encoding"] and isinstance(config["encoding"]["ascii"], bool) and config["encoding"]["ascii"]:
        logging.debug("Generating ASCII encoded dataset")
        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(ascii_encode(d))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["ascii"] = ec
        logging.debug("Generated ASCII encoded dataset")

    if "bin" in config["encoding"] and isinstance(config["encoding"]["bin"], bool) and config["encoding"]["bin"]:
        logging.debug("Generating Binary encoded dataset")
        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(binary_encode(d))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["bin"] = ec
        logging.debug("Generated Binary encoded dataset")

    if "caesar" in config["encoding"]:
        key = 3
        if "shift" in config["encoding"]["caesar"] and isinstance(config["encoding"]["caesar"]["shift"], int):
            key = config["encoding"]["caesar"]["shift"]
        encoding_keys["caesar"] = key
        logging.debug("Generating Caesar encoded dataset with shift: " + str(key))

        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(caesar_encrypt(d, shift=key))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["caesar"] = ec
        logging.debug("Generated Caesar encoded dataset")

    if "reverse" in config["encoding"] and isinstance(config["encoding"]["reverse"], bool) and config["encoding"]["reverse"]:
        logging.debug("Generating Reverse encoded dataset")
        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(reverse_cipher(d))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["reverse"] = ec
        logging.debug("Generated Reverse encoded dataset")

    if "aes" in config["encoding"]:
        key = client_title
        if "key" in config["encoding"]["aes"]:
            key = config["encoding"]["aes"]["key"]
        key = adjust_string_length(key, "_", 16)
        encoding_keys["aes"] = key
        logging.debug("Generating AES encoded dataset with key: " + key)

        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(aes_encrypt(d, key))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["aes"] = ec
        logging.debug("Generated AES encoded dataset")

    if "fernet" in config["encoding"]:
        key = client_title
        if "key" in config["encoding"]["fernet"]:
            key = config["encoding"]["fernet"]["key"]
        key = adjust_string_length(key, "_", 16)
        encoding_keys["fernet"] = key
        logging.debug("Generating Fernet encoded dataset with key: " + key)

        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(fernet_encrypt(d, key))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["fernet"] = ec
        logging.debug("Generated Fernet encoded dataset")

    if "base32" in config["encoding"] and isinstance(config["encoding"]["base32"], bool) and config["encoding"]["base32"]:
        logging.debug("Generating Base32 encoded dataset")
        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(base32_encode(d))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["base32"] = ec
        logging.debug("Generated Base32 encoded dataset")

    if "base16" in config["encoding"] and isinstance(config["encoding"]["base16"], bool) and config["encoding"]["base16"]:
        logging.debug("Generating Base16 encoded dataset")
        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(base16_encode(d))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["base16"] = ec
        logging.debug("Generated Base16 encoded dataset")

    if "zlib" in config["encoding"] and isinstance(config["encoding"]["zlib"], bool) and config["encoding"]["zlib"]:
        logging.debug("Generating Zlib encoded dataset")
        ec = []
        for fd in fake_data:
            encoded = []
            for d in fd["data"]:
                encoded.append(zlib_compress(d))

            ec.append({
                "type": fd["type"],
                "data": encoded
            })
        encoded_data["zlib"] = ec
        logging.debug("Generated Zlib encoded dataset")

    logging.info("Done generating data")
    return {
        "data": encoded_data,
        "encoding_keys": encoding_keys,
        "files": fake_files,
    }