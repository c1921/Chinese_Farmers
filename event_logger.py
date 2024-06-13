from PyQt6.QtWidgets import QTextEdit

class EventLogger:
    def __init__(self):
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

    def append_log(self, log_entry):
        self.text_edit.append(log_entry)
