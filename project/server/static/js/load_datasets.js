let last_dataset;

function load_dataset() {
    console.log("LOAD_DATASET" + $SCRIPT_ROOT + "/__get_datasets");

    var datasets_result = $.ajax({
        url: $SCRIPT_ROOT + "/__get_datasets",
        data: {},
        type: "GET",
        headers: {"Authorization": "Bearer " + $auth_token},
        success: function (data) {
            last_dataset = data
            data['result'].forEach(function (element) {
                console.log(element);
                $(".dataset__table").prepend("<tr><td>" + element + "</td><td>868КБ</td><td>(502,4)</td><td>26.01.2021</td><td><button onclick='select_dataset(element)'>Выбрать</button></td></tr>");
            })

            console.log("SUCCESS LOAD_DATASET");
            console.log(data);
        }
    }).fail(function (data) {
        console.log("dataset_load FAIL");
        console.log($auth_token);
        console.log(data)
        last_dataset = data;
    });
    console.log("dataset_result:" + datasets_result)
}

load_dataset()


function show_add_dataset_form() {
    $(".add_dataset_form").css("display", "block");
}