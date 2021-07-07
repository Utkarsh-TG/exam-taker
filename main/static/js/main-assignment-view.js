//on assigned
var chat_data, old_chat_data, warning_data, old_warning_data, attendee_data, old_attendee_data

function generateAssignmentChat(){
    let parent = document.getElementById('chat-log')
    chatData = chat_data
    oldChatData = old_chat_data
    chatDataList = []
    oldChatDataList = []
    if(chatData == null){
        chatDataList = []
        oldChatDataList = []
        old_chat_data = null
        document.getElementById('chat-log').innerHTML = ''
    }
    if(chatData != null){
        Object.entries(chatData).forEach(
            ([key, value]) => chatDataList.push(value)
        );
    }
    if(oldChatData != null){
        Object.entries(oldChatData).forEach(
            ([key, value]) => oldChatDataList.push(value)
        );
    }
    for(let i = 0; i < chatDataList.length; i++){
        for(let n = 0; n < oldChatDataList.length; n++){
            if(JSON.stringify(chatDataList[i]) == JSON.stringify(oldChatDataList[n])){
                chatDataList.splice(i, 1) 
            }
        }
    }
    if(chatDataList.length > 0){
        old_chat_data = chat_data
        oldChatData = chatData
        oldChatDataList = chatDataList
        for(let i = 0; i < chatDataList.length; i++){
            chat = document.createElement('div')
            chat.classList.add('chat-message')
            chat.innerHTML = '<div class="message-sender">'+ chatDataList[i]['name'] +'</div>' + chatDataList[i]['message'] + '<div class="chat-message"></div>'
            parent.appendChild(chat)
        }
    }
}

function generateChatUI(){
    title = currentAssignmentTitle
    _currentSection = currentSection
    let ref = firebase.database().ref("Chat"+'/'+ title+'/'+ _currentSection);
    ref.on('value', function(dataSnapshot){
        chat_data = dataSnapshot.val()
        generateAssignmentChat()
    });
}

function viewAssignment(e){
    let target = e.children[0];
    if(target == undefined){
        alert('Sorry there is some error. Please refresh the page or try reopening.')
        return false
    }
    $('.create-task-wrapper').css({'display':'none'});
    $('.assignments-container').css({'display':'none'});
    $('.assignment-window').css({'display':'block'});
    currentAssignmentTitle = target.textContent
    viewAssignmentWindow()
}

function generateAssignmentWarning(){
    let parent = document.getElementById('warning-log')
    warningData = warning_data
    oldWarningData = old_warning_data
    warningDataList = []
    oldWarningDataList = []

    if(warningData == null){
        warning_data = null
        old_warning_data = null
        warningDataList = []
        oldWarningDataList = []
        document.getElementById('warning-log').innerHTML = ''
    }
    if(warningData != null){
        Object.entries(warningData).forEach(
            ([key, value]) => warningDataList.push(value)
        );
    }
    if(oldWarningData != null){
        Object.entries(oldWarningData).forEach(
            ([key, value]) => oldWarningDataList.push(value)
        );
    }
    for(let i = 0; i < warningDataList.length; i++){
        for(let n = 0; n < oldWarningDataList.length; n++){
            if(JSON.stringify(warningDataList[i]) == JSON.stringify(oldWarningDataList[n])){
                warningDataList.splice(i, 1) 
            }
        }
    }
    if(warningDataList.length > 0){
        old_warning_data = warning_data
        for(let i = 0; i < warningDataList.length; i++){
            if(warningDataList[i]['error'] == 'warned'){
                warningPost = document.createElement('div')
                warningPost.classList.add('warning-error-warned', 'warning-error')
                warningPost.innerHTML = '<span class="warning-error-icon">!</span><span class="warning-error-message">'+ warningDataList[i]['name']+ '('+ warningDataList[i]['id']+ ') ' +'has been warned for attempt to cheat.</span>'
                parent.appendChild(warningPost)
            }
            if(warningDataList[i]['error'] == 'banned'){
                warningPost = document.createElement('div')
                warningPost.classList.add('warning-error-banned', 'warning-error')
                warningPost.innerHTML = '<span class="warning-error-icon">!</span><span class="warning-error-message">'+ warningDataList[i]['name']+ '('+ warningDataList[i]['id']+ ') ' +'has been banned for attempt to cheat.</span>'
                parent.appendChild(warningPost)
            }
            if(warningDataList[i]['error'] == 'unbanned'){
                warningPost = document.createElement('div')
                warningPost.classList.add('warning-error-unbanned', 'warning-error')
                warningPost.innerHTML = '<span class="warning-error-icon">!</span><span class="warning-error-message">'+ warningDataList[i]['name']+ '('+ warningDataList[i]['id']+ ') ' +'has been unbanned.</span>'
                parent.appendChild(warningPost)
            }
        }
    }
}

