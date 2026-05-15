const feira = document.getElementById("modelo")
const produto = document.getElementById("modulacao")
const modulacao = document.getElementById("variavel")


// FEIRAS
async function loadFeiras() {

const res = await fetch("/api/feiras")
const data = await res.json()

feira.innerHTML = "<option>Selecione</option>"

data.forEach(i => {
feira.innerHTML += `<option>${i}</option>`
})

}


// PRODUTOS
async function loadProdutos(f) {

const res = await fetch(`/api/produtos/${f}`)
const data = await res.json()

produto.innerHTML = "<option>Selecione</option>"
modulacao.innerHTML = "<option>Selecione</option>"

data.forEach(i => {
produto.innerHTML += `<option>${i}</option>`
})

}


// MODULAÇÕES
async function loadModulacoes(f, p) {

const res = await fetch(`/api/modulacoes/${f}/${p}`)
const data = await res.json()

modulacao.innerHTML = "<option>Selecione</option>"

data.forEach(i => {
modulacao.innerHTML += `<option>${i}</option>`
})

}


// EVENTS
feira.addEventListener("change", () => {
loadProdutos(feira.value)
})

produto.addEventListener("change", () => {
loadModulacoes(feira.value, produto.value)
})


// SUBMIT
document.getElementById("formulario").addEventListener("submit", async (e) => {

e.preventDefault()

const formData = new FormData(e.target)

const res = await fetch("/api/salvar", {
method: "POST",
body: formData
})

const r = await res.json()

alert("Salvo com sucesso!")

e.target.reset()

})


// INIT
loadFeiras()
