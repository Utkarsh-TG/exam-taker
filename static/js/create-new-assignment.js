// create assignment 
var file, today, thisref, file_URL;

//firebase config
var firebaseConfig = JSON.parse('{{ FIREBASE_CONFIG|escapejs }}')

firebase.initializeApp(firebaseConfig);

var database = firebase.database();
var storage = firebase.storage();

//storage ref
var storageref = storage.ref('Assignments').child(currentClass);

$(document).on('submit', '#create-assignment', function(e){
    loadWindow('mid', 2000)
    e.preventDefault()
    file_URL = []
    storageRef = storage.ref('Assignments').child(currentClass).child($('#assignment-title-input').val());
    // uploading file this storage ref
    file = document.getElementById("assignment-file-input").files[0];
    // uploading file this storage ref
    thisref = storageref.child(file.name).put(file);
    thisref.on('state_changed',function(snapshot) {
        console.log('Done');
    }, function(error) {
        console.log('Error',error);
    }, function() {thisref.snapshot.ref.getDownloadURL().then(function(downloadURL) {
            file_URL = downloadURL
            test()
        });
    });
});

function test(){
    today = new Date().toISOString().slice(0, 10);
    _class = currentClass
    $.ajax({
        type: 'POST',
        url: '/teacher/exam_create/',
        data:{
            class: _class,
            title: $('#assignment-title-input').val(),
            time: $('#assignment-time-input').val(),
            description: $('#assignment-description-input').val(),
            date: today,
            file: file_URL,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },success :function(){
            fetchAssignments();
            $('.create-task-wrapper').css({'display':'none'});
            $('.assignments-container').css({'display':'block'});
            $('#create-assignment').css({'display':'none'});
            $('#update-assignment').css({'display':'none'});
        }
    });
    $('#create-assignment').trigger("reset"); 
}