from django.urls import path
from main import views

urlpatterns = [
    path('ignition/', views.ignition),
    path('signup/', views.signup),
    path('login/', views.login),
    path('forgot_password/', views.forgotPassword),
    path('password_verification/', views.sendVerification),
    path('verify_code/', views.verifyCode),
    path('reset_password/', views.resetPassword),
    path('student_signup/', views.studentSignup),
    path('user_login/', views.userLogin),
    path('chat_message/', views.examChatMessage),
    path('logout/', views.logout),
    path('', views.home),
]
