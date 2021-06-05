let results;

var containers;
$email = localStorage.getItem('email');

function load_results() {
    console.log("LOAD_DATASET" + $SCRIPT_ROOT + "/__load_results");

    var datasets_result = $.ajax({
        url: $SCRIPT_ROOT + "/__load_results",
        data: {},
        type: "GET",
        headers: {"Authorization": "Bearer " + $auth_token},
        success: function (data) {
            results = data
            Object.keys(results.result).forEach(function (dataset) {
                let result_container = document.getElementsByClassName("results_container");
                result_container[0].innerHTML += `<details>
                <summary>${dataset}</summary>
                        <table border="1" className="result__table" id="${dataset}"
                               style="margin: 0px; margin-top: 5px;">
                            <thead>
                            <tr>
                                <td>№</td>
                                <td>accuracy</td>
                                <td>auc_pr</td>
                                
                                <td>auc_roc</td>
                                <td>loss</td>
                                <td>num_parameters</td>
                                
                                <td></td>
                            </tr>
                            </thead>
                        </table>
                </details>`
                let table = document.getElementById(dataset);
                Object.keys(results.result[dataset]).forEach(function (model, num) {
                    var newRow = table.insertRow(num+1);

                    newRow.insertCell(0).innerHTML = model;
                    newRow.insertCell(1).innerHTML = results.result[dataset][model]["accuracy"];
                    newRow.insertCell(2).innerHTML = results.result[dataset][model]["auc_pr"];

                    newRow.insertCell(3).innerHTML = results.result[dataset][model]["auc_roc"];
                    newRow.insertCell(4).innerHTML = results.result[dataset][model]["loss"];
                    newRow.insertCell(5).innerHTML = results.result[dataset][model]["num_parameters"];

                    newRow.insertCell(6).innerHTML = `<a href="/models/${$email}/${dataset}/${model}">Завантажити</a>`;

                });
                console.log(dataset);
            })
            console.log("SUCCESS LOAD_DATASET");
            console.log(data);
            initDrawers();
        }
    }).fail(function (data) {
        console.log("dataset_load FAIL");
        console.log($auth_token);
        console.log(data)
        last_dataset = data;
    });
    console.log("dataset_result:" + datasets_result)
}
window.onload = load_results();


