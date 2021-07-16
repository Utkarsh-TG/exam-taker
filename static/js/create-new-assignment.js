// create assignment 
var file, today, thisref, file_URL;

//firebase config
var firebaseConfig = {"apiKey": "AIzaSyD7ddl63JBC-Xxj2vKe99R5JJkxBJDvTVY", "authDomain": "exam-3d397.firebaseapp.com", "databaseURL": "https://exam-3d397-default-rtdb.asia-southeast1.firebasedatabase.app", "projectId": "exam-3d397", "storageBucket": "exam-3d397.appspot.com", "messagingSenderId": "647787494671", "appId": "1:647787494671:web:6afa3e03b1184d113c127a", "measurementId": "G-2CTKYSPY7P" }

firebase.initializeApp(firebaseConfig);

var database = firebase.database();
var storage = firebase.storage();

//storage ref

$('#assignment-form-submit').on('click', (e) => {
    console.log('aaa')
    loadWindow('mid', 2000)
    file_URL = []
    storageRef = storage.ref('Assignments').child(currentClass).child($('#assignment-title-input').val());
    alert(storageRef)
    // uploading file this storage ref
    file = document.getElementById("assignment-file-input").files[0];
    // uploading file this storage ref
    thisref = storageRef.child(file.name).put(file);
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