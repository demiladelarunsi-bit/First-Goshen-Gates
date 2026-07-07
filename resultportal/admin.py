from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentResult, TeacherProfile

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ['exam_number', 'student_name', 'year', 'term', 'subject', 'score', 'grade', 'uploaded_by']
    list_filter = ['year', 'term', 'grade']
    search_fields = ['exam_number', 'student_name', 'subject']

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'staff_id', 'department', 'user']
    search_fields = ['full_name', 'staff_id']