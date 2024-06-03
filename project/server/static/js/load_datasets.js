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
                $(".dataset__table").prepend(`<tr><td> ${element} </td><td>868КБ</td><td>(502,4)</td><td>26.01.2021</td><td><button onclick="select_dataset('${element}')">Обрати</button></td></tr>`);
            })

            console.log("SUCCESS LOAD_DATASET");
            console.log(data);
        }
    }).fail(function (data) {
        console.log("dataset_load FAIL");
        console.log($auth_token);
        console.log(data);
        last_dataset = data;
    }).always(function () {
        check_status();
    });
    console.log("dataset_result:")
    console.log(datasets_result)
}

load_dataset()

var selected_dataset;

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
            $(".dataset_form_title").text(data['result']['name']);
            $(".dataset_table_container").html(data['result']['table']);
            $(".dataset_shape_value").text(data['result']['shape']);
            $("input[name='dataset_name_hidden']").val(data['result']['name']);
            console.log("SUCCESS LOAD_DATASET");
            console.log(data);
            selected_dataset = data['result']['name'];
            $("#datasetModal").modal('show');
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

function delete_dataset() {
    var datasets_result = $.ajax({
        url: $SCRIPT_ROOT + "/__delete_dataset",
        data: {dataset: selected_dataset},
        type: "POST",
        headers: {"Authorization": "Bearer " + $auth_token},
        success: function (data) {
            alert("DONE")
            document.location.reload();
        }
    }).fail(function (data) {
        alert("Couldn't delete dataset")
    }).always(function (data) {
        $(".dataset_form").css("display", "block");

    });
    console.log("dataset_result:" + datasets_result)
}