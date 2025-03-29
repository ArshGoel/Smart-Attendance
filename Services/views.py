import os
import cv2
import time
import json
import datetime
import numpy as np
import face_recognition
from PIL import Image, ImageDraw
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from Services.models import Attendance
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse

# Paths for processed and original attendance images
PROCESSED_PATH = os.path.join(settings.MEDIA_ROOT, 'Attendance', 'processed')
ORIGINAL_PATH = os.path.join(settings.MEDIA_ROOT, 'Attendance', 'original')

# Ensure the directories exist
os.makedirs(PROCESSED_PATH, exist_ok=True)
os.makedirs(ORIGINAL_PATH, exist_ok=True)

# Training Directory (All User Folders)
DATASETS_PATH = os.path.join(settings.MEDIA_ROOT, 'Datasets')
ENCODING_PATH = os.path.join(settings.MEDIA_ROOT, 'Encodings','Overall', 'overall_model.npz')

def train_face_recognition():
    """Train the model and save encodings to NPZ file."""
    face_encodings = []
    face_labels = []

    if not os.path.exists(DATASETS_PATH):
        os.makedirs(DATASETS_PATH)

    for user_folder in os.listdir(DATASETS_PATH):
        user_folder_path = os.path.join(DATASETS_PATH, user_folder)
        if os.path.isdir(user_folder_path):
            for image_name in os.listdir(user_folder_path):
                image_path = os.path.join(user_folder_path, image_name)
                image = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(image)
                face_encodings_in_image = face_recognition.face_encodings(image, face_locations)

                label = user_folder  # Username as label

                for encoding in face_encodings_in_image:
                    face_encodings.append(encoding)
                    face_labels.append(label)

    np.savez(ENCODING_PATH, encodings=face_encodings, labels=face_labels)
    return {'status': 'success', 'message': 'Training completed successfully.', 'npz_file': ENCODING_PATH}

def load_training_data():
    """Load training data from NPZ file."""
    if not os.path.exists(ENCODING_PATH):
        return [], []

    data = np.load(ENCODING_PATH, allow_pickle=True)
    return list(data['encodings']), list(data['labels'])

def process_images(file_path):
    """Process images, recognize faces, and save processed images."""
    face_encodings, face_labels = load_training_data()
    if not face_encodings or not face_labels:
        return [], None

    test_image = face_recognition.load_image_file(file_path)
    face_locations = face_recognition.face_locations(test_image)
    if not face_locations:
        return [], None

    face_encodings_in_image = face_recognition.face_encodings(test_image, face_locations)
    img_with_boxes = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)

    results = []
    threshold = 0.6  # Distance threshold
    confidence_threshold = 55  # Minimum confidence percentage

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings_in_image):
        distances = face_recognition.face_distance(face_encodings, face_encoding)
        best_match_index = np.argmin(distances)
        best_match_distance = distances[best_match_index]

        if best_match_distance < threshold:
            confidence = (1 - best_match_distance) * 100
            if confidence > confidence_threshold:
                predicted_name = face_labels[best_match_index].split('_')[0]
                results.append(predicted_name)
                color = (0, 255, 0)  # Green for recognized
            else:
                predicted_name = "Unknown"
                color = (0, 0, 255)  # Red for unrecognized
        else:
            predicted_name = "Unknown"
            color = (0, 0, 255)

        cv2.rectangle(img_with_boxes, (left, top), (right, bottom), color, 2)

    # Resize image for display
    desired_width, desired_height = 800, 600
    img_with_boxes_resized = cv2.resize(img_with_boxes, (desired_width, desired_height))

    # Save processed image
    processed_image_path = os.path.join(PROCESSED_PATH, f'processed_{os.path.basename(file_path)}')
    cv2.imwrite(processed_image_path, img_with_boxes_resized)

    return results, processed_image_path

