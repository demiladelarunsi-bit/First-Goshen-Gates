from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import StudentResult, TeacherProfile, ExamQuestion, ExamAttempt, TuitionPayment, HolidayTask
import csv, io, json, math
from django.db.models import Q
from django.utils import timezone
from .utils import safe_int, safe_float, safe_str


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

    results = StudentResult.objects.filter(
        student_class=student_class, year=year, term=term
    )
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
            results = StudentResult.objects.filter(
                student_class=student_class, year=year, term=term
            )
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
                        'subject': r.subject,
                        'score': r.score,
                        'grade': r.grade,
                        'remarks': r.remarks,
                    })
                avg = round(total / len(subjects), 1)
                overall_grade = calculate_grade(avg)

                results_data = {
                    'student_name': results.first().student_name,
                    'exam_number': results.first().exam_number,
                    'student_class': student_class,
                    'year': year,
                    'term': term,
                    'subjects': subjects,
                    'total_subjects': len(subjects),
                    'average': avg,
                    'highest': highest,
                    'lowest': lowest,
                    'overall_grade': overall_grade,
                }
            else:
                error_message = 'No results found. Please verify your details and try again.'
    else:
        error_message = 'Missing required information. Please search again from the home page.'

    return render(request, 'student_results.html', {
        'results': results_data,
        'error': error_message,
    })


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
        results = results.filter(
            Q(student_name__icontains=search) | Q(exam_number__icontains=search)
        )
    
    unique_students = results.values(
        'exam_number', 'student_name', 'student_class', 'year', 'term'
    ).distinct().order_by('-year', 'student_class', 'student_name')
    
    page = int(request.GET.get('page', 1))
    per_page = 25
    total = unique_students.count()
    start = (page - 1) * per_page
    end = start + per_page
    page_students = unique_students[start:end]
    
    data = []
    for s in page_students:
        subj_count = results.filter(
            exam_number=s['exam_number'],
            student_class=s['student_class'],
            year=s['year'],
            term=s['term']
        ).count()
        
        data.append({
            'student_name': s['student_name'],
            'exam_number': s['exam_number'] or '',
            'student_class': s['student_class'],
            'year': s['year'],
            'term': s['term'],
            'subjects_count': subj_count,
        })
    
    all_classes = list(StudentResult.objects.values_list('student_class', flat=True).distinct().order_by('student_class'))
    all_years = list(StudentResult.objects.values_list('year', flat=True).distinct().order_by('-year'))[:10]
    
    return JsonResponse({
        'status': 'success',
        'results': data,
        'total': total,
        'pages': math.ceil(total / per_page) if total > 0 else 1,
        'page': page,
        'per_page': per_page,
        'filters': {
            'classes': all_classes,
            'years': all_years,
        }
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
        'status': 'success',
        'total_results': total_results,
        'total_students': total_students,
        'total_classes': total_classes,
        'total_years': total_years,
        'my_uploads': my_uploads,
        'my_students': my_students,
        'member_since': profile.created_at.strftime('%b %d, %Y') if profile else 'N/A',
        'department': profile.department if profile else 'N/A',
    })

