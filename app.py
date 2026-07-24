from flask import Flask, render_template, Response, request, jsonify
import cv2
import pyttsx3
import os
import csv

from face_registration import FaceRegistration
from face_recognition_attendance import FaceAttendance

app = Flask(__name__)


camera = cv2.VideoCapture(0)


engine = pyttsx3.init()

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass



register_obj = FaceRegistration()
attendance_obj = FaceAttendance()



def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("Register.html")


@app.route("/api/register", methods=["POST"])
def api_register():
    name = request.json.get("name")

    if not name:
        return jsonify({"status": "Name is required"}), 400

    status = register_obj.capture_face(camera, name)
    speak("Face registration successful")

    return jsonify({"status": status})


@app.route("/start", methods=["GET"])
def start_page():
    return render_template("start.html")


@app.route("/api/attendance", methods=["POST"])
def api_attendance():
    status = attendance_obj.mark_attendance(camera)
    speak("Attendance marked successfully")

    return jsonify({"status": status})


@app.route("/records")
def records_page():
    file_path = os.path.join("Attendance", "Attendance_Data.csv")
    records = []

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) >= 3:
                    records.append(row)

    return render_template("records.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)
