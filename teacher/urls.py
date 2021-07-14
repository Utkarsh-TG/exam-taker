from django.urls import path
from teacher import views

urlpatterns = [
    path('ignition/', views.ignition),
    path('teacher/dashboard/', views.teacherDashboard),
    path('teacher/exam/create/', views.examCreate),
    path('teacher/exam/update/', views.examUpdate),
    path('teacher/exam/update/file', views.examUpdateFile),
    path('teacher/exam/request/', views.teacherExamRequest),
    path('teacher/exam/assign/', views.teacherExamStart),
    path('teacher/exam/end/', views.teacherExamEnd),
    path('exam/student/block/', views.examBlockStudent),
    path('exam/student/unblock/', views.examUnblockStudent),
    path('teacher/exam/result/', views.teacherExamResult),
    path('logout/', views.logout),
    path('', views.home),
]
