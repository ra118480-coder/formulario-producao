from flask import Flask, render_template, jsonify, request
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

ARQUIVO_EXCEL = "registros.xlsx"


# =========================
# SQLITE (CASCATA)
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
    dados = conn.execute("SELECT DISTINCT colecao FROM produtos").fetchall()
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
    """, (feira, produto)).fetchall()
    conn.close()
    return jsonify([x[0] for x in dados])


# =========================
# SALVAR (MULTI DADOS + EXCEL HISTÓRICO)
# =========================
@app.route("/api/salvar", methods=["POST"])
def salvar():

    form = request.form.to_dict()
    files = request.files

    # =========================
    # DESCRIÇÕES MÚLTIPLAS
    # =========================
    descricoes = []
    i = 1
    while f"descricao_{i}" in form:
        if form.get(f"descricao_{i}"):
            descricoes.append(form.get(f"descricao_{i}"))
        i += 1

    # =========================
    # FOTOS MÚLTIPLAS
    # =========================
    fotos = []
    j = 1
    while f"foto_{j}" in files:
        file = files.get(f"foto_{j}")
        if file:
            fotos.append(file.filename)  # depois conecta SharePoint
        j += 1

    # =========================
    # REGISTRO FINAL
    # =========================
    nova_linha = {
        "feira": form.get("feira"),
        "produto": form.get("produto"),
        "modulacao": form.get("modulacao"),

        "fase": form.get("fase"),
        "tipo": form.get("melhoria"),

        "descricoes": " | ".join(descricoes),
        "fotos": " | ".join(fotos)
    }

    # =========================
    # SALVAR SEM PERDER HISTÓRICO
    # =========================
    if os.path.exists(ARQUIVO_EXCEL):
        df = pd.read_excel(ARQUIVO_EXCEL)
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    else:
        df = pd.DataFrame([nova_linha])

    df.to_excel(ARQUIVO_EXCEL, index=False)

    return jsonify({"status": "ok"})


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
