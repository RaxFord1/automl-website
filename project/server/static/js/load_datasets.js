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
                $(".dataset__table").prepend("<tr><td>" + element + "</td><td>868КБ</td><td>(502,4)</td><td>26.01.2021</td><td><button onclick='select_dataset(" + element + ")'>Выбрать</button></td></tr>");
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


function select_dataset(element) {
    var datasets_result = $.ajax({
        url: $SCRIPT_ROOT + "/__select_dataset",
        data: {dataset: element},
        type: "GET",
        headers: {"Authorization": "Bearer " + $auth_token},
        success: function (data) {
            if (data['result']['task_type'] == "Classification") {
                $(".task_type_classification").prop('checked', true);
            } else {
                $(".task_type_regression").prop('checked', true);
            }
            last_dataset = data;
            $(".dataset_table_container").html(data['result']['table']);
            $(".dataset_shape_value").text(data['result']['shape']);
            console.log("SUCCESS LOAD_DATASET");
            console.log(data);
        }
    }).fail(function (data) {
        document.location.reload();
        console.log("dataset_load FAIL");
        console.log($auth_token);
        console.log(data)
        last_dataset = data;
    }).always(function (data) {
        $(".dataset_form").css("display", "block");

    });
    console.log("dataset_result:" + datasets_result)


}

function show_add_dataset_form() {
    $(".add_dataset_form").css("display", "block");
}