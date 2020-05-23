# PiServoServer

This is a server process that runs on a Raspberry Pi and listens for servo commands over the loopback interface. Servo commands are executed serially to avoid drawing too much current from the Pi.

Commands can be sent to port `9338` if you use the `servo` package's  `__main__.py`, or any port supplied to the `ServoServer` constructor. Commands use the form `pin angle`, so `7 90` will set the servo connected to board pin 7 to 90 degrees. Pi board numbering is used, not BCM. The max angle is 180 degrees.

Try it with Netcat:
```Shell
python3 servo &
echo "7 90" | nc 127.0.0.1 9338
```
