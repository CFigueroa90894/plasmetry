""" G3 - Plasma Devs
Layer 4 - User Interface - Virtual Keyboard
    <...>

author: <-------------------------
author: <-------------------------

status: DONE

Classes:
    VirtualKeyboard

"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class VirtualKeyboard(QDialog):
    """<...>
    
    Attributes:
        + layout
        + input_text
        + display_text
        + keyboard_layout
        + current_mode
        + shift_mode
        + lowercase_letters
        + uppercase_letters
        + special_chars
        + action_button_layout
        + shift_button
        + switch_button
        + confirm_button
        * cancel_button

    Methods:
        + __init__()
        + load_buttons()
        + clear_keyboard_layout()
        + toggle_shift()
        + switch_characters()
        + add_character()
        + get_input_text()
        + key_pressed()
        + confirm_input()
    
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set the size of the dialog to match the main UI size
        self.setFixedSize(parent.width(), parent.height())

        # Update the background color of the dialog
        self.setStyleSheet("background-color: #fffcfc;")  # Changed background color

        # Layout setup
        self.setWindowTitle("Virtual Keyboard")
        self.layout = QVBoxLayout(self)

        # Store the input text
        self.input_text = ""

        # Create the display text field
        self.display_text = QLineEdit(self)
        self.display_text.setMinimumHeight(int(self.height() * 0.1)) # Make the text field take up 10% of the height
        self.display_text.setStyleSheet("font-size: 24px; border: 2px solid #4d5bbe;")
        self.layout.addWidget(self.display_text)

        # Keyboard layout (where the keys are placed)
        self.keyboard_layout = QVBoxLayout()
        self.layout.addLayout(self.keyboard_layout)

        # Track the current mode (letters, special chars, and shift for uppercase/lowercase)
        self.current_mode = "letters"
        self.shift_mode = False

        # Define the buttons for letters and special characters
        self.lowercase_letters = ["0123456789", "qwertyuiop", "asdfghjkl", "zxcvbnm"]
        self.uppercase_letters = ["0123456789", "QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        self.special_chars = ["!@#$%^&*()", "-_=+[]{}"]

        # Initially load lowercase letters
        self.load_buttons(self.lowercase_letters)

        # Add a horizontal layout for shift and 123 buttons
        self.action_button_layout = QHBoxLayout()

        # Shift button to toggle between uppercase and lowercase letters
        self.shift_button = QPushButton("Shift", self)
        self.shift_button.setStyleSheet("font-size: 20px; padding: 10px; background-color: #403c3c; color: white;")
        self.shift_button.clicked.connect(self.toggle_shift)
        self.action_button_layout.addWidget(self.shift_button)

        # 123 button to switch between letters and special characters
        self.switch_button = QPushButton("123", self)
        self.switch_button.setStyleSheet("font-size: 20px; padding: 10px; background-color: #403c3c; color: white;")
        self.switch_button.clicked.connect(self.switch_characters)
        self.action_button_layout.addWidget(self.switch_button)

        # Add the layout for the shift and 123 buttons to the main layout
        self.layout.addLayout(self.action_button_layout)

        # Add Confirm and Cancel buttons in a horizontal layout
        self.confirm_cancel_button_layout = QHBoxLayout()

        # Confirm button with increased size and text
        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.setStyleSheet("font-size: 20px; padding: 10px; background-color: #403c3c; color: white;")
        self.confirm_button.clicked.connect(self.accept)

        # Cancel button to close dialog without making changes
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setStyleSheet("font-size: 20px; padding: 10px; background-color: #403c3c; color: white;")
        self.cancel_button.clicked.connect(self.reject)  # Reject changes
        
        # Add both buttons to a horizontal layout
        self.confirm_cancel_button_layout.addWidget(self.cancel_button)
        self.confirm_cancel_button_layout.addWidget(self.confirm_button)

        # Add the confirm and cancel buttons layout to the main layout
        self.layout.addLayout(self.confirm_cancel_button_layout)

    def load_buttons(self, characters):
        """Load the buttons for the keyboard layout."""
        # Clear the layout first to remove any previous characters
        self.clear_keyboard_layout()

        # Add buttons to the layout for each character
        button_size = int(self.width() * 0.08)  # Button size based on dialog width (e.g., 8% of width)
        font_size = max(16, int(button_size * 0.4))  # Dynamically calculate font size (40% of button size)

        for row in characters:
            row_layout = QHBoxLayout()
            for char in row:
                button = QPushButton(char.replace("&", "&&"), self)
                button.setFixedSize(button_size, button_size)  # Set fixed size based on calculated button size
                button.setStyleSheet(f"font-size: {font_size}px; background-color: #505cbc; color: white; border-radius: 5px;")  # Adjust font size
                button.clicked.connect(lambda ch, char=char: self.add_character(char))
                row_layout.addWidget(button)
            self.keyboard_layout.addLayout(row_layout)

    def clear_keyboard_layout(self):
        """Clear the current keyboard layout before switching characters."""
        while self.keyboard_layout.count():
            child = self.keyboard_layout.takeAt(0)
            if child.layout():
                while child.layout().count():
                    widget = child.layout().takeAt(0).widget()
                    if widget:
                        widget.deleteLater()
            elif child.widget():
                child.widget().deleteLater()

    def toggle_shift(self):
        """Toggle between uppercase and lowercase letters."""
        if self.current_mode == "letters":
            if not self.shift_mode:
                # Switch to uppercase letters
                self.load_buttons(self.uppercase_letters)
                self.shift_mode = True
            else:
                # Switch back to lowercase letters
                self.load_buttons(self.lowercase_letters)
                self.shift_mode = False

    def switch_characters(self):
        """Switch between letters and special characters."""
        if self.current_mode == "letters":
            # Switch to special characters and hide the shift button
            self.load_buttons(self.special_chars)
            self.current_mode = "special"
            self.switch_button.setText("ABC")
            self.shift_button.hide()  # Hide the shift button
        else:
            # Switch back to letters and show the shift button again
            if self.shift_mode:
                self.load_buttons(self.uppercase_letters)
            else:
                self.load_buttons(self.lowercase_letters)
            self.current_mode = "letters"
            self.switch_button.setText("123")
            self.shift_button.show()  # Show the shift button again

    def add_character(self, char):
        """Add a character to the display."""
        self.display_text.insert(char)

    # Method to return the current input text
    def get_input_text(self):
        return self.display_text.text()

    def key_pressed(self, char):
        """Append character to the display text."""
        current_text = self.display_text.text()
        new_text = current_text + char
        self.display_text.setText(new_text)
        self.input_text = new_text  # Update input_text as well

    def confirm_input(self):
        """Close the dialog when the user confirms input."""
        self.accept()
