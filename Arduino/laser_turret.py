# required modules
import sys
import time
import keyboard
from telemetrix import telemetrix

# create a Telemetrix instance
board = telemetrix.Telemetrix(com_port='COM4')

# some globals
SERVO_1_PIN = 2
SERVO_2_PIN = 3
LASER_PIN = 4

# initialize servos and laser pins
board.set_pin_mode_servo(SERVO_1_PIN, 100, 3000)
board.set_pin_mode_servo(SERVO_2_PIN, 100, 3000)
board.set_pin_mode_digital_output(LASER_PIN)
time.sleep(.2)

angle  = 120     # initial angle
da = 5           # initial speed (degrees per keypress)
laser_state = 0  # initial led state

while True:

    if keyboard.is_pressed('d'):                  # check if d is pressed
        if angle - da > 0:                        # check to make sure new angle will not exceed 0 degrees
            angle = angle - da                    # decrease angle reference
            board.servo_write(SERVO_1_PIN, angle) # set servo position to new angle by calling the function we made earlier  
            time.sleep(0.1)                       # wait a little bit (0.1 seconds) before checking again  
    
    elif keyboard.is_pressed('a'):                # check if a is pressed
        if angle + da < 180:                      # check to make sure new angle will not exceed 180 degrees
            angle = angle + da                    # increase angle reference
            board.servo_write(SERVO_1_PIN, angle) # set servo position to new angle by calling the function we made earlier
            time.sleep(0.1)                       # wait a little bit (0.1 seconds) before checking again
    
    elif keyboard.is_pressed('w'):                # check if w is pressed
        if angle - da > 0:                        # check to make sure new angle will not exceed 0 degrees
            angle = angle - da                    # decrease angle reference
            board.servo_write(SERVO_2_PIN, angle) # set servo position to new angle by calling the function we made earlier    
            time.sleep(0.1)                       # wait a little bit (0.1 seconds) before checking again

    elif keyboard.is_pressed('s'):                # check if s is pressed
        if angle + da < 180:                      # check to make sure new angle will not exceed 180 degrees
            angle = angle + da                    # if new angle is OK, change to it
            board.servo_write(SERVO_2_PIN, angle) # set servo position to new angle by calling the function we made earlier
            time.sleep(0.1)                       # wait a little bit (0.1 seconds) before checking again

    elif keyboard.is_pressed('t'):                # check if t is pressed
        if da + 1 < 180:                          # check to make sure new angle will not exceed 180 degrees
            da = da + 1                           # increase the speed reference
            time.sleep(0.1)                       # wait a little bit (0.1 seconds) before checking again
   
    elif keyboard.is_pressed('g'):                # check if g is pressed
        if da - 1 > 0:                            # check to make sure new angle will not exceed 0 degrees 
            da = da - 1                           # decrease the speed reference
            time.sleep(0.1)                       # wait a little bit (0.1 seconds) before checking again 
    
    elif keyboard.is_pressed('r'):                # check if r is pressed
        angle = 90                                # set reset angle
        da = 5                                    # set reset speed
        board.servo_write(SERVO_1_PIN, angle)     # set servo position to new angle by calling the function we made earlier
        time.sleep(0.1)                           # wait a little bit (0.1 seconds) before checking again

    elif keyboard.is_pressed('space'):            # if space is pressed toggle the laser
        if laser_state == 0:                      # if laser is off
            board.digital_write(LASER_PIN, 1)     # turn laser on
            laser_state = 1                       
        elif laser_state == 1:                    # if laser is on
            board.digital_write(LASER_PIN, 0)     # turn laser off
            laser_state = 0
        time.sleep(0.2)                           # wait a little bit (0.1 seconds) before checking again

    elif keyboard.is_pressed('esc'):              # if esc is pressed, quit script
        break
