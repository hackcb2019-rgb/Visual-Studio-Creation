import cv2
import ctypes
import os
import urllib.request

# Haar cascade file ko local folder me automatically download karein
xml_filename = "haarcascade_frontalface_default.xml"
xml_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"

if not os.path.exists(xml_filename):
    print("Haar Cascade XML file download ho rahi hai...")
    urllib.request.urlretrieve(xml_url, xml_filename)
    print("Download Complete!")

face_cascade = cv2.CascadeClassifier(xml_filename)

if face_cascade.empty():
    print("Error: XML file corrupt hai ya load nahi hui.")
    exit()

cap = cv2.VideoCapture(0)
print("Security System Started! Screen se door jane par PC lock hoga.")

no_face_frames = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera access error.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    if len(faces) > 0:
        no_face_frames = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Access Granted: Face Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        no_face_frames += 1
        cv2.putText(frame, f"Warning: No Face ({no_face_frames})", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 30 frames tak face nahi milne par lock
    if no_face_frames > 30:
        print("Face missing! Windows lock ho raha hai...")
        ctypes.windll.user32.LockWorkStation()
        break

    cv2.imshow("Face Security System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()