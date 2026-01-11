# premoldados-cloud/cloud_service.py
import sqlite3

class CloudService:
    def __init__(self, db_path):
        self.db_path = db_path

    def start_monitoring(self): pass
    def stop_monitoring(self): pass
    def force_read(self): return False

    def test_connection(self):
        return {"success": False, "message": "Modo nuvem"}

    def get_realtime_data_public(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(volume_m3) FROM production_cycles")
        vol_total = cursor.fetchone()[0] or 0

        conn.close()

        return {
            "plc_online": False,
            "status_m35": False,
            "vol_total_acumulado": vol_total,
            "vol_total_ciclo": 0,
            "total_ciclos": 0,
            "volumes_setor": {},
            "estoque_clp": {},
            "receita_atual": {},
            "status_setores": {},
            "service_status": {
                "plc_online": False,
                "modbus_connected": False,
                "simulation_mode": True,
                "cycles_saved": 0
            }
        }
