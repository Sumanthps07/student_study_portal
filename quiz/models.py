# quiz/models.py
from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def _str_(self):
        return self.name

class Question(models.Model):
    SUBJECT_CHOICES = (
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Mathematics', 'Mathematics'),
        ('Computer Science', 'Computer Science'),
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=(
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ))

    def _str_(self):
        return f"{self.subject.name} - {self.question_text[:50]}..."

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.subject.name} {self.score}"
    

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username