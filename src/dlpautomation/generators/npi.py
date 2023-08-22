from faker import Faker
import logging

# Generate CC Info with below format:
# 'Discover\nKatherine Fisher\n6587647593824218 08/27\nCVC: 892\n'
# justnumber = True returns just the credit card number (i.e. 6504876475938248)
def getFakeCCs(n, justnumber=False):
    logging.debug("getFakeCCs(n=" + str(n) + ", justnumber=" + str(justnumber) + ")")
    fake = Faker()
    ret = []

    for _ in range(n):
        if not justnumber:
            ret.append(fake.credit_card_full())
        else:
            ret.append(fake.credit_card_number())
    logging.debug("getFakeCCs() returning with ret len: " + str(len(ret)))
    return ret

# Generate SSN nunmbers
# if seperator is set to '' ssn will be xxx-xx-xxxx, otherwise '-' will be replaced by the seperator
def getFakeSSNs(n, seperator=''):
    logging.debug("getFakeSSNs(n=" + str(n) + ", seperator=" + seperator + ")")
    fake = Faker()
    ret = []

    for _ in range(n):
        if seperator != '':
            ssn = fake.ssn().replace("-", seperator)
            ret.append(ssn)
        else:
            ret.append(fake.ssn())

    logging.debug("getFakeSSNs() returning with ret len: " + str(len(ret)))
    return ret

# Generate fake Banking Information
# codetypes:
#   aba = ABA routing transit number
#   bban = Basic Bank Account Number
#   iban = International Bank Account Number
#   swift8 = 8 digit SWIFT code
#   swift11 = 11 digit SWIFT code nonprimary
#   swift11primary = 11 digit primary SWIFT code
def getFakeBank(n, codetype):
    logging.debug("getFakeBank(n=" + str(n) + ", codetype=" + codetype + ")")
    fake = Faker()
    ret = []

    for _ in range(n):
        if codetype == "aba":
            ret.append(fake.aba())
        elif codetype == "bban":
            ret.append(fake.bban())
        elif codetype == "iban":
            ret.append(fake.iban())
        elif codetype == "swift8":
            ret.append(fake.swift())
        elif codetype == "swift11":
            ret.append(fake.swift(length=11))
        elif codetype == "swift11primary":
            ret.append(fake.swift(length=11, primary=True))

    logging.debug("getFakeBank() returning with ret len: " + str(len(ret)))
    return ret