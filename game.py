import cv2
import mediapipe as mp 
import random 
import time

# initialize mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

#game values
choices = ['Rock', 'Paper', 'Scissors']

def get_gesture(hand_landmarks):
    """
    Determines the hand gesture (Rock, Paper, or Scissors) based on hand landmarks.

    Args:
        hand_landmarks: A list or object containing the 3D coordinates of hand keypoints.
                        It is assumed that this object has a 'landmark' attribute,
                        which is a list of landmarks. Each landmark has 'x', 'y', and 'z' attributes.
                        Specifically, it expects the MediaPipe hand landmark format.

    Returns:
        str: The detected gesture ('Rock', 'Paper', or 'Scissors'). Returns None
             if no valid gesture is detected.
    """
    finger_states = []  # Initializes an empty list called `finger_states`.
                        # This list will store boolean values (True/False) indicating
                        # whether each finger is extended or not.  For example,
                        # if the index finger is extended, the first element of
                        # finger_states will be True.
    tip_ids = [8, 12, 16, 20]  # Creates a list called `tip_ids` containing the indices 8, 12, 16, and 20.
                            # These indices correspond to the positions of the finger tips
                            # (index, middle, ring, and pinky finger tips, respectively)
                            # within the `hand_landmarks` data structure.  The specific
                            # numbers (8, 12, 16, 20) are based on the MediaPipe
                            # hand landmark model's numbering scheme.
    for i in tip_ids:  # Starts a `for` loop that iterates through each index in the `tip_ids` list.
                    # In each iteration, the variable `i` will take on the values 8, 12, 16, and 20.
        finger_tip_y = hand_landmarks.landmark[i].y  # Inside the loop, this line retrieves the y-coordinate of a finger tip.
                                                    # `hand_landmarks` is assumed to be an object (like the output of MediaPipe)
                                                    # that contains the 3D coordinates of various hand keypoints.
                                                    # `hand_landmarks.landmark[i]` accesses the landmark data for the finger tip
                                                    # whose index is `i`.  For example, when i is 8, it gets the data for the
                                                    # index finger tip.  The result is a landmark object.
                                                    # `.y` extracts the y-coordinate of that finger tip landmark.
                                                    # The y-coordinate represents the vertical position of the finger tip in the image.
        finger_dip_y = hand_landmarks.landmark[i - 2].y  # This line retrieves the y-coordinate of the finger's
                                                        # proximal interphalangeal (PIP) joint.  The PIP joint is the
                                                        # joint in the middle of the finger.
                                                        # `i - 2` calculates the index of the PIP joint relative to
                                                        # the finger tip.  This assumes a specific ordering of landmarks
                                                        # within the `hand_landmarks.landmark` list (which is the case
                                                        # for MediaPipe).  For example, if i is 8 (index finger tip),
                                                        # i-2 (which is 6) will give you the index of the index finger's PIP joint.
                                                        # `.y` extracts the y-coordinate of the PIP joint.
        finger_states.append(finger_tip_y < finger_dip_y)  # This is the core logic for determining if a finger is extended.
                                                            # It compares the y-coordinate of the finger tip (`finger_tip_y`)
                                                            # with the y-coordinate of the finger's PIP joint (`finger_dip_y`).
                                                            # In most hand tracking systems (like MediaPipe), the y-axis
                                                            # increases as you go down the image.  Therefore:
                                                            # -   If `finger_tip_y` is less than `finger_dip_y`, it means the
                                                            #     finger tip is "higher" (more extended) than the PIP joint.
                                                            # -   If `finger_tip_y` is greater than or equal to `finger_dip_y`,
                                                            #     it means the finger is bent.
                                                            # The result of this comparison (either `True` or `False`) is
                                                            # appended to the `finger_states` list.  So, `finger_states`
                                                            # will eventually contain four boolean values, one for each
                                                            # of the four fingers (index, middle, ring, pinky).
    if all(x is False for x in finger_states):  # After the loop has processed all four fingers, this line checks if all
                                                # the values in the `finger_states` list are `False`.
                                                # `all()` is a built-in Python function that returns `True` if all
                                                # elements in an iterable (like a list) are true, and `False` otherwise.
                                                # `x is False for x in finger_states` is a generator expression that
                                                # iterates through `finger_states` and checks if each element `x` is `False`.
        return 'Rock'  # If all fingers are bent (not extended), the function returns the string 'Rock'.
    elif finger_states[0] and finger_states[1] and not any(finger_states[2:]):
        # This condition checks for the "Scissors" gesture.  It's a more complex condition:
        # -   `finger_states[0]` checks if the first finger (thumb) is extended (True).
        # -   `finger_states[1]` checks if the second finger (index finger) is extended (True).
        # -   `any(finger_states[2:])` checks if any of the remaining fingers
        #     (middle, ring, and pinky) are extended.  `any()` returns `True` if at least
        #     one element in the iterable is true.
        # -   `not any(finger_states[2:])` negates the result of `any()`.  So, this part
        #     checks if *none* of the remaining fingers are extended.
        # In summary, this line checks: "Is the thumb extended AND is the index finger
        # extended AND are the middle, ring, and pinky fingers all bent?".
        return 'Scissors'  # If the condition is true, the function returns 'Scissors'.
    elif all(x is True for x in finger_states):  # Checks if all the values in the `finger_states` list are `True`.
        return 'Paper'  # If all fingers are extended, the function returns the string 'Paper'.
    else:
        return None  # If none of the above conditions are met (i.e., the hand gesture doesn't
                    # match Rock, Paper, or Scissors), the function returns `None`.  This indicates
                    # that the function couldn't recognize a valid gesture.
