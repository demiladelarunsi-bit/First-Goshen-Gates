from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import StudentResult, TeacherProfile, ExamQuestion, ExamAttempt, TuitionPayment, HolidayTask
from .question_bank import get_questions_for_class, get_available_classes, get_class_question_count
import csv, io, json, math
from django.db.models import Q
from django.utils import timezone
# ============================================================
# NEW VIEWS — Add these to the bottom of your existing views.py
# ============================================================
import csv, io, json, math
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from .models import (
    Student, SchoolSettings, PromotionHistory,
    StudentResult, ExamAttempt, TuitionPayment
)



# ---------- STUDENT AUTH ----------
# Make sure these exist in views.py!
def student_login_page(request):
    if request.session.get('student_id'):
        return redirect('student_dashboard')
    return render(request, 'student_login.html')

def tasks_page(request):
    return render(request, 'tasks_page.html')

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        sid = request.session.get('student_id')
        if not sid:
            return redirect('student_login_page')
        try:
            request.student = Student.objects.get(id=sid)
        except Student.DoesNotExist:
            return redirect('student_login_page')
        return view_func(request, *args, **kwargs)
    return wrapper





@csrf_exempt
@require_POST
def ajax_student_login(request):
    admission = request.POST.get('admission_number', '').strip()
    password = request.POST.get('password', '')
    try:
        student = Student.objects.get(admission_number=admission)
        if not student.is_active:
            return JsonResponse({'status': 'error', 'message': 'Account deactivated. Contact admin.'})
        if student.check_password(password):
            request.session['student_id'] = student.id
            return JsonResponse({'status': 'success', 'name': student.full_name})
        return JsonResponse({'status': 'error', 'message': 'Invalid password'})
    except Student.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Admission number not found'})


def ajax_student_logout(request):
    if 'student_id' in request.session:
        del request.session['student_id']
    return JsonResponse({'status': 'success'})


@student_required
def student_dashboard(request):
    settings = SchoolSettings.get_settings()
    student = request.student

    from django.db.models import Q

    # Get the first word of the student's name (e.g., "David" from "David Johnson")
    first_name = student.full_name.split()[0] if student.full_name else ''

    # Search by exam number OR by the first name and class to ensure we catch all their exams
    exam_filter = Q(exam_number=student.admission_number)
    if first_name:
        exam_filter |= Q(student_name__icontains=first_name, student_class__icontains=student.current_class)

    results_count = StudentResult.objects.filter(
        Q(exam_number=student.admission_number) | Q(student_name__icontains=first_name, student_class__icontains=student.current_class)
    ).count()

    exam_count = ExamAttempt.objects.filter(exam_filter).count()

    latest_results = StudentResult.objects.filter(
        Q(exam_number=student.admission_number) | Q(student_name__icontains=first_name, student_class__icontains=student.current_class)
    ).order_by('-created_at')[:5]

    latest_exams = ExamAttempt.objects.filter(exam_filter).order_by('-created_at')[:5]

    return render(request, 'student_dashboard.html', {
        'student': student,
        'settings': settings,
        'results_count': results_count,
        'exam_count': exam_count,
        'latest_results': latest_results,
        'latest_exams': latest_exams,
    })



@student_required
def student_profile_view(request):
    return render(request, 'student_profile.html', {'student': request.student, 'settings': SchoolSettings.get_settings()})


@student_required
@require_POST
@csrf_exempt
def student_change_password(request):
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    if not request.student.check_password(old_password):
        return JsonResponse({'status': 'error', 'message': 'Current password is incorrect'})
    if len(new_password) < 6:
        return JsonResponse({'status': 'error', 'message': 'Password must be at least 6 characters'})
    request.student.set_password(new_password)
    request.student.save()
    return JsonResponse({'status': 'success', 'message': 'Password changed successfully'})

@student_required
def student_view_results(request):
    settings = SchoolSettings.get_settings()
    student = request.student

    available_terms = ['First Term', 'Second Term', 'Third Term']

    # Default to empty strings so the form is completely blank
    search_name = request.GET.get('name', '')
    search_exam = request.GET.get('exam', '')
    search_class = request.GET.get('class', '')
    year = request.GET.get('year', '')
    term = request.GET.get('term', '')

    results_data = None
    error_message = None

    if year and term:
        # Search based on the exact inputs provided in the form
        results = StudentResult.objects.filter(
            student_name__icontains=search_name,
            exam_number=search_exam,
            student_class=search_class,
            year=year,
            term=term
        ).order_by('subject')

        if results.exists():
            subjects = list(results)
            total = sum(float(r.score) for r in subjects)
            avg = round(total / len(subjects), 2) if subjects else 0

            overall_grade = 'F'
            if avg >= 90: overall_grade = 'A+'
            elif avg >= 80: overall_grade = 'A'
            elif avg >= 70: overall_grade = 'B'
            elif avg >= 60: overall_grade = 'C'
            elif avg >= 50: overall_grade = 'D'

            results_data = {
                'subjects': subjects,
                'total': total,
                'average': avg,
                'overall_grade': overall_grade,
            }
        else:
            error_message = f'No results found for {term} {year}.'

    return render(request, 'student_view_results.html', {
        'student': student,
        'settings': settings,
        'available_terms': available_terms,
        'search_name': search_name,
        'search_exam': search_exam,
        'search_class': search_class,
        'selected_year': year,
        'selected_term': term,
        'results_data': results_data,
        'error': error_message,
    })

