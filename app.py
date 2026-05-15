from flask import Flask, render_template, jsonify, request
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

ARQUIVO_EXCEL = "registros.xlsx"


# =========================
# CONEXÃO BANCO (modulações)
# =========================
def conectar():
    conn = sqlite3.connect("produtos.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# FEIRAS
# =========================
@app.route("/api/feiras")
def feiras():

    conn = conectar()

    dados = conn.execute("""
        SELECT DISTINCT colecao
        FROM produtos
        ORDER BY colecao
    """).fetchall()

    conn.close()

    return jsonify([x[0] for x in dados])


# =========================
# PRODUTOS
# =========================
@app.route("/api/produtos/<feira>")
def produtos(feira):

    conn = conectar()

    dados = conn.execute("""
        SELECT DISTINCT desc_tecnica
        FROM produtos
        WHERE colecao = ?
        ORDER BY desc_tecnica
    """, (feira,)).fetchall()

    conn.close()

    return jsonify([x[0] for x in dados])


# =========================
# MODULAÇÕES
# =========================
@app.route("/api/modulacoes/<feira>/<produto>")
def modulacoes(feira, produto):

    conn = conectar()

    dados = conn.execute("""
        SELECT DISTINCT variavel
        FROM produtos
        WHERE colecao = ?
        AND desc_tecnica = ?
        ORDER BY variavel
    """, (feira, produto)).fetchall()

    conn.close()

    return jsonify([x[0] for x in dados])


# =========================
# SALVAR NO EXCEL
# =========================
@app.route("/api/salvar", methods=["POST"])
def salvar():

    dados = request.json

    nova_linha = {

        "feira": dados.get("feira"),
        "produto": dados.get("produto"),
        "modulacao": dados.get("modulacao"),

        "setor": dados.get("setor"),
        "classificacao": dados.get("classificacao"),
        "tipo": dados.get("melhoria"),

        "descricao": dados.get("descricao"),

        # futuro SharePoint
        "imagem_url": dados.get("imagem_url")

    }

    # cria arquivo se não existir
    if not os.path.exists(ARQUIVO_EXCEL):

        df = pd.DataFrame([nova_linha])
        df.to_excel(ARQUIVO_EXCEL, index=False)

    else:

        df = pd.read_excel(ARQUIVO_EXCEL)
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        df.to_excel(ARQUIVO_EXCEL, index=False)

    return jsonify({"status": "ok"})


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
