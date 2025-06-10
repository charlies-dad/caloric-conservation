from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QLabel, QCheckBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QAction, QToolBar, QColorDialog
)
from objects.TextEdit import TextEdit
from objects.TabKeyFilter import TabKeyFilter

from util.plaid import plaid
from util.dialog_css import css

class Dialog(QDialog):
    def __init__(self, html):
        super().__init__()
        self.html = html

        self.init_dialog()

        self.set_title()
        self.set_html_edit()      
        self.setup_toolbar()
        self.setup_plaid() #input1_layout     
        self.setup_additional_info() #input2_layout 
        self.setup_submit_row() #submit_row_layout

        self.build()
        
    def setup_toolbar(self):
        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet("font-size: 24px; background-color: #2e2e2e; color: white; border: none;")
        bold_action = QAction("Bold", self)
        bold_action.setCheckable(True)
        bold_action.setShortcut("Ctrl+B")
        bold_action.triggered.connect(lambda: self.html_edit.toggle_format('bold'))
        self.toolbar.addAction(bold_action)

        italic_action = QAction("Italic", self)
        italic_action.setCheckable(True)
        italic_action.setShortcut("Ctrl+I")
        italic_action.triggered.connect(lambda: self.html_edit.toggle_format('italic'))
        self.toolbar.addAction(italic_action)

        underline_action = QAction("Underline", self)
        underline_action.setCheckable(True)
        underline_action.setShortcut("Ctrl+U")
        underline_action.triggered.connect(lambda: self.html_edit.toggle_format('underline'))
        self.toolbar.addAction(underline_action)

        color_action = QAction("Text Color", self)
        color_action.setShortcut("Ctrl+T")

        def pick_color():
            color = QColorDialog.getColor()
            if color.isValid():
                self.html_edit.setTextColor(color)

        color_action.triggered.connect(pick_color)
        self.toolbar.addAction(color_action)

        # Link actions back to text editor
        self.html_edit.format_actions = {
            'bold': bold_action,
            'italic': italic_action,
            'underline': underline_action,
            'color': pick_color
        }
        
    def init_dialog(self):
        self.standup = (
            "<style>br { line-height: 500%; }</style>"
            "<div style=\"background: #36393e; padding: 10px; border-radius: 12px; color: white; font-size: 28px;\">"
            + self.html +
            "</div>"
        )
        self.setWindowTitle("Caloric Conservation")
        self.setFixedWidth(1200)
        self.setStyleSheet(css)
        
    def set_title(self):
        date = datetime.strftime(datetime.now(), "%A %B %d, %Y")
        self.title_label = QLabel("<u><h2>Standup : " + date + "</h2></u><br/>")
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #f0f0f0;
            margin-top: 4px;
            margin-bottom: 4px;
        """)

    def set_html_edit(self):
        self.html_edit = TextEdit(submit_callback=self.accept)
        self.html_edit.submit_callback = self.accept  # Connect Enter to submit
        self.tab_filter = TabKeyFilter()
        self.html_edit.installEventFilter(self.tab_filter)

        self.html_edit.setAcceptRichText(True)
        self.html_edit.setHtml(self.standup)
        self.html_edit.setStyleSheet("font-size: 16px; background-color: #3a3a3a; color: #ffffff; padding: 8px; border-radius: 8px;")
        
        self.html_edit.setFixedHeight(500)
        
    def setup_plaid(self):
        self.label1 = QLabel()
        self.label1.setText(plaid)
        self.label1.setTextFormat(Qt.RichText)
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(True) 
        self.input1 = QLineEdit()
        self.label1.setStyleSheet("font-size: 28px;")
        self.input1.setStyleSheet("font-size: 28px; padding: 6px;")
        self.checkbox.setStyleSheet("margin: 0 10px;")
        self.input1_layout = QHBoxLayout()
        self.input1_layout.addWidget(self.label1)
        self.input1_layout.addWidget(self.checkbox)
        self.input1_layout.addWidget(self.input1)
        
    def setup_additional_info(self):
        self.label2 = QLabel("Additional Info: ")
        self.label2.setStyleSheet("font-size: 28px;")
        self.input2 = QLineEdit()
        self.input2.setStyleSheet("font-size: 28px; padding: 6px;")
        self.input2_layout = QHBoxLayout()
        self.input2_layout.addWidget(self.label2)
        self.input2_layout.addWidget(self.input2)
        
    def setup_submit_row(self):
        submit_button = QPushButton("Submit")
        submit_button.setMinimumHeight(40)
        submit_button.setMinimumWidth(120)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #5a5a5a;
                font-size: 28px;  
                color: #ffffff;
                padding: 10px 20px;  
                border-radius: 8px;
                font-size: 18px;  
                min-width: 120px; 
                min-height: 40px; 
            }
            QPushButton:hover {
                background-color: #777777;
            }
        """)
        submit_button.setDefault(True)
        submit_button.clicked.connect(self.accept)
        self.labelCopy = QLabel()
        self.labelCopy.setText("<h3>Copy Standup to clipboard</h3>")
        self.labelCopy.setTextFormat(Qt.RichText)
        self.checkboxCopy = QCheckBox()
        self.checkboxCopy.setChecked(True) 
        self.checkboxCopy.setStyleSheet("margin: 0 10px;")
        
        self.labelTeams = QLabel()
        self.labelTeams.setText("<h3>Post in SD Standups Teams Channel</h3>")
        self.labelTeams.setTextFormat(Qt.RichText)
        self.checkboxTeams = QCheckBox()
        self.checkboxTeams.setChecked(True) 
        self.checkboxTeams.setStyleSheet("margin: 0 10px;")
        
        self.submit_row_layout = QHBoxLayout()
        self.submit_row_layout.addWidget(self.labelCopy)
        self.submit_row_layout.addWidget(self.checkboxCopy)
        self.submit_row_layout.addWidget(self.labelTeams)
        self.submit_row_layout.addWidget(self.checkboxTeams)
        self.submit_row_layout.addWidget(submit_button)

    def build(self):
        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.addWidget(self.title_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.html_edit)
        layout.addLayout(self.input1_layout)
        layout.addLayout(self.input2_layout)
        layout.addLayout(self.submit_row_layout)
        self.setLayout(layout)

    def get_data(self):
        html = self.html_edit.toHtml()

        # Remove background + padding styles
        html = html.replace(
            '<style>br { line-height: 500%; }</style>'
            '<div style="background: #36393e; padding: 10px; border-radius: 12px; color: white; font-size: 28px;">',
            ''
        ).replace("</div>", "")

        html = html[html.index("<a href") :html.rfind("</p>")]
                
        import re
        html = re.sub(r'font-size:\s*\d+px;', '', html, flags=re.IGNORECASE)
        html = re.sub(r'(?:background(?:-color)?|color):\s*(?:#fff(?:fff)?|rgb\(255,\s*255,\s*255\)|white)\s*;?', '', html, flags=re.IGNORECASE)

        return html, self.checkbox.isChecked(), self.input1.text(), self.input2.text(), self.checkboxCopy.isChecked(), self.checkboxTeams.isChecked()