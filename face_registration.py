import cv2
import numpy as np
import pickle
import os
import time

class FaceRegistration:

    def __init__(self):
        self.detector = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")

    def capture_face(self, camera, name):

        faces_data = []
        count = 0
        start = time.time()

       
        while len(faces_data) < 60 and time.time() - start < 5:
            ret, frame = camera.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                crop = frame[y:y+h, x:x+w]
                resized = cv2.resize(crop, (50, 50))
                faces_data.append(resized)
                count += 1

        if len(faces_data) == 0:
            return "No face detected. Try again."

        faces_data = np.array(faces_data).reshape(len(faces_data), -1)

        # Save to database
        if not os.path.exists('data/faces_data.pkl'):
            pickle.dump(faces_data, open("data/faces_data.pkl", "wb"))
            pickle.dump([name] * len(faces_data), open("data/names.pkl", "wb"))
        else:
            old_faces = pickle.load(open("data/faces_data.pkl", "rb"))
            old_names = pickle.load(open("data/names.pkl", "rb"))

            all_faces = np.append(old_faces, faces_data, axis=0)
            all_names = old_names + [name] * len(faces_data)

            pickle.dump(all_faces, open("data/faces_data.pkl", "wb"))
            pickle.dump(all_names, open("data/names.pkl", "wb"))

        return f"Face registered successfully for {name}"
