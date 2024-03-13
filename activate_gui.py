"""Stardew Valley Expansion manager - gui toolkit specific code
"""
import sys
import os.path
import functools
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qgui


def show_dialog(cls, parent, modnames, first_time):
    "generic function for handling a dialog (instead of calling it directly"
    parent.dialog_data = {'mods': [], 'deps': {}, 'set_active': []}
    ok = cls(parent, modnames, first_time).exec()
    return ok == qtw.QDialog.DialogCode.Accepted, parent.dialog_data


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
        hbox.addWidget(qtw.QLabel('Dit overzicht toont de namen van expansies die je kunt activeren'
                                  ' (inclusief die al geactiveerd zijn).\n'
                                  'In de achterliggende configuratie is geregeld welke mods'
                                  ' hiervoor eventueel nog meer aangezet moeten worden'))
        self.vbox.addLayout(hbox)
        self.widgets = {}
        self.refresh_widgets(first_time=True)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('add &Mod', self)
        btn.clicked.connect(self.master.add_to_config)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Edit config', self)
        btn.clicked.connect(self.master.edit_config)
        hbox.addWidget(btn)
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
                self.add_checkbox(item)
            loc = os.path.join(self.master.modbase,
                               self.master.conf['Mod Directories'][item].split(', ')[0])
            # print(item, loc)
            self.widgets[item].setChecked(os.path.exists(loc))

    def add_checkbox(self, text):
        "add a checkbox with the given text"
        hbox = qtw.QHBoxLayout()
        check = qtw.QCheckBox(text)
        hbox.addSpacing(100)
        hbox.addWidget(check)
        hbox.addStretch()
        self.vbox.addLayout(hbox)
        self.widgets[text] = check

    def check(self):
        "check for non-matching names in config file"
        results = self.master.check_config()
        qtw.QMessageBox.information(self, 'Check Config', '\n'.join(results))


class NewModDialog(qtw.QDialog):
    """Dialog for adding a new mod with dependencies (if any)

    also used for defining a new dependency
    """
    def __init__(self, parent, modnames, first_time):
        self.parent = parent
        self.modnames = modnames
        super().__init__(parent)
        gbox = qtw.QGridLayout()
        gbox.addWidget(qtw.QLabel('Mod name:', self), 0, 0)
        self.first_name = qtw.QLineEdit(self)
        gbox.addWidget(self.first_name, 0, 1)
        gbox.addWidget(qtw.QLabel('Unpack directory:', self), 1, 0)
        self.last_name = qtw.QLineEdit(self)
        gbox.addWidget(self.last_name, 1, 1)
        self.can_activate = qtw.QCheckBox('Activatable', self)
        if first_time:
            self.can_activate.setChecked(True)
        gbox.addWidget(self.can_activate, 2, 0, 1, 2)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Cancel', self)
        btn.clicked.connect(self.reject)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Add dependency', self)
        btn.clicked.connect(self.add_depline)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Update', self)
        btn.clicked.connect(self.update_deps)
        hbox.addWidget(btn)
        hbox.addStretch()
        gbox.addLayout(hbox, 3, 0, 1, 2)
        self.deps = []
        self.vbox = qtw.QVBoxLayout()
        gbox.addLayout(self.vbox, 4, 0, 1, 2)
        self.setLayout(gbox)

    def add_depline(self):
        """add a combobox to define a new dependency
        """
        hbox = qtw.QHBoxLayout()
        lbox = qtw.QComboBox(self)
        lbox.setEditable(False)
        lbox.addItems(['-- add a new mod --', '-- remove this mod --'])
        lbox.addItems(self.modnames)
        self.deps.append((lbox, ''))
        lbox.activated.connect(functools.partial(self.process_dep, lbox))
        self.can_activate.setEnabled(False)
        hbox.addWidget(lbox)
        self.vbox.addLayout(hbox)
        self.update()

    def process_dep(self, lbox, choice):
        """react to manipulating the combobox
        """
        if choice == 0:
            ok, data = show_dialog(NewModDialog, self, self.modnames, first_time=False)
            if ok:
                # print(data)
                self.parent.dialog_data['mods'].extend(data['mods'])
                for key, value in data['deps'].items():
                    self.parent.dialog_data['deps'][key] = value
                    # self.parent.dialog_data['deps'][data['mods'][0]] = value
                if data['set_active']:
                    self.parent.dialog_data['set_active'].append(data['set_active'][0])
                for ix, dep in enumerate(self.deps):
                    if dep[0] == lbox:
                        self.deps[ix] = (lbox, key)
                        break
                # print(self.parent.dialog_data)
                # lbox.setEditText(data['mods'][0])
                lbox.addItem(key)
                lbox.setCurrentText(key)
            return
        if choice == 1:
            self.remove_depline(lbox)
            return
        for ix, dep in enumerate(self.deps):
            if dep[0] == lbox:
                self.deps[ix] = (lbox, lbox.itemText(choice))
                break

    def remove_depline(self, lbox):
        """remove a combobox for a dependency
        """
        self.vbox.removeWidget(lbox)
        for dep in self.deps:
            if dep[0] == lbox:
                self.deps.remove(dep)
                break
        if not self.deps:
            self.can_activate.setEnabled(True)
        lbox.close()
        self.update()

    def update_deps(self):
        """return the new mod configuration
        """
        modname = self.first_name.text()
        self.parent.dialog_data['mods'].insert(0, (modname, self.last_name.text()))
        self.parent.dialog_data['deps'][modname] = [x[1] for x in self.deps]
        self.parent.dialog_data['set_active'].append(modname if self.can_activate.isChecked() else '')
        self.accept()
