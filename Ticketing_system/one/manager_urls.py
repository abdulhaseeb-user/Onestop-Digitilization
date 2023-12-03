from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('add_subject/', views.add_subject_view, name='add_subject'),
    path('add_faculty/', views.add_faculty_view, name='add_faculty'),
    path('add_section/', views.add_section_view, name='add_section'),
    path('add_student/', views.add_student_view, name='add_student'),
    path('create_timetable/', views.index, name='create_timetable'),
    path('add_department/', views.index, name='add_department'),
    path('add_services/', views.index, name='add_services'),
    path('view_notifications/', views.index, name='view_notifications'),
    path('view_tickets/', views.index, name='view_tickets'),
]
