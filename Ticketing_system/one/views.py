from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from .forms import StudentAdvisingForm
from .models import StudentAdvising
import random

def index(request):
    return render(request, 'one/index.html')

def advising_view(request):
    if request.method == 'POST':
        form = StudentAdvisingForm(request.POST)
        if form.is_valid():
            advising_ticket = form.save(commit=False)
            
            advising_ticket.service = form.cleaned_data['services']

            advising_ticket.ticket_id = random.randint(1, 1000000)
            advising_ticket.save()
            
            request.session['ticket_id'] = advising_ticket.ticket_id
            
            return HttpResponse('success_page')
    else:
        form = StudentAdvisingForm()

    return render(request, 'one/advising_form.html', {'form': form})


def quick_help(request):
    student_id_search = request.GET.get('student_id')
    
    if student_id_search:
        student_advisings = StudentAdvising.objects.filter(student_id=student_id_search)
    else:
        student_advisings = StudentAdvising.objects.all()
    
    return render(request, 'one/quick_help.html', {'student_advisings': student_advisings, 'student_id_search': student_id_search})

def ticket_details(request, ticket_id):
    advising_ticket = get_object_or_404(StudentAdvising, ticket_id=ticket_id)
    return render(request, 'one/ticket_details.html', {'advising_ticket': advising_ticket})
