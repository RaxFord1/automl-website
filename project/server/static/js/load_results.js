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
            console.log("__load_results")
            console.log(data)
            Object.keys(results.result).forEach(function (dataset) {
                let result_container = document.getElementsByClassName("results_container");
                result_container[0].innerHTML += `
                <div class="card mt-3">
                    <div class="card-header">
                        <h5>${dataset}</h5>
                    </div>
                    <div class="card-body">
                        <details>
                            <summary>${dataset}</summary>
                            <table class="table table-bordered table-hover mt-3" id="${dataset}">
                                <thead class="thead-dark">
                                    <tr>
                                        <td scope="col">№</td>
                                        <td scope="col">accuracy</td>
                                        <td scope="col">auc_pr</td>
                                        <td scope="col">auc_roc</td>
                                        <td scope="col">loss</td>
                                        <td scope="col">num_parameters</td>
                                        <td scope="col">Дія</td>
                                        <td scope="col">Images</td>
                                        <td scope="col">Images-Val</td>
                                        <td scope="col">Architecture</td>
                                    </tr>
                                </thead>
                                <tbody>
                                </tbody>
                            </table>
                        </details>
                    </div>
                </div>`
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

                    let imagesCell = newRow.insertCell(7);
                    let images = results.result[dataset][model]["images"];
                    images.forEach(function (image) {
                        let imgElement = document.createElement("img");
                        imgElement.src = `/results/${$email}/${dataset}/${model}/${image}`;
                        imgElement.style.width = "50px";  // Adjust the size as needed
                        imgElement.style.height = "50px"; // Adjust the size as needed
                        imgElement.style.cursor = "pointer";

                        imgElement.setAttribute("data-toggle", "modal");
                        imgElement.setAttribute("data-target", "#imageModal");

                        imgElement.setAttribute("data-src", `/results/${$email}/${dataset}/${model}/${image}`);
                        imagesCell.appendChild(imgElement);
                    });

                    let imagesCell2 = newRow.insertCell(8);
                    let images2 = results.result[dataset][model]["val_images"];
                    images2.forEach(function (image) {
                        let imgElement = document.createElement("img");
                        imgElement.src = `/results/${$email}/${dataset}/${model}/${image}`;
                        imgElement.style.width = "50px";  // Adjust the size as needed
                        imgElement.style.height = "50px"; // Adjust the size as needed
                        imgElement.style.cursor = "pointer";

                        imgElement.setAttribute("data-toggle", "modal");
                        imgElement.setAttribute("data-target", "#imageModal");

                        imgElement.setAttribute("data-src", `/results/${$email}/${dataset}/${model}/${image}`);
                        imagesCell2.appendChild(imgElement);
                    });

                    let architectureCell = newRow.insertCell(9);
                    let architecture = results.result[dataset][model]["architecture"];
                    architecture.forEach(function (arch) {
                        architectureCell.innerHTML += `<p>${arch.name}: ${arch.shape}</p>`;
                    });
                });
                console.log(dataset);
            })
            console.log("SUCCESS LOAD_DATASET");
            console.log(data);

            if (!document.getElementById("imageModal")) {
                let modalHtml = `
                <div class="modal fade" id="imageModal" tabindex="-1" aria-labelledby="imageModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="imageModalLabel">Image Preview</h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <img id="modalImage" src="" class="img-fluid" alt="Image">
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>`;
                document.body.insertAdjacentHTML('beforeend', modalHtml);

                // Add event listener to update modal image source
                $('#imageModal').on('show.bs.modal', function (event) {
                    var button = $(event.relatedTarget); // Button that triggered the modal
                    var src = button.data('src'); // Extract info from data-* attributes
                    var modal = $(this);
                    modal.find('.modal-body img').attr('src', src);
                });
            }
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


