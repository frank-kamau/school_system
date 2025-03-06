from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

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