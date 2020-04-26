import re
from servo.servo import Servo
import socket
import time
from threading import Thread
import queue

ERROR_TIMEOUT = 0.5  # Seconds to wait after a client socket error.


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
            servo_queue = ServoQueue()
            servo_queue.start()
            while True:
                try:
                    server_socket.listen(2)
                    client_socket, _ = server_socket.accept()
                    message = client_socket.recv(2048).decode("utf-8")
                    re_result = re.match('^(?P<pin>[0-9]+) (?P<angle>[0-9]{1,3})$', message)
                    if re_result:
                        pin = int(re_result.group('pin'))
                        angle = int(re_result.group('angle'))
                        servo_queue.add_servo(Servo(pin, angle))
                    client_socket.shutdown(socket.SHUT_RDWR)
                    client_socket.close()
                except Exception as e:
                    # print('Socket exception %s' % e)
                    time.sleep(ERROR_TIMEOUT)
        except Exception as e:
            # print('Server exception %s' % e)
            return


class ServoQueue(Thread):
    """
    A thread class that manages the servos in a queue. Allows only one servo to
    run at a time.
    """
    
    def __init__(self):
        self.__queue = queue.Queue()
        super(ServoQueue, self).__init__()

    def add_servo(self, srvo):
        self.__queue.put(srvo)

    def run(self):
        while True:
            srvo = self.__queue.get()
            srvo.start()
            while srvo.is_alive():
                time.sleep(0.1)
