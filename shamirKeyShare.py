import argparse
import configparser
import smtplib
from Crypto.PublicKey import RSA
import numpy as np
from random import randint
from getpass import getpass

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--email-list', help="file containing share receiver's emails", required=True)
    return parser.parse_args()

def shamirKeyShare(key, emails, k):
    a = []
    for i in range(k):
        a.append(randint(1, 2**1024))
    a.append(key.n)
    print(a)
    for i in range(k):
        point = randint(1,2**512)
        partial_key = tuple([point, np.polyval(a,point)])
        sharePartialKey(partial_key, emails[i])

def sharePartialKey(partial_key, email):
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        server = smtplib.SMTP(config['default']['SMTP_HOST'], config['default']['SMTP_PORT'])
        server.starttls()
        fromaddr = input("Enter sender email: ")
        password = getpass("Enter sender email password: ")
        server.login(fromaddr, password)
        server.sendmail(fromaddr, email, str(partial_key))
    except:
        raise Exception('Unable to send Email')

def main(args):
    fin = open(args.email_list, "r")
    emails = fin.read().splitlines()
    fin.close()
    k = len(emails)
    key = RSA.generate(1024)
    shamirKeyShare(key, emails, k)

if __name__ == "__main__":
    args = parse_args()
    main(args)
