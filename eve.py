import argparse
import sys
import os

from common import *
from const import *
from eve_socket import Eve_Socket

# set up for Eve to connect with Alice and Bob


def eve_setup(target, buffer_dir, buffer_file_name):
    dialog = Dialog('print')
    socket = Eve_Socket(target, buffer_dir, buffer_file_name)
    shared_key = do_Diffie_Hellman(socket)
    dialog.info('Did DHKE! Channel established with {}'.format(target.upper()))
    aes = AES(shared_key)
    return socket, aes


# set up arguments
parser = argparse.ArgumentParser(description="Attacker")
parser.add_argument('--relay',  action='store_true', default='relay',
                    help="just relay messages")  # default argument is relay
parser.add_argument('--break-heart', action='store_true',
                    help="send heart broken msgs")
parser.add_argument('--custom', action='store_true', help="send custom msgs")
options = vars(parser.parse_args())

flag = None
# get the flag the user passes in
for option, val in options.items():
    if val:
        flag = option

dialog = Dialog('print')
player = os.path.basename(sys.argv[0]).split('.', 1)[0]

# build 2 sockets for Eve to connect with Alice and Bob
socket_alice, aes_alice = eve_setup('alice', BUFFER_DIR, BUFFER_FILE_NAME)
socket_bob, aes_bob = eve_setup('bob', BUFFER_DIR, BUFFER_FILE_NAME)

if flag == 'relay':
    # relay msg from Bob to Alice
    received_from_bob = receive_and_decrypt(aes_bob, socket_bob)
    to_send_alice = received_from_bob
    dialog.chat('Bob said: "{}"'.format(received_from_bob))
    encrypt_and_send(to_send_alice, aes_alice, socket_alice)
    dialog.info(
        'Relay message from Bob to Alice, waiting for Alice response...')

    # relay msg from Alice to Bob
    received_from_alice = receive_and_decrypt(aes_alice, socket_alice)
    to_send_bob = received_from_alice
    dialog.chat('Alice said: "{}"'.format(received_from_alice))
    encrypt_and_send(to_send_bob, aes_bob, socket_bob)
    dialog.info('Relay message from Alice to Bob, socket closing...')

elif flag == 'break_heart':
    # get nice msg from Bob and send bad one to Alice
    received_from_bob = receive_and_decrypt(aes_bob, socket_bob)
    to_send_alice = BAD_MSG['bob']
    dialog.chat('Bob said: "{}"'.format(received_from_bob))
    encrypt_and_send(to_send_alice, aes_alice, socket_alice)
    dialog.info(
        'Sent heart broken msg to Alice, waiting for Alice response...')

    # get nice msg from Alice and send bad one to Bob
    received_from_alice = receive_and_decrypt(aes_alice, socket_alice)
    # make sure that Bob receives bad msf from Alice
    if received_from_alice != BAD_MSG['alice']:
        to_send_bob = BAD_MSG['alice']
    else:
        to_send_bob = received_from_alice
    dialog.chat('Alice said: "{}"'.format(received_from_alice))
    encrypt_and_send(to_send_bob, aes_bob, socket_bob)
    dialog.info('Sent heart broken msg to Bob, socket closing...')

elif flag == 'custom':
    # get msg from Bob, change it, and send to Alice
    received_from_bob = receive_and_decrypt(aes_bob, socket_bob)
    dialog.info('Bob said: "{}"'.format(received_from_bob))
    dialog.prompt('What you want to send Alice?')
    to_send_alice = input()
    encrypt_and_send(to_send_alice, aes_alice, socket_alice)
    dialog.info('Sent custom msg to Alice, waiting for Alice response...')

    # get msg from Alice, change it, and send to Bob
    received_from_alice = receive_and_decrypt(aes_alice, socket_alice)
    dialog.info('Alice said: "{}"'.format(received_from_alice))
    dialog.prompt('What you want to send Bob?')
    to_send_bob = input()
    encrypt_and_send(to_send_bob, aes_bob, socket_bob)
    dialog.info('Sent custom msg to Bob, socket closing...')

tear_down(socket_alice, BUFFER_DIR, BUFFER_FILE_NAME)
