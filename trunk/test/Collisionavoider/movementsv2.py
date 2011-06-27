import string
import socket

COLOR       = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
TYPES       = ['SonarSensor', 'SICKL-MS', 'OdometrySensor']
NAMES       = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Scanner1', 'Odometry']
OPCODE      = ['RESET', 'NOP']
OPCODE_RFID = ['Release', 'Read', 'Write']

# The movement handler contains all sorts of possible movements.
def handle_movement(type, *args):
    handlers = {"forward":         go_drive,
                "left":            go_left,
                "right":           go_right,
                "reverse":         go_reverse,
                "brake":           go_brake,
                "rotate_left":     go_rotate_left,
                "rotate_right":    go_rotate_right,
               }
    return handlers[type](*args)

# Method to drive forward and backwards, make turns and rotations.
def go_drive(s1):
    s1 = str(s1)
    string = "DRIVE {Left " + s1 + "} {Right " + s1 + "}\r\n"
    #print string
    return string


# Method to make a rotation right.s1 is the speed at which you want to rotate.
def go_rotate_right(s1):
    s1 = str(s1)
    string = "DRIVE {Left " + s1 + "} {Right -" + s1 + "}\r\n"
    print string
    return string
# Method to make a rotation left.s1 is the speed at which you want to rotate.
def go_rotate_left(s1):
    s1 = str(s1)
    string = "DRIVE {Left -" + s1 + "} {Right " + s1 + "}\r\n"
    print string
    return string
# Method to drive to the right. s1 needs to be greater than s2.
def go_right(s1 ,s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    return string
# Method to drive to the left.s1 needs to be greater than s2.
def go_left(s1,s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    return string
# Method to stop.
def go_brake():
    string = "DRIVE {Left 0} {Right 0}\r\n"
    return string
# Method to drive backwards
def go_reverse():
    string = "DRIVE {Left -1} {Right -1}\r\n"
    return string

