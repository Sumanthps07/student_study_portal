from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home, name='quiz_home'),
    path('take/<int:subject_id>/', views.take_quiz, name='take_quiz'),
    path('result/<int:subject_id>/', views.quiz_result, name='quiz_result'),

    path('faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/manage_questions/<int:subject_id>/', views.manage_questions, name='manage_questions'),
    path('faculty/view_results/<int:subject_id>/', views.view_student_results, name='view_student_results'),
]