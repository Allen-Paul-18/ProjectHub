# ============================================================
# CONSOLE PANEL
# ============================================================

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class ConsolePanel(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName(
            "ConsolePanel"
        )
        self.setMaximumHeight(200)
        self.setMinimumHeight(130)

        self.build_ui()

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            8
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QHBoxLayout()

        title = QLabel(
            "Console"
        )

        title.setObjectName(
            "ConsoleTitle"
        )

        clear_button = QPushButton(
            "Clear"
        )

        clear_button.setObjectName(
            "ConsoleButton"
        )

        clear_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        clear_button.clicked.connect(
            self.clear
        )

        header.addWidget(
            title
        )

        header.addStretch()

        header.addWidget(
            clear_button
        )

        layout.addLayout(
            header
        )

        # ----------------------------------------------------
        # TEXT OUTPUT
        # ----------------------------------------------------

        self.output = QTextEdit()

        self.output.setReadOnly(
            True
        )

        self.output.setObjectName(
            "Console"
        )

        self.output.setFont(
            QFont(
                "Cascadia Mono",
                10
            )
        )

        layout.addWidget(
            self.output
        )

    # --------------------------------------------------------
    # APPEND OUTPUT
    # --------------------------------------------------------

    def append(
        self,
        text
    ):

        self.output.moveCursor(
            self.output.textCursor().MoveOperation.End
        )

        self.output.insertPlainText(
            text
        )

        self.output.ensureCursorVisible()

    # --------------------------------------------------------
    # CLEAR
    # --------------------------------------------------------

    def clear(self):

        self.output.clear()

    # --------------------------------------------------------
    # SET TEXT
    # --------------------------------------------------------

    def set_text(
        self,
        text
    ):

        self.output.setPlainText(
            text
        )

        self.output.ensureCursorVisible()

    # --------------------------------------------------------
    # GET TEXT
    # --------------------------------------------------------

    def get_text(self):

        return self.output.toPlainText()