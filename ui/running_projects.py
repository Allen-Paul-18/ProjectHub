# ============================================================
# RUNNING PROJECTS PANEL
# ============================================================

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class RunningProjects(QFrame):

    def __init__(self, process_manager, parent=None):
        super().__init__(parent)

        self.process_manager = process_manager
        self.setObjectName("RunningProjects")

        self.build_ui()

        # Refresh the running-project list every second.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

        self.refresh()

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        header = QHBoxLayout()

        title = QLabel("Running Projects")
        title.setObjectName("RunningProjectsTitle")

        self.count_label = QLabel("0 running")
        self.count_label.setObjectName("RunningProjectsCount")

        refresh_button = QPushButton("Refresh")
        refresh_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        refresh_button.clicked.connect(self.refresh)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.count_label)
        header.addWidget(refresh_button)

        layout.addLayout(header)

        self.projects_layout = QVBoxLayout()
        self.projects_layout.setSpacing(8)

        layout.addLayout(self.projects_layout)
        layout.addStretch()

    # --------------------------------------------------------
    # REFRESH
    # --------------------------------------------------------

    def refresh(self):
        running_names = self.process_manager.get_running_projects()

        # Remove the previous list.
        while self.projects_layout.count():
            item = self.projects_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.count_label.setText(
            f"{len(running_names)} running"
        )

        if not running_names:
            empty_label = QLabel(
                "No projects are currently running."
            )
            empty_label.setObjectName("RunningProjectsEmpty")
            self.projects_layout.addWidget(empty_label)
            return

        for name in running_names:
            self.add_project_row(name)

    # --------------------------------------------------------
    # PROJECT ROW
    # --------------------------------------------------------

    def add_project_row(self, project_name):
        row = QFrame()
        row.setObjectName("RunningProjectRow")

        layout = QHBoxLayout(row)
        layout.setContentsMargins(12, 10, 12, 10)

        status = QLabel("●")
        status.setStyleSheet("color: #58c994;")

        name_label = QLabel(project_name)
        name_label.setObjectName("RunningProjectName")

        stop_button = QPushButton("Stop")
        stop_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        stop_button.clicked.connect(
            lambda checked=False, name=project_name:
                self.stop_project(name)
        )

        layout.addWidget(status)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(stop_button)

        self.projects_layout.addWidget(row)

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    def stop_project(self, project_name):
        self.process_manager.stop(project_name)
        self.refresh()