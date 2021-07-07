from django.http import request
from django.http.response import JsonResponse
from main.models import *
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from .forms import DocumentForm
import pyrebase

#firebase config
config = {
    "apiKey": "AIzaSyD7ddl63JBC-Xxj2vKe99R5JJkxBJDvTVY",
    "authDomain": "exam-3d397.firebaseapp.com",
    "databaseURL": "https://exam-3d397-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "exam-3d397",
    "storageBucket": "exam-3d397.appspot.com",
    "messagingSenderId": "647787494671",
    "appId": "1:647787494671:web:6afa3e03b1184d113c127a",
    "measurementId": "G-2CTKYSPY7P"
}

firebase=pyrebase.initialize_app(config)

#initializing firebase database
db=firebase.database()

#initializing firebase storage
storage = firebase.storage()

#validate class and section
validateList = [['12','11','10','9','8','7','6','5','4','3','2','1'],['A','B','C','D','E','F','G','H','I','J','K']]

def home(request):
    #check if already logged in
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') == 'teacher':
            return redirect(teacherDashboard)
        elif request.COOKIES.get('loggedIn') == 'student':
            return redirect(studentDashboard)
    return render(request, 'index.html')

def login(request):
    #check if already logged in
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') == 'teacher':
            return redirect(teacherDashboard)
        elif request.COOKIES.get('loggedIn') == 'student':
            return redirect(studentDashboard)

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
                    response = redirect(teacherDashboard)
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
                        response = redirect(studentDashboard)
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

def teacherDashboard(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
        return render(request, 'teacherDashboard.html', {'username':currentUser})
    
    return redirect(login)

def examCreate(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
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

        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'false', 'ended':'false', 'result':[]}

        #ref database/Assignments/class/title
        db.child("Assignments").child(currentClass).child(title).set(assignmentData)

        return HttpResponse('')
    
    return redirect(teacherDashboard)

def examUpdate(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
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
        
        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'false', 'ended':'false', 'result':[]}
        
        #ref database/Assignments/class/title
        db.child("Assignments").child(currentClass).child(oldtitle).remove()
        db.child("Assignments").child(currentClass).child(title).update(assignmentData)

        return redirect(teacherDashboard)

    return redirect(teacherDashboard)

def teacherExamRequest(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
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

        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'true', 'ended':'false', 'result':[]}

        #ref database/Assignments/class/title
        db.child("Assignments").child(currentClass).child(title).update(assignmentData)
        return HttpResponse('')

    return redirect(teacherDashboard)

def teacherExamEnd(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
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

        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'true', 'ended':'true', 'result':[]}

        #ref database/Assignments/class/title
        db.child("Assignments").child(currentClass).child(title).update(assignmentData)
        return HttpResponse('')

    return redirect(teacherDashboard)

def teacherExamWindow(request):
    return render(request, 'login.html')

def examChatMessage(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    
    if request.method == 'POST':
        message = request.POST['message']
        assignment = request.POST['assignment']
        section = request.POST['section']
        time = request.POST['time']

        if section not in validateList[1]:
            return HttpResponse('')

        chatData = {'name':currentUser, 'message':message}

        #ref database/assignment/section/time
        db.child('Chat').child(assignment).child(section).child(time).set(chatData)

        return HttpResponse('')

    return redirect(teacherDashboard)

def examBlockStudent(request):
    #return if not logged in as teacher
    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    
    if request.method == 'POST':
        username = request.POST['user']
        _class = request.POST['class']
        _section = request.POST['section']
        assignmentName = request.POST['assignment']
        time = request.POST['time']
        
        data = {'blocked':'true'}

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
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    
    if request.method == 'POST':
        username = request.POST['user']
        _class = request.POST['class']
        _section = request.POST['section']
        assignmentName = request.POST['assignment']
        time = request.POST['time']
        
        data = {'blocked':'false'}

        #ref database/Login/student/class/section/username
        userData = db.child('Login').child('student').child(_class).child(_section).child(username).get().val()

        if userData is not None:
            db.child('Login').child('student').child(_class).child(_section).child(username).update(data)
        
        unbanData = {'error':'unbanned', 'id':username, 'name':userData['username']}

        #ref database/Warnings/title/section/time
        db.child('Warnings').child(_class).child(assignmentName).child(_section).child(time).set(unbanData)

        return HttpResponse('')

    return redirect(teacherDashboard)

def studentDashboard(request):
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'student':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    #request class
    if 'class' in request.COOKIES:
        currentClass = request.COOKIES.get('class')
    #request section
    if 'section' in request.COOKIES:
        currentSection = request.COOKIES.get('section')

    return render(request, 'studentDashboard.html', {'username':currentUser, 'class':currentClass, 'section':currentSection})

def studentExamSubmit(request):
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'student':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if  request.method == 'POST':
        _username = request.POST['user']
        _class = request.POST['class']
        _section = request.POST['section']
        _time = request.POST['time']
        _answers = request.POST['textanswer']
        _files = request.POST['files']
        _title = request.POST['title']

        if _class not in validateList[0] or _section not in validateList[1]:
            return HttpResponse('')
        
        data = {'username':_username, 'answers':_answers, 'files':_files.split(','), 'time':_time}

        db.child('Answers').child(_class).child(_title).child(_section).child(_username).update(data)

        return HttpResponse('')
    
    return redirect(studentDashboard)

def studentExamWarn(request):
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'student':
            return redirect(login)
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
        userData = db.child('Login').child('student').child(_class).child(_section).child(_user).get().val()

        banData = {'error':'warned', 'id':_user, 'name':userData['username']}

        #ref database/Warnings/class/assignment/section/time
        db.child('Warnings').child(_class).child(_assignment).child(_section).child(_time).set(banData)

    return redirect(studentDashboard)

def studentExamBlock(request):
    #return if not logged in as student
    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'student':
            return redirect(login)
    #request userid
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    
    if request.method == 'POST':
        _user = currentUser or request.POST['user']
        _class = request.POST['class']
        _section = request.POST['section']
        _time = request.POST['time']
        _assignment = request.POST['assignment']

        data = {'blocked':'true'}

        #ref database/Login/student/class/section/username
        db.child('Login').child('student').child(_class).child(_section).child(_user).update(data)

        #getting user data
        userData = db.child('Login').child('student').child(_class).child(_section).child(_user).get().val()

        banData = {'error':'banned', 'id':_user, 'name':userData['username']}

        #ref database/Warnings/class/assignment/section/time
        db.child('Warnings').child(_class).child(_assignment).child(_section).child(_time).set(banData)

    return redirect(studentDashboard)