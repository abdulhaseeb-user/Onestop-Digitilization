from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, "index.html")



def register_user(request):
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            email = request.POST["email"]
            password = request.POST["password1"]

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("student")
        else:
            # Handle invalid form data
            pass

    context = {"form": form}
    return render(request, "register.html", context)

def login_user(request):
    form = UserForm()

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("student")
        else:
            # Handle invalid login credentials
            pass
    context = {"form": form}
    return render(request, "login.html")

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
