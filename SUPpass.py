#!/usr/bin/python3
import base64
import getopt
import hashlib
import sys


def display_usage():
    print("SUP'Pass -- The Safest Password Manager\n")
    print("Usage : ./SUPpass.py -u <username> -d <domain_name> -p <master_password>\n")
    print("Options :")
    print("     -h, --help      : show the help")
    print("     -u, --username  : input username for the site (pseudo, mail, etc...)")
    print("     -d, --domain    : domain name of the site")
    print("     -p, --password  : master password of the user\n")
    sys.exit(1)


def get_options():
    try:
        options, arguments = getopt.getopt(sys.argv[1:], 'hu:d:p:', ['help', 'username=', 'domain=', 'password='])
        return options
    except getopt.GetoptError:
        return -1


def set_options(options):
    username, domain, password = "", "", ""

    for option, argument in options:
        if option in ('-h', '--help'):
            display_usage()
        elif option in ('-u', '--username'):
            username = argument
        elif option in ('-d', '--domain'):
            domain = argument
        elif option in ("-p", "--password"):
            password = argument

    if "" in (username, domain, password):
        display_usage()
    else:
        return username, domain, password


def build_password(input_data):
    password = ""
    input_data_hashed = hashlib.sha256(input_data.encode()).hexdigest()  # Hash the input_data with SHA-256

    for i in range(0, 60, 4):
        password += input_data_hashed[i]  # Select 1 char every 4 chars on a 60 chars string (total of 15 chars)

    password = base64.b64encode(password.encode()).decode()  # Convert to Base64, add Upper and Lower case

    return password[:15]  # Return only the 15 first characters of the Base64 result


def SUPpass():
    options = get_options()

    if options == -1 or options == []:
        display_usage()

    username, domain, password = set_options(options)

    final_password = build_password(username + domain + password)

    print("\nYour password :", final_password, "\n")


SUPpass()
