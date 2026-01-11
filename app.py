import os
os.environ["CLOUD_MODE"] = "true"

import dashboard_app
from cloud_service import CloudService

# troca SOMENTE a fonte de dados
dashboard_app.service = CloudService("production_history.db")

app = dashboard_app.app
server = app.server