@student_required
def student_view_exam_scores(request):
    from django.db.models import Q
    student = request.student

    first_name = student.full_name.split()[0] if student.full_name else ''
    exam_filter = Q(exam_number=student.admission_number)
    if first_name:
        exam_filter |= Q(student_name__icontains=first_name, student_class__icontains=student.current_class)

    attempts = ExamAttempt.objects.filter(exam_filter).order_by('-created_at')
    return render(request, 'student_exam_scores.html', {
        'student': student,
        'attempts': attempts,
        'settings': SchoolSettings.get_settings(),
    })

@student_required
def student_print_result(request):
    year = request.GET.get('year', '')
    term = request.GET.get('term', '')
    results = StudentResult.objects.filter(
        exam_number=request.student.admission_number,
        student_class=request.student.current_class
    )
    if year:
        results = results.filter(year=year)
    if term:
        results = results.filter(term=term)
    results = results.order_by('subject')
    total = sum(float(r.score) for r in results)
    avg = total / len(results) if results else 0
    overall_grade = 'F'
    if avg >= 90: overall_grade = 'A+'
    elif avg >= 80: overall_grade = 'A'
    elif avg >= 70: overall_grade = 'B'
    elif avg >= 60: overall_grade = 'C'
    elif avg >= 50: overall_grade = 'D'
    return render(request, 'print_result.html', {
        'student': request.student,
        'results': results,
        'total': total,
        'average': round(avg, 2),
        'overall_grade': overall_grade,
        'year': year,
        'term': term,
        'settings': SchoolSettings.get_settings(),
    })


@csrf_exempt
@require_POST
def forgot_password(request):
    admission = request.POST.get('admission_number', '').strip()
    parent_phone = request.POST.get('parent_phone', '').strip()
    try:
        student = Student.objects.get(admission_number=admission, parent_phone=parent_phone)
        new_pwd = 'student123'
        student.set_password(new_pwd)
        student.save()
        return JsonResponse({
            'status': 'success',
            'message': f'Password reset successfully. New password: {new_pwd}. Please change it after login.'
        })
    except Student.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No matching student found. Contact admin.'})


# ---------- STUDENT MANAGEMENT (Admin) ----------
@login_required
def manage_students(request):
    return render(request, 'manage_students.html', {'settings': SchoolSettings.get_settings()})


@login_required
def get_students(request):
    search = request.GET.get('search', '').strip()
    student_class = request.GET.get('class', '').strip()
    page = int(request.GET.get('page', 1))
    per_page = 25
    qs = Student.objects.all()
    if search:
        qs = qs.filter(
            Q(full_name__icontains=search) |
            Q(admission_number__icontains=search) |
            Q(parent_name__icontains=search)
        )
    if student_class:
        qs = qs.filter(current_class=student_class)
    total = qs.count()
    start = (page - 1) * per_page
    students = qs.order_by('current_class', 'full_name')[start:start + per_page]
    data = [{
        'id': s.id,
        'admission_number': s.admission_number,
        'full_name': s.full_name,
        'current_class': s.current_class,
        'gender': s.gender,
        'parent_name': s.parent_name,
        'parent_phone': s.parent_phone,
        'is_active': s.is_active,
        'created_at': s.created_at.strftime('%Y-%m-%d'),
    } for s in students]
    all_classes = list(Student.objects.values_list('current_class', flat=True).distinct().order_by('current_class'))
    return JsonResponse({
        'status': 'success',
        'students': data,
        'total': total,
        'pages': math.ceil(total / per_page) if total > 0 else 1,
        'page': page,
        'classes': all_classes,
    })

@login_required
@require_POST
@csrf_exempt
def add_student(request):
    try:
        data = request.POST
        admission = data.get('admission_number', '').strip()
        full_name = data.get('full_name', '').strip()
        current_class = data.get('current_class', '').strip()
        password = data.get('password', 'student123')

        if not all([admission, full_name, current_class]):
            return JsonResponse({'status': 'error', 'message': 'Admission number, name, and class are required'})

        if Student.objects.filter(admission_number=admission).exists():
            return JsonResponse({'status': 'error', 'message': 'Admission number already exists'})

        student = Student(
            admission_number=admission,
            full_name=full_name,
            current_class=current_class,
            gender=data.get('gender', '').strip(),
            parent_name=data.get('parent_name', '').strip(),
            parent_phone=data.get('parent_phone', '').strip(),
        )
        student.set_password(password)
        student.save()

        return JsonResponse({'status': 'success', 'message': f'Student "{full_name}" added successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
@require_POST
@csrf_exempt
def edit_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Student not found'})
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    except Exception:
        data = request.POST
    student.full_name = data.get('full_name', student.full_name).strip()
    student.current_class = data.get('current_class', student.current_class).strip()
    student.gender = data.get('gender', student.gender).strip()
    student.parent_name = data.get('parent_name', student.parent_name).strip()
    student.parent_phone = data.get('parent_phone', student.parent_phone).strip()
    student.parent_email = data.get('parent_email', student.parent_email).strip()
    student.address = data.get('address', student.address).strip()
    student.is_active = data.get('is_active', 'true').lower() in ('true', '1', 'on')
    new_password = data.get('password', '').strip()
    if new_password:
        if len(new_password) < 6:
            return JsonResponse({'status': 'error', 'message': 'Password must be at least 6 characters'})
        student.set_password(new_password)
    student.save()
    return JsonResponse({'status': 'success', 'message': 'Student updated successfully'})


@login_required
@require_POST
@csrf_exempt
def delete_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        name = student.full_name
        student.delete()
        return JsonResponse({'status': 'success', 'message': f'Student "{name}" deleted'})
    except Student.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Student not found'})


@login_required
@require_POST
@csrf_exempt
def promote_students(request):
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    except Exception:
        data = request.POST
    from_class = data.get('from_class', '').strip()
    to_class = data.get('to_class', '').strip()
    session = data.get('session', '').strip()
    if not all([from_class, to_class]):
        return JsonResponse({'status': 'error', 'message': 'Both classes are required'})
    students = Student.objects.filter(current_class=from_class)
    count = 0
    for s in students:
        PromotionHistory.objects.create(
            student=s, from_class=from_class, to_class=to_class,
            session=session, promoted_by=request.user
        )
        s.current_class = to_class
        s.save()
        count += 1
    return JsonResponse({
        'status': 'success',
        'message': f'{count} student(s) promoted from {from_class} to {to_class}'
    })


@login_required
@require_POST
@csrf_exempt
def bulk_upload_students(request):
    csv_file = request.FILES.get('csv_file')
    if not csv_file:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded'})
    if not csv_file.name.endswith('.csv'):
        return JsonResponse({'status': 'error', 'message': 'Please upload a CSV file'})
    try:
        decoded = csv_file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded))
        required = ['admission_number', 'full_name', 'current_class']
        if not all(f in reader.fieldnames for f in required):
            return JsonResponse({'status': 'error', 'message': f'CSV must contain: {", ".join(required)}'})
        count = 0
        default_password = 'student123'
        for row in reader:
            admission = row['admission_number'].strip()
            if Student.objects.filter(admission_number=admission).exists():
                continue
            s = Student(
                admission_number=admission,
                full_name=row['full_name'].strip(),
                current_class=row['current_class'].strip(),
                gender=row.get('gender', '').strip(),
                parent_name=row.get('parent_name', '').strip(),
                parent_phone=row.get('parent_phone', '').strip(),
                parent_email=row.get('parent_email', '').strip(),
                address=row.get('address', '').strip(),
            )
            pwd = row.get('password', '').strip() or default_password
            s.set_password(pwd)
            s.save()
            count += 1
        return JsonResponse({'status': 'success', 'message': f'{count} student(s) imported', 'count': count})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# ---------- SCHOOL SETTINGS ----------
