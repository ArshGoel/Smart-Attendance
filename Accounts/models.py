from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    CATEGORIES = [
        ('BC-A', 'BC-A'),
        ('BC-B', 'BC-B'),
        ('BC-C', 'BC-C'),
        ('BC-D', 'BC-D'),
        ('BC-E', 'BC-E'),
        ('OBC', 'OBC'),
        ('SC', 'SC'),
        ('OC', 'OC'),
    ]

    RELIGION_CATEGORY = [
        ('CHRISTAN', 'CHRISTAN'),
        ('HINDU', 'HINDU'),
        ('CHRISTIAN', 'CHRISTIAN'),
        ('MUSLIM', 'MUSLIM'),
    ]

    ADMISSION_CATEGORY = [
        ('CONVENER', 'CONVENER'),
        ('SPOT', 'SPOT'),
        ('MANAGEMENT', 'MANAGEMENT'),
    ]

    DEPARTMENT_CATEGORIES = [
        ('CSE','CSE'),
        ('CSM','CSM'),
        ('ECE','ECE'),
        ('IT','IT'),
        ('CSD','CSD'),
    ]

    roll_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    fathername = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    religion = models.CharField(max_length=10, choices=RELIGION_CATEGORY, blank=True, null=True)
    admission_category = models.CharField(max_length=10, choices=ADMISSION_CATEGORY, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORIES, blank=True, null=True) 
    mole = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=3, choices=DEPARTMENT_CATEGORIES, blank=True, null=True)
    section = models.CharField(max_length=1, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username