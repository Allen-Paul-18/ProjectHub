# ============================================================
# MAIN WINDOW
# ============================================================

import json
from pathlib import Path

from PySide6.QtCore import Qt,QTimer
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QStackedWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core.process_manager import ProcessManager
from core.project_manager import ProjectManager

from ui.project_card import ProjectCard
from ui.console_panel import ConsolePanel
from ui.project_editor import ProjectEditor

from core.system_monitor import SystemMonitor
from ui.running_projects import RunningProjects

BASE_DIR = Path(__file__).parent
PROJECTS_FILE = BASE_DIR / "projects.json"

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.project_manager = ProjectManager()

        self.projects = self.project_manager.projects

        self.cards = {}

        self.setWindowTitle(
            "Project Hub"
        )

        self.resize(
            1350,
            900
        )

        self.process_manager = ProcessManager(
            self.append_console,
            self.update_project_status
        )

        self.system_monitor = SystemMonitor()

        self.build_ui()

        self.system_timer = QTimer(self)
        self.system_timer.timeout.connect(
            self.update_sidebar_stats
        )
        self.system_timer.start(2000)

        self.update_sidebar_stats()

    def update_sidebar_stats(self):
        stats = self.system_monitor.get_stats()

        self.sidebar_cpu.setText(
            f'{stats["cpu_percent"]:.0f}%'
        )

        self.sidebar_ram.setText(
            f'{stats["ram_percent"]:.0f}%'
        )

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def build_ui(self):

        root = QWidget()

        self.setCentralWidget(
            root
        )

        self.pages = QStackedWidget()

        main_layout = QHBoxLayout(
            root
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(
            0
        )

        # ====================================================
        # SIDEBAR
        # ====================================================

        # ============================================================
        # SIDEBAR
        # ============================================================

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 28, 20, 20)
        sidebar_layout.setSpacing(8)

        # ------------------------------------------------------------
        # LOGO
        # ------------------------------------------------------------

        logo = QLabel("PROJECT")
        logo.setObjectName("Logo")

        logo2 = QLabel("HUB")
        logo2.setObjectName("LogoAccent")

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(logo2)
        sidebar_layout.addSpacing(28)

        # ------------------------------------------------------------
        # WORKSPACE
        # ------------------------------------------------------------

        workspace_label = QLabel("WORKSPACE")
        workspace_label.setObjectName("SidebarSection")
        sidebar_layout.addWidget(workspace_label)

        self.sidebar_buttons = {}

        navigation_items = [
            ("Overview", "◈"),
            ("Running Projects", "●"),
        ]

        for name, icon in navigation_items:
            button = QPushButton(f"{icon}   {name}")
            button.setObjectName("SidebarButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            sidebar_layout.addWidget(button)
            self.sidebar_buttons[name] = button

        sidebar_layout.addSpacing(20)

        # ------------------------------------------------------------
        # SYSTEM
        # ------------------------------------------------------------

        system_label = QLabel("SYSTEM")
        system_label.setObjectName("SidebarSection")
        sidebar_layout.addWidget(system_label)

        # CPU
        cpu_row = QHBoxLayout()

        cpu_label = QLabel("CPU")
        cpu_label.setObjectName("SidebarInfoLabel")

        self.sidebar_cpu = QLabel("--%")
        self.sidebar_cpu.setObjectName("SidebarInfoValue")

        cpu_row.addWidget(cpu_label)
        cpu_row.addStretch()
        cpu_row.addWidget(self.sidebar_cpu)

        sidebar_layout.addLayout(cpu_row)

        # RAM
        ram_row = QHBoxLayout()

        ram_label = QLabel("RAM")
        ram_label.setObjectName("SidebarInfoLabel")

        self.sidebar_ram = QLabel("--%")
        self.sidebar_ram.setObjectName("SidebarInfoValue")

        ram_row.addWidget(ram_label)
        ram_row.addStretch()
        ram_row.addWidget(self.sidebar_ram)

        sidebar_layout.addLayout(ram_row)

        sidebar_layout.addSpacing(20)

        # ------------------------------------------------------------
        # DEVELOPER TOOLS
        # ------------------------------------------------------------

        tools_label = QLabel("DEVELOPER TOOLS")
        tools_label.setObjectName("SidebarSection")
        sidebar_layout.addWidget(tools_label)

        tool_items = [
            ("Terminals", "⌘"),
            ("Active Ports", "⇄"),
            ("Stop All Projects", "■"),
        ]

        for name, icon in tool_items:
            button = QPushButton(f"{icon}   {name}")
            button.setObjectName("SidebarButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            sidebar_layout.addWidget(button)
            self.sidebar_buttons[name] = button

        sidebar_layout.addStretch()

        # ------------------------------------------------------------
        # SETTINGS
        # ------------------------------------------------------------

        settings = QPushButton("⚙   Settings")
        settings.setObjectName("SidebarButton")
        settings.setCursor(Qt.CursorShape.PointingHandCursor)

        sidebar_layout.addWidget(settings)
        self.sidebar_buttons["Settings"] = settings

        # ====================================================
        # CONTENT
        # ====================================================

        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            35,
            30,
            35,
            25
        )

        content_layout.setSpacing(
            15
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QHBoxLayout()

        title = QLabel(
            "My Projects"
        )

        title.setObjectName(
            "Title"
        )

        search = QLineEdit()

        search.setPlaceholderText(
            "⌕  Search projects..."
        )

        search.setFixedWidth(
            320
        )

        search.setObjectName(
            "Search"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        add_button = QPushButton(
            "+  Add Project"
        )

        add_button.setObjectName(
            "AddProjectButton"
        )

        add_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        add_button.clicked.connect(
            self.add_project
        )

        header.addWidget(
            add_button
        )

        header.addWidget(
            search
        )

        content_layout.addLayout(
            header
        )

        self.subtitle = QLabel(
            f"{len(self.projects)} projects · "
            "Your personal development workspace"
        )

        self.subtitle.setObjectName(
            "Subtitle"
        )

        content_layout.addWidget(
            self.subtitle
        )

        # ====================================================
        # GRID
        # ====================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        container = QWidget()

        self.grid = QGridLayout(
            container
        )

        self.grid.setSpacing(
            18
        )

        self.build_project_cards()

        scroll.setWidget(
            container
        )

        content_layout.addWidget(
            scroll,
            1
        )

        # ====================================================
        # CONSOLE
        # ====================================================

        self.console = ConsolePanel()
        content_layout.addWidget(self.console)

        # ============================================================
        # PAGE STACK
        # ============================================================

        # Existing project screen becomes the Overview page.
        self.pages.addWidget(content)

        # Running Projects page
        running_page = QWidget()
        running_layout = QVBoxLayout(running_page)
        running_layout.setContentsMargins(25, 25, 25, 25)
        running_layout.setSpacing(15)

        running_title = QLabel("Running Projects")
        running_title.setObjectName("Title")

        running_subtitle = QLabel(
            "Monitor and manage your active processes"
        )
        running_subtitle.setObjectName("Subtitle")

        self.running_projects = RunningProjects(
            self.process_manager
        )

        running_layout.addWidget(running_title)
        running_layout.addWidget(running_subtitle)
        running_layout.addWidget(self.running_projects)
        running_layout.addStretch()

        self.pages.addWidget(running_page)

        # Sidebar navigation
        self.sidebar_buttons["Overview"].clicked.connect(
            lambda: self.pages.setCurrentWidget(content)
        )

        self.sidebar_buttons["Running Projects"].clicked.connect(
            lambda: self.pages.setCurrentWidget(running_page)
        )

        # Assemble the main window
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)


        search.textChanged.connect(
            self.filter_projects
        )

        self.apply_styles()

    # --------------------------------------------------------
    # CARDS
    # --------------------------------------------------------

    def build_project_cards(self):

        columns = 3

        for index, project in enumerate(
            self.projects
        ):

            row = index // columns
            column = index % columns

            card = ProjectCard(
                project
            )

            card.launch_requested.connect(
                self.launch_project
            )

            card.edit_requested.connect(
                self.edit_project
            )

            card.delete_requested.connect(
                self.delete_project
            )

            card.stop_requested.connect(
                self.stop_project
            )

            card.restart_requested.connect(
                self.restart_project
            )

            self.cards[
                project["name"]
            ] = card

            self.grid.addWidget(
                card,
                row,
                column
            )

    # --------------------------------------------------------
    # ADD PROJECT
    # --------------------------------------------------------

    def add_project(self):

        editor = ProjectEditor(
            parent=self
        )

        if editor.exec():

            new_project = editor.get_project()

            if self.project_manager.add_project(
                new_project
            ):

                self.projects = (
                    self.project_manager.projects
                )

                self.refresh_projects()

    # --------------------------------------------------------
    # EDIT PROJECT
    # --------------------------------------------------------

    def edit_project(
        self,
        project
    ):

        index = self.projects.index(
            project
        )

        editor = ProjectEditor(
            project,
            self
        )

        if editor.exec():

            updated_project = editor.get_project()

            if self.project_manager.update_project(
                index,
                updated_project
            ):

                self.projects = (
                    self.project_manager.projects
                )

                self.refresh_projects()

    # --------------------------------------------------------
    # REFRESH PROJECTS
    # --------------------------------------------------------

    def refresh_projects(self):

        self.cards.clear()

        while self.grid.count():

            item = self.grid.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()

        self.projects = self.project_manager.projects

        self.subtitle.setText(
            f"{len(self.projects)} projects · "
            "Your personal development workspace"
        )

        self.build_project_cards()

    # --------------------------------------------------------
    # DELETE PROJECT
    # --------------------------------------------------------

    def delete_project(self, project):

        name = project["name"]

        reply = QMessageBox.question(
            self,
            "Delete Project",
            f"Are you sure you want to remove '{name}' from Project Hub?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        if name in self.process_manager.processes:
            self.process_manager.stop(name)

        index = self.projects.index(project)

        if self.project_manager.delete_project(index):
            self.projects = self.project_manager.projects
            self.refresh_projects()

    # --------------------------------------------------------
    # LAUNCH
    # --------------------------------------------------------

    def launch_project(
        self,
        project
    ):

        self.process_manager.launch(
            project
        )

        self.update_project_status(
            project["name"],
            "Running"
        )

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    def stop_project(
        self,
        project
    ):

        self.process_manager.stop(
            project["name"]
        )

    # --------------------------------------------------------
    # RESTART
    # --------------------------------------------------------

    def restart_project(
        self,
        project
    ):

        self.process_manager.restart(
            project
        )

        self.update_project_status(
            project["name"],
            "Running"
        )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    def update_project_status(
        self,
        project_name,
        status
    ):

        card = self.cards.get(
            project_name
        )

        if card:

            card.set_status(
                status
            )

    # --------------------------------------------------------
    # CONSOLE
    # --------------------------------------------------------

    def append_console(
        self,
        text
    ):

        self.console.append(
            text
        )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    def filter_projects(
        self,
        text
    ):

        text = text.lower().strip()

        for project in self.projects:

            card = self.cards[
                project["name"]
            ]

            searchable = " ".join([
                project["name"],
                project["description"],
                project["category"]
            ]).lower()

            card.setVisible(
                text in searchable
            )

    # --------------------------------------------------------
    # STYLES
    # --------------------------------------------------------

    def apply_styles(self):

        self.setStyleSheet("""

            QMainWindow {
                background: #0d0f12;
            }

            QWidget {
                color: #e8eaed;
                font-family: "Segoe UI";
            }

            #Sidebar {
                background: #111318;
                border-right: 1px solid #24272d;
            }

            #Logo {
                font-size: 20px;
                font-weight: 700;
                letter-spacing: 3px;
                color: #ffffff;
            }

            #LogoAccent {
                font-size: 20px;
                font-weight: 700;
                letter-spacing: 3px;
                color: #7c5cff;
            }

            #AddProjectButton {
                background: #7c5cff;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                color: white;
                font-weight: 600;
            }

            #AddProjectButton:hover {
                background: #9075ff;
            }

            #AddProjectButton:pressed {
                background: #6848e8;
            }

            #SidebarButton {
                text-align: left;
                padding: 12px;
                border-radius: 8px;
                border: none;
                background: transparent;
                color: #a9adb5;
                font-size: 14px;
            }

            #SidebarButton:hover {
                background: #1b1e25;
                color: #ffffff;
            }

            #Title {
                font-size: 28px;
                font-weight: 700;
            }

            #Subtitle {
                color: #777c86;
                font-size: 13px;
            }

            #Search {
                background: #15181e;
                border: 1px solid #292d35;
                border-radius: 9px;
                padding: 10px 14px;
                color: #ffffff;
            }

            #Search:focus {
                border: 1px solid #7c5cff;
            }

            #ProjectCard {
                background: #15181e;
                border: 1px solid #242831;
                border-radius: 14px;
            }

            #ProjectCard:hover {
                border: 1px solid #3b4050;
                background: #181b21;
            }

            #ProjectName {
                color: #ffffff;
            }

            #Category {
                color: #8d73ff;
                font-size: 12px;
                font-weight: 600;
            }

            #Description {
                color: #858a94;
                font-size: 12px;
            }

            #Status {
                color: #777c86;
                font-size: 11px;
            }

            #LaunchButton {
                background: #7c5cff;
                border: none;
                border-radius: 8px;
                padding: 9px;
                color: white;
                font-weight: 600;
            }

            #LaunchButton:hover {
                background: #9075ff;
            }

            #LaunchButton:disabled {
                background: #383244;
                color: #77727f;
            }

            #StopButton {
                background: #20242b;
                border: none;
                border-radius: 8px;
                padding: 9px;
                color: #d1d4da;
                font-weight: 600;
            }

            #StopButton:hover {
                background: #30353e;
            }

            #StopButton:disabled {
                color: #555a63;
            }

            #MenuButton {
                background: transparent;
                border: none;
                color: #777c86;
                font-size: 20px;
                border-radius: 7px;
            }

            #MenuButton:hover {
                background: #252932;
                color: #ffffff;
            }

            QMenu {
                background: #181b21;
                border: 1px solid #30343d;
                padding: 6px;
            }

            QMenu::item {
                padding: 9px 25px 9px 12px;
                border-radius: 6px;
            }

            QMenu::item:selected {
                background: #292d36;
            }

            #ConsoleTitle {
                font-size: 13px;
                font-weight: 600;
                color: #aeb3bc;
            }

            #Console {
                background: #090b0e;
                border: 1px solid #20242b;
                border-radius: 10px;
                color: #c9cdd3;
                font-family: "Cascadia Mono", "Consolas";
                font-size: 12px;
                padding: 10px;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 8px;
            }

            QScrollBar::handle:vertical {
                background: #30343d;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: #454a55;
            }
            
            /* System resource monitoring */
            #SystemStats {
                background: #15181e;
                border: 1px solid #242831;
                border-radius: 12px;
            }

            #SystemStatsTitle {
                color: #aeb3bc;
                font-size: 12px;
                font-weight: 600;
            }

            #SystemStatsValue {
                color: #ffffff;
                font-size: 15px;
                font-weight: 700;
            }

            #SystemStatsDetails {
                color: #858a94;
                font-size: 11px;
            }

            #SystemStats QProgressBar {
                background: #292d35;
                border: none;
                border-radius: 4px;
            }

            #SystemStats QProgressBar::chunk {
                background: #7c5cff;
                border-radius: 4px;
            }

            #SidebarSection {
                color: #777c86;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                padding: 4px 2px;
            }

            #SidebarInfoLabel {
                color: #aeb3bc;
                font-size: 12px;
            }

            #SidebarInfoValue {
                color: #ffffff;
                font-size: 12px;
                font-weight: 600;
            }

            #SidebarButton {
                text-align: left;
                padding: 11px 10px;
                border-radius: 8px;
                border: none;
                background: transparent;
                color: #a9adb5;
                font-size: 12px;
            }

            #SidebarButton:hover {
                background: #1b1e25;
                color: #ffffff;
            }

            #SidebarButton:checked {
                background: #252033;
                color: #a38aff;
            }

        """)
