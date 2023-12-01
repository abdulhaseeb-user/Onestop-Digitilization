# forms.py
from django.shortcuts import get_object_or_404
from django import forms
from django.core.exceptions import ValidationError
from .models import Service, StudentAdvising, Student
import re

class StudentAdvisingForm(forms.ModelForm):
    student_id = forms.CharField(
        max_length=20,
        error_messages={
            'required': 'Please enter your student ID',
        },
        label='Student ID',
        help_text='Enter your student ID in the format: 21k-3217',
    )

    services = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=forms.Select,
    )

    class Meta:
        model = StudentAdvising
        exclude = ['ticket_id', 'status', 'manager', 'student']
        fields = ['student_id', 'email', 'services', 'issues_explanation']

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if not re.match(r'^\d{2}k-\d{4}$', student_id):
            raise ValidationError('Student ID must be in the format: 21k-3217')
        return student_id

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id')

        # Fetch the corresponding Student instance
        student_instance = get_object_or_404(Student, StudentID=student_id)

        # Assign the student instance to the form data
        cleaned_data['student_id'] = student_instance
        return cleaned_data


# @user_passes_test(lambda u: u.is_staff)
# def update_status_view(request, ticket_id):
#     ticket = get_object_or_404(StudentAdvising, ticket_id=ticket_id)

#     if request.method == 'POST':
#         form = StatusUpdateForm(request.POST, instance=ticket)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')  # Redirect to success page
#     else:
#         form = StatusUpdateForm(instance=ticket)

#     return render(request, 'one/update_status.html', {'form': form, 'ticket': ticket})
