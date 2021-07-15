from django.urls import path
from main import views

urlpatterns = [
    path('ignition/', views.ignition),
    path('signup/', views.signup),
    path('login/', views.login),
    path('student/signup/', views.studentSignup),
    path('user/login/teacher/', views.teacherLogin),
    path('user/login/student/', views.studentLogin),
    path('logout/', views.logout),
    path('', views.home),
]
