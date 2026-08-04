from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


# ==========================================
# EXISTING (Extended with new fields - all have defaults so nothing breaks)
# ==========================================
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

    # NEW FIELDS — safe defaults so existing rows still work
    ca1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ca2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    position = models.IntegerField(default=0)
    teacher_remark = models.CharField(max_length=300, blank=True, default='')
    principal_remark = models.CharField(max_length=300, blank=True, default='')

    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['exam_number', 'student_class', 'year', 'term', 'subject']
        ordering = ['subject']

    def __str__(self):
        return f"{self.student_name} ({self.student_class}) - {self.subject}: {self.score}"

    def save(self, *args, **kwargs):
        # Auto-calculate total when CA fields used
        if (self.ca1 or self.ca2 or self.exam_score) and not self.total:
            self.total = (self.ca1 or 0) + (self.ca2 or 0) + (self.exam_score or 0)
            if not self.score:
                self.score = self.total
        # Auto-grade
        if not self.grade:
            self.grade = self._grade()
        super().save(*args, **kwargs)

    def _grade(self):
        s = float(self.score or 0)
        if s >= 90: return 'A+'
        if s >= 80: return 'A'
        if s >= 70: return 'B'
        if s >= 60: return 'C'
        if s >= 50: return 'D'
        return 'F'


# ==========================================
# NEW: Student account (login + profile)
# ==========================================
class Student(models.Model):
    admission_number = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=200)
    current_class = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, default='')
    parent_name = models.CharField(max_length=200, blank=True, default='')
    parent_phone = models.CharField(max_length=20, blank=True, default='')
    parent_email = models.EmailField(blank=True, default='')
    address = models.TextField(blank=True, default='')
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw):
        self.password = make_password(raw)

    def check_password(self, raw):
        return check_password(raw, self.password)

    def __str__(self):
        return f"{self.full_name} ({self.admission_number}) - {self.current_class}"


# ==========================================
# NEW: School Settings (singleton)
# ==========================================
class SchoolSettings(models.Model):
    school_name = models.CharField(max_length=200, default='First Goshen Gate School')
    school_motto = models.CharField(max_length=200, blank=True, default="Nurturing Tomorrow's Leaders Today")
    school_logo = models.ImageField(upload_to='school/', blank=True, null=True)
    school_address = models.TextField(blank=True, default='')
    school_phone = models.CharField(max_length=50, blank=True, default='')
    school_email = models.EmailField(blank=True, default='')
    current_session = models.CharField(max_length=20, default='2024/2025')
    current_term = models.CharField(max_length=20, default='First Term')

    class Meta:
        verbose_name = 'School Settings'
        verbose_name_plural = 'School Settings'

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.school_name


# ==========================================
# NEW: Promotion History
# ==========================================
class PromotionHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='promotions')
    from_class = models.CharField(max_length=50)
    to_class = models.CharField(max_length=50)
    session = models.CharField(max_length=20, blank=True, default='')
    promoted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    promoted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name}: {self.from_class} → {self.to_class}"


# ==========================================
# EXISTING (unchanged)
# ==========================================
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
