from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class StudentAdvising(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
    ]

    ticket_id = models.IntegerField(primary_key=True, blank=False, null=False)
    student_id = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField()
    issues_explanation = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    def __str__(self):
        return f"{self.student_id}"
