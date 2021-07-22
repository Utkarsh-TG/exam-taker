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

#validate class and section
validateList = [['12','11','10','9','8','7','6','5','4','3','2','1'],['A','B','C','D','E','F','G','H','I','J','K']]

def teacherDashboard(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
        return render(request, 'teacherDashboard.html', {'username':currentUser, 'FIREBASE_CONFIG':dumps(config)})
    
    return redirect(mainViews.login)

def examCreate(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        _type = request.POST['type']
        currentClass = request.POST['class']
        title = request.POST['title']
        time = request.POST['time']
        description = request.POST['description']
        questions = request.POST['file']
        date = request.POST['date']
        windowCheat = request.POST['windowCheat']
        if(_type == 'mcq'):
            questionCheat = request.POST['questionCheat']
        #return error if title is empty
        if(windowCheat == 'true'):
            windowCheat = True
        if(windowCheat == 'false'):
            windowCheat = False

        try:
            questionCheat
        except NameError:
            questionCheat = None
        else:
            if(questionCheat == 'true'):
                questionCheat = True
            if(questionCheat == 'false'):
                questionCheat = False
        
        if len(title) < 1:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Enter a title!','error-display':'flex'})
        
        if(_type == 'long'):
            assignmentData = {'title':title, 'time':time, 'description':description, 'file':questions, 'date':date, 'type':_type, 'windowCheat': windowCheat}
        elif(_type == 'mcq'):
            assignmentData = {'title':title, 'time':time, 'description':description, 'file':json.loads(questions), 'date':date, 'type':_type, 'windowCheat': windowCheat, 'questionCheat':questionCheat}

        #ref database/Assignments/class/title
        db.child("Assignments").child(currentClass).child(title).set(assignmentData)

        return HttpResponse('')
    
    return redirect(teacherDashboard)

def examUpdateFile(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        _type = request.POST['type']
        currentClass = request.POST['class']
        oldtitle = request.POST['old_title']
        title = request.POST['title']
        time = request.POST['time']
        description = request.POST['description']
        questions = request.POST['file']
        date = request.POST['date']
        windowCheat = request.POST['windowCheat']
        if(_type == 'mcq'):
            questionCheat = request.POST['questionCheat']

        if(windowCheat == 'true'):
            windowCheat = True
        if(windowCheat == 'false'):
            windowCheat = False

        try:
            questionCheat
        except NameError:
            questionCheat = None
        else:
            if(questionCheat == 'true'):
                questionCheat = True
            if(questionCheat == 'false'):
                questionCheat = False

        if len(title) < 1 or currentClass not in validateList[0]:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Details!','error-display':'flex'})
        
        if(_type == 'long'):
            assignmentData = {'title':title, 'time':time, 'description':description, 'file':questions, 'date':date, 'type':_type, 'windowCheat': windowCheat}
        if(_type == 'mcq'):
            assignmentData = {'title':title, 'time':time, 'description':description, 'file':json.loads(questions), 'date':date, 'type':_type, 'windowCheat': windowCheat, 'questionCheat':questionCheat}

        #ref database/Assignments/class/title
        db.child("Assignments").child(currentClass).child(oldtitle).remove()
        db.child("Assignments").child(currentClass).child(title).update(assignmentData)

        return redirect(teacherDashboard)

    return redirect(teacherDashboard)

def teacherExamRequest(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(mainViews.login)
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
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']
        title = request.POST['title']
        section = request.POST['section']
        time = request.POST['date']

        sectionList = section.split (",")

        if len(title) < 1 or currentClass not in validateList[0]:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Details!','error-display':'flex'})

        assignmentData = {'assigned':True, 'ended':False, 'title':title, 'sections':section, 'class':currentClass, 'time':time}

        #ref database/Assignments/class/title
        for i in range(0,len(sectionList)):
            db.child("Assigned").child(currentClass).child(sectionList[i]).child(title).update(assignmentData)

        return HttpResponse('')

    return redirect(teacherDashboard)

def teacherExamEnd(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']
        title = request.POST['title']
        section = request.POST['section']
        time = request.POST['date']

        sectionList = section.split (",")

        if len(title) < 1 or currentClass not in validateList[0]:
            return HttpResponse('')
        
        assignmentData = {'assigned':True, 'ended':True, 'title':title, 'sections':section, 'class':currentClass, 'time':time}

        #ref database/Assignments/class/title
        for i in range(0,len(sectionList)):
            db.child("Assigned").child(currentClass).child(sectionList[i]).child(title).update(assignmentData)

        db.child('Chat').child(currentClass).child(title).remove()
        db.child('TurnedIn').child(currentClass).child(title).remove()
        db.child('Warnings').child(currentClass).child(title).remove()

        return HttpResponse('')

    return redirect(teacherDashboard)

def examBlockStudent(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(mainViews.login)
    
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
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(mainViews.login)
    
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

def teacherExamResult(request):
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(mainViews.login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    
    if request.method == 'POST':
        _class = request.POST['class']
        _title = request.POST['assignment']

        if _class not in validateList[0]:
            return HttpResponse('')

        data = db.child('Answers').child(_class).child(_title).get().val()

        return JsonResponse({'resultData':data})
    
    return redirect(teacherDashboard)

def teacherExamResultReturn(request):
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        return redirect(mainViews.login)
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(mainViews.login)

    if request.method == 'POST':
        _class = request.POST['_class']
        _section = request.POST['section']
        _title = request.POST['title']
        _id = request.POST['id']
        _marks = request.POST['marks']
        _desc = request.POST['note']
        _date = request.POST['date']

        if _class not in validateList[0] or _section not in validateList[1]:
            return HttpResponse('')

        data = {'class':_class, 'section':_section, 'title':_title, 'id':_id, 'marks':_marks, 'note':_desc, 'date':_date}

        db.child('Returns').child(_class).child(_section).child(_id).child(_title).set(data)

        return HttpResponse('')

    return redirect(teacherDashboard)