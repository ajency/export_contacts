var socket = io.connect('http://' + document.domain + ':' + location.port, {
    'timeout': 120000
});
socket.on('connect', function() {
    // we emit a connected message to let knwo the client that we are connected.
    socket.emit('client_connected', {data: 'New client!'});
});

socket.on('message', function (data) {
    console.log('message form backend ' + data);
});

socket.on('alert', function (data) {
    alert('Alert Message!! ' + data);
});


socket.on('prompt_user', function (data) {
    var prompt_data = $.parseJSON(data);
    if(prompt_data.input_type == 'otp'){
        $("#otp_verification_form").show();
        $("#otp_verification_form #otp_box").attr('placeholder',prompt_data.message);
        $("#otp_verification_form #prompt_handler").val(prompt_data.handler);
        $("#otp_verification_form #prompt_key").val(prompt_data.key);
    }
});

socket.on('active_screenshots_link', function (session_id) {
    var screenshot_url = 'http://' + document.domain + ':' + location.port+'/webdriver_screenshots/'+session_id;
    var el = '<a href="'+screenshot_url+'" target="_blank">SCREENSHOTS: '+session_id+'</a><br />';
    $("#screenshots_link").append(el);
});

socket.on('contacts_csv_link', function (session_id) {
    var csv_url = 'http://' + document.domain + ':' + location.port+'/export_contacts/'+session_id;
    var el = '<a href="'+csv_url+'" target="_blank">Exported Contacts: '+session_id+'</a><br />';
    $("#csv_link").append(el);
});

function json_button() {
    socket.send('json_button', '{"message": "test"}');
}

function alert_button() {
    socket.send('alert_button', 'Message from client!!')
}

function getIp_button() {
  var hostelement = document.getElementById("hostname");
  socket.emit('get_ip', hostelement.value)
}

socket.on('ip_data', function (ip) {
    console.log('IP Data: ' + ip);
});


socket.on('get_captcha', function (captcha_url) {
    //alert('password is missing!! for ' + username);
    console.log(captcha_url);
    $('#login_captcha_wrap').append('<img src="'+captcha_url+'"/>');
    $('#loginCaptchaModal').modal({ show: true});
});

socket.on('action', function (message) {
    $(".terminal").append("<p>"+message+"</p>");
});

socket.on('steps', function (message) {
    $("#initiate_form").hide();
    $("#step_form").show();
    var steps = JSON.parse(message);
    for (var key in steps) {
        var step = steps[key];
        if (isString(step)){
            var checkbox = '<div class="form-check"><input name="steps[]" data-label="'+step+'" class="form-check-input" type="checkbox" value="'+key+'"><label class="form-check-label">'+step+'</label></div>';
            $("#step_form .step_fields").append(checkbox);
        }else{
            for (var subkey in step){
                var substep = step[subkey];
                var checkbox = '<div class="form-check"><input name="steps[]" data-label="'+substep+'" class="form-check-input" type="checkbox" value="'+subkey+'"><label class="form-check-label">'+substep+'</label></div>';
            $("#step_form .step_fields").append(checkbox);
            }
        }
    }

});



socket.on('sequence_tree', function (message) {
    var sequence_tree = JSON.parse(message);
    //console.log(sequence_tree);
    var html ="<h4>Sequence Tree</h4><ul class='sequence_tree_list'>";
    sequence_tree.forEach(function(account){
        var username = account.linkedIn.username
        var main_sequences = account.linkedIn.sequences
        var emails_providers = account.email
        //console.log(username, main_sequences);
        html +="<li>";
            html +="<div>"+username+"</div>";
                html +="<ul>";
                if(main_sequences.length > 0){
                    html +='<li><div>Sequences</div>';
                        html +="<ul>";
                        main_sequences.forEach(function(mseq){
                            html +='<li id="'+mseq.key+'">'+mseq.title+'</li>';
                        });
                        html +="</ul>";
                    html +='</li>';
                 }

                    $.each(emails_providers, function(provider,emails){
                        html +='<li><div>'+provider+'</div>';
                            html +="<ul>";
                            emails.forEach(function(email){
                                var email_sequences = email.sequences
                                html +='<li><div>'+email.username+'</div>';
                                    html +="<ul>";
                                    email_sequences.forEach(function(eseq){
                                        html +='<li id="'+eseq.key+'">'+eseq.title+'</li>';
                                    });
                                    html +="</ul>";
                                html +='</li>';
                            });
                            html +="</ul>";
                        html +='</li>';
                    });

                html +="</ul>";


        html +="</li>";
    });
    html +="</ul>";
    $("#sequence_tree").html(html);
});



