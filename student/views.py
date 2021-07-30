import json
from json import dumps
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from django.conf import settings
import pyrebase
from main.models import *
from main import views as mainViews

#firebase config
config = settings.FIREBASE_CONFIG

firebase = pyrebase.initialize_app(config)

#initializing firebase database
db=firebase.database()

# Get a reference to the auth service
auth = firebase.auth()

student_mail = settings.STUDENT_MAIL
student_password = settings.STUDENT_PASSWORD

user = auth.sign_in_with_email_and_password(student_mail, student_password)

#validate class and section
validateList = [['12','11','10','9','8','7','6','5','4','3','2','1'],['A','B','C','D','E','F','G','H','I','J','K']]

def authData(request):
    if request.method == 'POST':
        data = {'mail':student_mail, 'password':student_password, 'firebase_config':dumps(config)}
        return JsonResponse(data)
        
def studentDashboard(request):
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'student':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    #request class
    if 'class' in request.COOKIES:
        currentClass = request.COOKIES.get('class')
    #request section
    if 'section' in request.COOKIES:
        currentSection = request.COOKIES.get('section')

    return render(request, 'studentDashboard.html', {'username':currentUser, 'class':currentClass, 'section':currentSection, 'user_token':dumps(user)})

def studentGetExam(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'student':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    
    if  request.method == 'POST':
        _class = request.POST['class']
        title = request.POST['title']

        data = db.child('Assignments').child(_class).child(title).get(user['idToken']).val()

        return JsonResponse({'assignmentData':data})

    return redirect(studentDashboard)
    
def studentExamSubmit(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'student':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if  request.method == 'POST':
        _username = request.POST['user']
        _class = request.POST['class']
        _section = request.POST['section']
        _time = request.POST['time']
        _answers = request.POST['textanswer']
        _file = request.POST.get('file', False)
        _title = request.POST['title']

        if _class not in validateList[0] or _section not in validateList[1]:
            return HttpResponse('')
        
        #getting user data
        userData = db.child('Login').child('Student').child(_class).child(_section).child(_username).get(user['idToken']).val()

        data = {'username':_username, 'answers':_answers, 'files':_file, 'time':_time, 'name':userData['username']}

        db.child('Answers').child(_class).child(_title).child(_section).child(_username).update(data, user['idToken'])

        return HttpResponse('')
    
    return redirect(studentDashboard)

def studentExamWarn(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'student':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        _user = currentUser or request.POST['user']
        _class = request.POST['class']
        _section = request.POST['section']
        _time = request.POST['time']
        _assignment = request.POST['assignment']
        
        #getting user data
        userData = db.child('Login').child('Student').child(_class).child(_section).child(_user).get(user['idToken']).val()

        banData = {'error':'warned', 'id':_user, 'name':userData['username']}

        if not userData['blocked']:
            #ref database/Warnings/class/assignment/section/time
            db.child('Warnings').child(_class).child(_assignment).child(_section).child(_time).set(banData, user['idToken'])
        
        return HttpResponse('')

    return redirect(studentDashboard)

def studentExamBlock(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'student':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    
    if request.method == 'POST':
        _user = currentUser or request.POST['user']
        _class = request.POST['class']
        _section = request.POST['section']
        _time = request.POST['time']
        _assignment = request.POST['assignment']

        #getting user data
        userData = db.child('Login').child('Student').child(_class).child(_section).child(_user).get(user['idToken']).val()

        data = {'blocked':True}

        banData = {'error':'banned', 'id':_user, 'name':userData['username']}

        if not userData['blocked']:
            #ref database/Login/student/class/section/username
            db.child('Login').child('Student').child(_class).child(_section).child(_user).update(data, user['idToken'])

            #ref database/Warnings/class/assignment/section/time
            db.child('Warnings').child(_class).child(_assignment).child(_section).child(_time).set(banData, user['idToken'])
        
        return HttpResponse('')
        
    return redirect(studentDashboard)

def studentExamAttendee(request):
    user = auth.sign_in_with_email_and_password(student_mail, student_password)
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'student':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    
    if request.method == 'POST':
        _user = currentUser or request.POST['user']
        _class = request.POST['class']
        _section = request.POST['section']
        _time = request.POST['time']
        _assignment = request.POST['assignment']

        userData = db.child('Login').child('Student').child(_class).child(_section).child(_user).get(user['idToken']).val()

        data = {'id':_user, 'username':userData['username']}

        db.child('TurnedIn').child(_class).child(_assignment).child(_section).child(_time).set(data, user['idToken'])

        return HttpResponse('')

    return redirect(studentDashboard)