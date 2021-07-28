// create assignment 
var file, today, thisref, file_URL;

const postAssignment = (questions, w_cheat, q_cheat) => {
    today = new Date().toISOString().slice(0, 10);
    _class = currentClass
    $.ajax({
        type: 'POST',
        url: '/teacher/exam_create/',
        data:{
            type: 'mcq',
            class: _class,
            windowCheat: w_cheat,
            questionCheat: q_cheat,
            title: $('#assignment-title-input').val(),
            time: $('#assignment-time-input').val(),
            description: $('#assignment-description-input').val(),
            date: today,
            file: questions,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },success :function(){
            fetchAssignments();
            //reset
            $('#assignment-title-input').val('')
            $('#assignment-time-input').val('')
            $('#assignment-description-input').val('')
            $('#assignment-file-input').val('')
            $('#allow-change-window-check')[0].checked = false
            $('#allow-change-question-check')[0].checked = false
            $('#long-answer-type')[0].checked = false
            $('#mcq-answer-type')[0].checked = false

            $('.create-task-wrapper').css({'display':'none'});
            $('.assignments-container').css({'display':'block'});
            $('#create-assignment').css({'display':'none'});
            $('#update-assignment').css({'display':'none'});
        }
    });
}

$('#assignment-form-submit').on('click', (e) => {
    let window_cheat = false
    let view_question = false
    loadWindow('mid', 2000)
    today = new Date().toISOString().slice(0, 10);
    _class = currentClass
    if($('#allow-change-window-check').is(':checked')){
        window_cheat = true;
    }
    if($('#allow-change-question-check').is(':checked')){
        view_question = true;
    }
    if(paperType == 'long'){
        $.ajax({
            type: 'POST',
            url: '/teacher/exam_create/',
            data:{
                type: 'long',
                windowCheat: window_cheat,
                class: _class,
                title: $('#assignment-title-input').val(),
                time: $('#assignment-time-input').val(),
                description: $('#assignment-description-input').val(),
                date: today,
                file: $('#assignment-file-input').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },success :function(){
                //reset
                $('#assignment-title-input').val('')
                $('#assignment-time-input').val('')
                $('#assignment-description-input').val('')
                $('#assignment-file-input').val('')
                $('#allow-change-window-check')[0].checked = false
                $('#allow-change-question-check')[0].checked = false
                $('#long-answer-type')[0].checked = false
                $('#mcq-answer-type')[0].checked = false

                fetchAssignments();
                $('.create-task-wrapper').css({'display':'none'});
                $('.assignments-container').css({'display':'block'});
                $('#create-assignment').css({'display':'none'});
                $('#update-assignment').css({'display':'none'});
            }
        });
    }
    if(paperType == 'mcq'){
        let questions = []
        questionList = document.getElementsByClassName('question-wrapper')
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
        postAssignment(JSON.stringify(questions), window_cheat, view_question)
    }   
    $('#create-assignment').trigger("reset"); 
});
    