from django.db import models

# Create your models here.

from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]

    id = models.AutoField(primary_key=True)
    admission_number = models.CharField(max_length=50, unique=True)  # Unique student ID
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)  # Email
    class_name = models.CharField(max_length=50)  # Class/Grade
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True, blank=True)  # Date of Birth
    address = models.TextField(null=True, blank=True)  # Home Address
    parent_contact = models.CharField(max_length=15)  # Parent/Guardian Contact
    profile_picture = models.ImageField(upload_to='students/', null=True, blank=True)  # Profile Picture
    date_registered = models.DateTimeField(auto_now_add=True)  # Auto-set registration date

    def __str__(self):
        return f"{self.name} ({self.admission_number})"