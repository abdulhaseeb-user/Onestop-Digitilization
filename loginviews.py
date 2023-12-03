from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re


def index(request):
    return render(request, "index.html")

def register_user(request):
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                
                # Check if the user is a student
                if is_student_email(email):
                    return redirect("student")
                else:
                    # User is not a student, redirect to admin page
                    return redirect("manager")
            else:
                # Handle invalid login credentials
                messages.error(request, 'Invalid login credentials. Please check your email and password.')

    context = {"form": form}
    return render(request, "register.html", context)

# def register_user(request):
#     form = UserForm()

#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = request.POST["email"]
#             password = request.POST["password1"]

#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#             # Check if the user is a student
#                 if is_student_email(email):
#                     login(request, user)
#                     return redirect("student")
#                 else:
#                     # User is not a student, redirect to admin page
#                     login(request, user)
#                     return redirect("manager")
#             else:
#                 # Handle invalid login credentials
#                 messages.error(request, 'Invalid login credentials. Please check your email and password.')

#     context = {"form": form}
#     return render(request, "register.html", context)

def login_user(request):
    form = UserForm()

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        # Check if the email is in the correct format
        # if not is_student_email(email):
        #     messages.error(request, 'Invalid email format. Only students are allowed to login.')
        #     return render(request, "login.html", {"form": form})

        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Check if the user is a student
            if is_student_email(email):
                login(request, user)
                return redirect("student")
            else:
                # User is not a student, redirect to admin page
                login(request, user)
                return redirect("manager")
        else:
            # Handle invalid login credentials
            messages.error(request, 'Invalid login credentials. Please check your email and password.')
            
    context = {"form": form}
    return render(request, "login.html", context)

def is_student_email(email):
    # Implement your logic to check if the email is in the correct format for students
    # For example, you can use regular expressions
    pattern = re.compile(r'^[kIlLpPcC]\d{6}@nu\.edu\.pk$')
    return bool(pattern.match(email))

def logout_user(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def student(request):
    if request.user.first_name and request.user.last_name:
        name = request.user.first_name + " " + request.user.last_name
    else:
        name = ""

    if request.user.email:
        email = request.user.email
    else:
        email = ""

    # if request.user.student_id:
    #     student_id = request.user.student_id
    # else:
    #     student_id = ""

    # if request.user.program:
    #     program = request.user.program
    # else:
    #     program = ""


    context = {"name": name, "email": email, } #"student_id": student_id, "program": program
    return render(request, "student.html", context)

@login_required
def manager(request):
    if request.user.first_name and request.user.last_name:
        name = request.user.first_name + " " + request.user.last_name
    else:
        name = ""

    if request.user.email:
        email = request.user.email
    else:
        email = ""



    context = {"name": name, "email": email, } 
    return render(request, "manager.html", context)
