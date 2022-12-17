"""Stardew Valley Expansion manager - gui toolkit specific code
"""
import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qgui


class ShowMods(qtw.QWidget):
    "GUI presenting the available mods/extensions to make selection possible of mods to (de)activate"
    def __init__(self, master):
        self.master = master
        self.master.modnames = []
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        self.setup_screen()

    def setup_screen(self):
        "define the screen elements"
        self.setWindowTitle('Select Expansions to activate')
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('\n'.join((
            'Dit overzicht toont de namen van expansies die je kunt activeren.',
            'In de achterliggende configuratie is geregeld',
            'welke mods hiervoor aangezet moeten worden'))))
        vbox.addLayout(hbox)
        self.widgets = []
        for item in self.master.conf['Expansions']:
            hbox = qtw.QHBoxLayout()
            check = qtw.QCheckBox(item)
            hbox.addSpacing(100)
            hbox.addWidget(check)
            hbox.addStretch()
            vbox.addLayout(hbox)
            self.widgets.append(check)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Klaar, activeren maar', self)
        btn.clicked.connect(self.confirm)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Afbreken', self)
        btn.clicked.connect(self.close)
        hbox.addWidget(btn)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def show_screen(self):
        "finish the screen setup, show the screen and start the event loop"
        do = qgui.QAction('Done', self)
        do.triggered.connect(self.confirm)
        do.setShortcut('Ctrl+Enter')
        self.addAction(do)
        dont = qgui.QAction('Cancel', self)
        dont.triggered.connect(self.close)
        dont.setShortcut('Escape')
        self.addAction(dont)
        self.show()
        return self.app.exec()  # niet via sys.exit() want we zijn nog niet klaar

    def confirm(self):
        "build a list from the checked entriesi and pass it back to the caller, then close the gui"
        self.master.modnames = [x.text() for x in self.widgets if x.isChecked()]
        self.close()