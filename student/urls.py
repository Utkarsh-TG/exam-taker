from django.urls import path
from student import views

urlpatterns = [
    path('dashboard/', views.studentDashboard),
    path('exam_submit/', views.studentExamSubmit),
    path('exam_block/', views.studentExamBlock),
    path('exam_warn/', views.studentExamWarn),
    path('exam_attendee/', views.studentExamAttendee),
]
