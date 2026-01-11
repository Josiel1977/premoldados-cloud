import os
import sqlite3
import requests
import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

# =============================
# CONFIG
# =============================
DB_FILE = "production_history.db"
GITHUB_RAW_URL = os.getenv(
    "GITHUB_RAW_URL",
    "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/production_history.db"
)

# =============================
# BAIXAR BANCO
# =============================
def download_db():
    try:
        r = requests.get(GITHUB_RAW_URL, timeout=20)
        r.raise_for_status()
        with open(DB_FILE, "wb") as f:
            f.write(r.content)
        print("✅ Banco baixado com sucesso")
    except Exception as e:
        print("⚠️ Falha ao baixar banco:", e)

download_db()

# =============================
# LER DADOS
# =============================
def load_data():
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql("SELECT * FROM production_cycles", conn)
        conn.close()
        return df
    except Exception as e:
        print("Erro ao ler banco:", e)
        return pd.DataFrame()

df = load_data()

# =============================
# DASH APP
# =============================
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    title="Central da Estrutura (Cloud)"
)

server = app.server  # 👈 ESSENCIAL PARA O RAILWAY

# =============================
# LAYOUT
# =============================
if df.empty:
    content = dbc.Alert("Nenhum dado disponível.", color="warning")
else:
    fig = px.bar(
        df.groupby("setor", as_index=False)["volume_m3"].sum(),
        x="setor",
        y="volume_m3",
        title="Volume Produzido por Setor (m³)"
    )
    fig.update_layout(
        plot_bgcolor="#222",
        paper_bgcolor="#222",
        font_color="white"
    )

    content = dcc.Graph(figure=fig)

app.layout = dbc.Container(
    [
        html.H2("🏭 Central da Estrutura – Cloud", className="text-center my-3"),
        html.P("Visualização em nuvem (somente leitura)", className="text-center text-muted"),
        html.Hr(),
        content
    ],
    fluid=True
)

# =============================
# RUN LOCAL
# =============================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False
    )
