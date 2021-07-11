from django.urls import path
from main import views

urlpatterns = [
    path('ignition/', views.ignition),
    path('login/', views.login),
    path('teacher/login/', views.teacherLogin),
    path('student/login/', views.studentLogin),
    path('teacher/dashboard/', views.teacherDashboard),
    path('teacher/exam/create/', views.examCreate),
    path('teacher/exam/update/', views.examUpdate),
    path('teacher/exam/update/file', views.examUpdateFile),
    path('teacher/exam/request/', views.teacherExamRequest),
    path('teacher/exam/assign/', views.teacherExamStart),
    path('teacher/exam/end/', views.teacherExamEnd),
    path('teacher/exam/window/', views.teacherExamWindow),
    path('exam/chat/message/', views.examChatMessage),
    path('exam/student/block/', views.examBlockStudent),
    path('exam/student/unblock/', views.examUnblockStudent),
    path('student/dashboard/', views.studentDashboard),
    path('student/exam/submit/', views.studentExamSubmit),
    path('student/exam/block/', views.studentExamBlock),
    path('student/exam/warn/', views.studentExamWarn),
    path('student/exam/attendee/', views.studentExamAttendee),
    path('teacher/exam/result/', views.teacherExamResult),
    path('logout/', views.logout),
    path('', views.home),
]
