from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperM$

import time

mh = Adafruit_MotorHAT(addr=0x60)

# Motor 1 = Left, Motor 2 = Right
motor1 = mh.getMotor(1)
motor2 = mh.getMotor(2)
motor3 = mh.getStepper(100,2)

# set the speed to start, from 0 (off) to 255 (max speed)


motor1.setSpeed(150)
motor2.setSpeed(150)
motor3.setSpeed(30)

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

def speedUp(speed):


    if speed <= 240:
        speed += 10
        motor1.setSpeed(speed)
        return speed
    else:
        return "Top Speed"

def speedDown(speed):
    if speed >= 60:
        speed -= 10
        motor1.setSpeed(speed)
        return speed
    else:
        return "Minimum Speed"

def lookUp():
    motor3.step(2, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)

def lookDown():
    motor3.step(2, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
