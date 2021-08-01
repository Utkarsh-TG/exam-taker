from logging import log
import os
import json
import random
from json import dumps
from random import randint
from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.conf import settings
import pyrebase
import hashlib, binascii
from cryptography.fernet import Fernet
from requests.api import request
from main.models import *
from teacher import views as teacherViews
from student import views as studentViews

#firebase config
config = settings.FIREBASE_CONFIG

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Get a reference to the database service
db = firebase.database()

#auth config
#student
student_mail = settings.STUDENT_MAIL
student_password = settings.STUDENT_PASSWORD
#teacher
teacher_mail = settings.TEACHER_MAIL
teacher_password = settings.TEACHER_PASSWORD

#validate class and section
validateList = [['12','11','10','9','8','7','6','5','4','3','2','1'],['A','B','C','D','E','F','G','H','I','J','K']]

user = auth.sign_in_with_email_and_password(student_mail, student_password)

def ignition(request):
    return JsonResponse({'test':'run successful'}, status=200)

def home(request):
    #check if already logged in
    return render(request, 'index.html')

def signup(request):
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') == 'teacher':
            return redirect(teacherViews.teacherDashboard)
        elif request.COOKIES.get('loggedIn') == 'student':
            return redirect(studentViews.studentDashboard)
    
    return render(request, 'signup.html')

