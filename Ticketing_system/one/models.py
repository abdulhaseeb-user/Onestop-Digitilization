from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Department(models.TextChoices):
    CS = 'CS', 'Computer Science'
    CYS = 'CYS', 'Cybersecurity'
    SE = 'SE', 'Software Engineering'
    AI = 'AI', 'Artificial Intelligence'

# superadmin addition


class Manager(models.Model):
    ManagerID = models.CharField(
        primary_key=True, max_length=10, blank=False, null=False)
    Email = models.EmailField(unique=True)
    Name = models.CharField(max_length=255)
    Role = models.CharField(max_length=50)
    services_overseen = models.ManyToManyField('Service')

    def __str__(self):
        return self.Name

#manager addition
class Subject(models.Model):
    SubjectID = models.CharField(
        primary_key=True, max_length=6, blank=False, null=False)
    SubjectName = models.CharField(max_length=255)
    Department = models.CharField(max_length=3, choices=Department.choices)
    
    def __str__(self):
        return f"{self.SubjectName} | {self.SubjectName}"

#manager addition
class Faculty(models.Model):
    FacultyID = models.CharField(
        primary_key=True, max_length=10, blank=False, null=False)
    Email = models.EmailField(unique=True)
    Name = models.CharField(max_length=255)
    Department = models.CharField(max_length=4, choices=Department.choices)
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)  # Use ManyToManyField for multiple subjects
    Role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.FacultyID} | {self.Name}"

# manager addition


class Section(models.Model):
    SectionID = models.CharField(
        primary_key=True, max_length=10, blank=False, null=False)
    Department = models.CharField(max_length=3, choices=Department.choices)
    
    def __str__(self):
        return f"{self.SectionID}"

# superadmin addition/ manager addition


class Student(models.Model):
    StudentID = models.CharField(
        primary_key=True, max_length=10, blank=False, null=False)
    Email = models.EmailField(unique=True)
    Name = models.CharField(max_length=255)
    Department = models.CharField(max_length=3, choices=Department.choices)
    Batch = models.IntegerField()
    Section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.StudentID

# superadmin addition


class Service(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# manager
class Appointment(models.Model):
    AppointmentID = models.IntegerField(primary_key=True, blank=False, null=False)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Staff = models.ForeignKey(Manager, on_delete=models.CASCADE)
    Service = models.ForeignKey(Service, on_delete=models.CASCADE)
    Date = models.DateField()
    Time = models.TimeField()
    Status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.AppointmentID} | {self.Status}"

# done


class StudentAdvising(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
    ]

    ticket_id = models.IntegerField(primary_key=True, blank=False, null=False)
    # Reference the Student model
    student_id = models.ForeignKey(
        Student, on_delete=models.CASCADE, default=None)
    email = models.EmailField()
    issues_explanation = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        Manager, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='submitted')

    def __str__(self):
        return f"{self.ticket_id}"


@receiver(post_save, sender=StudentAdvising)
def assign_manager(sender, instance, created, **kwargs):
    if created and not instance.manager:
        managers = Manager.objects.filter(services_overseen=instance.service)
        if managers.exists():
            instance.manager = managers.first()
            instance.save()

# manager implementation


class Notification(models.Model):
    NotificationID = models.IntegerField(primary_key=True, blank=False, null=False)
    Manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    Timestamp = models.DateTimeField(auto_now_add=True)
    NotificationContent = models.TextField()
    Status = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.NotificationID} | {self.Status}"

# still deciding


class Report(models.Model):
    ReportID = models.IntegerField(primary_key=True, blank=False, null=False)
    User = models.ForeignKey(Manager, on_delete=models.CASCADE)
    ReportContent = models.TextField()
    Timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.ReportID}"

# class ChatMessage(models.Model):
#     MessageID = models.AutoField(primary_key=True)
#     Sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages')
#     Receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_messages')
#     Timestamp = models.DateTimeField(auto_now_add=True)
#     MessageContent = models.TextField()
