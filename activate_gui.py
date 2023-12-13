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

    def setup_screen(self):
        "define the screen elements"
        self.setWindowTitle('Select expansions/mods to activate')
        self.vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Dit overzicht toont de namen van expansies die je kunt activeren\n'
                                  '(inclusief die al geactiveerd zijn).\n'
                                  'In de achterliggende configuratie is geregeld welke mods\n'
                                  'hiervoor eventueel nog meer aangezet moeten worden'))
        self.vbox.addLayout(hbox)
        self.widgets = {}
        self.refresh_widgets(first_time=True)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Check config', self)
        btn.clicked.connect(self.check)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Activeer wijzigingen', self)
        btn.clicked.connect(self.confirm)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Klaar', self)
        btn.clicked.connect(self.close)
        hbox.addWidget(btn)
        hbox.addStretch()
        self.vbox.addLayout(hbox)
        self.setLayout(self.vbox)

    def setup_actions(self):
        "define hotkey actions"
        do = qgui.QAction('Done', self)
        do.triggered.connect(self.confirm)
        do.setShortcut('Ctrl+Enter')
        self.addAction(do)
        dont = qgui.QAction('Cancel', self)
        dont.triggered.connect(self.close)
        dont.setShortcut('Escape')
        self.addAction(dont)

    def show_screen(self):
        "show the screen and start the event loop"
        self.show()
        return self.app.exec()  # niet via sys.exit() want we zijn nog niet klaar

    def confirm(self):
        "build a list from the checked entriesi and pass it back to the caller, then close the gui"
        self.master.modnames = [x.text() for x in self.widgets.values() if x.isChecked()]
        self.master.select_activations()
        if self.master.directories:   # is deze conditie nog nodig of misschien zelfs te beperkend?
            self.master.activate()
        self.refresh_widgets()  # is eigenlijk niet nodig
        qtw.QMessageBox.information(self, 'Change Config', 'wijzigingen zijn doorgevoerd')


    def refresh_widgets(self, first_time=False):
        "set the checkboxes to the right values (first time: also create them)"
        # for item in self.master.conf['Expansions']:
        for item in self.master.conf.sections():
            if item == 'Mod Directories':
                continue
            if first_time:
                hbox = qtw.QHBoxLayout()
                check = qtw.QCheckBox(item)
                hbox.addSpacing(100)
                hbox.addWidget(check)
                hbox.addStretch()
                self.vbox.addLayout(hbox)
                self.widgets[item] = check
            loc = os.path.join(self.master.modbase,
                               self.master.conf['Mod Directories'][item].split(', ')[0])
            self.widgets[item].setChecked(os.path.exists(loc))

    def check(self):
        "check for non-matching names in config file"
        results = self.master.check_config()
        qtw.QMessageBox.information(self, 'Check Config', '\n'.join(results))