@login_required
def school_settings_page(request):
    return render(request, 'school_settings.html', {'settings': SchoolSettings.get_settings()})


@login_required
@require_POST
@csrf_exempt
def update_school_settings(request):
    settings = SchoolSettings.get_settings()
    settings.school_name = request.POST.get('school_name', settings.school_name)
    settings.school_motto = request.POST.get('school_motto', settings.school_motto)
    settings.school_address = request.POST.get('school_address', settings.school_address)
    settings.school_phone = request.POST.get('school_phone', settings.school_phone)
    settings.school_email = request.POST.get('school_email', settings.school_email)
    settings.current_session = request.POST.get('current_session', settings.current_session)
    settings.current_term = request.POST.get('current_term', settings.current_term)
    if 'school_logo' in request.FILES:
        settings.school_logo = request.FILES['school_logo']
    settings.save()
    return JsonResponse({'status': 'success', 'message': 'School settings updated successfully'})


# ---------- CBT SCORES (Admin) ----------
@login_required
def view_exam_scores(request):
    return render(request, 'exam_scores.html', {'settings': SchoolSettings.get_settings()})


from django.core.paginator import Paginator
from django.db.models import Q
from .models import ExamAttempt

@login_required
def get_exam_scores(request):
    page = int(request.GET.get('page', 1))
    per_page = 25
    search = request.GET.get('search', '').strip()

    qs = ExamAttempt.objects.all()
    if search:
        qs = qs.filter(Q(student_name__icontains=search) | Q(exam_number__icontains=search))

    total = qs.count()
    paginator = Paginator(qs.order_by('-created_at'), per_page)
    attempts = paginator.get_page(page)

    data = [{
        'id': a.id,
        'student_name': a.student_name,
        'exam_number': a.exam_number,
        'student_class': a.student_class,
        'subject': a.subject,
        'term': a.term,
        'year': a.year,
        'score': str(a.score),
        'total_marks': a.total_marks,
        'percentage': round(float(a.score) / a.total_marks * 100, 2) if a.total_marks > 0 else 0,
        'date': a.created_at.strftime('%Y-%m-%d %H:%M'),
    } for a in attempts]

    return JsonResponse({
        'status': 'success',
        'scores': data,
        'total': total,
        'pages': paginator.num_pages,
        'page': page,
    })


# ---------- PAYMENTS (Admin) ----------
@login_required
def view_payments(request):
    return render(request, 'view_payments.html', {'settings': SchoolSettings.get_settings()})


@login_required
def get_payments(request):
    page = int(request.GET.get('page', 1))
    per_page = 25
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    qs = TuitionPayment.objects.all()
    if search:
        qs = qs.filter(Q(student_name__icontains=search) | Q(exam_number__icontains=search))
    if status:
        qs = qs.filter(status=status)
    total = qs.count()
    start = (page - 1) * per_page
    payments = qs.order_by('-created_at')[start:start + per_page]
    data = [{
        'id': p.id,
        'student_name': p.student_name,
        'exam_number': p.exam_number,
        'student_class': p.student_class,
        'amount': str(p.amount),
        'term': p.term,
        'year': p.year,
        'payment_method': p.get_payment_method_display(),
        'payment_date': p.payment_date.strftime('%Y-%m-%d') if p.payment_date else '',
        'reference_number': p.reference_number,
        'status': p.get_status_display(),
        'status_code': p.status,
        'remarks': p.remarks,
    } for p in payments]
    return JsonResponse({
        'status': 'success',
        'payments': data,
        'total': total,
        'pages': math.ceil(total / per_page) if total > 0 else 1,
        'page': page,
    })


