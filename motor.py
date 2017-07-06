from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time

class Motor(object):

    def __init__(self):
        self.speed = 150
        mh = Adafruit_MotorHAT(addr=0x60)
        self.lookCurrent = 0

        self.motor1 = mh.getMotor(3)    # left drive
        self.motor2 = mh.getMotor(4)    # right drive
        self.motor3 = mh.getStepper(100, 1)   # stepper up/down
        self.motor1.setSpeed(150)
        self.motor2.setSpeed(150)
        self.motor3.setSpeed(30)

    def leftForward(self):
        self.motor2.run(Adafruit_MotorHAT.FORWARD)
        return

    def rightForward(self):
        self.motor1.run(Adafruit_MotorHAT.FORWARD)
        return

    def leftBackward(self):
        self.motor2.run(Adafruit_MotorHAT.BACKWARD)
        return

    def rightBackward(self):
        self.motor1.run(Adafruit_MotorHAT.BACKWARD)
        return

    def leftStop(self):
        self.motor2.run(Adafruit_MotorHAT.RELEASE)
        return

    def rightStop(self):
        self.motor1.run(Adafruit_MotorHAT.RELEASE)
        return

    def speedUp(self):
        if self.speed <= 240:
            self.speed += 10
            self.motor1.setSpeed(self.speed)
        else:
            return "Speed already max"

    def speedDown(self):
        if self.speed >= 60:
            self.speed -= 10
            self.motor1.setSpeed(self.speed)
        else:
            return "Speed already min"

    def lookUp(self):
        if self.lookCurrent < 7:
            self.lookCurrent += 1
            self.motor3.step(2, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)

    def lookDown(self):
        if self.lookCurrent > -5:
            self.lookCurrent -= 1
            self.motor3.step(2, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)

    def shutDown(self):
        while self.lookCurrent < 0:
            self.lookUp()
            self.lookCurrent +=1
        while self.lookCurrent > 0:
            self.lookDown()
            self.lookCurrent -=1





# set the speed to start, from 0 (off) to 255 (max speed)