def teacher(request):
    """Handle teacher attendance marking."""
    if not request.user.is_superuser:
        messages.error(request, "Forbidden Access")
        return redirect('not_allowed')

    days = [(datetime.datetime.now() + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    if request.method == 'POST':
        date = request.POST.get('date')
        if date:
            images = request.FILES.getlist('images')
            file_paths = []

            for image in images:
                original_filename = f'original_{datetime.datetime.now().strftime("%d%m%y_%H%M%S")}.jpg'
                original_path = os.path.join(ORIGINAL_PATH, original_filename)

                with open(original_path, 'wb') as f:
                    f.write(image.read())

                file_paths.append(original_path)

            results = []
            recognized_students = set()

            for file_path in file_paths:
                result, img_with_boxes_path = process_images(file_path)
                recognized_students.update(result)
                processed_image_url = os.path.join(settings.MEDIA_URL, 'Attendance', 'processed', os.path.basename(img_with_boxes_path)) # type: ignore

                results.append({'result': result, 'image_path': processed_image_url})

            # Store results in session
            request.session['attendance_results'] = results
            request.session['attendance_date'] = date
            request.session['recognized_students'] = list(recognized_students)

            return redirect('attendance')

    return render(request, 'teacher_dashboard.html', {'days': days})

def attendance(request):
    # Retrieve results and recognized students from session
    results = request.session.get('attendance_results', [])
    date = request.session.get('attendance_date', '')
    recognized_students = request.session.get('recognized_students', [])
    # Clear session data after retrieval
    request.session.pop('attendance_results', None)
    request.session.pop('attendance_date', None)
    request.session.pop('recognized_students', None)
    return render(request, 'attendance.html', {
        'results': results,
        'date': date,
        'recognized_students': recognized_students,
    })

@login_required
def save_attendance(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        detected_faces_json = request.POST.get('detected_faces')
        
        if not detected_faces_json:
            return JsonResponse({'error': 'Detected faces are required'}, status=400)
        
        try:
            detected_faces = json.loads(detected_faces_json)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid detected faces data'}, status=400)
        
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        # Get or create the attendance record for the given date
        attendance_record, created = Attendance.objects.get_or_create(date=date)
        
        # Mark all students as absent initially by creating or updating AttendanceReport
        student_ids_present = []  # List to keep track of present student IDs

        # Mark detected students as present
        for name in detected_faces:
            if name != "Unknown":
                if User.objects.filter(username=name).exists():
                    student_ids_present.append(name)
        
        attendance_record.students_present = student_ids_present
        attendance_record.save()

        # Success message and redirect
        messages.success(request, 'Successfully marked Attendance')
        return redirect('teacher')

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def student(request):
    if request.user.is_superuser:
        # If the user is a superuser (teacher), return a forbidden response or redirect
        return redirect('not_allowed')
    else:
        student = request.user  # Assuming the logged-in user is the student
        today = datetime.date.today()
        period = request.GET.get('period', 'week')  # Default to 'week' if not provided

        if period == 'week':
            week_start = today - datetime.timedelta(days=today.weekday())  # Start of the week (Monday)
            week_end = week_start + datetime.timedelta(days=6)  # End of the week (Sunday)
            start_date, end_date = week_start, week_end
            
            # Prepare attendance data for each day of the week
            attendance_details = []
            for single_date in (week_start + datetime.timedelta(n) for n in range(7)):
                record = Attendance.objects.filter(date=single_date).first()
                if record:
                    status = 'Present' if student.username in record.students_present else 'Absent'
                else:
                    status = 'Nil'
                attendance_details.append({
                    'date': single_date,
                    'status': status
                })
            attendance_details.sort(key=lambda x: x['date'])  # Ensure proper date order

            context = {
                'attendance_details': attendance_details,
                'week_start': week_start,
                'week_end': week_end,
                'current_period': period
            }

        elif period == 'month':
            start_date = today.replace(day=1)  # Start of the month
            end_date = (start_date + datetime.timedelta(days=31)).replace(day=1) - datetime.timedelta(days=1)  # End of the month

            # Prepare a calendar view
            calendar_data = []
            current_day = start_date
            while current_day <= end_date:
                record = Attendance.objects.filter(date=current_day).first()
                if record:
                    status = 'Present' if student.username in record.students_present else 'Absent'
                else:
                    status = 'Nil'
                calendar_data.append({
                    'date': current_day,
                    'status': status
                })
                current_day += datetime.timedelta(days=1)

            # Organize calendar data into weeks
            weeks = []
            current_week = []
            for day in calendar_data:
                if len(current_week) == 7:
                    weeks.append(current_week)
                    current_week = []
                current_week.append(day)
            if current_week:
                weeks.append(current_week)
            
            context = {
                'weeks': weeks,
                'start_date': start_date,
                'end_date': end_date,
                'current_period': period
            }

        else:
            context = {
                'attendance_details': [],
                'message': 'Invalid period selected'
            }

    return render(request, 'student_dashboard.html', context)

def not_allowed(request):
    return render(request,'invalid.html')

cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('static/models/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('static/models/haarcascade_eye.xml')

def generate_frames():
    global cam
    if not cam.isOpened():
        cam = cv2.VideoCapture(0)
    while True:
        success, frame = cam.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@login_required
def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_exempt
@login_required
def stop_camera(request):
    global cam
    if cam.isOpened():
        cam.release()
    return JsonResponse({'status': 'Camera Released'})

@login_required
def capture_image(request):
    if request.method == 'POST':
        face_id = request.user.username
        dataset_path = os.path.join(settings.MEDIA_ROOT, "Datasets", face_id)

        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)

        captured_images = []
        c = 0

        cam = cv2.VideoCapture(0)  # Initialize camera

        while c < 40:
            ret, img = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(face_roi)

                if len(eyes) >= 1:
                    c += 1
                    filename = f"{face_id}_{c}.jpg"
                    image_path = os.path.join(dataset_path, filename)
                    cv2.imwrite(image_path, face_roi)
                    captured_images.append(f"{settings.MEDIA_URL}Datasets/{face_id}/{filename}")

                    time.sleep(0.5)

            if c >= 40:
                break

        cam.release()  # Release camera when done
        return render(request, 'capture_success.html', {'captured_images': captured_images})

    return render(request, 'capture_image.html')

def train_images(request, username):
    # Define folder paths
    folder_path = os.path.join(settings.MEDIA_ROOT, 'Datasets', username)
    output_folder = os.path.join(settings.MEDIA_ROOT, 'Encodings', 'Students', username)

    if not os.path.exists(folder_path):
        return render(request, 'error.html', {'message': 'No images found for this user.'})

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create NPZ file path
    output_file = os.path.join(output_folder, f"{username}.npz")

    # Function to create NPZ file
    def create_npz_file(image_folder, output_file):
        face_encodings = []
        face_labels = []

        for image_name in os.listdir(image_folder):
            image_path = os.path.join(image_folder, image_name)
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings_in_image = face_recognition.face_encodings(image, face_locations)

            label = image_name.split('_')[0]  # Extract only username (e.g., "228R1A0571")

            for encoding in face_encodings_in_image:
                face_encodings.append(encoding)
                face_labels.append(label)

        # Save to NPZ file
        np.savez(output_file, encodings=face_encodings, labels=face_labels)
        print(f"NPZ file saved to {output_file}")

    create_npz_file(folder_path, output_file)

    return render(request, 'train_success.html', {'username': username, 'output_file': output_file})

def train_all_images(request):
    if request.method == "POST":  # Ensure it's a POST request
        # You can add print statements for debugging
        print("Training started...")
        
        base_folder = os.path.join(settings.MEDIA_ROOT, 'Datasets')
        face_encodings = []
        face_labels = []

        for user_folder in os.listdir(base_folder):
            user_folder_path = os.path.join(base_folder, user_folder)
            if os.path.isdir(user_folder_path):
                for image_name in os.listdir(user_folder_path):
                    image_path = os.path.join(user_folder_path, image_name)
                    image = face_recognition.load_image_file(image_path)
                    face_locations = face_recognition.face_locations(image)
                    face_encodings_in_image = face_recognition.face_encodings(image, face_locations)

                    label = os.path.splitext(image_name)[0]
                    for encoding in face_encodings_in_image:
                        face_encodings.append(encoding)
                        face_labels.append(label)

        output_file = os.path.join(settings.MEDIA_ROOT, 'Encodings','Overall', 'overall_model.npz')
        np.savez(output_file, encodings=face_encodings, labels=face_labels)


        print("Training completed successfully.")
        return JsonResponse({'status': 'success', 'message': 'All images trained successfully.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def view_student(request):
    users = User.objects.filter(is_superuser=False)  # Get only regular users
    user_data = []

    for user in users:
        folder_path = os.path.join(settings.MEDIA_ROOT, 'Datasets', user.username)
        folder_exists = os.path.exists(folder_path)
                
        user_data.append({
            'username': user.username,
            'folder_exists': folder_exists,
            'folder_path': folder_path if folder_exists else None,  # Only store path if folder exists
        })

    return render(request, 'view_user_data.html', {'user_data': user_data})

def view_images(request, username):
    folder_path = os.path.join(settings.MEDIA_ROOT, 'Datasets', username)

    if not os.path.exists(folder_path):
        return render(request, 'error.html', {'message': 'No images found for this user.'})

    # Generate image URLs using MEDIA_URL instead of MEDIA_ROOT
    images = os.listdir(folder_path)
    image_urls = [os.path.join(settings.MEDIA_URL, 'Datasets', username, img) for img in images]

    return render(request, 'view_images.html', {'username': username, 'image_urls': image_urls})
