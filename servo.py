import RPi.GPIO as GPIO
import time

# Pin Definitons:
pwmPin = 18 # Broadcom pin 18 (P1 pin 12)

dc = 20 # duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(pwmPin, GPIO.OUT) # PWM pin set as output
pwm = GPIO.PWM(pwmPin, 12.5)  # Initialize PWM on pwmPin 100Hz frequency

# Initial state for LEDs:
pwm.start(1)
time.sleep(2)
pwm.ChangeDutyCycle(2)
time.sleep(2)
pwm.ChangeDutyCycle(3)
time.sleep(2)
pwm.ChangeDutyCycle(2)
time.sleep(2)
pwm.ChangeDutyCycle(3)
time.sleep(2)
pwm.ChangeDutyCycle(2)
time.sleep(2)
pwm.stop()
GPIO.cleanup()
