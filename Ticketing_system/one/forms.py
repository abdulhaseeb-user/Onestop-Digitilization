from django.http import Http404
from django.shortcuts import get_object_or_404
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import *
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

        try:
            student_instance = get_object_or_404(Student, StudentID=student_id)
        except Http404:
            raise ValidationError('Student not found. Please enter a valid student ID.')

        cleaned_data['student_id'] = student_instance
        return cleaned_data

class AddSubjectForm(forms.ModelForm):
    Departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Subject
        fields = ['SubjectID', 'SubjectName', 'Departments']

    def clean_SubjectID(self):
        subject_id = self.cleaned_data.get('SubjectID')

        if not subject_id[:2].isalpha() or not subject_id[2:].isdigit() or len(subject_id) != 6:
            raise forms.ValidationError('Invalid Subject ID format. It should be in the format: CS1002')

        return subject_id

class FacultyForm(forms.ModelForm):
    sub = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Faculty
        exclude = ['FacultyID']
        fields = ['Name', 'Email', 'Department', 'sub','Role']
        
class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'
    
    def clean_SectionID(self):
        section_id = self.cleaned_data['SectionID']
        
        if not (len(section_id) == 4 and section_id[:3].isdigit() and section_id[3].isalpha()):
            raise forms.ValidationError("SectionID should be in the format '###X' where X is a single alphabet.")

        return section_id

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
    
    BATCH_CHOICES = [(year, str(year)) for year in range(2010, 2100)] 

    Batch = forms.ChoiceField(
        choices=BATCH_CHOICES,
        validators=[MinValueValidator(2010), MaxValueValidator(2100)], 
    )
    def clean_student_id(self):
        student_id = self.cleaned_data.get('StudentID')
        if not re.match(r'^\d{2}k-\d{4}$', student_id):
            raise ValidationError('Student ID must be in the format: 21k-3217')
        return student_id
    
    def clean_Batch(self):
        batch = self.cleaned_data['Batch']

        try:
            batch_int = int(batch)
        except ValueError:
            raise ValidationError('Batch must be a valid integer.')

        if not (2010 <= batch_int <= 2100):
            raise ValidationError('Batch must be between 2000 and 2100.')

        return batch_int

    
    
    
    

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
