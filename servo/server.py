import re
import servo
import socket
import time
from threading import Thread

TIMEOUT = 0.5


class ServoServer(Thread):
    """
    A thread class that listens for servo messages over a socket in the form of
    "<pin address> <angle>".
    """

    def __init__(self, port):
        """
        Initialized the server but does not open any ports until run() is
        called.

        :param port: The port to use to listen for commands.
        """
        super(ServoServer, self).__init__()
        self.__port = port

    def run(self):
        """
        Infinitely loops, waiting for socket connections and commands.
        """
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('127.0.0.1', self.__port))

            while True:
                try:
                    server_socket.listen(2)
                    client_socket, address = server_socket.accept()
                    message = client_socket.recv(2048)
                    re_result = re.match('^(?P<pin>[0-9]+) (?P<angle>[0-9]{1,3})$', message)
                    if re_result:
                        pin = int(re_result.group('pin'))
                        angle = int(re_result.group('angle'))
                        servo.Servo(pin, angle).start()

                    client_socket.shutdown(socket.SHUT_RDWR)
                    client_socket.close()
                except Exception as e:
                    print('Socket exception %s' % e.message)
                    time.sleep(TIMEOUT)
        except Exception as e:
            print('Server exception %s' % e.message)
