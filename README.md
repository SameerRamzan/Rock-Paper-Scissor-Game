# Rock Paper Scissors Game

This repository contains a Rock Paper Scissors game that can be played in two ways:
1.  **Gesture Recognition:** Using a webcam, the game detects your hand gestures (Rock, Paper, or Scissors) in real-time.
2.  **Web Interface:** A simple web-based version where you can click buttons to make your choice.

## Features

*   **Gesture Recognition (Python):**
    *   Utilizes OpenCV for video capture and image processing.
    *   Employs MediaPipe for hand tracking and landmark detection.
    *   Detects Rock, Paper, and Scissors gestures from your hand.
    *   Real-time feedback and game logic.
*   **Web Interface (HTML/CSS/JavaScript):**
    *   Clean and user-friendly interface.
    *   Clickable buttons for Rock, Paper, and Scissors.
    *   Score tracking for player and computer.
    *   Responsive design.

## Technologies Used

*   **Python:**
    *   OpenCV (`cv2`): For camera interaction and image manipulation.
    *   MediaPipe (`mediapipe`): For hand landmark detection.
    *   `random`: For computer's choice generation.
    *   `time`: For timing game events.
*   **Web:**
    *   HTML: Structure of the web page.
    *   CSS: Styling for the web page, including a retro gaming font.
    *   JavaScript: Game logic for the web interface.

## Setup and Installation

### Gesture Recognition Game (`game.py`)

1.  **Prerequisites:**
    *   Python 3.x installed.
    *   A webcam connected to your computer.
2.  **Install Dependencies:**
    Open your terminal or command prompt and run:
    ```bash
    pip install opencv-python mediapipe
    ```
3.  **Run the Game:**
    Navigate to the repository's directory in your terminal and execute:
    ```bash
    python game.py
    ```
    A window will open showing your webcam feed. Show your hand to make a gesture (Rock, Paper, or Scissors). Hold the gesture for a few seconds to register your choice.

### Web Interface Game (`game.html`)

1.  **Prerequisites:**
    *   A modern web browser (e.g., Chrome, Firefox, Safari, Edge).
2.  **Run the Game:**
    *   Simply open the `game.html` file in your web browser.
    *   Click on the "Rock", "Paper", or "Scissors" buttons to play.

## How to Play

The rules are the classic Rock Paper Scissors rules:
*   Rock crushes Scissors
*   Scissors cuts Paper
*   Paper covers Rock

### Gesture Recognition Version:

1.  Run `game.py`.
2.  Position your hand in front of the webcam.
3.  Make one of the three gestures:
    *   **Rock:** A closed fist.
    *   **Paper:** An open hand with all fingers extended.
    *   **Scissors:** Index and middle fingers extended, other fingers curled.
4.  The game will detect your gesture. Hold it steady for a couple of seconds.
5.  The computer will make its choice, and the result will be displayed on the screen.
6.  Press 'q' to quit the game.

### Web Interface Version:

1.  Open `game.html` in your browser.
2.  Click on one of the buttons: "Rock", "Paper", or "Scissors".
3.  The computer will make its choice, and the result will be displayed on the page along with the updated scores.

## File Structure

*   `game.py`: The Python script for the gesture-based Rock Paper Scissors game. It uses OpenCV and MediaPipe to detect hand gestures from a webcam feed.
*   `game.html`: An HTML file that provides a web-based interface for playing Rock Paper Scissors. It includes CSS for styling and JavaScript for game logic.
*   `README.md`: This file, providing information about the project.
