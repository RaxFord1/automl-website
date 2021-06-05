function myFunction() {
    var x = document.getElementsByClassName("register")[0];
    if (x.style.display === "none" || x.style.display === "") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

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
        }
    }).fail(function (data) {
        console.log("FAIL");
        console.log($auth_token);
        console.log(data)
    }).always(function (data){
        location.reload();
    });

}

$(document).mouseup(function (e) {
    var container = $(".register");
    if (container.has(e.target).length === 0) {
        container.hide();
    }
    var container = $(".add_dataset_form");
    if (container.has(e.target).length === 0) {
        container.hide();
    }
    var container = $(".dataset_form");
    if (container.has(e.target).length === 0) {
        container.hide();
    }

});

