function myFunction() {
    var x = document.getElementsByClassName("register")[0];
    if (x.style.display === "none" || x.style.display === "") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }












/*

    $.ajax({
        method: "POST",
        url: "some.php",
        data: { name: "John", location: "Boston" }
      })
        .done(function( msg ) {
          alert( "Data Saved: " + msg );
        });
    
}*/