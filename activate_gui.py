"""Stardew Valley Expansion manager - gui toolkit specific code
"""
import sys
import os.path
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
            'Dit overzicht toont de namen van expansies die je kunt activeren',
            '(inclusief die al geactiveerd zijn).',
            'In de achterliggende configuratie is geregeld',
            'welke mods hiervoor aangezet moeten worden'))))
        vbox.addLayout(hbox)
        self.widgets = []
        for item in self.master.conf['Expansions']:
            hbox = qtw.QHBoxLayout()
            check = qtw.QCheckBox(item)
            hbox.addSpacing(100)
            hbox.addWidget(check)
            loc = self.master.conf['Mod Directories'][item].split(', ')[0]
            if os.path.exists(os.path.join(self.master.modbase, loc)):
                check.setChecked(True)
            hbox.addStretch()
            vbox.addLayout(hbox)
            self.widgets.append(check)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Check config', self)
        btn.clicked.connect(self.check)
        hbox.addWidget(btn)
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

    def check(self):
        "check for non-matching names in config file"
        results = self.master.check_config()
        qtw.QMessageBox.information(self, 'Check Config', '\n'.join(results))
