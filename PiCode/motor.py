import RPi.GPIO as GPIO
import json
import time

config = json.load(open("config.json"))

servoPIN = config["servo_pin"]

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)
p.start(2.5)  # Initialization


def SetAngle(angle):
    duty = angle / 18 + 2.5
    GPIO.output(17, True)
    p.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(17, False)
    p.ChangeDutyCycle(0)


if __name__ == "__main__":
    while True:
        SetAngle(int(input("Angle (0-180): ")))
