from django.urls import path
from teacher import views

urlpatterns = [
    path('dashboard/', views.teacherDashboard),
    path('exam/create/', views.examCreate),
    path('exam/update/', views.examUpdate),
    path('exam/update/file/', views.examUpdateFile),
    path('exam/request/', views.teacherExamRequest),
    path('exam/assign/', views.teacherExamStart),
    path('exam/end/', views.teacherExamEnd),
    path('student/block/', views.examBlockStudent),
    path('student/unblock/', views.examUnblockStudent),
    path('exam/result/', views.teacherExamResult),
    path('exam/results/return/', views.teacherExamResultReturn),
]
