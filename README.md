
# Pushup - Counter

# 📌 Project Overview: Push-up Counter with MediaPipe

- This project is a real-time push-up counter developed using Python, MediaPipe, and OpenCV. It uses a webcam feed (e.g., a regular webcam or DroidCam mobile camera) to detect body landmarks and calculate joint angles to accurately count push-ups based on user posture.

# 🎯 Key Features
- Pose Detection: Utilizes MediaPipe's pose estimation model to track body landmarks such as shoulders, elbows, wrists, hips, and ankles.

- Angle Calculation: Calculates elbow angles to determine the user's push-up stage (up or down) and checks back straightness to ensure proper form.

# Real-time Feedback:

-  Displays the angle of arms on screen.

-  Gives audio beep feedback and increments the counter on every valid push-up.

-  Warns the user with an on-screen alert if the back is not straight.

-  Threaded Sound Playback: Uses a separate thread to play a beep sound (beep.wav) without interrupting the main video    loop.

# 🧠 How It Works
- Detects pose landmarks via MediaPipe.

- Calculates the average angle of both arms.

- Monitors the up and down stages of push-ups by comparing arm angles.

- Checks back posture using the shoulder–hip–ankle alignment.

- Updates the push-up counter only if the movement and posture are valid.

# 🛠️ Technologies Used
-> Python

-> OpenCV

-> MediaPipe (Pose Estimation)

-> NumPy

-> playsound (for beep sound)

-> threading (for non-blocking sound)

