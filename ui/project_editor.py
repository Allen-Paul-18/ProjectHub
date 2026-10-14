# ============================================================
# PROJECT EDITOR
# ============================================================

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)


class ProjectEditor(QDialog):

    def __init__(
        self,
        project=None,
        parent=None
    ):

        super().__init__(parent)

        self.project = project

        self.setWindowTitle(
            "Edit Project"
            if project
            else "Add Project"
        )

        self.setMinimumWidth(
            520
        )

        self.build_ui()

        if project:

            self.load_project(
                project
            )

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            24,
            24,
            24,
            24
        )

        layout.setSpacing(
            16
        )

        form = QFormLayout()

        form.setSpacing(
            12
        )

        # ----------------------------------------------------
        # NAME
        # ----------------------------------------------------

        self.name_input = QLineEdit()

        self.name_input.setPlaceholderText(
            "Project name"
        )

        form.addRow(
            "Name",
            self.name_input
        )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        self.description_input = QLineEdit()

        self.description_input.setPlaceholderText(
            "Short project description"
        )

        form.addRow(
            "Description",
            self.description_input
        )

        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        self.category_input = QLineEdit()

        self.category_input.setPlaceholderText(
            "e.g. AI / ML"
        )

        form.addRow(
            "Category",
            self.category_input
        )

        # ----------------------------------------------------
        # ICON
        # ----------------------------------------------------

        self.icon_input = QLineEdit()

        self.icon_input.setPlaceholderText(
            "🧠"
        )

        form.addRow(
            "Icon",
            self.icon_input
        )

        # ----------------------------------------------------
        # PATH
        # ----------------------------------------------------

        path_layout = QHBoxLayout()

        self.path_input = QLineEdit()

        self.path_input.setPlaceholderText(
            "Project folder"
        )

        browse_button = QPushButton(
            "Browse"
        )

        browse_button.clicked.connect(
            self.browse_path
        )

        path_layout.addWidget(
            self.path_input
        )

        path_layout.addWidget(
            browse_button
        )

        form.addRow(
            "Path",
            path_layout
        )

        # ----------------------------------------------------
        # TYPE
        # ----------------------------------------------------

        self.type_input = QComboBox()

        self.type_input.addItems(
            [
                "python",
                "node",
                "flutter",
                "java",
                "custom"
            ]
        )

        self.type_input.currentTextChanged.connect(
            self.update_venv_visibility
        )

        form.addRow(
            "Type",
            self.type_input
        )

        # ----------------------------------------------------
        # COMMAND
        # ----------------------------------------------------

        self.command_input = QLineEdit()

        self.command_input.setPlaceholderText(
            "e.g. main.py or npm run dev"
        )

        form.addRow(
            "Command",
            self.command_input
        )

        # ----------------------------------------------------
        # VIRTUAL ENVIRONMENT
        # ----------------------------------------------------

        venv_layout = QHBoxLayout()

        self.venv_input = QLineEdit()

        self.venv_input.setPlaceholderText(
            "E:/venv"
        )

        venv_browse_button = QPushButton(
            "Browse"
        )

        venv_browse_button.clicked.connect(
            self.browse_venv
        )

        venv_layout.addWidget(
            self.venv_input
        )

        venv_layout.addWidget(
            venv_browse_button
        )

        self.venv_row = venv_layout

        form.addRow(
            "Virtual Environment",
            venv_layout
        )

        layout.addLayout(
            form
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self.save
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(
            buttons
        )

        self.update_venv_visibility(
            self.type_input.currentText()
        )

    # --------------------------------------------------------
    # LOAD EXISTING PROJECT
    # --------------------------------------------------------

    def load_project(
        self,
        project
    ):

        self.name_input.setText(
            project.get(
                "name",
                ""
            )
        )

        self.description_input.setText(
            project.get(
                "description",
                ""
            )
        )

        self.category_input.setText(
            project.get(
                "category",
                ""
            )
        )

        self.icon_input.setText(
            project.get(
                "icon",
                ""
            )
        )

        self.path_input.setText(
            project.get(
                "path",
                ""
            )
        )

        project_type = project.get(
            "type",
            "python"
        )

        index = self.type_input.findText(
            project_type
        )

        if index >= 0:

            self.type_input.setCurrentIndex(
                index
            )

        self.command_input.setText(
            project.get(
                "command",
                ""
            )
        )

        self.venv_input.setText(
            project.get(
                "venv",
                ""
            )
        )

    # --------------------------------------------------------
    # BROWSE PROJECT
    # --------------------------------------------------------

    def browse_path(self):

        path = QFileDialog.getExistingDirectory(
            self,
            "Select Project Folder"
        )

        if path:

            self.path_input.setText(
                path
            )

    # --------------------------------------------------------
    # BROWSE VENV
    # --------------------------------------------------------

    def browse_venv(self):

        path = QFileDialog.getExistingDirectory(
            self,
            "Select Virtual Environment"
        )

        if path:

            self.venv_input.setText(
                path
            )

    # --------------------------------------------------------
    # VENV VISIBILITY
    # --------------------------------------------------------

    def update_venv_visibility(
        self,
        project_type
    ):

        is_python = (
            project_type == "python"
        )

        label = self.layout().itemAt(
            0
        )

        if label:

            form = label.layout()

            if form:

                venv_label = form.labelForField(
                    self.venv_input
                )

                if venv_label:

                    venv_label.setVisible(
                        is_python
                    )

        self.venv_input.setVisible(
            is_python
        )

        for i in range(
            self.venv_row.count()
        ):

            widget = self.venv_row.itemAt(
                i
            ).widget()

            if widget:

                widget.setVisible(
                    is_python
                )

    # --------------------------------------------------------
    # VALIDATE
    # --------------------------------------------------------

    def validate(self):

        name = self.name_input.text().strip()

        path = self.path_input.text().strip()

        project_type = self.type_input.currentText()

        if not name:

            QMessageBox.warning(
                self,
                "Missing Name",
                "Please enter a project name."
            )

            return False

        if not path:

            QMessageBox.warning(
                self,
                "Missing Path",
                "Please select the project folder."
            )

            return False

        if not Path(path).exists():

            QMessageBox.warning(
                self,
                "Invalid Path",
                "The selected project folder does not exist."
            )

            return False

        if project_type != "java":

            if not self.command_input.text().strip():

                QMessageBox.warning(
                    self,
                    "Missing Command",
                    "Please enter a launch command."
                )

                return False

        return True

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self):

        if not self.validate():

            return

        project = {
            "name": self.name_input.text().strip(),
            "description": self.description_input.text().strip(),
            "category": self.category_input.text().strip(),
            "icon": self.icon_input.text().strip(),
            "path": self.path_input.text().strip(),
            "type": self.type_input.currentText(),
            "command": self.command_input.text().strip(),
        }

        venv = self.venv_input.text().strip()

        if (
            self.type_input.currentText()
            == "python"
            and venv
        ):

            project["venv"] = venv

        self.project = project

        self.accept()

    # --------------------------------------------------------
    # GET RESULT
    # --------------------------------------------------------

    def get_project(self):

        return self.project
