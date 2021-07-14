from django.urls import path
from student import views

urlpatterns = [
    path('ignition/', views.ignition),
    path('student/dashboard/', views.studentDashboard),
    path('student/exam/submit/', views.studentExamSubmit),
    path('student/exam/block/', views.studentExamBlock),
    path('student/exam/warn/', views.studentExamWarn),
    path('student/exam/attendee/', views.studentExamAttendee),
    path('logout/', views.logout),
    path('', views.home),
]
