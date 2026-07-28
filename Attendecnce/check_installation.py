"""
Installation Verification Script
Run this script to check if all dependencies are installed correctly
"""

import sys

def check_imports():
    """Check if all required packages can be imported"""
    
    print("=" * 60)
    print("Face Detection Attendance System - Installation Check")
    print("=" * 60)
    print()
    
    packages = {
        'Flask': 'flask',
        'MySQL Connector': 'mysql.connector',
        'OpenCV': 'cv2',
        'NumPy': 'numpy',
        'Pandas': 'pandas',
        'OpenPyXL': 'openpyxl',
        'PIL': 'PIL'
    }
    
    optional_packages = {
        'Face Recognition (Optional)': 'face_recognition'
    }
    
    all_good = True
    
    for name, module in packages.items():
        try:
            __import__(module)
            print(f"✅ {name}: OK")
        except ImportError as e:
            print(f"❌ {name}: FAILED - {str(e)}")
            all_good = False
    
    print()
    print("Optional packages:")
    for name, module in optional_packages.items():
        try:
            __import__(module)
            print(f"✅ {name}: OK")
        except ImportError:
            print(f"⚠️  {name}: Not installed (using OpenCV fallback)")
    
    print()
    print("=" * 60)
    
    if all_good:
        print("✅ All required packages installed successfully!")
        print()
        print("📝 Note: System is using OpenCV for face detection")
        print("   (Simplified matching algorithm)")
        print()
        print("Next steps:")
        print("1. Install and start MySQL server")
        print("2. Update database password in database.py")
        print("3. Run: python app.py")
        print("4. Open browser: http://127.0.0.1:5000")
    else:
        print("❌ Some required packages are missing!")
        print()
        print("Please run: pip install -r requirements.txt")
        print()
        print("Note: face_recognition is optional and can be skipped")
    
    print("=" * 60)
    print()
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    if sys.version_info < (3, 8):
        print("⚠️  Warning: Python 3.8+ is recommended")
    else:
        print("✅ Python version is compatible")
    
    return all_good

def check_mysql():
    """Check MySQL connection"""
    print()
    print("=" * 60)
    print("Checking MySQL Connection...")
    print("=" * 60)
    
    try:
        import mysql.connector
        
        # Try to connect (this will fail if MySQL is not installed/running)
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password=''  # Empty password for test
            )
            if connection.is_connected():
                print("✅ MySQL is running and accessible")
                connection.close()
                print()
                print("⚠️  Remember to update your MySQL password in database.py")
                return True
        except mysql.connector.Error as e:
            if "Access denied" in str(e):
                print("✅ MySQL is running (password protected)")
                print("⚠️  Update your MySQL password in database.py")
                return True
            else:
                print(f"❌ MySQL connection failed: {e}")
                print()
                print("Please ensure:")
                print("1. MySQL is installed")
                print("2. MySQL service is running")
                return False
    except ImportError:
        print("❌ MySQL Connector not installed")
        return False
    
    print("=" * 60)

def check_camera():
    """Check if camera is accessible"""
    print()
    print("=" * 60)
    print("Checking Camera Access...")
    print("=" * 60)
    
    try:
        import cv2
        
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            print("✅ Camera is accessible")
            ret, frame = camera.read()
            if ret:
                print("✅ Camera can capture frames")
            else:
                print("⚠️  Camera opened but cannot capture frames")
            camera.release()
            return True
        else:
            print("❌ Cannot access camera")
            print()
            print("Please ensure:")
            print("1. Camera is connected")
            print("2. No other application is using the camera")
            print("3. Camera permissions are granted")
            return False
    except Exception as e:
        print(f"❌ Camera check failed: {e}")
        return False
    
    print("=" * 60)

if __name__ == "__main__":
    print()
    
    # Check package imports
    packages_ok = check_imports()
    
    if packages_ok:
        # Check MySQL
        mysql_ok = check_mysql()
        
        # Check Camera
        camera_ok = check_camera()
        
        print()
        print("=" * 60)
        print("FINAL STATUS")
        print("=" * 60)
        print(f"Packages: {'✅ OK' if packages_ok else '❌ FAILED'}")
        print(f"MySQL: {'✅ OK' if mysql_ok else '❌ FAILED'}")
        print(f"Camera: {'✅ OK' if camera_ok else '❌ FAILED'}")
        print("=" * 60)
        
        if packages_ok and mysql_ok and camera_ok:
            print()
            print("🎉 System is ready to run!")
            print()
            print("Start the application with:")
            print("  python app.py")
            print()
            print("Or double-click: run.bat")
        else:
            print()
            print("⚠️  Please fix the issues above before running the application")
    
    print()
    input("Press Enter to exit...")
