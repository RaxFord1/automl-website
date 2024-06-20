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
            result = data['result']

            console.log(result)
            result.forEach(function (element) {
                console.log(element);
                let dimensions = "()"
                if (element.dataset_type == "image") {
                    dimensions = "(" + element.n_classes + "," + element.n_files + ")"
                } else {
                    dimensions = "(" + element.n_rows + "," + element.n_cols + ")"
                }
                $(".dataset__table").prepend(`<tr><td> ${element.dataset_name} </td><td>${element.size}КБ</td><td>${dimensions}</td><td>${element.upload_time}</td><td><button onclick="select_dataset('${element.dataset_name}')">Обрати</button></td></tr>`);
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

            debugger
            if (data['result']['task_type'] == "classification") {
                $("#task_type_classification").prop('checked', true);
            } else {
                $("#task_type_regression").prop('checked', true);
            }

            if (data['result']['data_type'] == "image") {
                $("#data_type_image").prop('checked', true);
                $(".dataset_shape_value").text("(" + data['result'].n_classes + "," + data['result'].n_files + ")");
                displayFilesByCategory(data['result']['category_has_files'])
            } else {
                $("#data_type_csv").prop('checked', true);
                $(".dataset_shape_value").text(data['result']['shape']);
                $(".dataset_table_container").html(data['result']['table']);
            }

            last_dataset = data;
            $(".dataset_form_title").text(data['result']['name']);
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

function displayFilesByCategory(data) {
    const container = $('.dataset_table_container');

    container.html("")

    // Create table element
    var table = $('<table class="table table-bordered"></table>');

    // Create table head
    var thead = $('<thead><tr><th>Category</th><th>Files</th></tr></thead>');
    table.append(thead);

    // Create table body
    var tbody = $('<tbody></tbody>');

    $.each(data, function(category, files) {
        var fileLinks = files.map(function(file) {
            return '<a href="' + file + '">' + file + '</a>';
        }).join(", ");

        var row = '<tr>' +
                  '<td>' + category + '</td>' +
                  '<td>' + fileLinks + '</td>' +
                  '</tr>';

        tbody.append(row);
    });

    // Append tbody to table
    table.append(tbody);

    // Append table to container
    container.append(table);
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