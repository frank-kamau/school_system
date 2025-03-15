"""
URL configuration for School_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from School_System import settings
from students import views
from students.views import home

urlpatterns = [

    path("", home, name="home"),  # New homepage
    path('students/', views.student_list, name='student_list'),
    path('students/register/', views.student_register, name='student_register'),
    path('students/<int:student_id>/', views.student_profile, name='student_profile'),
    path('admin/', admin.site.urls),
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/add/', views.add_exam, name='add_exam'),
    path('exams/results/add/', views.add_exam_result, name='add_exam_result'),
    path('exams/results/<int:exam_id>/', views.exam_results, name='exam_results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)