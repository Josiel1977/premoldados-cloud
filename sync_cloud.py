import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# 🔴 ORIGEM REAL DO BANCO (PC DA FÁBRICA)
DB_ORIG = Path(r"C:\Users\eletrica\Documents\Premoldados_SCADA\production_history.db")

# 🔵 REPOSITÓRIO CLOUD
REPO_PATH = Path(r"C:\Users\eletrica\Documents\Premoldados_SCADA\premoldados-cloud")
DB_DEST = REPO_PATH / "production_history.db"

def run(cmd):
    return subprocess.run(cmd, cwd=REPO_PATH, shell=True,
                          capture_output=True, text=True)

print("📦 Copiando banco...")
shutil.copy2(DB_ORIG, DB_DEST)

print("📌 Git add")
run("git add production_history.db")

status = run("git status --porcelain").stdout.strip()

if not status:
    print("ℹ️ Nenhuma alteração no banco. Nada para sincronizar.")
else:
    msg = f"sync db {datetime.now():%Y-%m-%d %H:%M:%S}"
    print(f"📝 Commit: {msg}")
    run(f'git commit -m "{msg}"')

    print("🚀 Git push")
    push = run("git push")

    if push.returncode == 0:
        print("✅ Banco sincronizado com a nuvem")
    else:
        print("❌ Erro no push:")
        print(push.stderr)
