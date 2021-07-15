from django.urls import path
from student import views

urlpatterns = [
    path('dashboard/', views.studentDashboard),
    path('exam/submit/', views.studentExamSubmit),
    path('exam/block/', views.studentExamBlock),
    path('exam/warn/', views.studentExamWarn),
    path('exam/attendee/', views.studentExamAttendee),
]
