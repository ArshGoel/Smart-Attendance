from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    students_present = models.JSONField(default=list)  # Use JSONField to store list of student IDs

    def __str__(self):
        return f"Attendance for {self.date}"