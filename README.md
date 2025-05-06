# 📸 Smart Attendance System

A web-based attendance management system leveraging face recognition technology to automate and streamline the process of recording attendance. Built with Django for the backend and deployed via Vercel.

## 🧰 Features

- **User Authentication**: Secure login and registration for users.
- **Face Recognition**: Upload images to mark attendance using facial recognition.
- **Attendance Records**: View and manage attendance logs.

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Dlib
- Cmake
- Git

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ArshGoel/Smart-Attendance.git
   cd Smart-Attendance

   
2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

4. **Apply Migrations**

   ```bash
   python manage.py migrate

5. **Access the Application**

Open your browser and navigate to http://localhost:8000/

🐳 Docker Deployment (Optional)
To run the application using Docker:

**Build the Docker Image**

   ```bash
      docker build -t smart-attendance 

Run the Docker Container

   ```bash
   docker run -d -p 8000:8000 smart-attendance


