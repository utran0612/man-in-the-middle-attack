# (Wo)Man-in-the-middle Attack (MitM) 😎

## Overview

Alice and Bob implement an encrypted chat client so that
they are sure no one eavesdrops their intimate discussions. 
They decide to use AES5 to encrypt their message.
They also hear of the Diffie-Hellman key exchange6(DHKE) and figure it would be cool
to use a new secret key for AES every time they connect.

Unfortunately Alice and Bob overlooked a fatal flaw: When communicating over the internet (or even locally), 
one cannot know with certainty that they are speaking to the intended
party, at least not without using some form of cryptographic authentication. 

In this program, I'll implement the MitM attack to eavesdrop and change messages between Alice and Bob!

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [pyaes](https://pypi.org/project/pyaes/).

```bash
sudo pip install pyaes
```

## Usage

Open two terminals and navigate to the directory with the scripts

```python
python3 alice.py 
```
Eve has 3 flags:

--relay: Eve should just relay the two messages from Alice to Bob 
and from Bob to Alice. In this case, the outputs of both alice.py and bob.py 
in the terminals should be identical to the case when the MitM attack isn’t executed. 

--break-heart:  Eve should change the messages so that Alice receives 
the message ”I hateyou!” and Bob receives ”You broke my heart...”. 

--custom: after receiving Bob’s messsage, Eve must prompt the user 
to input a message to the terminal and then must send this message 
to Alice instead. The same would happen for Alice’s message; 
Eve would prompt the user for a second message and this time send it to Bob.

```python
python3 eve.py --flag
```

```python
python3 bob.py 
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
