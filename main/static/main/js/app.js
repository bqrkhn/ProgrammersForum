/**
 * Created by baqir on 03-07-2017.
 */

$("#username").change(function () {
      var username = $(this).val();

      $.ajax({
        url: '/ajax/validate_username/',
        data: {
          'username': username
        },
        dataType: 'json',
        success: function (data) {
          if (data.is_taken) {
            $("#form_username").addClass("form-group has-danger").removeClass("form-group").removeClass("form-group has-success")
            $("#feedback_username").text("Sorry, that username's taken. Try another?")
          }
          else{
            $("#form_username").addClass("form-group has-success").removeClass("form-group").removeClass("form-group has-danger")
            $("#feedback_username").text("Username is available")
          }
        }
      });

    });

$("#email").change(function () {
    var email = $(this).val();
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if(regex.test(email)){
        $("#form_email").addClass("form-group has-success").removeClass("form-group").removeClass("form-group has-danger")
        $("#feedback_email").text("Email is valid")
    }
    else {
        $("#form_email").addClass("form-group has-danger").removeClass("form-group").removeClass("form-group has-success")
        $("#feedback_email").text("Email is invalid")
    }
});

$("#password").change(function () {
    var password = $(this).val();
    if(password.length>5){
        $("#form_password").addClass("form-group has-success").removeClass("form-group").removeClass("form-group has-danger")
         $("#feedback_password").text("")
    }
    else {
        $("#form_password").addClass("form-group has-danger").removeClass("form-group").removeClass("form-group has-success")
        $("#feedback_password").text("Minimum password length is 6")
    }
});

$("#confirm_password").change(function () {
    var password1 = $("#password").val();
    var password2 = $(this).val();
    if(password1==password2){
        $("#form_password ,#form_confirm_password").addClass("form-group has-success").removeClass("form-group").removeClass("form-group has-danger")
        $("#feedback_confirm_password").text("Passwords match")
    }
    else {
        $("#form_password ,#form_confirm_password").addClass("form-group has-danger").removeClass("form-group").removeClass("form-group has-success")
        $("#feedback_confirm_password").text("Passwords do not match!")
    }
});

function vote($this) {
    var id = $this.attr("id");
    var type ,down, up, count;
    if($("#"+id).hasClass("disabled"))
        return;
    if(id[0]=='u') {
        type = 1;
        up = id;
        id=id.substr(3);
        down = "#down_"+id;
        count = "#count_"+id;
        if($(down).hasClass("disabled"))
            $(down).removeClass("disabled");
        else
            $("#"+up).addClass("disabled");
    }
    else {
        type = 0;
        down = id;
        id=id.substr(5);
        up = "#up_"+id;
        count = "#count_"+id;
        if($(up).hasClass("disabled"))
            $(up).removeClass("disabled");
        else
            $("#"+down).addClass("disabled");
    }
    $.ajax({
        url: '/discussions/vote',
        data: {
            id: id,
            type: type
        },
        success: function () {
            var value = parseInt($(count).text());
            if(type == 1)
                $(count).text(value+1);
            else
                $(count).text(value-1);
        }
    });
}

$(document).ready(function() {
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
});