# ==========================================
# SUPERUSER LOGIN & DASHBOARD
# ==========================================
def superuser_login_page(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/superuser/dashboard/')
    return render(request, 'superuser_login.html')

@csrf_exempt
@require_POST
def ajax_superuser_login(request):
    user = authenticate(request, username=request.POST.get('username', '').strip(), password=request.POST.get('password', ''))
    if user and user.is_superuser:
        login(request, user)
        return JsonResponse({'status': 'success', 'username': user.username})
    return JsonResponse({'status': 'error', 'message': 'Invalid superuser credentials'})

@login_required
def superuser_dashboard(request):
    if not request.user.is_superuser:
        return redirect('/superuser/login/')
    return render(request, 'superuser_dashboard.html', {'username': request.user.username})


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

        payments = TuitionPayment.objects.filter(
            student_name__iexact=student_name,
            student_class=student_class,
            year=year,
            term=term
        )
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
                'status': 'success',
                'student_name': student_name,
                'exam_number': exam_number,
                'student_class': student_class,
                'term': term,
                'year': year,
                'payments': payment_data
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'No payment records found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


# ==========================================
# CBT EXAM VIEWS (FIXED)
# ==========================================
def exam_list_page(request):
    return render(request, 'exam_lists.html')

def take_exam(request, exam_id):
    student_class = request.GET.get('class', '').strip()
    try:
        ref_q = ExamQuestion.objects.get(id=exam_id)
    except ExamQuestion.DoesNotExist:
        from django.shortcuts import redirect
        return redirect('exam_list_page')
    subject = ref_q.subject
    term = ref_q.term
    year = ref_q.year
    if request.method == 'POST':
        student_name = request.POST.get('student_name', '').strip()
        exam_number = request.POST.get('exam_number', '').strip()
        if not student_name:
            return render(request, 'exam_detail.html', {'exam_id': exam_id, 'subject': subject, 'student_class': student_class, 'term': term, 'year': year, 'error': 'Please enter your full name.'})
        all_questions = list(ExamQuestion.objects.filter(student_class=student_class, subject=subject, term=term, year=year).order_by('id').values('id', 'question_text', 'question_type', 'option_a', 'option_b', 'option_c', 'option_d', 'marks'))
        if not all_questions:
            from django.shortcuts import redirect
            return redirect('exam_list_page')
        # Limit questions based on count parameter
        import random
        count_val = int(request.POST.get('question_count', 0))
        if count_val > 0 and count_val < len(all_questions):
            all_questions = random.sample(all_questions, count_val)
        total_marks = sum(q['marks'] for q in all_questions)
        import json
        return render(request, 'take_exam_cbt.html', {
            'questions': all_questions, 'questions_json': json.dumps(all_questions),
            'student_name': student_name, 'exam_number': exam_number,
            'student_class': student_class, 'subject': subject,
            'term': term, 'year': year, 'exam_id': exam_id, 'total_marks': total_marks
        })
    return render(request, 'exam_detail.html', {'exam_id': exam_id, 'subject': subject, 'student_class': student_class, 'term': term, 'year': year})


def get_exam_questions_for_take(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_class = data.get('student_class', '')
            exam_id = int(data.get('exam_id', 0))
            
            all_questions = QUESTION_BANK.get(student_class, [])
            if not all_questions:
                return JsonResponse({'status': 'error', 'message': 'No questions for this class'})

            # Define subject ranges
            if 'Nursery' in student_class:
                subject_ranges = {
                    0: ('English & Numbers', 0, 5),
                    5: ('Basic Science & Nature', 5, 10),
                    10: ('Social Studies & Habits', 10, 15),
                    15: ('General Knowledge', 15, 20),
                }
            else:
                subject_ranges = {
                    0: ('English Language', 0, 12),
                    12: ('Mathematics', 12, 24),
                    24: ('Basic Science', 24, 32),
                    32: ('Social Studies', 32, 40),
                    40: ('Computer Studies & GK', 40, 50),
                }

            subject_name, start, end = subject_ranges.get(exam_id, ('Mixed', 0, len(all_questions)))
            end = min(end, len(all_questions))
            questions = all_questions[start:end]

            result = []
            for i, q in enumerate(questions):
                result.append({
                    'id': i + 1,
                    'question_text': q[0],
                    'question_type': q[1],
                    'option_a': q[2],
                    'option_b': q[3],
                    'option_c': q[4],
                    'option_d': q[5],
                    'correct_answer': q[6],
                    'marks': int(q[7])  # FIX: Convert to int
                })

            return JsonResponse({
                'status': 'success',
                'questions': result,
                'subject': subject_name,
                'student_class': student_class,
                'total_questions': len(result)
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def get_exams(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    try:
        student_class = request.POST.get('student_class', '').strip()
        if not student_class:
            return JsonResponse({'status': 'error', 'message': 'Please select a class'})
        questions = ExamQuestion.objects.filter(student_class=student_class)
        from django.db.models import Count, Sum
        subject_data = questions.values('subject').annotate(
            count=Count('id'), total=Sum('marks')
        ).order_by('subject')
        exams_list = []
        for s in subject_data:
            first_q = questions.filter(subject=s['subject']).first()
            exam_id = first_q.id if first_q else 0
            exams_list.append({
                'exam_id': exam_id, 'subject': s['subject'],
                'count': s['count'] or 0, 'total': s['total'] or 0,
            })
        return JsonResponse({'status': 'success', 'exams': exams_list})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def submit_exam(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    try:
        import json
        from django.utils.timezone import now
        data = json.loads(request.body)
        answers = data.get('answers', {})
        student_name = data.get('student_name', '')
        student_class = data.get('student_class', '')
        exam_number = data.get('exam_number', '')
        subject = data.get('subject', '')
        term = data.get('term', '')
        year = str(data.get('year', ''))
        exam_id = data.get('exam_id', '')
        
        # Get all questions for this exam
        questions = list(ExamQuestion.objects.filter(
            student_class=student_class,
            subject=subject,
            term=term,
            year=year
        ).order_by('id'))
        
        if not questions:
            return JsonResponse({'status': 'error', 'message': 'No questions found'})
        
        total_marks = 0
        score = 0
        correct_answers = {}
        
        for question in questions:
            qid = str(question.id)
            total_marks += question.marks
            correct_answers[qid] = question.correct_answer.strip().upper()
            
            if qid in answers:
                user_answer = str(answers[qid]).strip().upper()
                if user_answer == question.correct_answer.strip().upper():
                    score += question.marks
        
        # Save attempt
        ExamAttempt.objects.create(
            student_name=student_name,
            student_class=student_class,
            exam_number=exam_number,
            subject=subject,
            term=term,
            year=year,
            score=score,
            total_marks=total_marks,
            time_started=now(),
            time_completed=now(),
            answers=answers
        )
        
        percentage = (score / total_marks * 100) if total_marks > 0 else 0
        
        return JsonResponse({
            'status': 'success',
            'score': int(score),
            'total_marks': int(total_marks),
            'percentage': round(percentage, 2),
            'correct_answers': correct_answers
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
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
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'task_type': task.get_task_type_display(),
                'subject': task.subject,
                'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else '',
                'has_attachment': bool(task.attachment),
                'created_at': task.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        return JsonResponse({
            'status': 'success',
            'tasks': tasks_list
        })
        
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

@login_required
@csrf_exempt
def create_exam(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            questions = data.get('questions', [])
            for q in questions:
                ExamQuestion.objects.create(
                    subject=data['subject'],
                    student_class=data['student_class'],
                    term=data['term'],
                    year=data['year'],
                    question_text=q['question_text'],
                    question_type=q['question_type'],
                    option_a=q.get('option_a', ''),
                    option_b=q.get('option_b', ''),
                    option_c=q.get('option_c', ''),
                    option_d=q.get('option_d', ''),
                    correct_answer=q['correct_answer'],
                    marks=int(q.get('marks', 1)),  # FIX: Convert to int
                    created_by=request.user
                )
            return JsonResponse({'status': 'success', 'message': f'{len(questions)} questions created successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def tasks_page(request):
    return render(request, 'tasks.html')

@login_required
def get_superuser_dashboard_data(request):
    if not request.user.is_superuser:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'})
    
    from django.db.models import Avg, Count, Sum
    from django.db.models.functions import Cast
    
    # Basic stats
    total_students = StudentResult.objects.values('exam_number').distinct().count()
    total_results = StudentResult.objects.count()
    total_exams = ExamAttempt.objects.count()
    
    # CBT Pass rates by subject
    exam_stats = ExamAttempt.objects.values('subject').annotate(
        total=Count('id'),
        passed=Count('id', filter=models.Q(score__gte=models.F('total_marks') * 0.5))
    ).order_by('subject')
    
    pass_rates = []
    for stat in exam_stats:
        rate = (stat['passed'] / stat['total'] * 100) if stat['total'] > 0 else 0
        pass_rates.append({
            'subject': stat['subject'],
            'rate': round(rate, 1),
            'total': stat['total'],
            'passed': stat['passed']
        })
    
    avg_pass_rate = sum(pr['rate'] for pr in pass_rates) / len(pass_rates) if pass_rates else 0
    
    # Recent exams
    recent_exams = list(ExamAttempt.objects.all().order_by('-created_at')[:10].values(
        'student_name', 'subject', 'score', 'total_marks'
    ))
    
    # Class performance
    class_performance = []
    all_classes = StudentResult.objects.values_list('student_class', flat=True).distinct()
    for cls in all_classes:
        class_results = StudentResult.objects.filter(student_class=cls)
        students = class_results.values('exam_number').distinct().count()
        avg_score = class_results.aggregate(avg=Avg('score'))['avg'] or 0
        class_performance.append({
            'class_name': cls,
            'students': students,
            'avg_score': avg_score
        })
    
    # Payments
    total_payments = TuitionPayment.objects.aggregate(total=Sum('amount'))['total'] or 0
    recent_payments = list(TuitionPayment.objects.all().order_by('-created_at')[:10].values(
        'student_name', 'amount', 'payment_date', 'status'
    ))
    for p in recent_payments:
        p['payment_date'] = p['payment_date'].strftime('%Y-%m-%d') if p['payment_date'] else ''
        p['status'] = p['status'].title()
    
    return JsonResponse({
        'status': 'success',
        'stats': {
            'total_students': total_students,
            'total_results': total_results,
            'total_exams': total_exams,
            'avg_pass_rate': round(avg_pass_rate, 1),
            'total_payments': float(total_payments)
        },
        'pass_rates': pass_rates,
        'recent_exams': recent_exams,
        'class_performance': class_performance,
        'recent_payments': recent_payments
    })
