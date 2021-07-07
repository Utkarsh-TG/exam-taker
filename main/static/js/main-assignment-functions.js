//update
var updated_file, updated_file_URL
var fileChange = false;
var oldFile, oldTitle;

function openTask(title, time, desc, fileURL){
    $('.create-task-wrapper').css({'display':'block'});
    $('#create-assignment').css({'display':'none'});
    $('#update-assignment').css({'display':'block'});
    $('.assignments-container').css({'display':'none'});
    $('#update-title-input').val(title)
    $('#update-time-input').val(time)
    $('#update-description-input').val(desc)
    $('#file-viewer').attr('src',fileURL)
    oldTitle = title;
    oldFile = fileURL;
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
}

function getAssignmentData(_method, assignment_name){
    taskname = assignment_name;
    tempData = assignment_data;
    _func = _method

    if(_func == 'update'){
        for(var i = 0; i < tempData.length; i++){
            if(tempData[i]['title'] == taskname){
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
                openTask(tempData[i]['title'], tempData[i]['time'], tempData[i]['description'], tempData[i]['file']);
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
    e.preventDefault()
    if(fileChange){
        storageref = storage.ref('Assignments').child(currentClass);
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