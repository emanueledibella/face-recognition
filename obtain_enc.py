import cv2
import numpy as np
import face_recognition
import mysql.connector

img = "/var/www/photos/c.jpeg"
known_db = face_recognition.load_image_file(img)
known_db_enc = face_recognition.face_encodings(known_db)[0]

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="root",
  database="face"
)
mycursor = mydb.cursor()
finalstr = ""
print(known_db_enc)
for el in known_db_enc:
    finalstr += str(el) + " "
#mycursor.execute("UPDATE `people` set img="+finalstr+" WHERE id=2")
print(finalstr)
