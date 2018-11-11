import RPi.GPIO as GPIO
from threading import Thread
import time

PWM_FREQUENCY = 50  # Hz
MAX_PULSE_WIDTH = 2.5  # ms
MIN_PULSE_WIDTH = 1.0  # ms


class Servo(Thread):
    def __init__(self, pwm_pin, angle):
        super(Servo, self).__init__()
        self.__pwm_pin = pwm_pin
        self.__angle = angle

    def run(self):
        print('Pin: %d angle: %d' % (self.__pwm_pin, self.__angle))
        try:
            GPIO.setmode(GPIO.BOARD)
            percentage = max(0.0, min(1.0, self.angle/180.0))
            pulse_width = (MIN_PULSE_WIDTH + ((MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) * percentage)) / 1000.0
            duty_cycle = pulse_width * PWM_FREQUENCY * 100

            GPIO.setup(self.__pwm_pin, GPIO.OUT)
            pwm = GPIO.PWM(self.__pwm_pin, PWM_FREQUENCY)
            pwm.start(duty_cycle)
            time.sleep(0.5)
            pwm.stop()
        finally:
            GPIO.cleanup()
