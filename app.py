from flask import Flask, render_template, jsonify, request
import pandas as pd
import sqlite3
import os
import requests

app = Flask(__name__)

ARQUIVO_EXCEL = "registros.xlsx"


# =========================
# BANCO SQLITE (FONTE CASCATA)
# =========================
def conectar():
    conn = sqlite3.connect("produtos.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# SHAREPOINT (OPCIONAL)
# =========================
TENANT_ID = "SEU_TENANT"
CLIENT_ID = "SEU_CLIENT_ID"
CLIENT_SECRET = "SEU_SECRET"
SITE_ID = "SEU_SITE_ID"
DRIVE_ID = "SEU_DRIVE_ID"


def get_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }

    r = requests.post(url, data=data)
    return r.json().get("access_token")


def upload_sharepoint(file_bytes, filename):

    try:
        token = get_token()

        url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root:/{filename}:/content"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream"
        }

        r = requests.put(url, headers=headers, data=file_bytes)

        if r.status_code in [200, 201]:
            return r.json().get("webUrl")

    except Exception as e:
        print("Erro SharePoint:", e)
        return None


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
        SELECT DISTINCT colecao FROM produtos ORDER BY colecao
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
# SALVAR (EXCEL + HISTÓRICO SEGURO)
# =========================
@app.route("/api/salvar", methods=["POST"])
def salvar():

    dados = request.form.to_dict()
    file = request.files.get("imagem")

    imagem_url = None

    # upload imagem
    if file:
        imagem_url = upload_sharepoint(file.read(), file.filename)

    nova_linha = {
        "feira": dados.get("feira"),
        "produto": dados.get("produto"),
        "modulacao": dados.get("modulacao"),

        "setor": dados.get("setor"),
        "classificacao": dados.get("classificacao"),
        "tipo": dados.get("melhoria"),

        "descricao": dados.get("descricao"),
        "imagem_url": imagem_url
    }

    # =========================
    # GARANTIR QUE NUNCA PERDE HISTÓRICO
    # =========================
    try:

        if os.path.exists(ARQUIVO_EXCEL):

            df = pd.read_excel(ARQUIVO_EXCEL)

            # adiciona nova linha sem sobrescrever
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)

        else:
            df = pd.DataFrame([nova_linha])

        # salva sempre acumulando histórico
        df.to_excel(ARQUIVO_EXCEL, index=False)

    except Exception as e:
        return jsonify({
            "status": "erro",
            "msg": str(e)
        })

    return jsonify({
        "status": "ok",
        "imagem": imagem_url
    })


# =========================
# START
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
