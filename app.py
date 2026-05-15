from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)


# =========================
# CONEXAO COM BANCO
# =========================
def conectar():

    conn = sqlite3.connect("produtos.db")

    conn.row_factory = sqlite3.Row

    return conn


# =========================
# PAGINA PRINCIPAL
# =========================
@app.route("/")
def home():

    return render_template("index.html")


# =========================
# BUSCAR COLECOES
# =========================
@app.route("/api/modelos")
def modelos():

    conn = conectar()

    cursor = conn.execute("""
        SELECT DISTINCT colecao
        FROM produtos
        ORDER BY colecao
    """)

    dados = [x[0] for x in cursor.fetchall()]

    conn.close()

    return jsonify(dados)


# =========================
# BUSCAR MODULACOES
# =========================
@app.route("/api/modulacoes/<colecao>")
def modulacoes(colecao):

    conn = conectar()

    cursor = conn.execute("""
        SELECT DISTINCT desc_tecnica
        FROM produtos
        WHERE colecao = ?
        ORDER BY desc_tecnica
    """, (colecao,))

    dados = [x[0] for x in cursor.fetchall()]

    conn.close()

    return jsonify(dados)


# =========================
# SALVAR REGISTRO
# =========================
@app.route("/api/salvar", methods=["POST"])
def salvar():

    dados = request.json

    conn = conectar()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS registros (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            modelo TEXT,

            modulacao TEXT,

            setor TEXT,

            versao TEXT,

            melhoria TEXT,

            descricao TEXT,

            data_registro TEXT
        )
    """)

    conn.execute("""
        INSERT INTO registros (

            modelo,

            modulacao,

            setor,

            versao,

            melhoria,

            descricao,

            data_registro

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        dados["modelo"],

        dados["modulacao"],

        dados["setor"],

        dados["versao"],

        dados["melhoria"],

        dados["descricao"],

        datetime.now().strftime("%d/%m/%Y %H:%M")
    ))

    conn.commit()

    conn.close()

    return jsonify({
        "status": "ok"
    })


# =========================
# LISTAR REGISTROS
# =========================
@app.route("/api/registros")
def registros():

    conn = conectar()

    cursor = conn.execute("""
        SELECT *
        FROM registros
        ORDER BY id DESC
    """)

    dados = [dict(x) for x in cursor.fetchall()]

    conn.close()

    return jsonify(dados)


# =========================
# RODAR SISTEMA
# =========================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
