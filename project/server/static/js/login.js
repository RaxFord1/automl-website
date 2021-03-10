$auth_token = localStorage.getItem('token');
$SCRIPT_ROOT = "";//{{ request.script_root|tojson|safe }};

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