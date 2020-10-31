import face_recognition
import mysql.connector
import cv2
import numpy as np
import threading
from imutils.video import FPS
from numba import jit, cuda

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="root",
  database="face"
)
# Initialize some variables
face_locations = [1]
face_encodings = [1]
name = "Unkown"
video_capture = cv2.VideoCapture(0)
fps = FPS().start()
mycursor = mydb.cursor()
def tofloat(s):
    for idx, val in enumerate(s):
        s[idx] = float(val)
    return s
def search(name):
    for face_encoding in face_encodings:
        mycursor.execute("SELECT * FROM `people`")
        myresult = mycursor.fetchall()
        for row in myresult:
            known_db_enc = row[3].split(" ")
            known_db_enc = np.array(tofloat(known_db_enc))
            result = face_recognition.compare_faces([known_db_enc], face_encoding)
            if(result[0]):
                name = row[1] + " " + row[2]
                break
    for (top, right, bottom, left) in face_locations:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)




while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    search(name)
    # Display the resulting image
    cv2.imshow('Video', frame)
    #threading.Thread(target=draw, args=(face_locations,frame, name)).start()
    #Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
