from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'email', 'phone_number', 'department', 'section', 'category', 'admission_category', 'date_joined')
    list_filter = ('department', 'category', 'admission_category', 'gender', 'religion')
    search_fields = ('roll_number', 'name', 'email', 'phone_number', 'aadhar_card')
    ordering = ('roll_number',)
