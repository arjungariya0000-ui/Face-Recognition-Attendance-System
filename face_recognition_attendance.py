import cv2
import numpy as np
import pickle
import csv
import os
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier

class FaceAttendance:

    def __init__(self):
        self.detector = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")

        if os.path.exists("data/faces_data.pkl") and os.path.exists("data/names.pkl"):
            self.faces = pickle.load(open("data/faces_data.pkl", "rb"))
            self.labels = pickle.load(open("data/names.pkl", "rb"))

            if len(self.faces) > 0:
                self.knn = KNeighborsClassifier(n_neighbors=5)
                self.knn.fit(self.faces, self.labels)
            else:
                self.knn = None
        else:
            self.knn = None

    def mark_attendance(self, camera):

        if self.knn is None:
            return "No registered faces. Please register first."

        ret, frame = camera.read()
        if not ret:
            return "Camera error."

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return "No face detected."

        (x, y, w, h) = faces[0]
        crop = frame[y:y+h, x:x+w]
        resized = cv2.resize(crop, (50, 50)).flatten().reshape(1, -1)

        name = self.knn.predict(resized)[0]

        os.makedirs("Attendance", exist_ok=True)
        file_path = "Attendance/Attendance_Data.csv"

        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")

        new_file = not os.path.exists(file_path)

        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)

            if new_file:
                writer.writerow(["Name", "Date", "Time"])

            writer.writerow([name, date, time])

        return f"Attendance marked for {name}"
