from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('LIBRARIAN', 'Librarian'),
        ('STUDENT', 'Student'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser
    
    def is_librarian(self):
        return self.role == 'LIBRARIAN' or self.is_admin()
    
    def is_student(self):
        return self.role == 'STUDENT'
