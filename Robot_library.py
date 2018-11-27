"""
* Team Id : CB#756
* Author List :[Ankur_Sonawane]
* Filename: Robot_library.py
* Theme: Collector_bot
* Classes:
   Robot


"""
from __future__ import print_function, division

from warnings import warn
import time
from serial import Serial, serialutil
from Util_library import *


class Robot:
    """
    An Interface to the AVR Microcontroller in the Bot via serial communcation through Xbee
    Command Protocol is Stateless Unidirectional and Master-Slave
    Send commands to Microcontroller via XBee as bytes whose meaning is defined in commands.
    These preform very simple procedures which are non-blocking completed without delay.
    Thus the only blocking calls are made to this class and not to the AVR, greatly simplifying sync.
    Example:

    >>> robot=Robot(port=0)
    Connecting to Robot
    Robot Connected

    >>> robot.move(1.5)  # move 1.5 steps forward

    >>> robot.move(-2)   # move 2 steps behind

    >>> robot.turn(180)  # turn 180 degrees clockwise

    >>> robot.turn(-90)  # turn 90 degrees anticlockwise

    >>> robot.pick()     # pickup object

    >>> robot.drop()     # drop object

    >>> del robot        # Automatically stop bot on deletion or program termination
    Closed Serial

    """
    opened = True

    commands = {
        'close_hand': b'p',
        'open_hand': b'd',
        'stop': b's',
        'forward': b'8',
        'left': b'4',
        'right': b'6',
        'reverse': b'2',
        'left_pwm': b'l',
        'right_pwm': b'r',
        'stop_hand': b'h',
        'lift_hand': b'u',
        'lower_hand': b'b',
    }

    def __init__(self, port=0):
        try:
            print('Connecting to Robot')
            self.serial = Serial('/dev/ttyUSB' + str(port))
            print("Robot Connected")
        except serialutil.SerialException as e:
            raise HardwareError(e.strerror)
        self.send('stop')

    def _set_pwm(self, pwm=(150, 150)):
        self.send('left_pwm')
        self.serial.write(pwm[0])
        self.send('right_pwm')
        self.serial.write(pwm[1])

    def send(self, command_name):
        self.serial.write(self.commands[command_name])

    def pick(self):
        if self.opened:
            self.send('close_hand')
            time.sleep(2.5)
            self.send('stop_hand')
            self.send('lift_hand')
            time.sleep(1)
            self.opened = False
        else:
            warn("Pick Disabled")

    def drop(self):
        if not self.opened:
            self.send('open_hand')
            time.sleep(2)
            self.send('stop_hand')
            self.move(-0.9)

            self.send('lower_hand')
            time.sleep(1)

            self.opened = True
        else:
            warn("Drop Disabled")

    def move(self, step):
        if step > 0:
            self.send('forward')
        else:
            self.send('reverse')
        time.sleep(abs(step))
        self.send('stop')

    def turn(self, theta, kp=.593 / 90):
        if theta < 0:
            self.send('left')
        else:
            self.send('right')
        time.sleep(abs(theta) * kp)
        self.send('stop')

    def __del__(self):
        self.send('stop')
        self.send('stop_hand')
        self.serial.close()
        print("Closed Serial")

# class Robot(Robot):
#     def __init__(self,*args):
#         print ("Dummy Robot")
#         self.serial=open('robot.log','wb')


def ankur():
    global r
    for i in range(4):
        r.move(2)
        r.turn(90)
    for i in range(4):
        r.move(-2)
        r.turn(90)


if __name__ == "__main__":
    import time
    r = Robot(0)
    # r.turn(3)
    # r.pick()
    # r.drop()
    # r.forward(2)
    #del r