@login_required
@require_POST
@csrf_exempt
def verify_payment(request, payment_id):
    try:
        p = TuitionPayment.objects.get(id=payment_id)
        new_status = request.POST.get('status', '')
        if new_status in ['pending', 'verified', 'rejected']:
            p.status = new_status
            p.verified_by = request.user
            p.save()
            return JsonResponse({'status': 'success', 'message': f'Payment marked as {new_status}'})
        return JsonResponse({'status': 'error', 'message': 'Invalid status'})
    except TuitionPayment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Payment not found'})


# ---------- UPDATED: Enhanced get_dashboard_stats ----------
# Replace your existing get_dashboard_stats with this:
@login_required
def get_dashboard_stats(request):
    total_results = StudentResult.objects.count()
    total_students = Student.objects.count()
    total_students_with_results = StudentResult.objects.values('exam_number').distinct().count()
    total_classes = Student.objects.values('current_class').distinct().count()
    total_exam_attempts = ExamAttempt.objects.count()
    total_payments = TuitionPayment.objects.count()
    pending_payments = TuitionPayment.objects.filter(status='pending').count()
    verified_payments = TuitionPayment.objects.filter(status='verified').count()
    total_teachers = TeacherProfile.objects.count()
    try:
        profile = request.user.teacherprofile
        my_uploads = StudentResult.objects.filter(uploaded_by=request.user).count()
        my_students = StudentResult.objects.filter(uploaded_by=request.user).values('exam_number').distinct().count()
    except TeacherProfile.DoesNotExist:
        profile = None
        my_uploads = 0
        my_students = 0
    return JsonResponse({
        'status': 'success',
        'total_results': total_results,
        'total_students': total_students,
        'total_students_with_results': total_students_with_results,
        'total_classes': total_classes,
        'total_exam_attempts': total_exam_attempts,
        'total_payments': total_payments,
        'pending_payments': pending_payments,
        'verified_payments': verified_payments,
        'total_teachers': total_teachers,
        'my_uploads': my_uploads,
        'my_students': my_students,
        'member_since': profile.created_at.strftime('%b %d, %Y') if profile else 'N/A',
        'department': profile.department if profile else 'N/A',
    })

def calculate_grade(score):
    if score >= 90: return 'A+'
    elif score >= 80: return 'A'
    elif score >= 70: return 'B'
    elif score >= 60: return 'C'
    elif score >= 50: return 'D'
    else: return 'F'


def get_remarks(grade):
    return {'A+': 'Excellent', 'A': 'Very Good', 'B': 'Good', 'C': 'Credit', 'D': 'Pass', 'F': 'Fail'}.get(grade, '')


def student_page(request):
    return render(request, 'student.html')


def about_page(request):
    return render(request, 'about.html')


@csrf_exempt
@require_POST
def check_result(request):
    exam_number = request.POST.get('exam_number', '').strip()
    student_name = request.POST.get('student_name', '').strip()
    student_class = request.POST.get('student_class', '').strip()
    year = request.POST.get('year', '').strip()
    term = request.POST.get('term', '').strip()
    if not all([student_class, year, term]):
        return JsonResponse({'status': 'error', 'message': 'Class, year, and term are required'})
    if not exam_number and not student_name:
        return JsonResponse({'status': 'error', 'message': 'Please enter examination number or full name'})
    results = StudentResult.objects.filter(student_class=student_class, year=year, term=term)
    if exam_number:
        results = results.filter(exam_number=exam_number)
    if student_name:
        results = results.filter(student_name__icontains=student_name)
    if not results.exists():
        return JsonResponse({'status': 'not_found', 'message': 'No results found'})
    data = [{'subject': r.subject, 'score': str(r.score), 'grade': r.grade, 'remarks': r.remarks} for r in results]
    return JsonResponse({
        'status': 'success',
        'student_name': results.first().student_name,
        'exam_number': results.first().exam_number,
        'student_class': student_class,
        'year': year, 'term': term, 'results': data,
    })


def get_stats(request):
    return JsonResponse({
        'total_students': StudentResult.objects.values('exam_number').distinct().count(),
        'total_results': StudentResult.objects.count(),
        'years': list(StudentResult.objects.values_list('year', flat=True).distinct().order_by('-year'))[:10],
    })


def admin_signup_page(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    return render(request, 'admin_signup.html')


def admin_login_page(request):
    if request.user.is_authenticated:
        return redirect('/admin/dashboard/')
    return render(request, 'admin_login.html')


@login_required
def admin_dashboard(request):
    if not request.session.get('allow_dashboard'):
        logout(request)
        return redirect('/admin/login/')
    del request.session['allow_dashboard']
    try:
        profile = request.user.teacherprofile
    except TeacherProfile.DoesNotExist:
        profile = None
    return render(request, 'admin_dashboard.html', {
        'username': request.user.username, 'profile': profile,
    })


@login_required
def teacher_profile(request):
    try:
        profile = request.user.teacherprofile
    except TeacherProfile.DoesNotExist:
        profile = None
    return render(request, 'teacher_profile.html', {
        'username': request.user.username, 'profile': profile,
    })


@csrf_exempt
@require_POST
def ajax_signup(request):
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password1 = request.POST.get('password1', '')
    password2 = request.POST.get('password2', '')
    full_name = request.POST.get('full_name', '').strip()
    staff_id = request.POST.get('staff_id', '').strip()
    department = request.POST.get('department', '').strip()
    phone = request.POST.get('phone', '').strip()
    if not all([username, email, password1, password2, full_name, staff_id]):
        return JsonResponse({'status': 'error', 'message': 'All required fields must be filled'})
    if password1 != password2:
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})
    if len(password1) < 6:
        return JsonResponse({'status': 'error', 'message': 'Password must be at least 6 characters'})
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'error', 'message': 'Username already taken'})
    if User.objects.filter(email=email).exists():
        return JsonResponse({'status': 'error', 'message': 'Email already registered'})
    if TeacherProfile.objects.filter(staff_id=staff_id).exists():
        return JsonResponse({'status': 'error', 'message': 'Staff ID already registered'})
    user = User.objects.create_user(username=username, email=email, password=password1)
    TeacherProfile.objects.create(user=user, full_name=full_name, staff_id=staff_id, department=department, phone=phone)
    login(request, user)
    request.session['allow_dashboard'] = True
    return JsonResponse({'status': 'success', 'message': 'Account created successfully', 'username': username})


