from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, session
from database import Database
from face_recognition_module import FaceRecognitionSystem
from excel_generator import ExcelReportGenerator
from datetime import datetime, timedelta
from functools import wraps
import os
import cv2
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_this'  # Change this to a random secret key

# Initialize components
db = Database()
face_system = FaceRecognitionSystem()
excel_generator = ExcelReportGenerator()

# Connect to database
connection = db.create_connection()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin only decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Admin access required!', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', 
                         logged_in='user_id' in session,
                         username=session.get('username', ''),
                         role=session.get('role', ''))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.verify_user(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome {username}!', 'success')
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    total_students = len(db.get_all_students())
    today_attendance = db.get_attendance_by_date()
    present_count = sum(1 for r in today_attendance if r.get('status'))
    
    return render_template('admin_dashboard.html',
                         total_students=total_students,
                         present_today=present_count,
                         absent_today=total_students - present_count)

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    """Student dashboard"""
    return render_template('student_dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
@admin_required
def register():
    """Student registration page"""
    if request.method == 'POST':
        name = request.form.get('name')
        roll_number = request.form.get('roll_number')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        if not name or not roll_number:
            flash('Name and Roll Number are required!', 'error')
            return redirect(url_for('register'))
        
        # Check if roll number already exists
        students = db.get_all_students()
        if any(s['roll_number'] == roll_number for s in students):
            flash('Roll Number already exists!', 'error')
            return redirect(url_for('register'))
        
        # Capture and encode face
        try:
            captured_image, message = face_system.capture_face()
            
            if captured_image is None:
                flash(f'Face capture failed: {message}', 'error')
                return redirect(url_for('register'))
            
            face_encoding, encode_message = face_system.encode_face(captured_image)
            
            if face_encoding is None:
                flash(f'Face encoding failed: {encode_message}', 'error')
                return redirect(url_for('register'))
            
            # Save face image
            photo_path = face_system.save_face_image(captured_image, name, roll_number)
            
            # Convert encoding to string
            encoding_string = face_system.encode_to_string(face_encoding)
            
            # Register student in database
            student_id = db.register_student(name, roll_number, email, phone, encoding_string, photo_path)
            
            if student_id:
                flash(f'Student {name} registered successfully!', 'success')
                return redirect(url_for('students'))
            else:
                flash('Failed to register student in database.', 'error')
                return redirect(url_for('register'))
                
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    """Student self-registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        roll_number = request.form.get('roll_number')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        if not username or not password or not name or not roll_number:
            flash('Username, Password, Name and Roll Number are required!', 'error')
            return redirect(url_for('student_register'))
        
        # Check if username already exists
        if db.get_user_by_username(username):
            flash('Username already exists!', 'error')
            return redirect(url_for('student_register'))
        
        # Check if roll number already exists
        students = db.get_all_students()
        if any(s['roll_number'] == roll_number for s in students):
            flash('Roll Number already exists!', 'error')
            return redirect(url_for('student_register'))
        
        # Capture and encode face
        try:
            captured_image, message = face_system.capture_face()
            
            if captured_image is None:
                flash(f'Face capture failed: {message}', 'error')
                return redirect(url_for('student_register'))
            
            face_encoding, encode_message = face_system.encode_face(captured_image)
            
            if face_encoding is None:
                flash(f'Face encoding failed: {encode_message}', 'error')
                return redirect(url_for('student_register'))
            
            # Save face image
            photo_path = face_system.save_face_image(captured_image, name, roll_number)
            
            # Convert encoding to string
            encoding_string = face_system.encode_to_string(face_encoding)
            
            # Register user account
            user_id = db.register_user(username, password, 'student')
            
            if not user_id:
                flash('Failed to create user account.', 'error')
                return redirect(url_for('student_register'))
            
            # Register student in database
            student_id = db.register_student(name, roll_number, email, phone, encoding_string, photo_path)
            
            if student_id:
                flash(f'Registration successful! You can now login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Failed to register student in database.', 'error')
                return redirect(url_for('student_register'))
                
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'error')
            return redirect(url_for('student_register'))
    
    return render_template('student_register.html')

@app.route('/students')
@admin_required
def students():
    """View all registered students"""
    all_students = db.get_all_students()
    return render_template('students.html', students=all_students)

@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    """Mark attendance page"""
    if request.method == 'POST':
        try:
            # Load all known faces
            students_data = db.get_all_students()
            
            if len(students_data) == 0:
                flash('No students registered yet. Please register students first.', 'warning')
                return redirect(url_for('attendance'))
            
            face_system.load_known_faces(students_data)
            
            # Recognize face from camera
            student_id, student_name, message = face_system.recognize_face_from_camera(timeout=30)
            
            if student_id is None:
                flash(f'Attendance failed: {message}', 'error')
                return redirect(url_for('attendance'))
            
            # Mark attendance
            success = db.mark_attendance(student_id)
            
            if success:
                flash(f'Attendance marked for {student_name}!', 'success')
            else:
                flash(f'Failed to mark attendance for {student_name}.', 'error')
                
        except Exception as e:
            flash(f'Error during attendance: {str(e)}', 'error')
        
        return redirect(url_for('attendance'))
    
    # Get today's attendance
    today_attendance = db.get_attendance_by_date()
    return render_template('attendance.html', attendance_records=today_attendance)

@app.route('/reports')
@admin_required
def reports():
    """View attendance reports"""
    # Get today's attendance
    today = datetime.now().date()
    today_attendance = db.get_attendance_by_date(today)
    
    return render_template('reports.html', 
                         attendance_records=today_attendance,
                         current_date=today)

@app.route('/generate_daily_report', methods=['POST'])
@admin_required
def generate_daily_report():
    """Generate daily attendance Excel report"""
    try:
        date_str = request.form.get('date')
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = datetime.now().date()
        
        attendance_data = db.get_attendance_by_date(date)
        filepath, message = excel_generator.generate_daily_report(attendance_data, date)
        
        flash(message, 'success')
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('reports'))

@app.route('/generate_range_report', methods=['POST'])
@admin_required
def generate_range_report():
    """Generate date range attendance Excel report"""
    try:
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        if not start_date_str or not end_date_str:
            flash('Please provide both start and end dates.', 'error')
            return redirect(url_for('reports'))
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        attendance_data = db.get_attendance_report(start_date, end_date)
        filepath, message = excel_generator.generate_range_report(attendance_data, start_date, end_date)
        
        flash(message, 'success')
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('reports'))

@app.route('/generate_student_list')
@admin_required
def generate_student_list():
    """Generate student list Excel report"""
    try:
        filepath, message = excel_generator.generate_student_summary(db)
        flash(message, 'success')
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        flash(f'Error generating student list: {str(e)}', 'error')
        return redirect(url_for('students'))

@app.route('/delete_student/<int:student_id>', methods=['POST'])
@admin_required
def delete_student(student_id):
    """Delete a student"""
    try:
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        db.connection.commit()
        cursor.close()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'error')
    
    return redirect(url_for('students'))

if __name__ == '__main__':
    print("Starting Face Detection Attendance System...")
    print("Access the application at: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
