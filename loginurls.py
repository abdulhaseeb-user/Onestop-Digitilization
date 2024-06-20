from django.urls import path
from .import views

urlpatterns = [
    path("student/", views.student, name="student"),
    
    path("manager/", views.manager, name="manager"),
    path("logout/", views.logout_user, name="logout"),
    path("login/", views.login_user, name="login"),
    path("", views.login_user, name="login"),
    path("register", views.register_user),
    path('register/', views.register_user, name='register_user')
    
]
