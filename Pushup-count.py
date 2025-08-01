import cv2
import mediapipe as mp
import numpy as np
from playsound import playsound
import threading

# For sound playback in parallel
def play_beep():
    threading.Thread(target=playsound, args=("beep.wav",), daemon=True).start()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

cap = cv2.VideoCapture(1)  # Use correct index for DroidCam

counter = 0
stage = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
        lm = results.pose_landmarks.landmark
        h, w, _ = image.shape

        # Right arm
        r_shoulder = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        r_elbow = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                   lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        r_wrist = [lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                   lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        # Left arm
        l_shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                      lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        l_elbow = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                   lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        l_wrist = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                   lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        # Back straightness check (shoulder, hip, ankle)
        r_hip = [lm[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                 lm[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        r_ankle = [lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        back_angle = calculate_angle(r_shoulder, r_hip, r_ankle)

        # Calculate angles
        r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
        l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
        avg_angle = (r_angle + l_angle) / 2

        # Display angle on screen
        cv2.putText(image, f'Angle: {int(avg_angle)}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # Push-up detection
        if avg_angle > 160 and back_angle > 150:
            stage = "up"
        if avg_angle < 90 and stage == "up" and back_angle > 150:
            stage = "down"
            counter += 1
            play_beep()
            print(f"Reps: {counter}")

        # Draw counter box
        cv2.rectangle(image, (0, 0), (200, 100), (0, 0, 0), -1)
        cv2.putText(image, 'Push-ups', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(image, str(counter), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 2)

        # Form feedback
        if back_angle < 140:
            cv2.putText(image, "❗Keep your back straight!", (w//3, h - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    except AttributeError:
        pass

    # Draw pose landmarks
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Push-up Counter", image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("total push-up: ",counter)
        break

cap.release()
cv2.destroyAllWindows()
