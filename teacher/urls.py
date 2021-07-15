from django.urls import path
from teacher import views

urlpatterns = [
    path('dashboard/', views.teacherDashboard),
    path('exam_create/', views.examCreate),
    path('exam_update/', views.examUpdate),
    path('exam_update_file/', views.examUpdateFile),
    path('exam_request/', views.teacherExamRequest),
    path('exam_assign/', views.teacherExamStart),
    path('exam_end/', views.teacherExamEnd),
    path('student_block/', views.examBlockStudent),
    path('student_unblock/', views.examUnblockStudent),
    path('exam_result/', views.teacherExamResult),
    path('exam_results_return/', views.teacherExamResultReturn),
]
