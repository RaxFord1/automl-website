function myFunction() {
    var x = document.getElementsByClassName("register")[0];
    if (x.style.display === "none" || x.style.display === "") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}


$(document).mouseup(function (e) {
    var container = $(".register");
    if (container.has(e.target).length === 0){
        container.hide();
    }
    var container = $(".add_dataset_form");
    if (container.has(e.target).length === 0){
        container.hide();
    }
});