@csrf_exempt
@require_POST
def ajax_login(request):
    user = authenticate(request, username=request.POST.get('username', '').strip(), password=request.POST.get('password', ''))
    if user:
        login(request, user)
        request.session['allow_dashboard'] = True
        return JsonResponse({'status': 'success', 'username': user.username})
    return JsonResponse({'status': 'error', 'message': 'Invalid username or password'})


@csrf_exempt
def ajax_logout(request):
    logout(request)
    return JsonResponse({'status': 'success'})


@login_required
@require_POST
def add_result(request):
    exam_number = request.POST.get('exam_number', '').strip()
    student_name = request.POST.get('student_name', '').strip()
    student_class = request.POST.get('student_class', '').strip()
    year = request.POST.get('year', '').strip()
    term = request.POST.get('term', '').strip()
    if not all([student_name, student_class, year, term]):
        return JsonResponse({'status': 'error', 'message': 'Please fill in student name, class, year, and term'})
    try:
        subjects = json.loads(request.POST.get('subjects', '[]'))
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid subjects data'})
    count = 0
    for subj in subjects:
        subject_name = subj.get('subject', '').strip()
        score_raw = subj.get('score', '').strip()
        if not subject_name or score_raw == '':
            continue
        try:
            score = float(score_raw)
        except ValueError:
            continue
        if not (0 <= score <= 100):
            continue
        grade = calculate_grade(score)
        remarks = get_remarks(grade)
        StudentResult.objects.update_or_create(
            exam_number=exam_number or student_name,
            student_class=student_class,
            year=year, term=term, subject=subject_name,
            defaults={'student_name': student_name, 'score': score, 'grade': grade, 'remarks': remarks, 'uploaded_by': request.user}
        )
        count += 1
    if count == 0:
        return JsonResponse({'status': 'error', 'message': 'No valid subject scores provided'})
    return JsonResponse({'status': 'success', 'message': f'{count} subject result(s) saved for {student_name} ({student_class})'})


@login_required
@csrf_exempt
@require_POST
def bulk_upload(request):
    csv_file = request.FILES.get('csv_file')
    if not csv_file:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded'})
    if not csv_file.name.endswith('.csv'):
        return JsonResponse({'status': 'error', 'message': 'Please upload a CSV file'})
    try:
        decoded = csv_file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded))
        required = ['student_name', 'student_class', 'year', 'term', 'subject', 'score']
        if not all(f in reader.fieldnames for f in required):
            return JsonResponse({'status': 'error', 'message': f'CSV must contain: {", ".join(required)}'})
        count = 0
        for row in reader:
            try:
                score = float(row['score'].strip())
                if not (0 <= score <= 100):
                    continue
                grade = row.get('grade', '').strip() or calculate_grade(score)
                remarks = row.get('remarks', '').strip() or get_remarks(grade)
                exam_number = row.get('exam_number', '').strip() or row['student_name'].strip()
                StudentResult.objects.update_or_create(
                    exam_number=exam_number,
                    student_class=row['student_class'].strip(),
                    year=row['year'].strip(),
                    term=row['term'].strip(),
                    subject=row['subject'].strip(),
                    defaults={'student_name': row['student_name'].strip(), 'score': score, 'grade': grade, 'remarks': remarks, 'uploaded_by': request.user}
                )
                count += 1
            except Exception:
                continue
        return JsonResponse({'status': 'success', 'message': f'{count} result(s) uploaded', 'count': count})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def get_teacher_profile(request):
    try:
        p = request.user.teacherprofile
        uploaded = StudentResult.objects.filter(uploaded_by=request.user).count()
        students = StudentResult.objects.filter(uploaded_by=request.user).values('exam_number').distinct().count()
        return JsonResponse({
            'status': 'success', 'full_name': p.full_name, 'staff_id': p.staff_id,
            'department': p.department, 'phone': p.phone,
            'email': request.user.email, 'username': request.user.username,
            'uploaded_results': uploaded, 'unique_students': students,
            'member_since': p.created_at.strftime('%b %d, %Y'),
        })
    except TeacherProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Profile not found'})


def student_results_page(request):
    student_name = request.GET.get('name', '').strip()
    exam_number = request.GET.get('exam', '').strip()
    student_class = request.GET.get('class', '').strip()
    year = request.GET.get('year', '').strip()
    term = request.GET.get('term', '').strip()
    results_data = None
    error_message = None
    if student_class and year and term:
        if not exam_number and not student_name:
            error_message = 'Please enter examination number or full name'
        else:
            results = StudentResult.objects.filter(student_class=student_class, year=year, term=term)
            if exam_number:
                results = results.filter(exam_number=exam_number)
            if student_name:
                results = results.filter(student_name__icontains=student_name)
            if results.exists():
                subjects = []
                total = 0
                highest = 0
                lowest = 100
                for r in results:
                    score_val = float(r.score)
                    total += score_val
                    if score_val > highest:
                        highest = score_val
                    if score_val < lowest:
                        lowest = score_val
                    subjects.append({
                        'subject': r.subject, 'score': r.score,
                        'grade': r.grade, 'remarks': r.remarks,
                    })
                avg = round(total / len(subjects), 1)
                overall_grade = calculate_grade(avg)
                results_data = {
                    'student_name': results.first().student_name,
                    'exam_number': results.first().exam_number,
                    'student_class': student_class, 'year': year, 'term': term,
                    'subjects': subjects, 'total_subjects': len(subjects),
                    'average': avg, 'highest': highest, 'lowest': lowest,
                    'overall_grade': overall_grade,
                }
            else:
                error_message = 'No results found. Please verify your details and try again.'
    else:
        error_message = 'Missing required information. Please search again from the home page.'
    return render(request, 'student_results.html', {'results': results_data, 'error': error_message})


