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
from .forms import DocumentForm
from teacher import views as teacherViews
from student import views as studentViews

#firebase config
config = settings.FIREBASE_CONFIG

firebase = pyrebase.initialize_app(config)

#initializing firebase database
db=firebase.database()

#initializing firebase storage
storage = firebase.storage()

#validate class and section
validateList = [['12','11','10','9','8','7','6','5','4','3','2','1'],['A','B','C','D','E','F','G','H','I','J','K']]

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

        #db reference
        data = {'blocked':False, 'id':uid, 'username':username, 'class':_class, 'section':_section, 'password':password}

        if _class in validateList[0] and _section in validateList[1]:
            db.child('Login').child('student').child(_class).child(_section).child(uid).set(data)
            return redirect(login)

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

def teacherLogin(request):
    #and request.POST.get('') == 'teacher'
    if request.method == 'POST':
        teacherUsername = request.POST.get('teacher-username')
        teacherPassword = request.POST.get('teacher-password')

        if len(teacherUsername) < 3 or len(teacherPassword) < 8:
            return render(request, 'login.html', {'error':'Login Failed! Ivalid Details', 'displayError':'flex'})

        #ref database/Login/Teacher
        loginDdata = db.child('Login').child('Teacher').get()
        teacherData = []

        if loginDdata.val() is not None:
            for data in loginDdata.each():
                teacherData.append(data.val())

        for i in range(len(teacherData)):
            if teacherUsername == teacherData[i]['username']:
                if teacherPassword == teacherData[i]['password']:
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

    return redirect(login)

def studentLogin(request):
    if request.method == 'POST':
        studentUsername = request.POST.get('student-username')
        studentPassword = request.POST.get('student-password')
        studentClass = request.POST.get('student-class')
        studentSection = request.POST.get('student-section')
        
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
                    if dataList[i]['password'] == studentPassword:
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