from flask import Flask, render_template, request, redirect, url_for, flash, session
import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
from database import register_user, mark_attendance, get_attendance_by_date, is_face_registered, update_checkout_time

app = Flask(__name__)
app.secret_key = "your_secret_key"

REGISTERED_FACES_DIR = 'images/registered_faces'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        video_capture = cv2.VideoCapture(0)

        ret, frame = video_capture.read()
        if not ret:
            flash('Failed to capture image', 'danger')
            return redirect(url_for('register'))

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            face_encoding = face_encodings[0]

            if is_face_registered(face_encoding):
                flash('User face captured already...', 'warning')
                return redirect(url_for('register'))

            image_path = os.path.join(REGISTERED_FACES_DIR, f"{name}.jpg")
            cv2.imwrite(image_path, frame)

            register_user(name, image_path, face_encoding)
            flash(f'Registration successful for {name}', 'success')
            return redirect(url_for('index'))
        else:
            flash('No face detected. Please try again.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/mark-attendance', methods=['GET'])
def mark_attendance_route():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            flash('Failed to capture image', 'danger')
            return redirect(url_for('index'))

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            for face_encoding in face_encodings:
                user_name = mark_attendance(face_encoding)
                if user_name:
                    session['user_name'] = user_name
                    flash(f"Your attendance is recorded, {user_name}", 'success')
                    return redirect(url_for('index'))
            flash('Face not recognized.', 'warning')
            return redirect(url_for('index'))
        else:
            flash('No face detected.', 'danger')
            return redirect(url_for('index'))


@app.route('/view-attendance', methods=['GET', 'POST'])
def view_attendance():
    attendance_records = None
    selected_date = None
    
    if request.method == 'POST':
        selected_date = request.form.get('attendance_date')
        if selected_date:
            attendance_records = get_attendance_by_date(selected_date)
    
    return render_template('view_attendance.html', attendance_records=attendance_records, selected_date=selected_date)

def get_user_id_by_name(name):
    """Retrieve user ID by user name."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user['id'] if user else None

if __name__ == "__main__":
    app.run(debug=True)