@login_required
def get_all_results(request):
    results = StudentResult.objects.all()
    student_class = request.GET.get('student_class', '').strip()
    year = request.GET.get('year', '').strip()
    term = request.GET.get('term', '').strip()
    search = request.GET.get('search', '').strip()
    if student_class:
        results = results.filter(student_class=student_class)
    if year:
        results = results.filter(year=year)
    if term:
        results = results.filter(term=term)
    if search:
        results = results.filter(Q(student_name__icontains=search) | Q(exam_number__icontains=search))
    unique_students = results.values('exam_number', 'student_name', 'student_class', 'year', 'term').distinct().order_by('-year', 'student_class', 'student_name')
    page = int(request.GET.get('page', 1))
    per_page = 25
    total = unique_students.count()
    start = (page - 1) * per_page
    end = start + per_page
    page_students = unique_students[start:end]
    data = []
    for s in page_students:
        subj_count = results.filter(exam_number=s['exam_number'], student_class=s['student_class'], year=s['year'], term=s['term']).count()
        data.append({
            'student_name': s['student_name'], 'exam_number': s['exam_number'] or '',
            'student_class': s['student_class'], 'year': s['year'],
            'term': s['term'], 'subjects_count': subj_count,
        })
    all_classes = list(StudentResult.objects.values_list('student_class', flat=True).distinct().order_by('student_class'))
    all_years = list(StudentResult.objects.values_list('year', flat=True).distinct().order_by('-year'))[:10]
    return JsonResponse({
        'status': 'success', 'results': data, 'total': total,
        'pages': math.ceil(total / per_page) if total > 0 else 1,
        'page': page, 'per_page': per_page,
        'filters': {'classes': all_classes, 'years': all_years},
    })


@login_required
@require_POST
@csrf_exempt
def delete_result(request):
    result_id = request.POST.get('id', '')
    try:
        result = StudentResult.objects.get(id=result_id)
        result.delete()
        return JsonResponse({'status': 'success', 'message': 'Result deleted successfully'})
    except StudentResult.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Result not found'})


@login_required
def get_dashboard_stats(request):
    total_results = StudentResult.objects.count()
    total_students = StudentResult.objects.values('exam_number').distinct().count()
    total_classes = StudentResult.objects.values('student_class').distinct().count()
    total_years = StudentResult.objects.values('year').distinct().count()
    try:
        profile = request.user.teacherprofile
        my_uploads = StudentResult.objects.filter(uploaded_by=request.user).count()
        my_students = StudentResult.objects.filter(uploaded_by=request.user).values('exam_number').distinct().count()
    except TeacherProfile.DoesNotExist:
        profile = None
        my_uploads = 0
        my_students = 0
    return JsonResponse({
        'status': 'success', 'total_results': total_results,
        'total_students': total_students, 'total_classes': total_classes,
        'total_years': total_years, 'my_uploads': my_uploads,
        'my_students': my_students,
        'member_since': profile.created_at.strftime('%b %d, %Y') if profile else 'N/A',
        'department': profile.department if profile else 'N/A',
    })


# ==========================================
# PAYMENT VIEWS
# ==========================================
def payment_page(request):
    return render(request, 'payment.html')


