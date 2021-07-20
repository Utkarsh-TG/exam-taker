// create assignment 
var file, today, thisref, file_URL;

//firebase config
var firebaseConfig = {"apiKey": "AIzaSyD7ddl63JBC-Xxj2vKe99R5JJkxBJDvTVY", "authDomain": "exam-3d397.firebaseapp.com", "databaseURL": "https://exam-3d397-default-rtdb.asia-southeast1.firebasedatabase.app", "projectId": "exam-3d397", "storageBucket": "exam-3d397.appspot.com", "messagingSenderId": "647787494671", "appId": "1:647787494671:web:6afa3e03b1184d113c127a", "measurementId": "G-2CTKYSPY7P" }

firebase.initializeApp(firebaseConfig);

var database = firebase.database();
var storage = firebase.storage();

const postAssignment = (questions) => {
    today = new Date().toISOString().slice(0, 10);
    _class = currentClass
    $.ajax({
        type: 'POST',
        url: '/teacher/exam_create/',
        data:{
            type: 'mcq',
            class: _class,
            title: $('#assignment-title-input').val(),
            time: $('#assignment-time-input').val(),
            description: $('#assignment-description-input').val(),
            date: today,
            file: questions,
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

$('#assignment-form-submit').on('click', (e) => {
    loadWindow('mid', 2000)
    today = new Date().toISOString().slice(0, 10);
    _class = currentClass
    if(paperType == 'long'){
        $.ajax({
            type: 'POST',
            url: '/teacher/exam_create/',
            data:{
                type: 'long',
                class: _class,
                title: $('#assignment-title-input').val(),
                time: $('#assignment-time-input').val(),
                description: $('#assignment-description-input').val(),
                date: today,
                file: $('#assignment-file-input').val(),
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
        postAssignment(JSON.stringify(questions))
    }   
    $('#create-assignment').trigger("reset"); 
});
    