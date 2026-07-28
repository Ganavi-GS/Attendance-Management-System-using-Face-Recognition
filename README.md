# Face Detection Attendance System

A comprehensive web-based attendance management system using facial recognition technology. This system allows automatic attendance marking by recognizing registered students' faces through a webcam.

## Features

✅ **Student Registration**
- Register new students with face capture
- Store student details (name, roll number, email, phone)
- Automatic face encoding and database storage

✅ **Automatic Attendance**
- Real-time face recognition
- Automatic attendance marking
- Error handling for unregistered faces
- One attendance per student per day

✅ **Database Management**
- MySQL database for secure data storage
- Student information management
- Attendance records tracking
- Automatic table creation

✅ **Excel Reports**
- Daily attendance reports
- Date range reports
- Student list export
- Color-coded status (Present/Absent)

✅ **Web Interface**
- Modern, responsive design
- User-friendly navigation
- Real-time feedback
- Mobile-compatible

## Technology Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Face Recognition:** face_recognition library, OpenCV
- **Frontend:** HTML, CSS
- **Reports:** Pandas, OpenPyxl

## Prerequisites

Before installation, ensure you have:

1. **Python 3.8 or higher**
2. **MySQL Server** (5.7 or higher)
3. **Webcam** (for face capture and recognition)
4. **Visual Studio Build Tools** (for Windows, to compile dlib)

## Installation Steps

### Step 1: Install MySQL

1. Download MySQL from: https://dev.mysql.com/downloads/mysql/
2. Install MySQL Server
3. Remember your MySQL root password
4. Start MySQL service

### Step 2: Clone/Download Project

Download or clone this project to your computer.

### Step 3: Install Python Dependencies

Open Command Prompt in the project directory and run:

```cmd
pip install -r requirements.txt
```

**Note for Windows Users:**
If you encounter errors installing `dlib`, you may need to:
1. Install Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
2. Or download pre-compiled dlib wheel from: https://github.com/z-mahmud22/Dlib_Windows_Python3.x

### Step 4: Configure Database

1. Open `database.py` file
2. Update MySQL credentials:
```python
self.user = "root"           # Your MySQL username
self.password = "your_password"  # Your MySQL password
```

### Step 5: Run the Application

```cmd
python app.py
```

The application will:
- Create the database automatically
- Create necessary tables
- Start the web server

### Step 6: Access the Application

Open your web browser and go to:
```
http://127.0.0.1:5000
```

## Usage Guide

### 1. Register a Student

1. Click "Register Student" from the navigation menu
2. Fill in student details:
   - Full Name (required)
   - Roll Number (required, must be unique)
   - Email (optional)
   - Phone (optional)
3. Click "Register Student (Will Open Camera)"
4. When camera opens:
   - Position your face in the frame
   - Press SPACE to capture
   - Press ESC to cancel
5. System will encode and save the face data

### 2. Mark Attendance

1. Click "Mark Attendance" from the navigation menu
2. Click "Start Face Recognition" button
3. Camera will open automatically
4. Position your face in front of the camera
5. System will automatically:
   - Detect your face
   - Match with registered students
   - Mark attendance if match found
   - Show error if no match found
6. Press ESC to cancel at any time

### 3. View Students

- Click "View Students" to see all registered students
- View student details (roll number, name, email, phone, registration date)
- Delete students if needed
- Download student list as Excel file

### 4. Generate Reports

1. Click "Reports" from the navigation menu
2. For Daily Report:
   - Select a date
   - Click "Download Daily Report"
3. For Date Range Report:
   - Select start date
   - Select end date
   - Click "Download Range Report"
4. Reports are saved in `attendance_reports` folder

## Project Structure

```
Attendecnce/
│
├── app.py                      # Main Flask application
├── database.py                 # Database operations
├── face_recognition_module.py  # Face recognition logic
├── excel_generator.py          # Excel report generation
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
│
├── data/                       # Stored face images
├── attendance_reports/         # Generated Excel reports
│
├── static/
│   └── style.css              # CSS styling
│
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Home page
    ├── register.html          # Student registration
    ├── students.html          # View students
    ├── attendance.html        # Mark attendance
    └── reports.html           # Attendance reports
```

## Workflow

```
1. New Student Registration
   ↓
   Capture Face → Encode Face → Store in Database
   
2. Mark Attendance
   ↓
   Open Camera → Detect Face → Match with Database
   ↓
   Match Found? → Yes → Mark Attendance
                → No  → Show "No Match" Error

3. Generate Reports
   ↓
   Select Date/Range → Query Database → Generate Excel
```

## Troubleshooting

### Camera Not Opening
- Check if webcam is connected
- Ensure no other application is using the camera
- Grant camera permissions to Python

### Face Not Recognized
- Ensure good lighting
- Face the camera directly
- Remove glasses or obstructions if possible
- Try registering again with better image quality

### MySQL Connection Error
- Verify MySQL is running
- Check username and password in `database.py`
- Ensure MySQL server is accessible

### Installation Errors
- Use Python 3.8-3.10 (face_recognition compatibility)
- Install Visual Studio Build Tools for Windows
- Try using pre-compiled dlib wheel for Windows

## Database Schema

### Students Table
```sql
- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- name (VARCHAR)
- roll_number (VARCHAR, UNIQUE)
- email (VARCHAR)
- phone (VARCHAR)
- face_encoding (TEXT)
- photo_path (VARCHAR)
- registration_date (TIMESTAMP)
```

### Attendance Table
```sql
- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- student_id (INT, FOREIGN KEY)
- date (DATE)
- time (TIME)
- status (VARCHAR)
- UNIQUE constraint on (student_id, date)
```

## Security Notes

1. Change the Flask secret key in `app.py`
2. Use strong MySQL password
3. Don't commit database credentials to version control
4. Consider using environment variables for sensitive data

## Future Enhancements

- Multi-face detection in one frame
- SMS/Email notifications
- Admin dashboard with analytics
- API for mobile app integration
- Attendance history graphs
- Student photo gallery

## License

This project is for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all prerequisites are installed
3. Ensure MySQL is running and configured correctly
4. Check Python version compatibility (3.8-3.10 recommended)

## Credits

Built with:
- Flask (Web Framework)
- face_recognition library by Adam Geitgey
- OpenCV (Computer Vision)
- MySQL (Database)
- Pandas & OpenPyxl (Excel Reports)

---

**Note:** Make sure your webcam is functional and properly connected before using the system.
