//update
var results_data, c_section, _title, _id, oldTitle, _type;

function openTask(title, time, desc, fileText, type, cheatData){
    loadWindow('mid', 2000)
    $('.create-task-wrapper').css({'display':'block'});
    $('.results-container').css({'display':'none'})
    $('#create-assignment').css({'display':'none'});
    $('#update-assignment').css({'display':'block'});
    $('.assignments-container').css({'display':'none'});
    $('#update-title-input').val(title)
    $('#update-time-input').val(time)
    $('#update-description-input').val(desc)
    _type = type
    if(type == 'long'){
        $('#update-file-input').css({'display':'block'})
        $('.update-mcq-question-container').css({'display':'none'})
        $('#update-file-input').val(fileText)
        $('.update-advanced-cheat-prevent').css({'display':'none'})
        if(cheatData['windowCheat']){
            $('#update-allow-change-window-check')[0].checked = true;
        }
    }
    else if(type == 'mcq'){
        $('#update-file-input').css({'display':'none'})
        $('.update-mcq-question-container').css({'display':'block'})
        $('.update-advanced-cheat-prevent').css({'display':'block'})
        if(cheatData['windowCheat']){
            $('#update-allow-change-window-check')[0].checked = true;
        }
        if(cheatData['questionCheat']){
            $('#update-allow-change-question-check')[0].checked = true;
        }else if(!cheatData['questionCheat']){
            $('#update-allow-change-question-check')[0].checked = false;
        }
        parent = document.getElementById('update-question-container')
        parent.innerHTML = ''
        for(let i=0;i<fileText.length;i++){
            wrap = document.createElement('div')
            wrap.classList.add('update-question-wrapper')
            wrap.innerHTML = '<input type="text" class="question" placeholder="Enter Question" value="'+ fileText[i]['question'] +'"><input type="text" class="option" placeholder="Option A" value="'+ fileText[i]['options'][0] + '"><input type="text" class="option" placeholder="Option B" value="'+ fileText[i]['options'][1] + '"><input type="text" class="option" placeholder="Option C" value="'+ fileText[i]['options'][2] + '"><input type="text" class="option" placeholder="Option D" value="'+ fileText[i]['options'][3] + '"><input type=text class="correct" placeholder="Correct Option" value="' + fileText[i]['correct'] + '"><button class="delete-question-btn" onclick="deleteQuestion(this)">Delete</button>'
            parent.appendChild(wrap)
        }
    }
    oldTitle = title;
}

//results
$('#results-submit').on('click', ()=>{
    today = new Date().toISOString().slice(0, 10);
    $.ajax({
        type: 'POST',
        url: '/teacher/exam_results_return/',
        data: {
            _class: currentClass,
            section: c_section,
            title: _title,
            id: _id,
            marks: $('#marks-input').val(),
            note: $('#results-note-input').val(),
            date: today,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },success: () => {
            $('.error-message').css({'display':'flex'})
            $('#error-msg').html('Result posted successfully!')
            $('#marks-input').val('')
            $('#results-note-input').val('')
        }
    })
})

