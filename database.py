import mysql.connector
import numpy as np
import face_recognition
from datetime import datetime

def get_db_connection():
    """Establish and return a connection to the database."""
    try:
        connection = mysql.connector.connect(
            host='localhost', 
            user='root',  
            password='', 
            database='facial_attendance_system'  
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def register_user(name, image_path, face_encoding):
    """Register a new user with their face encoding."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    encoded_face = face_encoding.tobytes()
    
    if is_face_registered(face_encoding):
        cursor.close()
        conn.close()
        return False  
    
    cursor.execute(
        "INSERT INTO users (name, image_path, face_encoding) VALUES (%s, %s, %s)",
        (name, image_path, encoded_face)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True  

def is_face_registered(face_encoding):
    """Check if the face encoding is already registered in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT face_encoding FROM users")
    existing_faces = cursor.fetchall()
    
    for existing_face in existing_faces:
        existing_face_encoding = np.frombuffer(existing_face[0], dtype='float64')
        matches = face_recognition.compare_faces([existing_face_encoding], face_encoding)
        if matches[0]:
            cursor.close()
            conn.close()
            return True
    
    cursor.close()
    conn.close()
    return False

def mark_attendance(face_encoding):
    """Mark attendance if the face is recognized and return the user's name."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, face_encoding FROM users")
    users = cursor.fetchall()
    
    today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    for user in users:
        user_face_encoding = np.frombuffer(user['face_encoding'], dtype='float64')
        matches = face_recognition.compare_faces([user_face_encoding], face_encoding)
        if matches[0]:
            cursor.execute("SELECT * FROM attendance WHERE user_id = %s AND date = %s", (user['id'], today.split(' ')[0]))
            attendance = cursor.fetchone()
            if attendance:
                cursor.execute("UPDATE attendance SET check_out_time = %s WHERE user_id = %s AND date = %s", (today, user['id'], today.split(' ')[0]))
                conn.commit()
                cursor.close()
                conn.close()
                return user['name'] 
            
            
            cursor.execute("INSERT INTO attendance (user_id, date, check_in_time) VALUES (%s, %s, %s)", (user['id'], today.split(' ')[0], today))
            conn.commit()
            cursor.close()
            conn.close()
            return user['name']
    
    cursor.close()
    conn.close()
    return None

def get_attendance_by_date(date):
    """Retrieve attendance records for a specific date."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT users.name, attendance.check_in_time, attendance.check_out_time
        FROM attendance 
        JOIN users ON attendance.user_id = users.id 
        WHERE attendance.date = %s
    """
    cursor.execute(query, (date,))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records
def update_checkout_time(user_id):
    """Update the checkout time for a given user ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        UPDATE attendance 
        SET check_out_time = %s 
        WHERE user_id = %s AND date = %s AND check_out_time IS NULL
    """, (now, user_id, today))
    
    updated_rows = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()

    return updated_rows > 0