@csrf_exempt
def check_payment(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name', '')
        exam_number = request.POST.get('exam_number', '')
        student_class = request.POST.get('student_class', '')
        year = request.POST.get('year', '')
        term = request.POST.get('term', '')
        payments = TuitionPayment.objects.filter(student_name__iexact=student_name, student_class=student_class, year=year, term=term)
        if exam_number:
            payments = payments.filter(exam_number=exam_number)
        if payments.exists():
            payment_data = []
            for p in payments:
                payment_data.append({
                    'amount': str(p.amount),
                    'payment_method': p.get_payment_method_display(),
                    'payment_date': p.payment_date.strftime('%Y-%m-%d'),
                    'reference_number': p.reference_number,
                    'status': p.get_status_display(),
                    'remarks': p.remarks,
                })
            return JsonResponse({
                'status': 'success', 'student_name': student_name,
                'exam_number': exam_number, 'student_class': student_class,
                'term': term, 'year': year, 'payments': payment_data
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'No payment records found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


# ==========================================
# CBT EXAM VIEWS
# ==========================================
def exam_list_page(request):
    return render(request, 'exam_lists.html')


def take_exam(request, exam_id):
    student_class = request.GET.get('class', '').strip()

    # Check if this is a generated exam (exam_id 0 to 4)
    try:
        exam_id_int = int(exam_id)
        is_generated = 0 <= exam_id_int <= 4
    except ValueError:
        is_generated = False

    if is_generated:
        if request.method == 'POST':
            student_name = request.POST.get('student_name', '').strip()
            exam_number = request.POST.get('exam_number', '').strip()
            term = request.POST.get('term', 'First Term').strip()
            year = request.POST.get('year', str(timezone.now().year)).strip()

            if not student_name:
                return render(request, 'exam_detail.html', {
                    'exam_id': exam_id, 'subject': 'Generated Exam',
                    'student_class': student_class, 'term': term, 'year': year,
                    'error': 'Please enter your full name.'
                })

            # Fetch questions from question_bank.py
            questions, subject, sc, term, year = get_questions_for_class(student_class, exam_id_int)
            if not questions:
                return redirect('exam_list_page')

            all_questions = questions
            import random
            count_val = int(request.POST.get('question_count', 0))
            if count_val > 0 and count_val < len(all_questions):
                all_questions = random.sample(all_questions, count_val)

            total_marks = sum(int(q.get('marks', 1)) for q in all_questions)

            return render(request, 'take_exam_cbt.html', {
                'questions': all_questions,
                'questions_json': json.dumps(all_questions),
                'student_name': student_name, 'exam_number': exam_number,
                'student_class': student_class, 'subject': subject,
                'term': term, 'year': year, 'exam_id': exam_id, 'total_marks': total_marks
            })

        return render(request, 'exam_detail.html', {
            'exam_id': exam_id, 'subject': 'Generated Exam',
            'student_class': student_class, 'term': 'First Term', 'year': str(timezone.now().year)
        })

    # Database Exam (for exams created by teachers)
    try:
        ref_q = ExamQuestion.objects.get(id=exam_id)
    except ExamQuestion.DoesNotExist:
        return redirect('exam_list_page')

    subject = ref_q.subject
    term = ref_q.term
    year = ref_q.year

    if request.method == 'POST':
        student_name = request.POST.get('student_name', '').strip()
        exam_number = request.POST.get('exam_number', '').strip()
        if not student_name:
            return render(request, 'exam_detail.html', {
                'exam_id': exam_id, 'subject': subject,
                'student_class': student_class, 'term': term, 'year': year,
                'error': 'Please enter your full name.'
            })

        # FIX: Added 'correct_answer' to the values list so it shows up in corrections!
        all_questions = list(ExamQuestion.objects.filter(
            student_class=student_class, subject=subject, term=term, year=year
        ).order_by('id').values(
            'id', 'question_text', 'question_type',
            'option_a', 'option_b', 'option_c', 'option_d', 'marks', 'correct_answer'
        ))

        if not all_questions:
            return redirect('exam_list_page')

        import random
        count_val = int(request.POST.get('question_count', 0))
        if count_val > 0 and count_val < len(all_questions):
            all_questions = random.sample(all_questions, count_val)

        total_marks = sum(q['marks'] for q in all_questions)

        return render(request, 'take_exam_cbt.html', {
            'questions': all_questions,
            'questions_json': json.dumps(all_questions),
            'student_name': student_name, 'exam_number': exam_number,
            'student_class': student_class, 'subject': subject,
            'term': term, 'year': year, 'exam_id': exam_id, 'total_marks': total_marks
        })

    return render(request, 'exam_detail.html', {
        'exam_id': exam_id, 'subject': subject,
        'student_class': student_class, 'term': term, 'year': year
    })

@csrf_exempt
def get_exam_questions_for_take(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    try:
        data = json.loads(request.body)
        student_class = data.get('student_class', '').strip()
        exam_id = int(data.get('exam_id', 0))
        if not student_class:
            return JsonResponse({'status': 'error', 'message': 'No questions for this class'})
        questions, subject_name, sc, term, year = get_questions_for_class(student_class, exam_id)
        if not questions:
            available = ', '.join(get_available_classes())
            return JsonResponse({'status': 'error', 'message': f'No questions found for "{student_class}". Available: {available}'})
        result = []
        for q in questions:
            result.append({
                'id': q['id'], 'question_text': q['question_text'],
                'question_type': q['question_type'], 'option_a': q['option_a'],
                'option_b': q['option_b'], 'option_c': q['option_c'],
                'option_d': q['option_d'], 'correct_answer': q['correct_answer'],
                'marks': int(q.get('marks', 1)),
            })
        return JsonResponse({
            'status': 'success', 'questions': result,
            'subject': subject_name, 'student_class': student_class,
            'total_questions': len(result)
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def get_exams(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    try:
        student_class = request.POST.get('student_class', '').strip()
        if not student_class:
            return JsonResponse({'status': 'error', 'message': 'Please select a class'})
        db_questions = ExamQuestion.objects.filter(student_class=student_class)
        from django.db.models import Count, Sum
        subject_data = db_questions.values('subject').annotate(count=Count('id'), total=Sum('marks')).order_by('subject')
        exams_list = []
        for s in subject_data:
            first_q = db_questions.filter(subject=s['subject']).first()
            exam_id = first_q.id if first_q else 0
            exams_list.append({
                'exam_id': exam_id, 'subject': s['subject'],
                'count': s['count'] or 0, 'total': s['total'] or 0,
            })
        bank_count = get_class_question_count(student_class)
        if bank_count > 0:
            if 'Nursery' in student_class:
                bank_subjects = [
                    {'exam_id': 0, 'subject': 'English & Numbers', 'count': 5, 'total': 5},
                    {'exam_id': 1, 'subject': 'Basic Science & Nature', 'count': 5, 'total': 5},
                    {'exam_id': 2, 'subject': 'Social Studies & Habits', 'count': 5, 'total': 5},
                    {'exam_id': 3, 'subject': 'General Knowledge', 'count': 5, 'total': 5},
                ]
            else:
                bank_subjects = [
                    {'exam_id': 0, 'subject': 'English Language', 'count': 12, 'total': 12},
                    {'exam_id': 1, 'subject': 'Mathematics', 'count': 12, 'total': 12},
                    {'exam_id': 2, 'subject': 'Basic Science', 'count': 8, 'total': 8},
                    {'exam_id': 3, 'subject': 'Social Studies', 'count': 8, 'total': 8},
                    {'exam_id': 4, 'subject': 'Computer Studies & GK', 'count': 10, 'total': 10},
                ]
            exams_list.extend(bank_subjects)
        return JsonResponse({'status': 'success', 'exams': exams_list})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def submit_exam(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    try:
        data = json.loads(request.body)
        answers = data.get('answers', {})
        question_ids = data.get('question_ids', [])
        questions_data = data.get('questions_data', [])
        student_name = data.get('student_name', '')
        student_class = data.get('student_class', '')
        exam_number = data.get('exam_number', '')
        subject = data.get('subject', '')
        term = data.get('term', '')
        year = str(data.get('year', ''))
        total_marks = 0
        score = 0
        correct_answers = {}
        if questions_data:
            for q in questions_data:
                qid = str(q['id'])
                marks = int(q.get('marks', 1))
                total_marks += marks
                correct = str(q.get('correct_answer', '')).strip().upper()
                correct_answers[qid] = correct
                if qid in answers:
                    if str(answers[qid]).strip().upper() == correct:
                        score += marks
        else:
            questions = ExamQuestion.objects.filter(id__in=question_ids).order_by('id')
            for question in questions:
                total_marks += question.marks
                qid = str(question.id)
                correct_answers[qid] = question.correct_answer.strip().upper()
                if qid in answers:
                    if str(answers[qid]).strip().upper() == question.correct_answer.strip().upper():
                        score += question.marks
        ExamAttempt.objects.create(
            student_name=student_name, student_class=student_class,
            exam_number=exam_number, subject=subject, term=term, year=year,
            score=score, total_marks=total_marks,
            time_started=timezone.now(), time_completed=timezone.now(), answers=answers
        )
        percentage = (score / total_marks * 100) if total_marks > 0 else 0
        return JsonResponse({
            'status': 'success', 'score': score, 'total_marks': total_marks,
            'percentage': round(percentage, 2), 'correct_answers': correct_answers
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def get_tasks(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    try:
        student_class = request.POST.get('student_class', '')
        if not student_class:
            return JsonResponse({'status': 'error', 'message': 'Class is required'})
        tasks = HolidayTask.objects.filter(student_class=student_class).order_by('-created_at')
        tasks_list = []
        for task in tasks:
            tasks_list.append({
                'id': task.id, 'title': task.title, 'description': task.description,
                'task_type': task.get_task_type_display(), 'subject': task.subject,
                'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else '',
                'has_attachment': bool(task.attachment),
                'created_at': task.created_at.strftime('%Y-%m-%d %H:%M')
            })
        return JsonResponse({'status': 'success', 'tasks': tasks_list})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
@csrf_exempt
def record_payment(request):
    if request.method == 'POST':
        try:
            TuitionPayment.objects.create(
                student_name=request.POST.get('student_name', ''),
                exam_number=request.POST.get('exam_number', ''),
                student_class=request.POST.get('student_class', ''),
                amount=request.POST.get('amount', 0),
                term=request.POST.get('term', ''),
                year=request.POST.get('year', ''),
                payment_method=request.POST.get('payment_method', ''),
                payment_date=request.POST.get('payment_date', ''),
                reference_number=request.POST.get('reference_number', ''),
                status=request.POST.get('status', 'verified'),
                remarks=request.POST.get('remarks', ''),
                verified_by=request.user
            )
            return JsonResponse({'status': 'success', 'message': 'Payment recorded successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
@csrf_exempt
def upload_task(request):
    if request.method == 'POST':
        try:
            HolidayTask.objects.create(
                title=request.POST.get('title', ''),
                description=request.POST.get('description', ''),
                task_type=request.POST.get('task_type', 'assignment'),
                student_class=request.POST.get('student_class', ''),
                subject=request.POST.get('subject', ''),
                due_date=request.POST.get('due_date', ''),
                attachment=request.FILES.get('attachment', None),
                created_by=request.user
            )
            return JsonResponse({'status': 'success', 'message': 'Task uploaded successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


# ==========================================
# SUPERUSER VIEWS
# ==========================================
def superuser_login_page(request):
    """Superuser Login Page"""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/superuser/dashboard/')
    return render(request, 'superuser_login.html')

@login_required
def superuser_dashboard(request):
    """Superuser Dashboard - Only accessible by superusers"""
    if not request.user.is_superuser:
        return redirect('/admin/login/')

    # Get some basic stats for the superuser dashboard
    total_users = User.objects.count()
    total_teachers = TeacherProfile.objects.count()
    total_results = StudentResult.objects.count()
    total_exams = ExamQuestion.objects.count()

    return render(request, 'superuser_dashboard.html', {
        'username': request.user.username,
        'total_users': total_users,
        'total_teachers': total_teachers,
        'total_results': total_results,
        'total_exams': total_exams,
    })

@csrf_exempt
@require_POST
def ajax_superuser_login(request):
    """Handle Superuser AJAX Login"""
    import json
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials or not a superuser'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@csrf_exempt
def create_exam(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            questions = data.get('questions', [])
            for q in questions:
                ExamQuestion.objects.create(
                    subject=data['subject'], student_class=data['student_class'],
                    term=data['term'], year=data['year'],
                    question_text=q['question_text'], question_type=q['question_type'],
                    option_a=q.get('option_a', ''), option_b=q.get('option_b', ''),
                    option_c=q.get('option_c', ''), option_d=q.get('option_d', ''),
                    correct_answer=q['correct_answer'], marks=int(q.get('marks', 1)),
                    created_by=request.user
                )
            return JsonResponse({'status': 'success', 'message': f'{len(questions)} questions created successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
