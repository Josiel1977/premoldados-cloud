import os
import sqlite3
import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

DB_PATH = "production_history.db"

app = Dash(__name__)
server = app.server

def load_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame(columns=["timestamp", "setor", "volume_m3"])
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT timestamp, setor, volume_m3 FROM production_cycles", conn)
    conn.close()
    return df

app.layout = html.Div([
    html.H2("🏭 Central da Estrutura — Cloud"),
    dcc.Interval(id="refresh", interval=30_000, n_intervals=0),
    dcc.Graph(id="grafico")
])

@app.callback(
    dcc.Output("grafico", "figure"),
    dcc.Input("refresh", "n_intervals")
)
def atualizar(_):
    df = load_data()
    if df.empty:
        return px.bar(title="Sem dados ainda")
    return px.bar(
        df.groupby("setor")["volume_m3"].sum().reset_index(),
        x="setor", y="volume_m3",
        title="Produção acumulada por setor (m³)"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8050)))
