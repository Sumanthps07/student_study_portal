# quiz/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject, Question, QuizAttempt, Teacher
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from django.contrib.auth.models import User
@login_required
def quiz_home(request):
    subjects = Subject.objects.all()
    return render(request, 'quiz/quiz_home.html', {'subjects': subjects})

@login_required
def take_quiz(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    questions = list(subject.questions.all())
    if len(questions) < 10:
        messages.error(request, f"Not enough questions in {subject.name} to start the quiz.")
        return redirect('quiz_home')
    
    # Randomly select 20 questions
    selected_questions = random.sample(questions, 10)

    if request.method == 'POST':
        total = 10
        correct = 0
        for question in selected_questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_option:
                correct += 1
        score = correct
        # Save the attempt
        QuizAttempt.objects.create(user=request.user, subject=subject, score=score)
        messages.success(request, f'You scored {score} out of {total} in {subject.name}.')
        return redirect('quiz_result', subject_id=subject.id)

    context = {
        'subject': subject,
        'questions': selected_questions
    }
    return render(request, 'quiz/take_quiz.html', context)

@login_required
def quiz_result(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    attempts = QuizAttempt.objects.filter(user=request.user, subject=subject).order_by('-date_taken')
    return render(request, 'quiz/quiz_result.html', {'subject': subject, 'attempts':attempts})


@login_required
def faculty_dashboard(request):
    if not hasattr(request.user, 'teacher'):
        return redirect('quiz_home')
    
    subjects = Subject.objects.all()
    return render(request, 'quiz/faculty_dashboard.html', {'subjects': subjects})

@login_required
def manage_questions(request, subject_id):
    if not hasattr(request.user, 'teacher'):
        return redirect('quiz_home')
    
    subject = get_object_or_404(Subject, id=subject_id)
    questions = subject.questions.all()
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        option_a = request.POST.get('option_a')
        option_b = request.POST.get('option_b')
        option_c = request.POST.get('option_c')
        option_d = request.POST.get('option_d')
        correct_option = request.POST.get('correct_option')

        Question.objects.create(
            subject=subject,
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option
        )
        messages.success(request, 'Question added successfully!')
        return redirect('manage_questions', subject_id=subject.id)
    
    context = {
        'subject': subject,
        'questions': questions
    }
    return render(request, 'quiz/manage_questions.html', context)

@login_required
def view_student_results(request, subject_id):
    if not hasattr(request.user, 'teacher'):
        return redirect('quiz_home')
    
    subject = get_object_or_404(Subject, id=subject_id)
    attempts = QuizAttempt.objects.filter(subject=subject).order_by('-date_taken')
    
    context = {
        'subject': subject,
        'attempts': attempts
    }
    return render(request, 'quiz/view_student_results.html', context)