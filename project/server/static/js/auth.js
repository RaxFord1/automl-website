var email;

$auth_token = localStorage.getItem('token');
$SCRIPT_ROOT = "";//{{ request.script_root|tojson|safe }};

// Функция для переключения видимости кнопок
function toggleLoginLogout() {
    var isLoggedIn = localStorage.getItem('loggedIn') === 'true';
    var loginBtn = document.getElementById('login-btn');
    var logoutBtn = document.getElementById('logout-btn');

    if (isLoggedIn) {
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'inline-block';
    } else {
        loginBtn.style.display = 'inline-block';
        logoutBtn.style.display = 'none';
    }
}

// Вызов функции при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    toggleLoginLogout();

    window.addEventListener('storage', function(event) {
        console.log("asd");
        if (event.key === 'loggedIn') {
            toggleLoginLogout();
        }
    });
});

function logOut() {
    console.log("LogOut");
    $.ajax({
        url: "/auth/logout",
        data: {},
        type: "POST",
        headers: {"Authorization": "Bearer " + $auth_token},
        success: function (data) {
            console.log("Successfully log out");
            console.log(data);
            localStorage.setItem('loggedIn', false);
            toggleLoginLogout();
        }
    }).fail(function (data) {
        console.log("FAIL");
        console.log($auth_token);
        console.log(data)
        if (data.status == 401) {
            localStorage.setItem('token', '');
            localStorage.setItem('loggedIn', false);
            toggleLoginLogout();
        }
    });

}

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
            $(".logout").css("display", "block");
            $(".status_entered").text("Добро пожаловать, " + String(data.data['email']))

            email = String(data.data['email'])
            localStorage.setItem('email', email);
            localStorage.setItem('loggedIn', true);
            $("input[name='dataset_email']").val(email)
        }
    }).fail(function (data) {
        console.log("FAIL");
        console.log($auth_token);
        console.log(data)
    });
}

check_status();

setInterval(() => {
    check_status();
}, 3*60*1000)

