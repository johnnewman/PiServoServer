import RPi.GPIO as GPIO
from threading import Thread
import time

WAIT_TIME = 0.75  # sec
PWM_FREQUENCY = 50  # Hz
MAX_PULSE_WIDTH = 2.5  # ms
MIN_PULSE_WIDTH = 0.5  # ms


class Servo(Thread):
    def __init__(self, pwm_pin, angle):
        super(Servo, self).__init__()
        self.__pwm_pin = pwm_pin
        self.__angle = angle

    def run(self):
        try:
            GPIO.setmode(GPIO.BOARD)
            percentage = max(0.0, min(1.0, self.__angle/180.0))
            pulse_width = (MIN_PULSE_WIDTH + ((MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) * percentage)) / 1000.0  # in seconds
            duty_cycle = pulse_width * PWM_FREQUENCY
            GPIO.setup(self.__pwm_pin, GPIO.OUT)
            pwm = GPIO.PWM(self.__pwm_pin, PWM_FREQUENCY)
            pwm.start(duty_cycle * 100)
            time.sleep(WAIT_TIME)
            pwm.stop()
        finally:
            GPIO.cleanup()
