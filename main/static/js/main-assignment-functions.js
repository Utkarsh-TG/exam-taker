//update
var updated_file, updated_file_URL, results_data, c_section
var fileChange = false;
var oldFile, oldTitle;

function openTask(title, time, desc, fileURL){
    loadWindow('mid', 2000)
    $('.create-task-wrapper').css({'display':'block'});
    $('.results-container').css({'display':'none'})
    $('#create-assignment').css({'display':'none'});
    $('#update-assignment').css({'display':'block'});
    $('.assignments-container').css({'display':'none'});
    $('#update-title-input').val(title)
    $('#update-time-input').val(time)
    $('#update-description-input').val(desc)
    fileViewer = document.getElementById('file-viewer')
    fileViewer.src = fileURL
    oldTitle = title;
    console.log(fileURL)
    oldFile = fileURL;
}

const openStudentResult = (id) => {
    loadWindow('mid', 1000)
    $('.students-result-wrapper').css({'display':'block'})
    $('.section-wrapper').css({'display':'none'})
    $('.students-wrapper').css({'display':'none'})
    $('#student-id').html(results_data[c_section][id]['username'])
    $('#student-name').html(results_data[c_section][id]['name'])
    $('#student-answers').html(results_data[c_section][id]['answers'])
    $('#student-file').attr({'src':results_data[c_section][id]['files']})
}

const getStudentResults = (e) => {
    let thisTarget = e.target
    openStudentResult(thisTarget.textContent.replace(/\D/g,''))
}

const assignStudentBtn = () => {
    sectionBtn = document.querySelectorAll('.student-select-btn')
    sectionBtn.forEach(button => { 
        button.addEventListener('click', getStudentResults);
    });
}

const openStudentsList = (section) => {
    loadWindow('mid', 1000)
    $('.students-result-wrapper').css({'display':'none'})
    $('.students-wrapper').css({'display':'block'})
    $('.section-wrapper').css({'display':'none'})
    let students = results_data[section]
    parent = document.getElementById('students-wrapper')
    parent.innerHTML = ''
    if(students){
        Object.keys(students).forEach(key => {
            studentBtn = document.createElement('div')
            studentBtn.classList.add('student-select-btn')
            studentBtn.innerHTML = key + '-' + students[key]['name']
            parent.appendChild(studentBtn)
            assignStudentBtn()
        });
    }
}

const getResults = (e) => {
    let thisTarget = e.target
    c_section = thisTarget.textContent
    openStudentsList(thisTarget.textContent)
}

const assignSectionBtn = () => {
    sectionBtn = document.querySelectorAll('.section-select-btn')
    sectionBtn.forEach(button => { 
        button.addEventListener('click', getResults);
    });
}

const generateResults = (data) => {
    $('.students-wrapper').css({'display':'none'})
    $('.students-result-wrapper').css({'display':'none'})
    $('.section-wrapper').css({'display':'flex'})
    $('.results-container').css({'display':'block'})
    $('.assignment-window').css({'display':'none'})
    $('.create-task-wrapper').css({'display':'none'})
    $('.assignments-container').css({'display':'none'})
    parent = document.getElementById('section-wrapper')
    parent.innerHTML = ''
    if(data){
        Object.keys(data).forEach(key => {
            sectionBtn = document.createElement('div')
            sectionBtn.classList.add('section-select-btn')
            sectionBtn.innerHTML = key
            parent.appendChild(sectionBtn)
            assignSectionBtn()
        });
    }
}

function postTask(task, title, time, desc, fileURL, date){
    if(task == 'assign'){
        _class = currentClass
        $.ajax({
            type: 'POST',
            url: '/teacher/exam/assign/',
            data:{
                class: _class,
                title: title,
                time: time,
                description: desc,
                fileURL: fileURL,
                date: date,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },success :function(){
                fetchAssignments();
            }
        });
    }
    if(task == 'end'){
        console.log('end')
        _class = currentClass
        $.ajax({
            type: 'POST',
            url: '/teacher/exam/end/',
            data:{
                class: _class,
                title: title,
                time: time,
                description: desc,
                fileURL: fileURL,
                date: date,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },success :function(){
                fetchAssignments();
            }
        });
    }
    if(task == 'result'){
        loadWindow('mid', 2000)
        _class = currentClass
        $.ajax({
            type: 'POST',
            url: '/teacher/exam/result/',
            data:{
                class: _class,
                assignment: title,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data){
                let tempData = data.resultData;
                results_data = tempData
                generateResults(tempData)
            },
        });
    }
}