socket.on('tree_progress', function (key) {
    $("#"+key).addClass('spinner');
});

socket.on('tree_success', function (key) {
    $("#"+key).removeClass('spinner');
    $("#"+key).addClass('sequence_success');
});

socket.on('tree_failed', function (key) {
    $("#"+key).removeClass('spinner');
    $("#"+key).addClass('sequence_failed');
});




function isString (obj) {
  return (Object.prototype.toString.call(obj) === '[object String]');
}

socket.on('gmail_otp_verification', function (message) {
    $("#gmail_otp_verification_form").show();
});

// Exception - single user input
socket.on('exception_user_single_request', function (message) {
    console.log(message);
    var text_message = message.split("---")[1];
    console.log(text_message);
    var handler = message.split("---")[0];
    $("#handler").val(handler);
    $("#message").html(text_message);
    $("#user_input").val('');
    $("#get_user_single_input_form").show();
});

// socket.on('retry_method', function (message) {
//     $("#handler").value = message.split("---")[0];
//     $("#message").value = message.split("---")[1];
//     $("#get_user_single_input_form").show();
// });




// function showTestModal(){
//   $('#loginCaptchaModal').modal({ show: true});
// }
//
// function hideTestModal(){
//   $('#loginCaptchaModal').modal('hide');
// }



$( document ).ready(function() {

  $("#login_form").on("submit", function(event){
   event.preventDefault();
   var username = $("#username",this).val();
   var password = $("#password",this).val();
   var login_payload = {"username":username, "password":password};
   socket.emit('web_login', login_payload);
 })

 $("#login_captcha_form").on("submit", function(event){
  event.preventDefault();
  //var login_captcha = $("#login_captcha",this).val();
  //$('#loginCaptchaModal').modal('hide');
  //socket.emit('web_login_with_pass', login_captcha);
})






$("input[name='environment']").on("change", function(event){
    var env = $("input:checked[name='environment']").val();
    if(env == 'prod'){
        //$(".headless_mode").show();
        $('#headless_mode_true').prop('checked', true);
        $('#headless_mode_false').attr('disabled',true);
    }else{
        $("input[name='headless_mode']").removeAttr('disabled');
        $('#headless_mode_false').prop('checked', true);
    }
});


 $("#initiate_form").on("submit", function(event){
  event.preventDefault();
    var auto = $("input:checked[name='auto']").val();
    var is_auto = (auto == '1')? true : false;
    var env = $("input:checked[name='environment']").val();
    $(".environment_badge").show().text(env);
    var headless_mode = $("input:checked[name='headless_mode']").val();
    var is_headless = (headless_mode == '1')? true : false;
    var payload = {'env': env,'auto': is_auto, 'headless': is_headless};

    var accounts_config = $("#accounts_config").val();
    if(accounts_config.trim().length > 0){
        payload['accounts'] = accounts_config;
        console.log('Accounts Config <> ', accounts_config);
    }

    socket.emit('initiate_process', payload);
    if(is_auto){
        $("#initiate_form").hide();
        $(".step_select_msg").show();
        $(".steps_selected").text("AUTO");
        socket.emit('start_exporter', {});
    }
  });


 $("#step_form").on("submit", function(event){
  event.preventDefault();
  var steps=[];
  var step_selected_array=[]
    $("input:checked[name='steps[]']").each(function(){
        steps.push($(this).val());
        step_selected_array.push($(this).attr('data-label'));
    });
    $(".step_select_msg").show();
    $(".steps_selected").text(step_selected_array.join());
    console.log("Steps selected: "+steps);
   socket.emit('start_exporter', {'steps':steps});
   $(this).hide();
});


$("#gmail_otp_verification_form").on("submit", function(event){
  event.preventDefault();
  var otp = $("#gmail_otp").val();
  socket.emit('gmail_otp_login', {'otp':otp});
  $(this).hide();
});

// Common input box code
$("#get_user_single_input_form").on("submit", function(event){
  event.preventDefault();
  // $("#get_user_single_input_form").hide();
  var handler = $("#handler").val();
  var user_input = $("#user_input").val();
  $("#handler").val('');
  $("#user_input").val('');
  $('#exception_form').modal('hide');
  var payload = {'user_input': user_input, 'handler': handler};
  console.log(payload)
  socket.emit('exception_user_single_response', payload);
  $(this).hide();
})



$("#otp_verification_form").on("submit", function(event){
  event.preventDefault();
  var payload = {
    'otp': $("#otp_box").val(),
    'handler': $("#prompt_handler").val(),
    'key': $("#prompt_key").val(),
  }
  console.log('Sending data',payload);
  socket.emit('otp_submission', payload);
  $(this).hide();
});



});
