import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""  # XAMPP default - no password
        self.database = "attendance_system"
        self.connection = None
        
    def create_connection(self):
        """Create database connection"""
        try:
            # First connect without database to create it if needed
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                cursor.close()
                connection.close()
            
            # Now connect to the database
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                self.create_tables()
                return self.connection
                
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def create_tables(self):
        """Create necessary tables"""
        try:
            cursor = self.connection.cursor()
            
            # Users table for authentication
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Check if default admin exists, if not create one
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            if cursor.fetchone() is None:
                cursor.execute("""
                    INSERT INTO users (username, password, role) 
                    VALUES ('admin', 'admin123', 'admin')
                """)
                print("Default admin created - Username: admin, Password: admin123")
            
            # Students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    roll_number VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(255),
                    phone VARCHAR(20),
                    face_encoding TEXT NOT NULL,
                    photo_path VARCHAR(500),
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Attendance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    date DATE NOT NULL,
                    time TIME NOT NULL,
                    status VARCHAR(20) DEFAULT 'Present',
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_attendance (student_id, date)
                )
            """)
            
            self.connection.commit()
            cursor.close()
            print("Tables created successfully")
            
        except Error as e:
            print(f"Error creating tables: {e}")
    
    def register_student(self, name, roll_number, email, phone, face_encoding, photo_path):
        """Register a new student"""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO students (name, roll_number, email, phone, face_encoding, photo_path)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, roll_number, email, phone, face_encoding, photo_path))
            self.connection.commit()
            student_id = cursor.lastrowid
            cursor.close()
            return student_id
        except Error as e:
            print(f"Error registering student: {e}")
            return None
    
    def get_all_students(self):
        """Get all registered students"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
            cursor.close()
            return students
        except Error as e:
            print(f"Error fetching students: {e}")
            return []
    
    def get_student_by_id(self, student_id):
        """Get student by ID"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
            student = cursor.fetchone()
            cursor.close()
            return student
        except Error as e:
            print(f"Error fetching student: {e}")
            return None
    
    def mark_attendance(self, student_id, date=None, time=None):
        """Mark attendance for a student"""
        try:
            if date is None:
                date = datetime.now().date()
            if time is None:
                time = datetime.now().time()
                
            cursor = self.connection.cursor()
            query = """
                INSERT INTO attendance (student_id, date, time, status)
                VALUES (%s, %s, %s, 'Present')
                ON DUPLICATE KEY UPDATE time = %s, status = 'Present'
            """
            cursor.execute(query, (student_id, date, time, time))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error marking attendance: {e}")
            return False
    
    def get_attendance_by_date(self, date=None):
        """Get attendance for a specific date"""
        try:
            if date is None:
                date = datetime.now().date()
                
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT s.id, s.name, s.roll_number, a.date, a.time, a.status
                FROM students s
                LEFT JOIN attendance a ON s.id = a.student_id AND a.date = %s
                ORDER BY s.name
            """
            cursor.execute(query, (date,))
            attendance = cursor.fetchall()
            cursor.close()
            return attendance
        except Error as e:
            print(f"Error fetching attendance: {e}")
            return []
    
    def get_attendance_report(self, start_date, end_date):
        """Get attendance report for a date range"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT s.name, s.roll_number, a.date, a.time, a.status
                FROM attendance a
                JOIN students s ON a.student_id = s.id
                WHERE a.date BETWEEN %s AND %s
                ORDER BY a.date DESC, s.name
            """
            cursor.execute(query, (start_date, end_date))
            report = cursor.fetchall()
            cursor.close()
            return report
        except Error as e:
            print(f"Error fetching attendance report: {e}")
            return []
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                         (username, password))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Error as e:
            print(f"Error verifying user: {e}")
            return None
    
    def register_user(self, username, password, role='student'):
        """Register a new user"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, %s)
            """, (username, password, role))
            self.connection.commit()
            user_id = cursor.lastrowid
            cursor.close()
            return user_id
        except Error as e:
            print(f"Error registering user: {e}")
            return None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Error as e:
            print(f"Error fetching user: {e}")
            return None
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
