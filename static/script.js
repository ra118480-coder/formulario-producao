
let descCount = 1
let fotoCount = 1


// =========================
// CASCATA
// =========================
async function loadFeiras() {

const res = await fetch("/api/feiras")
const data = await res.json()

const feira = document.getElementById("feira")

feira.innerHTML = "<option>Selecione</option>"

data.forEach(i => {
feira.innerHTML += `<option>${i}</option>`
})

}


async function loadProdutos(feira) {

const res = await fetch(`/api/produtos/${feira}`)
const data = await res.json()

const produto = document.getElementById("produto")

produto.innerHTML = "<option>Selecione</option>"

data.forEach(i => {
produto.innerHTML += `<option>${i}</option>`
})

}


async function loadModulacoes(feira, produto) {

const res = await fetch(`/api/modulacoes/${feira}/${produto}`)
const data = await res.json()

const mod = document.getElementById("modulacao")

mod.innerHTML = "<option>Selecione</option>"

data.forEach(i => {
mod.innerHTML += `<option>${i}</option>`
})

}


// =========================
// EVENTS CASCATA
// =========================
document.getElementById("feira").addEventListener("change", (e) => {
loadProdutos(e.target.value)
})

document.getElementById("produto").addEventListener("change", (e) => {
loadModulacoes(
document.getElementById("feira").value,
e.target.value
)
})


// =========================
// MULTI DESCRIÇÕES
// =========================
function addDescricao() {
descCount++
document.getElementById("descricoes").innerHTML +=
`<input name="descricao_${descCount}" placeholder="Descrição ${descCount}">`
}


// =========================
// MULTI FOTOS
// =========================
function addFoto() {
fotoCount++
document.getElementById("fotos").innerHTML +=
`<input type="file" name="foto_${fotoCount}">`
}


// =========================
// SUBMIT
// =========================
document.getElementById("formulario").addEventListener("submit", async (e) => {

e.preventDefault()

const formData = new FormData(e.target)

await fetch("/api/salvar", {
method: "POST",
body: formData
})

alert("Salvo com sucesso!")

e.target.reset()

})

// INIT
loadFeiras()
