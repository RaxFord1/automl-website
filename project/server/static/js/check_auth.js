var email;

function check_status() {
    console.log("CHECK_STATUS");
    $.ajax({
        url: "/auth/status",
        data: {},
        type: "GET",
        headers: {"Authorization": "Bearer " + $auth_token},
        success: function (data) {
            console.log(data);
            $("button[name='Enter']").css("display", "none");
            $(".login__icon").css("background-color", "green");
            $(".status_entered").text("Добро пожаловать, " + String(data.data['email']))
            email = String(data.data['email'])
            $("input[name='dataset_email']").val(email)
        }
    }).fail(function (data) {
        console.log("FAIL");
        console.log($auth_token);
        console.log(data)
    });
}



const form = document.getElementById("myForm");

form.addEventListener("submit", function (event) {
    event.preventDefault();
});

let a;
let last;
$(function () {
    console.log("INIT" + String($SCRIPT_ROOT));
    $('.login100-form-btn').bind('click', function () {
        console.log($('input[name="email"]').val());
        console.log($('input[name="password"]').val())
        if ($('input[name="email"]').val() == "") {
            $(".result").addClass("error");
            $(".result").text("Все поля должны быть заполнены");
            return false;
        }
        if ($('input[name="password"]').val() == "") {
            $(".result").addClass("error");
            $(".result").text("Все поля должны быть заполнены");
            return false;
        }
        console.log("SEND_TO" + String($SCRIPT_ROOT));
        var jqxhr = $.post($SCRIPT_ROOT + '/auth/login',
            {
                email: $('input[name="email"]').val(),
                password: $('input[name="password"]').val()
            },
            function (data) {
                //alert( "success" );
                console.log(data);
            })
            .done(function (data) {
                //alert( "second success" );
                console.log(data);
                a = data;
                $(".result").text(data.message);
                $auth_token = data['auth_token'];
                localStorage.setItem('token', $auth_token);
                document.location.reload();
            })
            .fail(function (data) {

                console.log(data)

                alert("error");
                $(".result").addClass("error");
                $(".result").text(data.responseJSON.message);
            }).always(function (data) {
                last = data;
                check_status()
            });
        check_status()
    });
});




check_status();
