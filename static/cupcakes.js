

const BASE_URL = "http://localhost:5000/api"

function generateCupcake(cupcake){
    return `
    <div data-cupcake-id=${cupcake.id}">
        <li>
            ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
            <button class="delete-button btn-danger">X</button>
        </li>
        <img src="${cupcake.image}" alt="">
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


$(showList);