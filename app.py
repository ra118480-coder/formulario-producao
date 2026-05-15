from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)


# ==================================
# CONEXAO
# ==================================
def conectar():

    conn = sqlite3.connect("produtos.db")

    conn.row_factory = sqlite3.Row

    return conn


# ==================================
# HOME
# ==================================
@app.route("/")
def home():

    return render_template("index.html")


# ==================================
# FEIRAS / COLECOES
# ==================================
@app.route("/api/feiras")
def feiras():

    conn = conectar()

    cursor = conn.execute("""

        SELECT DISTINCT colecao
        FROM produtos
        ORDER BY colecao

    """)

    dados = [x[0] for x in cursor.fetchall()]

    conn.close()

    return jsonify(dados)


# ==================================
# PRODUTOS
# ==================================
@app.route("/api/produtos/<feira>")
def produtos(feira):

    conn = conectar()

    cursor = conn.execute("""

        SELECT DISTINCT desc_tecnica
        FROM produtos
        WHERE colecao = ?
        ORDER BY desc_tecnica

    """, (feira,))

    dados = [x[0] for x in cursor.fetchall()]

    conn.close()

    return jsonify(dados)


# ==================================
# MODULACOES
# ==================================
@app.route("/api/modulacoes/<feira>/<produto>")
def modulacoes(feira, produto):

    conn = conectar()

    cursor = conn.execute("""

        SELECT DISTINCT variavel
        FROM produtos
        WHERE colecao = ?
        AND desc_tecnica = ?
        ORDER BY variavel

    """, (feira, produto))

    dados = [x[0] for x in cursor.fetchall()]

    conn.close()

    return jsonify(dados)


# ==================================
# SALVAR
# ==================================
@app.route("/api/salvar", methods=["POST"])
def salvar():

    dados = request.json

    conn = conectar()

    conn.execute("""

        CREATE TABLE IF NOT EXISTS registros (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            feira TEXT,

            produto TEXT,

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

            feira,
            produto,
            modulacao,
            setor,
            versao,
            melhoria,
            descricao,
            data_registro

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        dados["feira"],
        dados["produto"],
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


# ==================================
# RODAR
# ==================================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
