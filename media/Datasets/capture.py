import cv2

url = "http://192.168.31.49:8080/video"  # Replace with your IP camera stream URL
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Failed to connect to IP camera")
else:
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        print("Image captured successfully")
    else:
        print("Failed to capture image")

cap.release()
