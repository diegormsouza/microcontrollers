# required modules
import cv2
import mediapipe as mp
from telemetrix import telemetrix

# create a Telemetrix instance.
board = telemetrix.Telemetrix(ip_address='192.168.15.6')

# 7 segment display pins
pin_a = 16
pin_b = 5
pin_c = 4
pin_d = 0
pin_e = 2
pin_f = 14
pin_g = 12

# set the DIGITAL_PIN as an output pin
board.set_pin_mode_digital_output(pin_a)
board.set_pin_mode_digital_output(pin_b)
board.set_pin_mode_digital_output(pin_c)
board.set_pin_mode_digital_output(pin_d)
board.set_pin_mode_digital_output(pin_e)
board.set_pin_mode_digital_output(pin_f)
board.set_pin_mode_digital_output(pin_g)

def off():
    board.digital_write(pin_a, 0)
    board.digital_write(pin_b, 0)
    board.digital_write(pin_c, 0)
    board.digital_write(pin_d, 0)
    board.digital_write(pin_e, 0)
    board.digital_write(pin_f, 0)
    board.digital_write(pin_g, 0)
def num_0():
    board.digital_write(pin_a, 1)
    board.digital_write(pin_b, 1)
    board.digital_write(pin_c, 1)
    board.digital_write(pin_d, 1)
    board.digital_write(pin_e, 1)
    board.digital_write(pin_f, 1)
    board.digital_write(pin_g, 0)
def num_1():
    board.digital_write(pin_a, 0)
    board.digital_write(pin_b, 1)
    board.digital_write(pin_c, 1)
    board.digital_write(pin_d, 0)
    board.digital_write(pin_e, 0)
    board.digital_write(pin_f, 0)
    board.digital_write(pin_g, 0)
def num_2():
    board.digital_write(pin_a, 1)
    board.digital_write(pin_b, 1)
    board.digital_write(pin_c, 0)
    board.digital_write(pin_d, 1)
    board.digital_write(pin_e, 1)
    board.digital_write(pin_f, 0)
    board.digital_write(pin_g, 1)
def num_3():
    board.digital_write(pin_a, 1)
    board.digital_write(pin_b, 1)
    board.digital_write(pin_c, 1)
    board.digital_write(pin_d, 1)
    board.digital_write(pin_e, 0)
    board.digital_write(pin_f, 0)
    board.digital_write(pin_g, 1)
def num_4():
    board.digital_write(pin_a, 0)
    board.digital_write(pin_b, 1)
    board.digital_write(pin_c, 1)
    board.digital_write(pin_d, 0)
    board.digital_write(pin_e, 0)
    board.digital_write(pin_f, 1)
    board.digital_write(pin_g, 1)
def num_5():
    board.digital_write(pin_a, 1)
    board.digital_write(pin_b, 0)
    board.digital_write(pin_c, 1)
    board.digital_write(pin_d, 1)
    board.digital_write(pin_e, 0)
    board.digital_write(pin_f, 1)
    board.digital_write(pin_g, 1)
def num_6():
    board.digital_write(pin_a, 1)
    board.digital_write(pin_b, 0)
    board.digital_write(pin_c, 1)
    board.digital_write(pin_d, 1)
    board.digital_write(pin_e, 1)
    board.digital_write(pin_f, 1)
    board.digital_write(pin_g, 1)
def num_7():
    board.digital_write(pin_a, 1)
    board.digital_write(pin_b, 1)
    board.digital_write(pin_c, 1)
    board.digital_write(pin_d, 0)
    board.digital_write(pin_e, 0)
    board.digital_write(pin_f, 0)
    board.digital_write(pin_g, 0)
def num_8():
    board.digital_write(pin_a, 1)
    board.digital_write(pin_b, 1)
    board.digital_write(pin_c, 1)
    board.digital_write(pin_d, 1)
    board.digital_write(pin_e, 1)
    board.digital_write(pin_f, 1)
    board.digital_write(pin_g, 1)
def num_9():
    board.digital_write(pin_a, 1)
    board.digital_write(pin_b, 1)
    board.digital_write(pin_c, 1)
    board.digital_write(pin_d, 0)
    board.digital_write(pin_e, 0)
    board.digital_write(pin_f, 1)
    board.digital_write(pin_g, 1)
#------------------------------------------------

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# for webcam input:
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # if loading a video, use 'break' instead of 'continue'.
            continue

        # to improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # initially set finger count to 0 for each cap
        fingerCount = 0

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:
                # get hand index to check label (left or right)
                handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                handLabel = results.multi_handedness[handIndex].classification[0].label

                # set variable to keep landmarks positions (x and y)
                handLandmarks = []

                # fill list with x and y positions of each landmark
                for landmarks in hand_landmarks.landmark:
                    handLandmarks.append([landmarks.x, landmarks.y])

                # test conditions for each finger: Count is increased if finger is 
                #   considered raised.
                # thumb: TIP x position must be greater or lower than IP x position, 
                #   deppeding on hand label.
                if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                    fingerCount = fingerCount+1
                elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                    fingerCount = fingerCount+1

                 # other fingers: TIP y position must be lower than PIP y position, 
                 #   as image origin is in the upper left corner.
                if handLandmarks[8][1] < handLandmarks[6][1]:       #Index finger
                    fingerCount = fingerCount+1
                if handLandmarks[12][1] < handLandmarks[10][1]:     #Middle finger
                    fingerCount = fingerCount+1
                if handLandmarks[16][1] < handLandmarks[14][1]:     #Ring finger
                    fingerCount = fingerCount+1
                if handLandmarks[20][1] < handLandmarks[18][1]:     #Pinky
                    fingerCount = fingerCount+1

                # draw hand landmarks 
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # display finger count
        cv2.putText(image, str(fingerCount), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)

        # display image
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

        print(fingerCount)

        if (fingerCount == 0):
            num_0()
        elif (fingerCount == 1):
            num_1()
        elif (fingerCount == 2):
            num_2()
        elif (fingerCount == 3):
            num_3()
        elif (fingerCount == 4):
            num_4()
        elif (fingerCount == 5):
            num_5()
        elif (fingerCount == 6):
            num_6()
        elif (fingerCount == 7):
            num_7()
        elif (fingerCount == 8):
            num_8()    
        elif (fingerCount == 9):
            num_9()
        elif (fingerCount > 9):
            num_9()
cap.release()