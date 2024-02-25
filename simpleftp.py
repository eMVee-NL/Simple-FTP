import argparse
import os
import socket
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Set the username
username = 'user'
# Set the password for the user
password = 'pass'
# Set the directory where the received files should be stored
directory = 'received'


def banner():
    banner = '''
      █████████   ███                            ████              ███████████ ███████████ ███████████ 
     ███░░░░░███ ░░░                            ░░███             ░░███░░░░░░█░█░░░███░░░█░░███░░░░░███
    ░███    ░░░  ████  █████████████   ████████  ░███   ██████     ░███   █ ░ ░   ░███  ░  ░███    ░███
    ░░█████████ ░░███ ░░███░░███░░███ ░░███░░███ ░███  ███░░███    ░███████       ░███     ░██████████ 
     ░░░░░░░░███ ░███  ░███ ░███ ░███  ░███ ░███ ░███ ░███████     ░███░░░█       ░███     ░███░░░░░░  
     ███    ░███ ░███  ░███ ░███ ░███  ░███ ░███ ░███ ░███░░░      ░███  ░        ░███     ░███        
    ░░█████████  █████ █████░███ █████ ░███████  █████░░██████     █████          █████    █████       
     ░░░░░░░░░  ░░░░░ ░░░░░ ░░░ ░░░░░  ░███░░░  ░░░░░  ░░░░░░     ░░░░░          ░░░░░    ░░░░░        
                                       ░███                                                            
                                       █████       
            Created by eMVee
        '''
    print(banner)


def create_dir(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except OSError as e:
        print("[!] Creation of the directory %s failed" % path)
        print("[!] Error: %s" % e)

def receive_file(filename, ftp, ip_address, port):
    try:
        # open a file for writing in binary mode
        with open(filename, 'wb') as f:
            # retrieve the file from the server and write it to the file
            ftp.retrbinary('RETR ' + filename, f.write)
            print(f'[I {ip_address}:{port}] {ip_address}:{port}-[user] RETR {filename}')
    except Exception as e:
        print(f'[E {ip_address}:{port}] {ip_address}:{port}-[user] RETR {filename} failed: {e}')

def ftp_server(ip_address, port, user=username, passwd=password):
    authorizer = DummyAuthorizer()

    # Create the received directory if it does not exist
    create_dir(os.path.join(os.getcwd(), directory))

    # Add a user
    authorizer.add_user(user, passwd, directory, perm='elradfmwM')

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "A simple FTP server."

    # Specify a masquerade address and the range of ports to use for passive connections.
    # This is useful behind NAT.
    handler.masquerade_address = ip_address
    handler.passive_ports = range(port, port + 10)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = (ip_address, port)
    server = FTPServer(address, handler)

    # set a maximum number of concurrent connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # Handle incoming file transfers
    while True:
        ftp = server.accept()
        if ftp is None:
            break
        try:
            filename = ftp[0].get_name()
            with open(os.path.join(os.getcwd(), 'received', filename), 'wb') as f:
                ftp[0].storbinary('STOR {}'.format(filename), f)
                print(f'[I {ip_address}:{port}] {ip_address}:{port}-[user] STOR {filename} completed=1 bytes=693 seconds=0.101')
        finally:
            ftp[0].quit()

    # start ftp server
    server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FTP Server')
    parser.add_argument('--ip', type=str, default='0.0.0.0',
                        help='The IP address to listen on (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=21, help='The port to listen on (default: 21)')
    args = parser.parse_args()
    banner()
    print('[+] Ftp Server started')
    try:
        ftp_server(args.ip, args.port)
    except KeyboardInterrupt:
        print('[+] Shutting down FTP service.')