const openStudentResult = (id) => {
    _id = id
    loadWindow('mid', 1000)
    $('.students-result-wrapper').css({'display':'block'})
    $('.section-wrapper').css({'display':'none'})
    $('.students-wrapper').css({'display':'none'})
    $('#student-id').html(results_data[c_section][id]['username'])
    $('#student-name').html(results_data[c_section][id]['name'])
    if(results_data[c_section][id]['type'] == 'long'){
        $('#long-results').css({'display':'block'})
        $('#marks-calc').css({'display':'none'})
        $('#short-results').css({'display':'none'})
        $('#student-answers').html(results_data[c_section][id]['answers'])
        $('#student-file').attr({'src':results_data[c_section][id]['files']})
    }
    else if(results_data[c_section][id]['type'] == 'mcq'){
        $('#long-results').css({'display':'none'})
        $('#marks-calc').css({'display':'block'})
        $('#short-results').css({'display':'block'})
        let generateMcqQuestions = (data) => {
            let parent = document.getElementById('short-results')
            parent.innerHTML = ''
            answers = results_data[c_section][id]['answers']
            console.log(data)
            console.log(answers)
            var totalMarks = 0
            for(let i=0;i<data.length;i++){
                if(answers[i+1] === undefined){
                    answers[i+1] = 'Not Attempted'
                }
                if(answers[i+1] == data[i]['correct']){
                    totalMarks += 1
                }
                wrap = document.createElement('div')
                wrap.classList.add('result-question-wrapper')
                wrap.innerHTML= "<span class='result-question'>"+ (i+1) + ") " + data[i]['question'] +"</span><div class='result-option'>(A) "+ data[i]['options'][0] +"</div>" + "<div class='result-option'>(B) "+ data[i]['options'][1] +"</div>" + "<div class='result-option'>(C) "+ data[i]['options'][2] +"</div>" + "<div class='result-option'>(D) "+ data[i]['options'][3] +"</div><div class='result-answers-wrapper'><span class='result-correct-option'>Corrrect : <strong>"+ data[i]['correct'] + "</strong></span><span class='student-answer'>Student Answer : <strong>"+ answers[i+1] +"</strong></span></div>"
                parent.appendChild(wrap)
            }
            $('#marks-calc').html('Total Marks : '+totalMarks)
        }
        $.ajax({
            type: 'POST',
            url: '/teacher/exam_request/',
            data:{
                class: currentClass,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },success :function(data){
                data = data['assignment_list']
                for(let i=0;i<data.length;i++){
                    if(data[i]['title'] == _title){
                        tempData = data[i]['file']
                        generateMcqQuestions(tempData)
                        break
                    }
                }
            }
        })
        let parent = document.getElementById('short-results')

    }
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

function postTask(task, title){
    if(task == 'assign'){
        $('.section-select-wrapper').css({'display':'block'})
        currentAssignment = title
        assignmentFunction = 'assign'
    }
    if(task == 'end'){
        $('.section-select-wrapper').css({'display':'block'})
        currentAssignment = title
        assignmentFunction = 'end'
    }
    if(task == 'result'){
        loadWindow('mid', 2000)
        _class = currentClass
        $.ajax({
            type: 'POST',
            url: '/teacher/exam_result/',
            data:{
                class: _class,
                assignment: title,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data){
                let tempData = data.resultData;
                results_data = tempData
                _title = title
                generateResults(tempData)
            },
        });
    }
}

function getAssignmentData(_method, assignment_name){
    taskname = assignment_name;
    tempData = assignment_data;
    _func = _method

    for(var i = 0; i < tempData.length; i++){
        if(tempData[i]['title'] == taskname){
            if(_func == 'update'){
                loadWindow('mid', 1000)
                openTask(tempData[i]['title'], tempData[i]['time'], tempData[i]['description'], tempData[i]['file'], tempData[i]['type'], tempData[i]);
            }
            else if(_func == 'assign'){
                postTask('assign', tempData[i]['title']);
            }
            else if(_func == 'end'){
                postTask('end', tempData[i]['title']);
            }
            else if(_func == 'result'){
                postTask('result', tempData[i]['title']);
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

const postUpdatedAssignment = (questions, q_cheat, w_cheat) => {
    console.log(questions)
    $.ajax({
        type: 'POST',
        url: '/teacher/exam_update_file/',
        data:{
            type: _type,
            class: _class,
            windowCheat: w_cheat,
            questionCheat: q_cheat,
            old_title: oldTitle,
            title: $('#update-title-input').val(),
            time: $('#update-time-input').val(),
            description: $('#update-description-input').val(),
            file: questions,
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
}   

$('#update-form-submit').on('click', (e) => {
    let window_cheat = false
    let view_question = false
    loadWindow('mid', 2000)
    e.preventDefault()
    _class = currentClass
    today = new Date().toISOString().slice(0, 10);
    if($('#update-allow-change-window-check').is(':checked')){
        window_cheat = true;
    }
    if($('#update-allow-change-window-check').is(':checked')){
        view_question = true;
    }
    if(_type == 'long'){
        $.ajax({
            type: 'POST',
            url: '/teacher/exam_update_file/',
            data:{
                type: _type,
                windowCheat: window_cheat,
                class: _class,
                old_title: oldTitle,
                title: $('#update-title-input').val(),
                time: $('#update-time-input').val(),
                description: $('#update-description-input').val(),
                file: $('#update-file-input').val(),
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
    }
    else if(_type == 'mcq'){
        let questions = []
        questionList = document.getElementsByClassName('update-question-wrapper')
        for(let j=0;j<questionList.length;j++){
            tempData = {}
            q = questionList[j].children[0].value
            o1 = questionList[j].children[1].value
            o2 = questionList[j].children[2].value
            o3 = questionList[j].children[3].value
            o4 = questionList[j].children[4].value
            c = questionList[j].children[5].value
            optionsList = [o1,o2,o3,o4]
            tempData.question = q
            tempData.options = optionsList
            tempData.correct = c.toUpperCase()
            questions.push(tempData)
        }
        postUpdatedAssignment(JSON.stringify(questions), window_cheat, view_question)
    }
    $('#update-assignment').trigger("reset");
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