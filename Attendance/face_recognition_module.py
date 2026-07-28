ṇimport cv2
import numpy as np
import pickle
import os
from datetime import datetime

# Simplified version without face_recognition library
# Uses OpenCV's Haar Cascade for basic face detection

class FaceRecognitionSystem:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        # Load OpenCV's face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def capture_face(self):
        """Capture face from webcam"""
        video_capture = cv2.VideoCapture(0)
        
        if not video_capture.isOpened():
            return None, "Could not open webcam"
        
        print("Position your face in the frame. Press SPACE to capture or ESC to cancel.")
        
        captured_image = None
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            
            # Display the frame
            cv2.putText(frame, "Press SPACE to capture, ESC to cancel", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Capture Face', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            # Space bar to capture
            if key == 32:
                captured_image = frame.copy()
                break
            # ESC to cancel
            elif key == 27:
                break
        
        video_capture.release()
        cv2.destroyAllWindows()
        
        if captured_image is None:
            return None, "Capture cancelled"
        
        return captured_image, "Success"
    
    def encode_face(self, image):
        """Encode face from image using OpenCV"""
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None, "No face detected"
        
        if len(faces) > 1:
            return None, "Multiple faces detected. Please ensure only one face is in frame."
        
        # Get the face region
        x, y, w, h = faces[0]
        face_roi = image[y:y+h, x:x+w]
        
        # Resize to standard size and flatten as "encoding"
        face_resized = cv2.resize(face_roi, (100, 100))
        face_encoding = face_resized.flatten()
        
        return face_encoding, "Success"
    
    def save_face_image(self, image, student_name, roll_number):
        """Save captured face image"""
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        
        # Create filename with roll number and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{roll_number}_{timestamp}.jpg"
        filepath = os.path.join(data_dir, filename)
        
        # Save image
        cv2.imwrite(filepath, image)
        return filepath
    
    def load_known_faces(self, students_data):
        """Load all registered students' face encodings"""
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        
        for student in students_data:
            try:
                # Decode face encoding from string
                face_encoding_str = student['face_encoding']
                face_encoding = np.frombuffer(
                    pickle.loads(eval(face_encoding_str)), 
                    dtype=np.uint8
                )
                
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(student['name'])
                self.known_face_ids.append(student['id'])
            except Exception as e:
                print(f"Error loading face encoding for {student['name']}: {e}")
        
        print(f"Loaded {len(self.known_face_encodings)} known faces")
    
    def recognize_face_from_camera(self, timeout=30):
        """Recognize face from webcam with timeout - Simplified version"""
        video_capture = cv2.VideoCapture(0)
        
        if not video_capture.isOpened():
            return None, None, "Could not open webcam"
        
        print("Looking for faces... Press ESC to cancel.")
        
        start_time = datetime.now()
        recognized_id = None
        recognized_name = None
        
        while True:
            # Check timeout
            if (datetime.now() - start_time).seconds > timeout:
                video_capture.release()
                cv2.destroyAllWindows()
                return None, None, "Timeout: No face recognized"
            
            ret, frame = video_capture.read()
            if not ret:
                break
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                # Extract face region
                face_roi = frame[y:y+h, x:x+w]
                face_resized = cv2.resize(face_roi, (100, 100))
                current_encoding = face_resized.flatten()
                
                # Compare with known faces (simplified matching)
                best_match_index = -1
                min_distance = float('inf')
                
                for idx, known_encoding in enumerate(self.known_face_encodings):
                    # Calculate simple distance
                    distance = np.linalg.norm(current_encoding.astype(float) - known_encoding.astype(float))
                    if distance < min_distance:
                        min_distance = distance
                        best_match_index = idx
                
                # Threshold for matching (adjust as needed)
                if min_distance < 50000:  # Simplified threshold
                    recognized_id = self.known_face_ids[best_match_index]
                    recognized_name = self.known_face_names[best_match_index]
                    
                    # Draw rectangle and name on frame
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"Recognized: {recognized_name}", 
                              (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                              0.75, (0, 255, 0), 2)
                    
                    cv2.imshow('Face Recognition', frame)
                    cv2.waitKey(2000)  # Show for 2 seconds
                    
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return recognized_id, recognized_name, "Success"
                else:
                    # Draw rectangle for unrecognized face
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", 
                              (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                              0.75, (0, 0, 255), 2)
            
            # Display frame with instructions
            cv2.putText(frame, "Looking for registered faces... Press ESC to cancel", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.imshow('Face Recognition', frame)
            
            if cv2.waitKey(1) & 0xFF == 27:  # ESC to cancel
                break
        
        video_capture.release()
        cv2.destroyAllWindows()
        return None, None, "No match found"
    
    def encode_to_string(self, face_encoding):
        """Convert face encoding to string for database storage"""
        return str(pickle.dumps(face_encoding.tobytes()))
    
    def decode_from_string(self, encoding_string):
        """Convert string back to face encoding"""
        return np.frombuffer(pickle.loads(eval(encoding_string)), dtype=np.uint8)
