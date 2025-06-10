from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit


class TextEdit(QTextEdit):
    def __init__(self, submit_callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submit_callback = submit_callback
        self.format_actions = {} 

    def keyPressEvent(self, event):
        key = event.key()
        ctrl = event.modifiers() & Qt.ControlModifier

        if key == Qt.Key_Tab and not event.modifiers() & Qt.ShiftModifier:
            if self.parent():
                self.parent().focusNextChild()
        elif key == Qt.Key_Tab and event.modifiers() & Qt.ShiftModifier:
            self.insertPlainText("\t")
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            if event.modifiers() & Qt.ShiftModifier:
                self.insertPlainText("\n")
            else:
                if self.submit_callback:
                    self.submit_callback()
        elif ctrl and key == Qt.Key_B:
            self.toggle_format('bold')
        elif ctrl and key == Qt.Key_I:
            self.toggle_format('italic')
        elif ctrl and key == Qt.Key_U:
            self.toggle_format('underline')
        elif ctrl and key == Qt.Key_T:
            self.format_actions.get('color')()
        else:
            super().keyPressEvent(event)
        self.update_action_states()

    def toggle_format(self, fmt_type):
        cursor = self.textCursor()
        fmt = cursor.charFormat()

        if fmt_type == 'bold':
            new_weight = QFont.Normal if fmt.fontWeight() > QFont.Normal else QFont.Bold
            fmt.setFontWeight(new_weight)
        elif fmt_type == 'italic':
            fmt.setFontItalic(not fmt.fontItalic())
        elif fmt_type == 'underline':
            fmt.setFontUnderline(not fmt.fontUnderline())

        cursor.setCharFormat(fmt)

    def update_action_states(self):
        fmt = self.currentCharFormat()
        if 'bold' in self.format_actions:
            self.format_actions['bold'].setChecked(fmt.fontWeight() > QFont.Normal)
        if 'italic' in self.format_actions:
            self.format_actions['italic'].setChecked(fmt.fontItalic())
        if 'underline' in self.format_actions:
            self.format_actions['underline'].setChecked(fmt.fontUnderline())

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.update_action_states()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.update_action_states()

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        self.update_action_states()