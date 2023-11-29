from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Service, StudentAdvising

class StudentAdvisingForm(forms.ModelForm):
    student_id = forms.CharField(
        max_length=20,
        error_messages={
            'required': 'Please enter your student ID',
        }
    )

    services = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=forms.Select,
    )

    class Meta:
        model = StudentAdvising
        exclude = ['ticket_id', 'status']
        fields = ['student_id', 'email','services','issues_explanation']

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if not re.match(r'^\d{2}k-\d{4}$', student_id):
            raise ValidationError('Student ID must be in the format: 21k-3217')
        return student_id

    # Add a clean_status method if you need custom cleaning for the status field
    # def clean_status(self):
    #     status = self.cleaned_data.get('status')
    #     # Your custom validation for the status field if needed
    #     return status


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
