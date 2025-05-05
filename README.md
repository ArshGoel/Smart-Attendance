# 📸 Smart Attendance System

A web-based attendance management system leveraging face recognition technology to automate and streamline the process of recording attendance. Built with Django for the backend and deployed via Vercel.

## 🌐 Live Demo

Access the live application here: [smart-attendance-rosy.vercel.app](https://smart-attendance-rosy.vercel.app)

## 🧰 Features

- **User Authentication**: Secure login and registration for users.
- **Face Recognition**: Upload images to mark attendance using facial recognition.
- **Attendance Records**: View and manage attendance logs.
- **Responsive Design**: Accessible across various devices.

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ArshGoel/Smart-Attendance.git
   cd Smart-Attendance
Create a Virtual Environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Apply Migrations

bash
Copy
Edit
python manage.py migrate
Run the Development Server

bash
Copy
Edit
python manage.py runserver
Access the Application

Open your browser and navigate to http://localhost:8000/

🐳 Docker Deployment (Optional)
To run the application using Docker:

Build the Docker Image

bash
Copy
Edit
docker build -t smart-attendance .
Run the Docker Container

bash
Copy
Edit
docker run -d -p 8000:8000 smart-attendance
📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙌 Acknowledgements
Django

Vercel

OpenCV

face_recognition

yaml
Copy
Edit

---

Feel free to customize this `README.md` further to suit your project's specific needs or to add more detailed instructions and features.
::contentReference[oaicite:0]{index=0}