function generateWarningUI(){
    title = currentAssignmentTitle
    _currentSection = currentSection
    let ref = firebase.database().ref("Warnings"+'/'+ title+'/'+ _currentSection);
    ref.on('value', function(dataSnapshot){
        warning_data = dataSnapshot.val()
        generateAssignmentWarning()        
    });
}

function generateAssignmentAttendee(){
    let parent = document.getElementById('attendee-log')
    attendeeData = attendee_data
    oldAttendeeData = old_attendee_data
    attendeeDataList = []
    oldAttendeeDataList = []
    if(attendeeData == null){
        old_attendee_data = null
        attendeeDataList = []
        oldAttendeeDataList = []
        document.getElementById('attendee-log').innerHTML = ''
    }
    if(attendeeData != null){
        Object.entries(attendeeData).forEach(
            ([key, value]) => attendeeDataList.push(value)
        );
    }
    if(oldAttendeeData != null){
        Object.entries(oldAttendeeData).forEach(
            ([key, value]) => oldAttendeeDataList.push(value)
        );
    }
    for(let i = 0; i < attendeeDataList.length; i++){
        for(let n = 0; n < oldAttendeeDataList.length; n++){
            if(JSON.stringify(attendeeDataList[i]) == JSON.stringify(oldAttendeeDataList[n])){
                attendeeDataList.splice(i, 1) 
            }
        }
    }
    if(attendeeDataList.length > 0){
        old_attendee_data = attendee_data
        for(let i = 0; i < attendeeDataList.length; i++){
            attendeePost = document.createElement('div')
            attendeePost.classList.add('attendee')
            attendeePost.innerHTML = attendeeDataList[i]['username']+ '('+ attendeeDataList[i]['id'] + ')'
            parent.appendChild(attendeePost)
        }
    }
}

function generateAttendeesUI(){
    title = currentAssignmentTitle
    _currentSection = currentSection
    let ref = firebase.database().ref("TurnedIn"+'/'+ title+'/'+ _currentSection);
    ref.on('value', function(dataSnapshot){
        attendee_data = dataSnapshot.val()
        generateAssignmentAttendee()        
    });
}

function viewAssignmentWindow(){
    title = currentAssignmentTitle
    $('#assignment-conduct-title').html(title);
    generateChatUI();
    generateWarningUI();
    generateAttendeesUI()
}

$('#section-list').on('change', function(){
    currentSection = $('#section-list').val()
    document.getElementById('chat-log').innerHTML = ''
    document.getElementById('warning-log').innerHTML = ''
    document.createElement('div').innerHTML = ''
    generateChatUI()
    generateWarningUI()
    generateAttendeesUI()
})

$('#return-view-assignment').click(function(){
    $('.create-task-wrapper').css({'display':'none'});
    $('.assignments-container').css({'display':'block'});
    $('.assignment-window').css({'display':'none'});
})

function blockUser(){
    _class = currentClass
    _section = currentSection
    let _today = new Date().toISOString()
    let dateToday = new Date(_today)
    _time = dateToday.toISOString().replace(/[\-\.\:ZT]/g,"").substr(0,14)
    $.ajax({
        type: 'POST',
        url: '/exam/student/block/',
        data:{
            user: $('#warning-input').val(),
            class: _class,
            section: _section,
            assignment: currentAssignmentTitle,
            time: _time,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },success: function(){
            $('#warning-input').val('')
        }
    });
}

function unBlockUser(){
    _class = currentClass
    _section = currentSection
    let _today = new Date().toISOString()
    let dateToday = new Date(_today)
    _time = dateToday.toISOString().replace(/[\-\.\:ZT]/g,"").substr(0,14)
    $.ajax({
        type: 'POST',
        url: '/exam/student/unblock/',
        data:{
            user: $('#warning-input').val(),
            class: _class,
            section: _section,
            assignment: currentAssignmentTitle,
            time: _time,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },success: function(){
            $('#warning-input').val('')
        }
    });
}

function submitChatMessage(){
    assignmentname = currentAssignmentTitle
    _section = currentSection
    _message = $('#chat-input').val()
    _user = $('.user-info').text()
    dateToday = new Date()
    _time = dateToday.toISOString().replace(/[\-\.\:ZT]/g,"").substr(0,14)
    if(!_message.trim() == ''){
        $.ajax({
            type: 'POST',
            url: '/exam/chat/message/',
            data:{
                user: _user,
                message: _message,
                assignment: assignmentname,
                section: _section,
                time: _time,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },success: function(){
                $('#chat-input').val('')
            }
        });
    }
}
