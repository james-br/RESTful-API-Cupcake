

const BASE_URL = "http://127.0.0.1:5000/api"

function generateCupcake(cupcake){
    return `
    <div class="col-sm-4 mx-auto my-3" data-cupcake-id="${cupcake.id}" >
        <img class="img-thumbnail rounded"  src="${cupcake.image}" alt="">
        <h4>
            ${cupcake.flavor} / ${cupcake.size} / Rating: ${cupcake.rating}
        </h4>
        <button class="delete-button rounded-pill btn-danger"><small>Delete</small></button>
    </div>
    `;
}


async function showList(){
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    for(let cups of response.data.cupcakes) {
        let newCup = $(generateCupcake(cups));
        $("#cupcakes-list").append(newCup);
    }
}

$("#new-cupcake-form").on("submit", async function(e){
    e.preventDefault();

    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const response = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor, rating, size, image
    });

    let newCupcake = $(generateCupcake(response.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});

$("#cupcakes-list").on("click", ".delete-button", async function(e){
    e.preventDefault();
    let $cupcake = $(e.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});

$(showList);