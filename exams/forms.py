from django import forms
from .models import Exam, ExamResult

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'exam_date', 'class_name']

class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = [
            'student', 'exam', 'mathematics', 'english', 'science', 'social_studies', 'computer_science'
        ]