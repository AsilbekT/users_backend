from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 1. Prisoner Model
class Prisoner(models.Model):
    prisoner_id = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=255)
    previous_available_date = models.DateTimeField(null=True, blank=True)
    next_available_date = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

# 2. ActivityType Model
class ActivityType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 3. RequestTemplate Model
class RequestTemplate(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Process', 'In Process'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied')
    ]

    prisoner = models.ForeignKey('Prisoner', on_delete=models.CASCADE, related_name='requests')
    activity_type = models.ForeignKey('ActivityType', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    details = models.TextField()
    date_of_request = models.DateTimeField(auto_now_add=True)
    desired_date = models.DateTimeField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_relationship = models.CharField(max_length=100, blank=True, null=True)
    image_confirmation = models.ImageField(upload_to='request_images/', blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.prisoner.full_name} - {self.activity_type.name} Request"

# 4. ApprovalProcess Model
class ApprovalProcess(models.Model):
    request_template = models.ForeignKey('RequestTemplate', on_delete=models.CASCADE, related_name='approval_processes')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)  # True = Approved, False = Denied
    comments = models.TextField(blank=True, null=True)
    approved_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.request_template.subject} - {'Approved' if self.status else 'Denied'} by {self.approved_by.username}"

# 5. DepartmentRole Model
class DepartmentRole(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()  # Defines the workflow order
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name