def studentSignup(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    if request.method == 'POST':
        uid = request.POST.get('uid')
        username = request.POST.get('name')
        _section = (request.POST.get('section')).upper()
        password = request.POST.get('password')
        _class = "10"

        if _class in validateList[0] and _section in validateList[1]:
            response = redirect(login)

            encPassword = hash_password(password)

            data = {'blocked':False, 'id':uid, 'username':username, 'class':_class, 'section':_section, 'password':str(encPassword)}

            db.child('Login').child('Student').child(_class).child(_section).child(uid).set(data, user['idToken'])
            
            return response

    return redirect(signup)    

def login(request):
    #check if already logged in
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') == 'teacher':
            return redirect(teacherViews.teacherDashboard)
        elif request.COOKIES.get('loggedIn') == 'student':
            return redirect(studentViews.studentDashboard)

    #render login page
    return render(request, 'login.html')

def logout(request):
    if 'loggedIn' in request.COOKIES:
        response = redirect(login)

        if request.COOKIES.get('loggedIn') == 'teacher':
            if 'uid' in request.COOKIES:
                response.delete_cookie('uid') #remove user id from cookie
            if 'loggedIn' in request.COOKIES:
                response.delete_cookie('loggedIn') #remove loggedin from cookie

        elif request.COOKIES.get('loggedIn') == 'student':
            if 'uid' in request.COOKIES:
                response.delete_cookie('uid') #remove userid from cookie
            if 'loggedIn' in request.COOKIES:
                response.delete_cookie('loggedIn') #remove loggedin from cookie
            if 'class' in request.COOKIES:
                response.delete_cookie('class') #remove class from cookie
            if 'section' in request.COOKIES:
                response.delete_cookie('section') #remove section from cookie
        
        return response

    return redirect(login)

def userLogin(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    if request.method == 'POST' and request.POST.get('login-for') == 'teacher':
        teacherUsername = request.POST.get('teacher-username')
        teacherPassword = request.POST.get('teacher-password')

        if(teacherPassword == "abc12345"):
            #ask to change default
            return redirect(forgotPassword)

        if len(teacherUsername) < 3:
            return render(request, 'login.html', {'error':'Login Failed! Ivalid Details', 'displayError':'flex'})

        #ref database/Login/Teacher
        loginDdata = db.child('Login').child('Teacher').get(user['idToken'])
        teacherData = []

        if loginDdata.val() is not None:
            for data in loginDdata.each():
                teacherData.append(data.val())

        for i in range(len(teacherData)):
            if teacherUsername == teacherData[i]['username']:
                if verify_password(teacherData[i]['password'], teacherPassword):
                    response = redirect(teacherViews.teacherDashboard)
                    #save credentials to cookies
                    response.set_cookie('loggedIn', 'teacher', max_age=60*60*60*60*60)
                    response.set_cookie('uid', teacherUsername, max_age=60*60*60*60*60)
                    #render dashboard
                    return response
                else:
                    #return password error
                    response = render(request, 'login.html', {'error':'Login Failed! Invalid Password', 'error-display':'flex'})
                    return response

    elif request.method == 'POST' and request.POST.get('login-for') == 'student':
        studentUsername = request.POST.get('student-username')
        studentPassword = request.POST.get('student-password')
        studentClass = request.POST.get('student-class')
        studentSection = (request.POST.get('student-section')).upper()

        #validate class & section
        if studentClass not in validateList[0]:
            return render(request, 'login.html', {'error':'Login Failed! Ivalid Class'})

        if studentSection not in validateList[1]:
            return render(request, 'login.html', {'error':'Login Failed! Ivalid Section'})

        if(studentPassword == 'abc12345'):
            #request password change
            return redirect(forgotPassword)

        #ref database/Login/student/class/section
        loginDdata = db.child('Login').child('Student').child(studentClass).child(studentSection).get(user['idToken'])
        dataList = []
        
        if loginDdata.val() is not None:
            for data in loginDdata.each():
                dataList.append(data.val())
        
        if len(dataList) > 0:
            for i in range(len(dataList)):
                if str(dataList[i]['id']) == studentUsername:
                    if (verify_password(dataList[i]['password'], studentPassword)):
                        response = redirect(studentViews.studentDashboard)
                        #save student credentials to cookies
                        response.set_cookie('loggedIn', 'student', max_age=60*60*60*60*60)
                        response.set_cookie('uid', studentUsername, max_age=60*60*60*60*60)
                        response.set_cookie('class', studentClass, max_age=60*60*60*60*60)
                        response.set_cookie('section', studentSection, max_age=60*60*60*60*60)
                        return response
                    else:
                        #return invalid password
                        return render(request, 'login.html', {'error':'Login Failed! Invalid Password', 'error-display':'flex'})
            else:
                #invalid details (data not exist)
                return render(request, 'login.html', {'error':'Login Failed! Invalid Details', 'error-display':'flex'})
        
    return redirect(login)

def examChatMessage(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(login)

    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        message = request.POST['message']
        assignment = request.POST['assignment']
        section = request.POST['section']
        time = request.POST['time']
        _class = request.POST['class']

        if section not in validateList[1]:
            return HttpResponse('')

        chatData = {'name':currentUser, 'message':message}

        #ref database/assignment/section/time
        db.child('Chat').child(_class).child(assignment).child(section).child(time).set(chatData, user['idToken'])

        return HttpResponse('')

def forgotPassword(request):
    if 'loggedIn' in request.COOKIES:
        return redirect(login)

    return render(request, 'forgotPass.html', {'display':'none'})

def sendVerification(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    if request.method == 'POST' and request.POST.get('user') == 'student':
        id = request.POST.get('userid')
        _class = request.POST.get('class')
        section = (request.POST.get('section')).upper()

        if _class not in validateList[0] or section not in validateList[1]:
            return render(request, 'forgotPass.html', {'error':'Invalid class or section!','display':'flex'})
        data = db.child('Login').child('Student').child(_class).child(section).child(id).get(user['idToken']).val()

        if data is not None:
            response = render(request, 'verification.html')

            response.set_cookie('logged', 'student', max_age=60*5)
            response.set_cookie('uid', id, max_age=60*5)
            response.set_cookie('class', _class, max_age=60*5)
            response.set_cookie('section', section, max_age=60*5)
            response.set_cookie('mail', data['email'], max_age=60*5)
            
            generateVerification(data['email'], 'student', id, _class, section)

            return response
        else:
            return render(request, 'forgotPass.html', {'error':'Invalid information!','display':'flex'})
    elif request.method == 'POST' and request.POST.get('user') == 'teacher':
        id = request.POST.get('userid')

        data = db.child('Login').child('Teacher').child(id).get(user['idToken']).val()

        if data is not None:
            response = render(request, 'verification.html')

            response.set_cookie('uid', id, max_age=60*5)
            response.set_cookie('logged', 'teacher', max_age=60*5)
            response.set_cookie('mail', data['email'], max_age=60*5)

            generateVerification(data['email'], 'teacher', id, None, None)

            return response

    return redirect(login)

def verifyCode(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    if request.method == 'POST':
        entered_verification_code = request.POST.get('verificationcode')

        if 'logged' in request.COOKIES:
            loggedAs = request.COOKIES.get('logged')
        
        if loggedAs == 'teacher':
            if 'uid' in request.COOKIES:
                uid = request.COOKIES.get('uid')
            if 'mail' in request.COOKIES:
                _mail = request.COOKIES.get('mail')
            verification_code = db.child('Login').child('Teacher').child(uid).get(user['idToken']).val()
        elif loggedAs == 'student':
            if 'uid' in request.COOKIES:
                uid = request.COOKIES.get('uid')
            if 'class' in request.COOKIES:
                _class = request.COOKIES.get('class')
            if 'section' in request.COOKIES:
                _section = request.COOKIES.get('section')
            if 'mail' in request.COOKIES:
                _mail = request.COOKIES.get('mail')
        
            verification_code = db.child('Login').child('Student').child(_class).child(_section).child(uid).get(user['idToken']).val()
        
        if(entered_verification_code == verification_code['verification']):
            #return change password page
            return render(request, 'resetPassword.html', {'userid':uid, 'usermail':_mail, 'display':'none'})
        else:
            return JsonResponse({'error':''})

    return redirect(login)

def resetPassword(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    if 'loggedIn' in request.COOKIES:
        return redirect(login)

    if request.method == 'POST':
        if 'logged' in request.COOKIES:
            loggedAs = request.COOKIES.get('logged')

            if loggedAs == 'student':
                password = request.POST.get('password')
                repassword = request.POST.get('re-password')

                if password != repassword:
                    return redirect(login)

                if 'uid' in request.COOKIES:
                    uid = request.COOKIES.get('uid')
                if 'class' in request.COOKIES:
                    _class = request.COOKIES.get('class')
                if 'section' in request.COOKIES:
                    _section = request.COOKIES.get('section')
                if 'mail' in request.COOKIES:
                        _mail = request.COOKIES.get('mail')

                if _class in validateList[0] and _section in validateList[1]:
                    response = redirect(login)

                    encPassword = hash_password(password)

                    data = {'password':str(encPassword)}
                
                    db.child('Login').child('Student').child(_class).child(_section).child(uid).update(data, user['idToken'])
                    
                    return response
            
            elif loggedAs == 'teacher':
                response = redirect(login)
                password = request.POST.get('password')
                repassword = request.POST.get('re-password')
                if 'uid' in request.COOKIES:
                    uid = request.COOKIES.get('uid')

                response = redirect(login)

                if password != repassword:
                    return response

                encPassword = hash_password(password)

                data = {'password':str(encPassword)}

                db.child('Login').child('Teacher').child(uid).update(data, user['idToken'])

                return response

    return redirect(login)

#custom
def generateVerification(email, logged, _user, _class, section):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    if(checkEmail(email)):
        verification_code = str(randint(100000, 999999))
        if logged:
            if logged == 'teacher':
                if _user:
                    data = {'verification':verification_code}
                    db.child('Login').child('Teacher').child(_user).update(data, user['idToken'])
                    m_subject = "Password Change Request on ExamTaker"
                    m_message = ""
                    m_sender = settings.EMAIL_HOST_USER
                    m_recievers = email
                    msg = EmailMultiAlternatives(m_subject, m_message, m_sender, [m_recievers])
                    html_content = "<div style='background: #bcf79e; padding: 15px; border-radius:12px;'><h3>You have applied for password change on ExamTaker.</h3><br><p>Your verification code for <strong>"+ email+ "</strong> is <strong>"+ verification_code+ "</strong>, use this code to verify your email. Ignore if you didn't applied.</p><br> Thanks & Regards <br> Team ExamTaker</div>"
                    msg.attach_alternative(html_content, "text/html") 
                    msg.send()
                    return True
            elif logged == 'student':
                if _user:
                    data = {'verification':verification_code}
                    db.child('Login').child('Student').child(_class).child(section).child(_user).update(data, user['idToken'])
                    m_subject = "Password Change Request on ExamTaker"
                    m_message = ""
                    m_sender = settings.EMAIL_HOST_USER
                    m_recievers = email
                    msg = EmailMultiAlternatives(m_subject, m_message, m_sender, [m_recievers])
                    html_content = "<div style='background: #bcf79e; padding: 15px; border-radius:12px;'><h3>You have applied for password change on ExamTaker.</h3><br><p>Your verification code for <strong>"+ email+ "</strong> is <strong>"+ verification_code+ "</strong>, use this code to verify your email. Ignore if you didn't applied.</p><br> Thanks & Regards <br> Team ExamTaker</div>"
                    msg.attach_alternative(html_content, "text/html") 
                    msg.send()
                    return True
    return(False)

def checkEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password