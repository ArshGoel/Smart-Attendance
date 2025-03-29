from django.contrib import admin
from .models import Attendance
 
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'created_at', 'updated_at', 'students_count')
    search_fields = ('date',)
    list_filter = ('date',)

    def students_count(self, obj):
        return len(obj.students_present)
    students_count.short_description = 'Number of Students Present'
