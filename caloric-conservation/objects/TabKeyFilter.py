from PyQt5.QtCore import Qt, QObject

class TabKeyFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress and event.key() == Qt.Key_Tab:
            obj.parentWidget().focusNextChild()
            return True
        return super().eventFilter(obj, event)