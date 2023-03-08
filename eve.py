import argparse
import sys
import os

from common import *
from const import *

parser = argparse.ArgumentParser(description="Attacker")
parser.add_argument('--relay',  action='store_true',
                    help="just relay messages")
parser.add_argument('--break-heart', action='store_true',
                    help="send heart broken msgs")
parser.add_argument('--custom', action='store_true', help="send custom msgs")
options = vars(parser.parse_args())

flag = None
# get the flag the user pass in
for option, val in options.items():
    if val:
        flag = option

if flag == 'relay':
    dialog = Dialog('print')
    player = os.path.basename(sys.argv[0]).split('.', 1)[0]
    socket_alice, aes_alice = eve_setup('alice', BUFFER_DIR, BUFFER_FILE_NAME)
    socket_bob, aes_bob = eve_setup('bob', BUFFER_DIR, BUFFER_FILE_NAME)
    received_from_bob = receive_and_decrypt(aes_bob, socket_bob)
    if CUSTOM_CHAT:
        dialog.prompt('Please input message...')
        to_send = input()
    else:
        to_send_alice = received_from_bob
    encrypt_and_send(to_send_alice, aes_alice, socket_alice)
    dialog.info('Relay message from Bob to Alice, waiting for Alice response...')
    received_from_alice = receive_and_decrypt(aes_alice, socket_alice)
    if CUSTOM_CHAT:
        dialog.prompt('Please input message...')
        to_send = input()
    else:
        to_send_bob = received_from_alice
    encrypt_and_send(to_send_bob, aes_bob, socket_bob)
    dialog.info('Relay message from Alice to Bob, socket closing...')

    tear_down(socket_alice, BUFFER_DIR, BUFFER_FILE_NAME)
