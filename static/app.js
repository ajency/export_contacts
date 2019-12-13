var socket = io.connect('http://' + document.domain + ':' + location.port);
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
        var checkbox = '<div class="form-check"><input name="steps[]" data-label="'+step+'" class="form-check-input" type="checkbox" value="'+key+'"><label class="form-check-label">'+step+'</label></div>';
        $("#step_form .step_fields").append(checkbox);
    }

});

socket.on('gmail_otp_verification', function (message) {
    $("#gmail_otp_verification_form").show();
});

// Exception
socket.on('exception_user_single_request', function (message) {
    $("#handler").value = message.split("---")[0];
    $("#message").value = message.split("---")[1];
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
    socket.emit('initiate_process', {'env': env,'auto': is_auto, 'headless': is_headless});
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
  var handler = $("input:checked[name='handler']").val();
  var user_input = $("input:checked[name='user_input']").val();
  $('#exception_form').modal('hide');
  socket.emit('exception_user_single_response', {'user_input': todo, 'handler': handler});
})


});
