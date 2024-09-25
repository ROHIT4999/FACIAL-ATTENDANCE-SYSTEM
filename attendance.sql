
CREATE DATABASE IF NOT EXISTS facial_attendance_system;
USE facial_attendance_system;


CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    face_encoding BLOB NOT NULL
);


CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    check_in_time DATETIME,
    check_out_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, date)
);


CREATE INDEX idx_user_id ON attendance(user_id);
CREATE INDEX idx_date ON attendance(date);
