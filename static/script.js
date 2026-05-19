let contador = 0;

async function carregarFeiras() {

    let response = await fetch("/feiras");

    let feiras = await response.json();

    let feiraSelect = document.getElementById("feira");

    feiraSelect.innerHTML = "";

    feiras.forEach(feira => {

        feiraSelect.innerHTML += `
            <option value="${feira}">${feira}</option>
        `;

    });

    carregarProdutos();
}

async function carregarProdutos() {

    let feira = document.getElementById("feira").value;

    let response = await fetch(`/produtos/${feira}`);

    let produtos = await response.json();

    let produtoSelect = document.getElementById("produto");

    produtoSelect.innerHTML = "";

    produtos.forEach(produto => {

        produtoSelect.innerHTML += `
            <option value="${produto}">${produto}</option>
        `;

    });

    carregarModulacoes();
}

async function carregarModulacoes() {

    let produto = document.getElementById("produto").value;

    let response = await fetch(`/modulacoes/${produto}`);

    let modulacoes = await response.json();

    let modulacaoSelect = document.getElementById("modulacao");

    modulacaoSelect.innerHTML = "";

    modulacoes.forEach(modulacao => {

        modulacaoSelect.innerHTML += `
            <option value="${modulacao}">${modulacao}</option>
        `;

    });

    carregarVersoes();
}

async function carregarVersoes() {

    let modulacao = document.getElementById("modulacao").value;

    let response = await fetch(`/versoes/${modulacao}`);

    let versoes = await response.json();

    let versaoSelect = document.getElementById("versao");

    versaoSelect.innerHTML = "";

    versoes.forEach(versao => {

        versaoSelect.innerHTML += `
            <option value="${versao}">${versao}</option>
        `;

    });

}

document.getElementById("feira")
.addEventListener("change", carregarProdutos);

document.getElementById("produto")
.addEventListener("change", carregarModulacoes);

document.getElementById("modulacao")
.addEventListener("change", carregarVersoes);

function adicionarCampo() {

    contador++;

    let div = document.createElement("div");

    div.className = "bloco";

    div.innerHTML = `

        <label>Descrição ${contador}</label>
        <textarea name="descricao_${contador}"></textarea>

        <label>Foto ${contador}</label>
        <input type="file" name="foto_${contador}">

    `;

    document.getElementById("campos").appendChild(div);
}

adicionarCampo();

document.getElementById("formulario")
.addEventListener("submit", async function(e){

    e.preventDefault();

    let formData = new FormData(this);

    let response = await fetch("/salvar",{
        method:"POST",
        body:formData
    });

    let resultado = await response.text();

    alert(resultado);

});

carregarFeiras();
