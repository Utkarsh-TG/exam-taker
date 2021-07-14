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

def teacherDashboard(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
        return render(request, 'teacherDashboard.html', {'username':currentUser, 'FIREBASE_CONFIG':dumps(config)})
    
    return redirect(login)

def examCreate(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']
        title = request.POST['title']
        time = request.POST['time']
        description = request.POST['description']
        file_URL = request.POST.get('file')
        date = request.POST['date']

        #return error if title is empty
        if len(title) < 1:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Enter a title!','error-display':'flex'})

        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'false', 'ended':'false'}

        #ref database/Assignments/class/title
        db.child("Assignments").child(currentClass).child(title).set(assignmentData)

        return HttpResponse('')
    
    return redirect(teacherDashboard)

def examUpdate(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    
    if request.method == 'POST':
        currentClass = request.POST['class']
        title = request.POST['assignment_title']

        #return error if title is empty
        if len(title) < 1 or currentClass not in validateList[0]:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Information!','error-display':'flex'})

        #ref database/Assignments/class/title
        assignmentData = db.child("Assignments").child(currentClass).child(title).get()
        sendData = []
        
        if assignmentData is not None:
            for data in assignmentData.each():
                sendData.append(data.val())

        print(sendData)
        
        return JsonResponse({'assignmentData':sendData})
    
    return redirect(teacherDashboard)

def examUpdateFile(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']
        oldtitle = request.POST['old_title']
        title = request.POST['title']
        time = request.POST['time']
        description = request.POST['description']
        file_URL = request.POST.get('fileURL')
        date = request.POST['date']

        if len(title) < 1 or currentClass not in validateList[0]:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Details!','error-display':'flex'})
        
        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'false', 'ended':'false'}

        #ref database/Assignments/class/title
        db.child("Assignments").child(currentClass).child(oldtitle).remove()
        db.child("Assignments").child(currentClass).child(title).update(assignmentData)

        return redirect(teacherDashboard)

    return redirect(teacherDashboard)

def teacherExamRequest(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']

        if currentClass not in validateList[0]:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Class!','error-display':'flex'})
        
        #ref database/Assignments/class
        assignments = db.child('Assignments').child(currentClass).get()
        assignments_data = []

        if assignments.val() is not None:
            for assignment in assignments.each():
                assignments_data.append(assignment.val())

        return JsonResponse({'assignment_list': assignments_data})

    return redirect(teacherDashboard)

def teacherExamStart(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']
        title = request.POST['title']
        time = request.POST['time']
        description = request.POST['description']
        file_URL = request.POST.get('fileURL')
        date = request.POST['date']

        if len(title) < 1 or currentClass not in validateList[0]:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Details!','error-display':'flex'})

        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'true', 'ended':'false'}

        #ref database/Assignments/class/title
        db.child("Assignments").child(currentClass).child(title).update(assignmentData)
        return HttpResponse('')

    return redirect(teacherDashboard)

def teacherExamEnd(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']
        title = request.POST['title']
        time = request.POST['time']
        description = request.POST['description']
        file_URL = request.POST.get('fileURL')
        date = request.POST['date']

        if len(title) < 1 or currentClass not in validateList[0]:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Details!','error-display':'flex'})

        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'true', 'ended':'true'}

        #ref database/Assignments/class/title
        db.child("Assignments").child(currentClass).child(title).update(assignmentData)

        db.child('Chat').child(currentClass).child(title).remove()
        db.child('TurnedIn').child(currentClass).child(title).remove()
        db.child('Warnings').child(currentClass).child(title).remove()

        return HttpResponse('')

    return redirect(teacherDashboard)

def examBlockStudent(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    
    if request.method == 'POST':
        username = request.POST['user']
        _class = request.POST['class']
        _section = request.POST['section']
        assignmentName = request.POST['assignment']
        time = request.POST['time']
        
        data = {'blocked':True}

        #ref database/Login/student/class/section/username
        db.child('Login').child('student').child(_class).child(_section).child(username).update(data)

        userData = db.child('Login').child('student').child(_class).child(_section).child(username).get().val()
        
        unbanData = {'error':'banned', 'id':username, 'name':userData['username']}

        #ref database/Warnings/title/section/time
        db.child('Warnings').child(_class).child(assignmentName).child(_section).child(time).set(unbanData)
        
        return HttpResponse('')

    return redirect(teacherDashboard)

def examUnblockStudent(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    
    if request.method == 'POST':
        username = request.POST['user']
        _class = request.POST['class']
        _section = request.POST['section']
        assignmentName = request.POST['assignment']
        time = request.POST['time']
        
        data = {'blocked':False}

        #ref database/Login/student/class/section/username
        userData = db.child('Login').child('student').child(_class).child(_section).child(username).get().val()

        if userData is not None:
            db.child('Login').child('student').child(_class).child(_section).child(username).update(data)
        
        unbanData = {'error':'unbanned', 'id':username, 'name':userData['username']}

        #ref database/Warnings/title/section/time
        db.child('Warnings').child(_class).child(assignmentName).child(_section).child(time).set(unbanData)

        return HttpResponse('')

    return redirect(teacherDashboard)