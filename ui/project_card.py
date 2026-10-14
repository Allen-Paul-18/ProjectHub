# ============================================================
# PROJECT CARD
# ============================================================

import subprocess
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)


class ProjectCard(QFrame):

    edit_requested = Signal(dict)
    launch_requested = Signal(dict)
    stop_requested = Signal(dict)
    restart_requested = Signal(dict)
    delete_requested = Signal(dict)

    def __init__(
        self,
        project
    ):

        super().__init__()

        self.project = project

        self.setObjectName(
            "ProjectCard"
        )

        self.setMinimumHeight(
            245
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            18,
            20,
            18
        )

        layout.setSpacing(
            7
        )

        # ----------------------------------------------------
        # TOP ROW
        # ----------------------------------------------------

        top = QHBoxLayout()

        icon = QLabel(
            project.get(
                "icon",
                "📦"
            )
        )

        icon.setFont(
            QFont(
                "Segoe UI Emoji",
                30
            )
        )

        top.addWidget(
            icon
        )

        top.addStretch()

        self.menu_button = QPushButton(
            "⋮"
        )

        self.menu_button.setObjectName(
            "MenuButton"
        )

        self.menu_button.setFixedSize(
            32,
            32
        )

        self.menu_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.menu_button.clicked.connect(
            self.show_menu
        )

        top.addWidget(
            self.menu_button
        )

        layout.addLayout(
            top
        )

        # ----------------------------------------------------
        # NAME
        # ----------------------------------------------------

        name = QLabel(
            project["name"]
        )

        name.setObjectName(
            "ProjectName"
        )

        name.setFont(
            QFont(
                "Segoe UI",
                16,
                QFont.Weight.Bold
            )
        )

        layout.addWidget(
            name
        )

        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        category = QLabel(
            project["category"]
        )

        category.setObjectName(
            "Category"
        )

        layout.addWidget(
            category
        )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = QLabel(
            project["description"]
        )

        description.setObjectName(
            "Description"
        )

        description.setWordWrap(
            True
        )

        layout.addWidget(
            description
        )

        layout.addStretch()

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status = QLabel(
            "● Ready"
        )

        self.status.setObjectName(
            "Status"
        )

        layout.addWidget(
            self.status
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        buttons = QHBoxLayout()

        self.launch_button = QPushButton(
            "▶  Launch"
        )

        self.launch_button.setObjectName(
            "LaunchButton"
        )

        self.stop_button = QPushButton(
            "■  Stop"
        )

        self.stop_button.setObjectName(
            "StopButton"
        )

        self.stop_button.setEnabled(
            False
        )

        self.launch_button.clicked.connect(
            lambda:
            self.launch_requested.emit(
                self.project
            )
        )

        self.stop_button.clicked.connect(
            lambda:
            self.stop_requested.emit(
                self.project
            )
        )

        buttons.addWidget(
            self.launch_button
        )

        buttons.addWidget(
            self.stop_button
        )

        layout.addLayout(
            buttons
        )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    def set_status(
        self,
        status
    ):

        self.status.setText(
            f"● {status}"
        )

        running = status in (
            "Running",
            "Starting..."
        )

        self.launch_button.setEnabled(
            not running
        )

        self.stop_button.setEnabled(
            running
        )

    # --------------------------------------------------------
    # MENU
    # --------------------------------------------------------

    def show_menu(self):

        menu = QMenu(
            self
        )

        edit_action = menu.addAction(
            "Edit Project"
        )

        edit_action.triggered.connect(
            lambda: self.edit_requested.emit(
                self.project
            )
        )

        open_folder = menu.addAction(
            "📂  Open Folder"
        )

        terminal = menu.addAction(
            "💻  Open Terminal"
        )

        vscode = menu.addAction(
            "📝  Open VS Code"
        )

        menu.addSeparator()

        restart = menu.addAction(
            "🔄  Restart"
        )

        delete = menu.addAction("🗑️  Delete Project")

        action = menu.exec(
            self.menu_button.mapToGlobal(
                self.menu_button.rect().bottomLeft()
            )
        )

        if action == open_folder:

            self.open_folder()

        elif action == terminal:

            self.open_terminal()

        elif action == vscode:

            self.open_vscode()

        elif action == restart:

            self.restart_requested.emit(
                self.project
            )
        elif action == delete:
            self.delete_requested.emit(self.project)

    # --------------------------------------------------------
    # OPEN FOLDER
    # --------------------------------------------------------

    def open_folder(self):

        path = Path(
            self.project["path"]
        )

        if not path.exists():

            QMessageBox.warning(
                self,
                "Project Not Found",
                f"The project folder does not exist:\n\n{path}"
            )

            return

        subprocess.Popen(
            [
                "explorer",
                str(path)
            ]
        )

    # --------------------------------------------------------
    # OPEN TERMINAL
    # --------------------------------------------------------

    def open_terminal(self):

        path = Path(
            self.project["path"]
        )

        if not path.exists():

            QMessageBox.warning(
                self,
                "Project Not Found",
                f"The project folder does not exist:\n\n{path}"
            )

            return

        subprocess.Popen(
            [
                "cmd.exe",
                "/K",
                f'cd /d "{path}"'
            ]
        )

    # --------------------------------------------------------
    # OPEN VS CODE
    # --------------------------------------------------------

    def open_vscode(self):

        path = Path(
            self.project["path"]
        )

        if not path.exists():

            QMessageBox.warning(
                self,
                "Project Not Found",
                f"The project folder does not exist:\n\n{path}"
            )

            return

        try:

            subprocess.Popen(
                [
                    "code",
                    str(path)
                ]
            )

        except FileNotFoundError:

            QMessageBox.warning(
                self,
                "VS Code Not Found",
                "The 'code' command was not found.\n\n"
                "Make sure VS Code is installed and "
                "the 'code' command is available."
            )