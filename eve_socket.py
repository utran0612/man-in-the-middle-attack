# Communication happens through UNIX sockets
import socket
import sys
import os
import errno

# Eve's socket to connect with Alice and Bob


class Eve_Socket:
    def __init__(self, target, buffer_dir, buffer_file_name):
        self.target = target
        self.conn = self.open_connection(buffer_dir, buffer_file_name)

    def open_connection(self, buffer_dir, buffer_file_name):
        buffer_path = buffer_dir + buffer_file_name
        # if the target is Alice, create a socket and connect
        if self.target == 'alice':
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                sock.connect(buffer_path)
            except socket.error:
                raise
            return sock
        # if the target is Bob, create a socket and wait for Bob to connect
        elif self.target == 'bob':
            try:
                os.makedirs(buffer_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            # Ensure the socket does not already exist
            try:
                os.unlink(buffer_path)
            except OSError:
                if os.path.exists(buffer_path):
                    raise

            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.bind(buffer_path)
            sock.listen(1)
            conn, rem_addr = sock.accept()
            return conn

        else:
            raise

    def send(self, msg):
        self.conn.sendall(msg)

    def recv(self, length):
        return self.conn.recv(length)

    def close(self, buffer_dir, buffer_file_name):
        self.conn.close()
        if self.target == 'bob':
            os.remove(buffer_dir + buffer_file_name)
