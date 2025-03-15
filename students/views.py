from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from exams.models import Exam, ExamResult
from exams.forms import ExamForm, ExamResultForm

def home(request):
    return render(request, "home.html")  # Ensure home.html exists in templates

# Student List View
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

# Student Profile View
def student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students/student_profile.html', {'student': student})

# Student Registration View
def student_register(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_registration.html', {'form': form})


#exams

# View for listing all exams
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exams/exam_list.html', {'exams': exams})

# View for adding an exam
def add_exam(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'exams/add_exam.html', {'form': form})

# View for adding student marks
def add_exam_result(request):
    if request.method == "POST":
        form = ExamResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamResultForm()
    return render(request, 'exams/add_exam_result.html', {'form': form})

# View for viewing exam results
def exam_results(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    results = ExamResult.objects.filter(exam=exam)
    return render(request, 'exams/exam_results.html', {'exam': exam, 'results': results})