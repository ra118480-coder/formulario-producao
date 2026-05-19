from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from openpyxl import load_workbook

app = Flask(__name__)

# =========================
# ARQUIVO EXCEL BASE
# =========================

arquivo = "Produtos_modulacoes_colecao (2).xlsx"

df = pd.read_excel(arquivo)

# PADRONIZAR NOMES DAS COLUNAS
df.columns = df.columns.str.strip().str.lower()

# PADRONIZAR DADOS
df["colecao"] = df["colecao"].astype(str).str.strip()
df["desc_tecnica"] = df["desc_tecnica"].astype(str).str.strip()
df["caracteristica"] = df["caracteristica"].astype(str).str.strip()
df["variavel"] = df["variavel"].astype(str).str.strip()

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# FEIRAS
# =========================

@app.route("/feiras")
def feiras():

    feiras = sorted(
        df["colecao"].dropna().unique().tolist()
    )

    return jsonify(feiras)

# =========================
# PRODUTOS
# =========================

@app.route("/produtos/<feira>")
def produtos(feira):

    feira = feira.strip()

    produtos = df[
        df["colecao"] == feira
    ]["desc_tecnica"].dropna().unique().tolist()

    produtos = sorted(produtos)

    return jsonify(produtos)

# =========================
# MODULAÇÕES
# =========================

@app.route("/modulacoes/<produto>")
def modulacoes(produto):

    produto = produto.strip()

    filtrado = df[
        df["desc_tecnica"] == produto
    ]

    # AQUI ESTÁ A CORREÇÃO
    modulacoes = filtrado[
        "variavel"
    ].dropna().unique().tolist()

    modulacoes = sorted(modulacoes)

    return jsonify(modulacoes)

# =========================
# SALVAR FORMULÁRIO
# =========================

@app.route("/salvar", methods=["POST"])
def salvar():

    feira = request.form.get("feira")
    produto = request.form.get("produto")
    modulacao = request.form.get("modulacao")
    versao = request.form.get("versao")
    fase = request.form.get("fase")
    tipo = request.form.get("tipo")

    dados = {
        "Feira": feira,
        "Produto": produto,
        "Modulacao": modulacao,
        "Versao": versao,
        "Fase": fase,
        "Tipo": tipo
    }

    contador = 1

    while True:

        descricao = request.form.get(f"descricao_{contador}")

        if descricao is None:
            break

        dados[f"Descricao_{contador}"] = descricao

        foto = request.files.get(f"foto_{contador}")

        if foto and foto.filename != "":

            pasta_upload = "static/uploads"

            os.makedirs(pasta_upload, exist_ok=True)

            caminho = os.path.join(
                pasta_upload,
                foto.filename
            )

            foto.save(caminho)

            dados[f"Foto_{contador}"] = caminho

        else:

            dados[f"Foto_{contador}"] = ""

        contador += 1

    # =========================
    # EXCEL FINAL
    # =========================

    arquivo_excel = "registros.xlsx"

    novo_df = pd.DataFrame([dados])

    # SE JÁ EXISTIR -> ADICIONA
    if os.path.exists(arquivo_excel):

        book = load_workbook(arquivo_excel)

        writer = pd.ExcelWriter(
            arquivo_excel,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="overlay"
        )

        writer.book = book

        sheet = book.active

        startrow = sheet.max_row

        novo_df.to_excel(
            writer,
            index=False,
            header=False,
            startrow=startrow
        )

        writer.close()

    # SE NÃO EXISTIR -> CRIA
    else:

        novo_df.to_excel(
            arquivo_excel,
            index=False
        )

    return "Formulário salvo com sucesso!"

# =========================
# RODAR
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
