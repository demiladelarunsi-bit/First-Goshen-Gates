from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    # Main pages
    path('', views.student_page, name='student_page'),
    path('about/', views.about_page, name='about_page'),
    path('results/', views.student_results_page, name='student_results'),
    
    # AJAX endpoints
    path('ajax/check-result/', views.check_result, name='check_result'),
    path('ajax/stats/', views.get_stats, name='get_stats'),
    path('ajax/add-result/', views.add_result, name='add_result'),
    path('ajax/bulk-upload/', views.bulk_upload, name='bulk_upload'),
    path('ajax/all-results/', views.get_all_results, name='get_all_results'),
    path('ajax/delete-result/', views.delete_result, name='delete_result'),
    path('ajax/dashboard-stats/', views.get_dashboard_stats, name='get_dashboard_stats'),
    path('ajax/teacher-profile/', views.get_teacher_profile, name='get_teacher_profile'),
    
    # Admin pages
    path('admin/signup/', views.admin_signup_page, name='admin_signup_page'),
    path('admin/login/', views.admin_login_page, name='admin_login_page'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/profile/', views.teacher_profile, name='teacher_profile'),
    
    # Admin AJAX
    path('ajax/admin/signup/', views.ajax_signup, name='ajax_signup'),
    path('ajax/admin/login/', views.ajax_login, name='ajax_login'),
    path('ajax/admin/logout/', views.ajax_logout, name='ajax_logout'),
    
    # Superuser
    path('superuser/login/', views.superuser_login_page, name='superuser_login'),
    path('superuser/dashboard/', views.superuser_dashboard, name='superuser_dashboard'),
    path('ajax/superuser/login/', views.ajax_superuser_login, name='ajax_superuser_login'),
    
    # Payment
    path('payments/', views.payment_page, name='payment_page'),
    path('ajax/check-payment/', views.check_payment, name='check_payment'),
    path('ajax/admin/record-payment/', views.record_payment, name='record_payment'),
    
    # CBT Exams
    path('exams/', views.exam_list_page, name='exam_list_page'),
    path('exams/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('ajax/get-exams/', views.get_exams, name='get_exams'),
    path('ajax/get-exam-questions/', views.get_exam_questions_for_take, name='get_exam_questions_for_take'),
    path('ajax/submit-exam/', views.submit_exam, name='submit_exam'),
    path('ajax/admin/create-exam/', views.create_exam, name='create_exam'),
    
    # Holiday Tasks
    path('tasks/', views.tasks_page, name='tasks_page'),
    path('ajax/get-tasks/', views.get_tasks, name='get_tasks'),
    path('ajax/admin/upload-task/', views.upload_task, name='upload_task'),
    path('ajax/superuser/dashboard-data/', views.get_superuser_dashboard_data, name='get_superuser_dashboard_data'),
    
    # Include admin site
    path('admin/', admin.site.urls),
]