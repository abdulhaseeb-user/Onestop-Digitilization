from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('one/', views.advising_view, name='student_advising'),
    path('quick_help/', views.quick_help, name='quick_help_page'),
    path('ticket_details/<int:ticket_id>/',
         views.ticket_details, name='ticket_details'),
]
