# FACIAL-ATTENDANCE-SYSTEM

The Facial Attendance System is an automated system that uses facial recognition technology to record and manage attendance in real-time. By leveraging a camera, the system captures and identifies individuals' faces, marks their attendance, and stores the data in a database. This system eliminates the need for manual attendance marking, offering a contactless, efficient, and secure solution for educational institutions, workplaces, and other environments where attendance tracking is required.

Features of the Facial Attendance System:

Real-Time Face Recognition: The system captures faces from a live video feed (e.g., a webcam) and compares them with stored facial data to identify the individuals.

Automatic Attendance Logging: Once a face is recognized, the system logs the person's attendance along with the time and date in a database or file.

Multiple Faces Detection: The system can detect and recognize multiple faces at once, allowing simultaneous attendance marking in group settings.

Attendance Database: Attendance records are stored in a database (e.g., MySQL), where administrators can retrieve, analyze, and generate reports.

User-Friendly Interface: The system can have a simple user interface, where administrators can monitor the attendance process or view attendance data.

Daily, Weekly, and Monthly Reports: The system can be extended to generate attendance reports for specific time periods, making it easy for administrators to track attendance history.

Face Registration/Enrollment: New users can be added to the system by capturing and storing their face encodings.

Technologies and Tools Used:

Python: The core programming language used to develop the system.

OpenCV: For video capturing and face detection from the camera feed.

Face Recognition Library: To perform face encoding, comparison, and recognition using deep learning techniques.

Flask (Optional): A lightweight web framework to build a web interface for attendance monitoring.

MySQL (Optional): For storing attendance data in a database.

Pickle: For storing and loading face encodings efficiently.

System Workflow:

User Registration (Enrollment):
Each individual needs to register in the system by capturing their face using a webcam.
The system generates a unique facial encoding for each registered individual and stores it in a file or a database.

Attendance Process:
When the system is active, it continuously captures a video feed from the camera and detects faces in real-time.
For each detected face, the system generates an encoding and compares it with the stored encodings to identify the individual.
If a match is found, the individual's attendance is marked in the database with a timestamp (date and time).

Attendance Logging:
The system logs the user’s attendance in a MySQL database or a local file, storing information such as:
User ID/Name
Date and Time of attendance
Additional details like location (if extended with GPS functionality)

Attendance Reports:
Administrators can query the attendance data and generate reports showing attendance for a day, week, or month.
The system can also be extended to send notifications or emails to absent individuals.


Setup Procedure:

1.Download the zip file and extract it in desired location.

2.Install the required packages using pip install -r 
requirements.txt.

3.Setup up the database by importing the sql file in the MySQL(phpMyAdmin) through Xampp Control Panel.

4.Run the application using "python app.py" in the command line.