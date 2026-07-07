from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class StudentResult(models.Model):
    exam_number = models.CharField(max_length=50, default='')
    student_name = models.CharField(max_length=200)
    student_class = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    term = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5)
    remarks = models.CharField(max_length=200, blank=True, default='')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['exam_number', 'student_class', 'year', 'term', 'subject']
        ordering = ['subject']

    def __str__(self):
        return f"{self.student_name} ({self.student_class}) - {self.subject}: {self.score}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    staff_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.staff_id})"

class TuitionPayment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
        ('pos', 'POS'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    student_name = models.CharField(max_length=200)
    student_class = models.CharField(max_length=50)
    exam_number = models.CharField(max_length=50, blank=True, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_date = models.DateField()
    reference_number = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    remarks = models.TextField(blank=True, default='')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student_name} - {self.term} {self.year} - {self.amount}"

class ExamQuestion(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
    ]
    
    subject = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)
    term = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    option_a = models.CharField(max_length=200, blank=True, default='')
    option_b = models.CharField(max_length=200, blank=True, default='')
    option_c = models.CharField(max_length=200, blank=True, default='')
    option_d = models.CharField(max_length=200, blank=True, default='')
    correct_answer = models.CharField(max_length=200)
    marks = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['subject', 'id']
    
    def __str__(self):
        return f"{self.subject} - Q{self.id}"

class ExamAttempt(models.Model):
    student_name = models.CharField(max_length=200)
    student_class = models.CharField(max_length=50)
    exam_number = models.CharField(max_length=50, blank=True, default='')
    subject = models.CharField(max_length=100)
    term = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_marks = models.IntegerField(default=0)
    time_started = models.DateTimeField()
    time_completed = models.DateTimeField(null=True, blank=True)
    answers = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student_name} - {self.subject} - {self.score}/{self.total_marks}"

class HolidayTask(models.Model):
    TASK_TYPES = [
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('reading', 'Reading'),
        ('practice', 'Practice'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    student_class = models.CharField(max_length=50)
    subject = models.CharField(max_length=100, blank=True, default='')
    due_date = models.DateField()
    attachment = models.FileField(upload_to='holiday_tasks/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.student_class}"