function getAssignmentData(_method, assignment_name){
    taskname = assignment_name;
    tempData = assignment_data;
    _func = _method

    if(_func == 'update'){
        for(var i = 0; i < tempData.length; i++){
            if(tempData[i]['title'] == taskname){
                loadWindow('mid', 1000)
                openTask(tempData[i]['title'], tempData[i]['time'], tempData[i]['description'], tempData[i]['file']);
            }
        }
    }
    else if(_func == 'assign'){
        for(var i = 0; i < tempData.length; i++){
            if(tempData[i]['title'] == taskname){
                postTask('assign', tempData[i]['title'], tempData[i]['time'], tempData[i]['description'], tempData[i]['file'], tempData[i]['date']);
            }
        }
    }
    else if(_func == 'end'){
        for(var i = 0; i < tempData.length; i++){
            if(tempData[i]['title'] == taskname){
                postTask('end', tempData[i]['title'], tempData[i]['time'], tempData[i]['description'], tempData[i]['file'], tempData[i]['date']);
            }
        }
    }
    else if(_func == 'result'){
        for(var i = 0; i < tempData.length; i++){
            if(tempData[i]['title'] == taskname){
                postTask('result', tempData[i]['title'], tempData[i]['time'], tempData[i]['description'], tempData[i]['file']);
            }
        }
    }
};

function updateAssignment(e){
    let target = e.target.parentNode.parentNode.children[0].children[0];
    getAssignmentData('update', target.textContent);
};

function assignAssignment(e){
    let target = e.target.parentNode.parentNode.children[0].children[0];
    getAssignmentData('assign', target.textContent);
}

function endAssignment(e){
    let target = e.target.parentNode.parentNode.children[0].children[0];
    getAssignmentData('end', target.textContent);
}

function resultsAssignment(e){
    let target = e.target.parentNode.parentNode.children[0].children[0];
    getAssignmentData('result', target.textContent);
}

function reAssignUpdateButton(){
    update_btn = document.querySelectorAll('.update-task');
    update_btn.forEach(button => { 
        button.addEventListener('click', updateAssignment);
    });
    assign_btn = document.querySelectorAll('.assign-task');
    assign_btn.forEach(button => { 
        button.addEventListener('click', assignAssignment);
    });
    end_btn = document.querySelectorAll('.end-task');
    end_btn.forEach(button => { 
        button.addEventListener('click', endAssignment);
    });
    result_btn = document.querySelectorAll('.view-results');
    result_btn.forEach(button => { 
        button.addEventListener('click', resultsAssignment);
    });
}

$('#update-file-input').on('change', function(){
    fileChange = true
}) 

function postUpdatedAssignmentForm(){
    _class = currentClass
    // today's date
    today = new Date().toISOString().slice(0, 10);
    $.ajax({
        type: 'POST',
        url: '/teacher/exam/update/file',
        data:{
            class: _class,
            old_title: oldTitle,
            title: $('#update-title-input').val(),
            time: $('#update-time-input').val(),
            description: $('#update-description-input').val(),
            fileURL: updated_file_URL,
            date: today,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },success :function(){
            fetchAssignments();
            $('.create-task-wrapper').css({'display':'none'});
            $('.assignments-container').css({'display':'block'});
            $('#create-assignment').css({'display':'none'});
            $('#update-assignment').css({'display':'none'});
        }
    });
    $('#update-assignment').trigger("reset");
}

$(document).on('submit', '#update-assignment', function(e){
    loadWindow('mid', 2000)
    e.preventDefault()
    if(fileChange){
        newStorageRef = storage.ref('Assignments').child(currentClass).child($('#update-title-input').val())
        // uploading file this storage ref
        updated_file = document.getElementById("update-file-input").files[0];
        thisref = storageref.child(updated_file.name).put(updated_file);
        thisref.on('state_changed',function(snapshot) {
                console.log('Done');
            }, function(error) {
                console.log('Error',error);
            }, function() {
                thisref.snapshot.ref.getDownloadURL().then(function(downloadURL) {
                    updated_file_URL = downloadURL;
                    postUpdatedAssignmentForm();
                });
            })
    }else{
        _class = currentClass
        // today's date
        today = new Date().toISOString().slice(0, 10);
        $.ajax({
            type: 'POST',
            url: '/teacher/exam/update/file',
            data:{
                class: _class,
                old_title: oldTitle,
                title: $('#update-title-input').val(),
                time: $('#update-time-input').val(),
                description: $('#update-description-input').val(),
                date: today,
                fileURL: oldFile,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },success :function(){
                fetchAssignments();
                $('.create-task-wrapper').css({'display':'none'});
                $('.assignments-container').css({'display':'block'});
                $('#create-assignment').css({'display':'none'});
                $('#update-assignment').css({'display':'none'});
            }
        });
        $('#update-assignment').trigger("reset");
    }
})

const returnStudentResultWrapper = () =>{
    loadWindow('mid', 500)
    $('.students-result-wrapper').css({'display':'none'})
    $('.students-wrapper').css({'display':'block'})
}

const returnStudentsWrapper = () =>{
    loadWindow('mid', 500)
    $('.section-wrapper').css({'display':'flex'})
    $('.students-wrapper').css({'display':'none'})
    $('.students-result-wrapper').css({'display':'none'})
}

const returnSectionWrapper = () =>{
    loadWindow('mid', 500)
    $('.assignments-container').css({'display':'block'})
    $('.results-container').css({'display':'none'})
}