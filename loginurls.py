from django.urls import path
from .import views

urlpatterns = [
    path("student/", views.student, name="student"),
    path("logout/", views.logout_user, name="logout"),
    path("login/", views.login_user, name="login"),
    path("", views.index),
    path("register", views.register_user)
    
]
