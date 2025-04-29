from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from exams.models import Exam, ExamResult
from exams.forms import ExamForm, ExamResultForm
from django.db.models import Q  # For complex queries
from django.db.models import Avg
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")  # Ensure home.html exists in templates

# Student List View
def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(admission_number__icontains=query) |
            Q(email__icontains=query)
        )
    else:
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
            print("Form errors:", form.errors)
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

def exam_analysis(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    # results = ExamResult.objects.filter(exam=exam).order_by('-total_marks')
    class_filter = request.GET.get('class')

    students = Student.objects.all().values_list('class_name', flat=True).distinct()

    if class_filter:
        results = ExamResult.objects.filter(exam=exam, student__class_name=class_filter).order_by('-total_marks')
    else:
        results = ExamResult.objects.filter(exam=exam).order_by('-total_marks')

    # Calculate average marks per subject
    subject_averages = results.aggregate(
        avg_math=Avg('mathematics'),
        avg_english=Avg('english'),
        avg_science=Avg('science'),
        avg_social=Avg('social_studies'),
        avg_computer=Avg('computer_science')
    )

    # Rank students based on total_marks (already ordered above)
    for index, result in enumerate(results, start=1):
        result.rank = index

    return render(request, 'exams/exam_analysis.html', {
        'exam': exam,
        'results': results,
        'subject_averages': subject_averages,
        'selected_class': class_filter,
        'class_list': students
    })

def generate_pdf_exam_analysis(request, exam_id, class_name):
    exam = Exam.objects.get(id=exam_id)
    results = ExamResult.objects.filter(exam=exam, student__class_name=class_name)

    subject_averages = results.aggregate(
        avg_math=Avg('mathematics'),
        avg_english=Avg('english'),
        avg_science=Avg('science'),
        avg_social=Avg('social_studies'),
        avg_computer=Avg('computer_science')
    )

    for i, result in enumerate(results.order_by('-total_marks'), start=1):
        result.rank = i

    template = get_template('exams/pdf_exam_report.html')
    html = template.render({
        'exam': exam,
        'results': results,
        'subject_averages': subject_averages,
        'class': class_name,
    })


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{class_name}_{exam.name}_report.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

def subject_comparison(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    classes = Student.objects.values_list('class_name', flat=True).distinct()

    data = {
        'labels': [],
        'math': [],
        'english': [],
        'science': [],
        'social': [],
        'computer': [],
    }

    for cls in classes:
        results = ExamResult.objects.filter(exam=exam, student__class_name=cls)
        data['labels'].append(cls)
        data['math'].append(results.aggregate(avg=Avg('mathematics'))['avg'] or 0)
        data['english'].append(results.aggregate(avg=Avg('english'))['avg'] or 0)
        data['science'].append(results.aggregate(avg=Avg('science'))['avg'] or 0)
        data['social'].append(results.aggregate(avg=Avg('social_studies'))['avg'] or 0)
        data['computer'].append(results.aggregate(avg=Avg('computer_science'))['avg'] or 0)

    return render(request, 'exams/subject_comparison.html', {
        'exam': exam,
        'chart_data': data,
    })

def student_progress(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    results = ExamResult.objects.filter(student=student).select_related('exam').order_by('exam__exam_date', 'exam__term')

    labels = [f"{r.exam.term} {r.exam.exam_date.year}" for r in results]
    total_marks = [r.total_marks for r in results]

    return render(request, 'exams/student_progress.html', {
        'student': student,
        'labels': labels,
        'total_marks': total_marks,
    })