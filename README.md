 AI Virtual Whiteboard

An AI-based virtual whiteboard that uses hand gesture recognition to draw in the air using your webcam. Built with Python, OpenCV, and MediaPipe, this project allows you to:

 Draw with different colors

 Erase drawings

 Undo strokes

Save your artwork

Control everything using hand gestures

Features

Real-time hand tracking using MediaPipe

Computer vision powered by OpenCV

Gesture-based drawing system

Dynamic brush thickness based on finger distance

Undo functionality using stack memory

Save drawings as PNG images

Smooth stroke rendering

Technologies Used

Python 3.x

OpenCV

MediaPipe

NumPy

 How It Works
1️ Hand Tracking

The webcam feed is processed using MediaPipe Hands to detect 21 hand landmarks.

2️ Gesture Detection

Two fingers up (Index + Middle) → Selection Mode

One finger up (Index only) → Drawing Mode

3️ Brush Thickness

The distance between the index and middle finger dynamically controls brush thickness.

4️ UI Controls

Top bar options:

 Color Selection

 Eraser
Controls
Gesture	Action
Index + Middle Finger	Select Mode
Index Finger Only	Draw
Touch Top Bar	Choose Color / Erase / Undo / Save

 Output
Saved images will be stored in the project folder as:

AI_board_<timestamp>.png

 Undo

 Save
