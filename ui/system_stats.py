# ============================================================
# SYSTEM STATS WIDGET
# ============================================================

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from core.system_monitor import SystemMonitor


class SystemStats(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.monitor = SystemMonitor()
        self.setObjectName("SystemStats")

        self.build_ui()
        self.refresh_stats()

        # Refresh system statistics every 2 seconds.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(2000)

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(20)

        # CPU
        cpu_layout = QVBoxLayout()

        cpu_header = QHBoxLayout()

        cpu_title = QLabel("CPU Usage")
        cpu_title.setObjectName("SystemStatsTitle")

        self.cpu_value = QLabel("0%")
        self.cpu_value.setObjectName("SystemStatsValue")

        cpu_header.addWidget(cpu_title)
        cpu_header.addStretch()
        cpu_header.addWidget(self.cpu_value)

        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setValue(0)
        self.cpu_bar.setTextVisible(False)
        self.cpu_bar.setFixedHeight(8)

        cpu_layout.addLayout(cpu_header)
        cpu_layout.addWidget(self.cpu_bar)

        # RAM
        ram_layout = QVBoxLayout()

        ram_header = QHBoxLayout()

        ram_title = QLabel("Memory Usage")
        ram_title.setObjectName("SystemStatsTitle")

        self.ram_value = QLabel("0%")
        self.ram_value.setObjectName("SystemStatsValue")

        ram_header.addWidget(ram_title)
        ram_header.addStretch()
        ram_header.addWidget(self.ram_value)

        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setValue(0)
        self.ram_bar.setTextVisible(False)
        self.ram_bar.setFixedHeight(8)

        self.ram_details = QLabel("Loading memory information...")
        self.ram_details.setObjectName("SystemStatsDetails")

        ram_layout.addLayout(ram_header)
        ram_layout.addWidget(self.ram_bar)
        ram_layout.addWidget(self.ram_details)

        layout.addLayout(cpu_layout, 1)
        layout.addLayout(ram_layout, 1)

    # --------------------------------------------------------
    # REFRESH STATS
    # --------------------------------------------------------

    def refresh_stats(self):
        stats = self.monitor.get_stats()

        cpu = round(stats["cpu_percent"])
        ram = round(stats["ram_percent"])

        self.cpu_value.setText(f"{cpu}%")
        self.cpu_bar.setValue(cpu)

        self.ram_value.setText(f"{ram}%")
        self.ram_bar.setValue(ram)

        self.ram_details.setText(
            f'{stats["ram_used_gb"]:.1f} GB used '
            f'of {stats["ram_total_gb"]:.1f} GB'
        )