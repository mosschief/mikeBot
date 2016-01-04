from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time

mh = Adafruit_MotorHAT(addr=0x60)


# Motor 1 = Left, Motor 2 = Right
motor1 = mh.getMotor(1)
motor2 = mh.getMotor(2)

# set the speed to start, from 0 (off) to 255 (max speed)
motor1.setSpeed(150)
motor2.setSpeed(150)

def leftForward():
    motor1.run(Adafruit_MotorHAT.FORWARD)

    return

def rightForward():
    motor2.run(Adafruit_MotorHAT.FORWARD)

    return

def leftBackward():
    motor1.run(Adafruit_MotorHAT.BACKWARD)
    return

def rightBackward():
    motor2.run(Adafruit_MotorHAT.BACKWARD)
    return

def leftStop():
    motor1.run(Adafruit_MotorHAT.RELEASE)

    return


def rightStop():
    motor2.run(Adafruit_MotorHAT.RELEASE)

    return

