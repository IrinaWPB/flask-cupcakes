const BASE_URL = "http://127.0.0.1:5000/api";
const list = document.querySelector('#list');
const newCCForm = document.querySelector('form');

function ccHTML(cupcake) {
    return `
        <li id=${cupcake.id}>
            <img width="200px" src="${cupcake.image}"><button>X</button>
            <ul>
                <li>${cupcake.flavor}</li>
                <li>${cupcake.size}</li>
                <li>${cupcake.rating}</li>
            </ul>
            
        </li>`;
}

async function showCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cc of response.data.cupcakes) {
        let newCupcake = document.createElement("div");
        newCupcake.innerHTML = ccHTML(cc);
        list.append(newCupcake);
    }
}

newCCForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    let flavor = document.querySelector('#flavor').value;
    let size = document.querySelector('#size').value;
    let rating = document.querySelector('#rating').value;
    let image = document.querySelector('#image').value != "" ? document.querySelector('#image').value : "https://tinyurl.com/demo-cupcake";
    const newCCResp = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor, size, rating, image
    });
    let newCupcake = document.createElement("div");
    newCupcake.innerHTML = ccHTML(newCCResp.data.cupcake);
    list.append(newCupcake); 
});

list.addEventListener("click", async function(e) {
    e.preventDefault();
    let idToRemove;
    if (e.target.tagName == "BUTTON") {
        idToRemove = e.target.parentElement.id;
        console.log(idToRemove);
        e.target.parentElement.remove();
        }
    await axios.delete(`${BASE_URL}/cupcakes/${idToRemove}`);
    console.log(idToRemove);
});

showCupcakes();

