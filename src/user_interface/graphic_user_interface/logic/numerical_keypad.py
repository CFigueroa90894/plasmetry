""" G3 - Plasma Devs
Layer 4 - User Interface - Numerical Keypad
    <...>

author: <-------------------------
author: <-------------------------

status: DONE

Classes:
    NumericalKeypad

"""
# third-party imports
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt


class NumericalKeypad(QDialog):
    """<.........>
    
    Attributes:
        + current_value
        + display_label

    Methods:
        + __init__()
        + init_ui()
        + button_clicked()
        + confirm()
        + get_value()

    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Enter Value')
        self.setFixedSize(400, 600)
        self.current_value = ''
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.display_label = QLabel('0')
        self.display_label.setAlignment(Qt.AlignRight)
        self.display_label.setStyleSheet("font-size: 32px;")  # Larger for touch
        layout.addWidget(self.display_label)

        buttons_layout = QVBoxLayout()
        button_texts = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', '.', 'C']
        ]

        for row in button_texts:
            row_layout = QHBoxLayout()
            for text in row:
                button = QPushButton(text)
                button.setStyleSheet("font-size: 24px; padding: 20px;")  # Larger buttons for touch
                button.clicked.connect(self.button_clicked)
                row_layout.addWidget(button)
            buttons_layout.addLayout(row_layout)

        layout.addLayout(buttons_layout)

        confirm_button = QPushButton("Confirm")
        confirm_button.setStyleSheet("font-size: 24px; padding: 20px;")
        confirm_button.clicked.connect(self.confirm)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def button_clicked(self):
        button_text = self.sender().text()
        if button_text == 'C':
            self.current_value = ''
        else:
            self.current_value += button_text
        self.display_label.setText(self.current_value or '0')

    def confirm(self):
        self.accept()

    def get_value(self):
        try:
            return float(self.current_value)
        except ValueError:
            return 0.0
