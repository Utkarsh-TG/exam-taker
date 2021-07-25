import os
import json
import random
from json import dumps
from random import randint
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.conf import settings
import pyrebase
from cryptography.fernet import Fernet
from main.models import *
from teacher import views as teacherViews
from student import views as studentViews

#firebase config
config = settings.FIREBASE_CONFIG

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

SERVICE_KEY_DIR = os.path.join(SETTINGS_PATH, 'Exam', "service_account_email_key.json")

with open(SERVICE_KEY_DIR, "r") as f:
    service_account_email = json.loads(f.read())
    print(service_account_email)

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Get a reference to the database service
db = firebase.database()

#validate class and section
validateList = [['12','11','10','9','8','7','6','5','4','3','2','1'],['A','B','C','D','E','F','G','H','I','J','K']]
verification_code = 1
c_user = {}

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
    if request.method == 'POST':
        uid = request.POST.get('uid')
        username = request.POST.get('name')
        _section = (request.POST.get('section')).upper()
        password = request.POST.get('password')
        _class = "10"

        if _class in validateList[0] and _section in validateList[1]:
            response = redirect(login)

            key = Fernet.generate_key()
            fernet = Fernet(key)

            encPassword = fernet.encrypt(password.encode())

            response.set_cookie('encryption', key.decode("UTF-8"), max_age=60*60*60*60*100)

            data = {'blocked':False, 'id':uid, 'username':username, 'class':_class, 'section':_section, 'password':str(encPassword.decode("UTF-8"))}
        
            db.child('Login').child('student').child(_class).child(_section).child(uid).set(data)
            
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
    if request.method == 'POST' and request.POST.get('login-for') == 'teacher':
        teacherUsername = request.POST.get('teacher-username')
        teacherPassword = request.POST.get('teacher-password')

        #if(teacherPassword == "abc12345"):
            #ask to change default
            #return

        if len(teacherUsername) < 3 or len(teacherPassword) < 8:
            return render(request, 'login.html', {'error':'Login Failed! Ivalid Details', 'displayError':'flex'})

        #ref database/Login/Teacher
        loginDdata = db.child('Login').child('Teacher').get()
        teacherData = []

        if loginDdata.val() is not None:
            for data in loginDdata.each():
                teacherData.append(data.val())

        if 'encryption' in request.COOKIES:
            key = request.COOKIES.get('encryption')
            fernet = Fernet(key.encode("UTF-8"))

        for i in range(len(teacherData)):
            if teacherUsername == teacherData[i]['username']:
                decPassword = teacherData[i]['password'].encode("UTF-8")
                decPassword = fernet.decrypt(decPassword).decode()
                if teacherPassword == decPassword:
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
        
        token = auth.create_custom_token(studentUsername)

        if 'encryption' in request.COOKIES:
            key = request.COOKIES.get('encryption')
            fernet = Fernet(key.encode("UTF-8"))

        #validate class & section
        if studentClass not in validateList[0]:
            return render(request, 'login.html', {'error':'Login Failed! Ivalid Class'})

        if studentSection not in validateList[1]:
            return render(request, 'login.html', {'error':'Login Failed! Ivalid Section'})

        #ref database/Login/student/class/section
        loginDdata = db.child('Login').child('student').child(studentClass).child(studentSection).get()
        dataList = []
        
        if loginDdata.val() is not None:
            for data in loginDdata.each():
                dataList.append(data.val())
        
        if len(dataList) > 0:
            for i in range(len(dataList)):
                if str(dataList[i]['id']) == studentUsername:
                    decPassword = dataList[i]['password'].encode("UTF-8")
                    decPassword = fernet.decrypt(decPassword).decode()
                    if decPassword == studentPassword:
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
        db.child('Chat').child(_class).child(assignment).child(section).child(time).set(chatData)

        return HttpResponse('')

def forgotPassword(request):
    if 'loggedIn' in request.COOKIES:
        return redirect(login)

    return render()

def sendVerification(request):
    global c_user
    if request.method == 'POST' and request.POST.get('user') == 'student':
        id = request.POST.get('userid')
        _class = request.POST.get('class')
        section = request.POST.get('section')

        data = db.child('Login').child('student').child(_class).child(section).child(id).get().val()
        
        c_user = {'logged':'student', 'class':_class, 'section':section, 'userid':id}

        if data is not None:
            generateVerification(data['email'])

            return render()
    elif request.method == 'POST' and request.POST.get('user') == 'teacher':
        id = request.POST.get('userid')

        data = db.child('Login').child('Teacher').child(id).get().val()
        
        c_user = {'logged':'teacher', 'userid':id}

        if data is not None:
            generateVerification(data['email'])

            return render()

    return redirect(login)

def verifyCode(request):
    global verification_code

    if request.method == 'POST':
        entered_verification_code = request.POST.get('verificationcode')
        if(entered_verification_code == verification_code):
            #return change password page
            return render()
        else:
            return JsonResponse({'error':''})

    return redirect(login)

def resetPassword(request):
    if 'loggedIn' in request.COOKIES:
        return redirect(login)

    global c_user

    if request.method == 'POST' and c_user['user'] == 'student':
        password = request.POST.get('password')
        _class = c_user['class']
        _section = c_user['section']
        uid = c_user['userid']

        if _class in validateList[0] and _section in validateList[1]:
            response = redirect(login)

            key = Fernet.generate_key()
            fernet = Fernet(key)

            encPassword = fernet.encrypt(password.encode())

            response.set_cookie('encryption', key.decode("UTF-8"), max_age=60*60*60*60*100)

            data = {'password':str(encPassword.decode("UTF-8"))}
        
            db.child('Login').child('student').child(_class).child(_section).child(uid).update(data)
            
            return response
    elif request.method == 'POST' and c_user['user'] == 'teacher':
        password = request.POST.get('password')
        uid = c_user['userid']

        response = redirect(login)

        key = Fernet.generate_key()
        fernet = Fernet(key)

        encPassword = fernet.encrypt(password.encode())

        response.set_cookie('encryption', key.decode("UTF-8"), max_age=60*60*60*60*100)

        data = {'password':str(encPassword.decode("UTF-8"))}

        db.child('Login').child('Teacher').child(uid).update(data)

    return redirect(login)

#custom
def generateVerification(email):
    global verification_code

    if(checkEmail(email)):
        verification_code = str(randint(100000, 999999))
        m_subject = "Password Change Request on ExamTaker"
        m_message = ""
        m_sender = settings.EMAIL_HOST_USER
        m_recievers = [email,]
        msg = EmailMultiAlternatives(m_subject, m_message, m_sender, [m_recievers])
        html_content = "<h3>You have applied for password change on ExamTaker.</h3><br><p>Your verification code for <strong>"+ email+ "</strong> is <strong>"+ verification_code+ "<strong>, use this code to verify your email. Ignore if you didn't applied.</p><br> Thanks & Regards <br> Team ExamTaker"
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
            return(True)
        except:
            return(False)
    
    return(False)

def checkEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