#capture the video
cap = cv2.VideoCapture(0)
prev_gest = None
timer_started = False
start_time = 0
print("show rock, paper or scissors with your hand!")

while True:
    success, image = cap.read()  # Reads a frame from the video capture object `cap`.
                                # `cap` is assumed to be a cv2.VideoCapture object that has been
                                # initialized to capture video from a camera or a video file.
                                # `cap.read()` returns a tuple:
                                #   - `success`: A boolean that is True if the frame was read successfully,
                                #              and False if there was an error or the end of the video stream was reached.
                                #   - `image`: A NumPy array representing the video frame.
    image = cv2.flip(image, 1)  # Flips the image horizontally (along the y-axis).
                                # This is commonly done when using a webcam, as the image is
                                # mirrored by default.  The '1' argument specifies horizontal flip.
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Converts the image from BGR color space (which is the
                                                # default color format used by OpenCV) to RGB color space.
                                                # MediaPipe, which is used for hand tracking, expects RGB input.
    result = hands.process(rgb)  # Processes the RGB image using the MediaPipe Hands model.
                                # `hands` is assumed to be a pre-initialized MediaPipe Hands object.
                                # This line detects hands in the image and returns the hand landmark
                                # information in the `result` object.
    gesture = None #initializes the gesture variable

    if result.multi_hand_landmarks:  # Checks if any hands were detected in the current frame.
        for handLms in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)
            gesture = get_gesture(handLms)
            if gesture:
                print(f"Gesture detected {gesture}")

            if gesture and gesture != prev_gest:
                timer_started = True
                start_time = time.time()
                prev_gest = gesture

            if timer_started:
                cv2.putText(image, "hold gesture..", (10,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,250), 2)
                if time.time() - start_time > 2:
                    computer_choice = random.choice(choices)
                    result_text = ""
                    if gesture == computer_choice:
                        result_text = "It's a Tie!"
                    elif (gesture == "Rock" and computer_choice == "Scissors") or (gesture == "Scissors" and computer_choice == "Paper") or (gesture == "Paper" and computer_choice == "Rock"):
                        result_text = "You Win!"
                    else:
                        result_text = 'You Lost The Game'
                    
                    result_display_time = time.time()
                    while time.time() - result_display_time < 3:
                        temp_img = image.copy()
                        cv2.putText(temp_img, f"you: {gesture}", (10, 100),
                                    cv2.FONT_HERSHEY_COMPLEX, 1.2, (0,250,0), 3)
                        cv2.putText(temp_img, f"Computer: {computer_choice}", (10, 150),
                                    cv2.FONT_HERSHEY_COMPLEX, 1.2, (0,250,0), 3)
                        cv2.putText(temp_img, result_text, (10, 200),
                                    cv2.FONT_HERSHEY_COMPLEX, 1.2, (250,0,0), 3)
                        cv2.imshow("Rock Paper Scissors", temp_img)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            cap.release()
                            cv2.destroyAllWindows()
                            exit()
                    timer_started = False

            cv2.imshow("Rock Paper Scissors", image)  # Displays the image with the hand landmarks and any text overlays
                                                # in a window titled "Rock Paper Scissors".
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Waits for a key press for 1 millisecond.
                                                # `cv2.waitKey(1)` returns the code of the pressed key.
                                                # `& 0xFF` is a bitmask that ensures the key code is within the
                                                # 8-bit range (0-255).  This is necessary for cross-platform compatibility.`ord('q')` returns the ASCII code of the character 'q'.
                break  # If the user presses the 'q' key, the loop breaks, and the program exits the game.
cap.release()  # Releases the video capture object `cap`, freeing up the camera or video file.    
cap.release()
cv2.destroyAllWindows()