# ============================================================
# SYSTEM MONITOR
# ============================================================

import psutil


class SystemMonitor:

    def __init__(self):
        # Prime CPU measurement so the next reading is meaningful.
        psutil.cpu_percent(interval=None)

    # --------------------------------------------------------
    # CPU USAGE
    # --------------------------------------------------------

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=None)

    # --------------------------------------------------------
    # RAM USAGE
    # --------------------------------------------------------

    def get_ram_usage(self):
        memory = psutil.virtual_memory()

        return {
            "percent": memory.percent,
            "used_gb": memory.used / (1024 ** 3),
            "total_gb": memory.total / (1024 ** 3),
            "available_gb": memory.available / (1024 ** 3),
        }

    # --------------------------------------------------------
    # ALL SYSTEM STATS
    # --------------------------------------------------------

    def get_stats(self):
        ram = self.get_ram_usage()

        return {
            "cpu_percent": self.get_cpu_usage(),
            "ram_percent": ram["percent"],
            "ram_used_gb": ram["used_gb"],
            "ram_total_gb": ram["total_gb"],
            "ram_available_gb": ram["available_gb"],
        }