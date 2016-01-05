from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time

mh = Adafruit_MotorHAT(addr=0x60)

# Motor 1 = Left, Motor 2 = Right
motor1 = mh.getMotor(1)
motor2 = mh.getMotor(2)

# set the speed to start, from 0 (off) to 255 (max speed)
motorSpeed = 150

motor1.setSpeed(motorSpeed)
motor2.setSpeed(motorSpeed)

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

def speedUp():
    if motorSpeed <= 200:
        motorSpeed += 50
        motor1.setSpeed(motorSpeed)
        return
    else:
        return "Top Speed"

def speedDown():
    if motorSpeed >= 100:
        motorSpeed -= 50
        motor1.setSpeed(motorSpeed)
        return
    else:
        return "Minimum Speed"