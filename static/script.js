let descCount = 1
let fotoCount = 1


function addDescricao() {
    descCount++
    document.getElementById("descricoes").innerHTML +=
        `<input name="descricao_${descCount}" placeholder="Descrição ${descCount}">`
}


function addFoto() {
    fotoCount++
    document.getElementById("fotos").innerHTML +=
        `<input type="file" name="foto_${fotoCount}">`
}
