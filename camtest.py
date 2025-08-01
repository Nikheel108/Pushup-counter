import cv2

print("🔍 Scanning available camera indices...\n")

for i in range(5):
    cap = cv2.VideoCapture(i)  # uses MSMF by default on Windows
    if cap.isOpened():
        print(f"✅ Camera index {i} is working.")
        ret, frame = cap.read()
        if ret:
            cv2.imshow(f"Camera {i}", frame)
            cv2.waitKey(2000)  # Show for 2 seconds
        cap.release()
        cv2.destroyAllWindows()
    else:
        print(f"❌ Camera index {i} failed.")
