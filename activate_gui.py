"""Stardew Valley Expansion manager - gui toolkit specific code
"""
import sys
import os.path
import functools
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qgui
download_dir = ''
maxpercol = 10


# def show_dialog(cls, parent, modnames, first_time):
def show_dialog(cls, parent, *args, **kwargs):
    "generic function for handling a dialog (instead of calling it directly"
    # parent.dialog_data = {'mods': [], 'deps': {}, 'set_active': []}
    # ok = cls(parent, modnames, first_time).exec()
    ok = cls(parent, *args, **kwargs).exec()
    # return ok == qtw.QDialog.DialogCode.Accepted, parent.dialog_data
    return ok == qtw.QDialog.DialogCode.Accepted  # , parent.dialog_data


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
        self.containers = {}
        self.positions = {}
        self.gbox = qtw.QGridLayout()
        self.refresh_widgets(first_time=True)
        self.vbox.addLayout(self.gbox)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Install / update', self)
        btn.setToolTip('Selecteer uit een lijst met recent gedownloade mods één of meer om te'
                       ' installeren')
        btn.clicked.connect(self.update)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Reorder mods on screen', self)
        btn.clicked.connect(self.reorder_gui)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('add &Mod to config', self)
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
        "build a list from the checked entries and pass it back to the caller"
        self.master.modnames = [x.text() for x in self.widgets.values() if x.isChecked()]
        self.master.select_activations()
        if self.master.directories:   # is deze conditie nog nodig of misschien zelfs te beperkend?
            self.master.activate()
        self.refresh_widgets(reorder_widgets=False)  # is eigenlijk niet nodig?
        qtw.QMessageBox.information(self, 'Change Config', 'wijzigingen zijn doorgevoerd')

    def refresh_widgets(self, first_time=False, reorder_widgets=True):
        "set the checkboxes to the right values (first time: also create them)"
        # on first-time we build all the checkbox containers
        if first_time:
            rownum, colnum = 0, 0
            # for text, scrpos in sorted(self.master.screenpos.items(), key=lambda x: x[1]):
            for text, scrpos in self.master.screenpos.items():
                self.containers[text], self.widgets[text] = self.add_checkbox(text)
                if scrpos:
                    row, col = [int(y) for y in scrpos.split('x', 1)]
                else:   # fallback voor als het scherm nog niet eerder geordend was
                    maxcol = 3  # len(self.master.screenpos) // maxpercol
                    row, col = rownum, colnum
                    colnum += 1
                    if colnum == maxcol:
                        rownum += 1
                        colnum = 0
                self.positions[(row, col)] = text
        if reorder_widgets:
            if not first_time:
                for text, layout in self.containers.items():
                    # print('removing widget for', text)
                    self.gbox.removeItem(layout)
            for pos, text in self.positions.items():
                # print('adding widget for', text)
                self.gbox.addLayout(self.containers[text], pos[0], pos[1])
            if not first_time:
                self.gbox.update()  # werkt helaas niet om de nieuwe volgorde te laten zien
        for text, check in self.widgets.items():
            loc = os.path.join(self.master.modbase,
                               self.master.conf['Mod Directories'][text].split(', ')[0])
            check.setChecked(os.path.exists(loc))

    def add_checkbox(self, text):
        "add a checkbox with the given text"
        hbox = qtw.QHBoxLayout()
        check = qtw.QCheckBox(text)
        hbox.addSpacing(50)
        hbox.addWidget(check)
        hbox.addSpacing(50)
        return hbox, check

    def check(self):
        "check for non-matching names in config file"
        results = self.master.check_config()
        qtw.QMessageBox.information(self, 'Check Config', '\n'.join(results))

    def update(self):
        "(re)install downloaded mods"
        filenames, ok = qtw.QFileDialog.getOpenFileNames(self, caption="Install downloaded mods",
                                                         directory=self.master.downloads,
                                                         filter='Zip files (*.zip)')
        if ok:
            report = self.master.update_mods(filenames)
            qtw.QMessageBox.information(self, 'Change Config', '\n'.join(report))

    def add_entries_for_name(self, name):
        "add entries for managing the new plugin in the gui"
        self.containers[name], self.widgets[name] = self.add_checkbox(name)
        row, col = self.determine_next_row_col()
        self.positions[row, col] = name

    def determine_next_row_col(self):
        "calculate placement on screen for new mod"
        maxcol, maxrow = 0, 0
        for row, col in self.positions:
            maxcol = max(col, maxcol)
            maxrow = max(row, maxrow)
        for col in range(maxcol + 1):
            if (maxrow, col) not in self.positions:
                return maxrow, col
            row += 1
        return maxrow + 1, 0

    def reorder_gui(self):
        "Bring up a dialog to reodere the names on the screen and process the results"
        ok = show_dialog(ReorderDialog, self)
        if ok:
            self.master.update_config_from_screenpos()
            self.widgets = {}
            self.containers = {}
            self.positions = {}
            self.refresh_widgets()


class NewModDialog(qtw.QDialog):
    """Dialog for adding a new mod with dependencies (if any)

    also used for defining a new dependency
    """
    def __init__(self, parent, modnames, first_time):
        self.parent = parent
        self.parent.dialog_data = {'mods': [], 'deps': {}, 'set_active': []}
        self.modnames = modnames
        super().__init__(parent)
        gbox = qtw.QGridLayout()
        gbox.addWidget(qtw.QLabel('Mod name:', self), 0, 0)
        self.first_name = qtw.QLineEdit(self)
        self.first_name.setMinimumWidth(200)
        gbox.addWidget(self.first_name, 0, 1)
        gbox.addWidget(qtw.QLabel('Unpack directory:', self), 1, 0)
        self.last_name = qtw.QLineEdit(self)
        self.last_name.setMinimumWidth(200)
        gbox.addWidget(self.last_name, 1, 1)
        self.select = qtw.QPushButton('&Select\nfrom Downloads', self)
        self.select.clicked.connect(self.select_mod)
        gbox.addWidget(self.select, 0, 2, 2, 1)
        self.can_activate = qtw.QCheckBox('Activatable', self)
        if first_time:
            self.can_activate.setChecked(True)
        gbox.addWidget(self.can_activate, 2, 0)  # , 1, 2)

        self.deps = []
        self.vbox = qtw.QVBoxLayout()
        btn = qtw.QPushButton('&Add dependency', self)
        btn.clicked.connect(self.add_depline)
        self.vbox.addWidget(btn)
        gbox.addLayout(self.vbox, 3, 0, 1, 3)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Cancel', self)
        btn.clicked.connect(self.reject)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Update', self)
        btn.clicked.connect(self.update_deps)
        hbox.addWidget(btn)
        hbox.addStretch()
        gbox.addLayout(hbox, 4, 0, 1, 3)
        self.setLayout(gbox)

    def select_mod(self):
        """choose a mod to determine the directory it unpacks into
        """
        filename, ok = qtw.QFileDialog.getOpenFileName(self, caption="Select mod",
                                                       directory=self.parent.master.downloads,
                                                       filter='Zip files (*.zip)')
        if ok:
            dirname = self.parent.master.determine_unpack_directory(filename)
            if not dirname:
                qtw.QMessageBox.information(self, 'Read mod name', "Can't auto-determine;\n"
                                            'zipfile contains more than one base directory')
            else:
                self.first_name.setText(dirname)
                self.last_name.setText(dirname)

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
            ok = show_dialog(NewModDialog, self, self.modnames, first_time=False)
            if ok:
                data = self.dialog_data
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
        if self.can_activate.isChecked():
            self.parent.dialog_data['set_active'].append(modname)
        self.accept()


class ReorderDialog(qtw.QDialog):
    "Mod volgorde op scherm veranderen"
    # toon tablewidget met buttons voor toevoegen/weghalen kolommen en rijen (vgl HtmlEdit)
    # bij refreshen laden met namen uit self.master.screenpos
    # t.z.t. misschien direct in de main gui, met drag en drop o.i.d.i
    def __init__(self, parent):
        self._parent = parent
        self.data = parent.master.screenpos
        # self.headings = ['']
        super().__init__(parent)
        rowcount, colcount = self.determine_rows_cols()
        self.colwidth = 200
        # self.setWindowTitle('Screen Setup')
        # self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()

        self.table = qtw.QTableWidget(self)
        self.table.setRowCount(rowcount)     # de eerste rij is voor de kolomtitels
        self.table.setColumnCount(colcount)  # de eerste rij is voor de rijtitels
        for col in range(colcount):
            self.table.setColumnWidth(col - 1, self.colwidth)
        # self.table_table.setHorizontalHeaderLabels(self.headings)
        # self.hdr = self.table_table.horizontalHeader()
        # self.table_table.verticalHeader().setVisible(False)
        # self.hdr.setSectionsClickable(True)
        # self.hdr.sectionClicked.connect(self.on_title)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.table)
        self.populate()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        button = qtw.QPushButton('&> Add Column', self)
        button.clicked.connect(self.add_column)
        hbox.addWidget(button)
        button = qtw.QPushButton('&< Remove Last Column', self)
        button.clicked.connect(self.remove_column)
        hbox.addWidget(button)
        button = qtw.QPushButton('(Re)&Position texts in grid', self)
        button.clicked.connect(self.populate)
        hbox.addWidget(button)
        button = qtw.QPushButton('&+ Add Row', self)
        button.clicked.connect(self.add_row)
        hbox.addWidget(button)
        button = qtw.QPushButton('&- Remove Last Row', self)
        button.clicked.connect(self.remove_row)
        hbox.addWidget(button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def determine_rows_cols(self):
        """derive number of rows and columns from texts to lay out
        """
        colcount = rowcount = 0
        for pos in self.data.values():
            if not pos:
                break
            row, col = [int(x) + 1 for x in pos.split('x')]
            rowcount = max(rowcount, row)
            colcount = max(colcount, col)
        if colcount == 0:
            colcount = 3
            rowcount = len(self.data) // colcount
            if len(self.data) % colcount > 0:
                rowcount += 1
        return rowcount, colcount

    def add_column(self):
        "new column at the end"
        self.table.insertColumn(self.table.columnCount())
        self.table.setColumnWidth(self.table.columnCount() - 1, self.colwidth)

    def remove_column(self):
        "remove last column"
        self.table.removeColumn(self.table.columnCount() - 1)

    def add_row(self):
        "new row at the bottom"
        self.table.insertRow(self.table.rowCount())

    def remove_row(self):
        "remove last roeself."
        self.table.removeRow(self.table.rowCount() - 1)

    def populate(self):
        """(re)distribute texts over the table cells"""
        self.table.clear()
        if not list(self.data.values())[0]:
            texts = list(self.data.keys())
            textindex = 0
            for colnum in range(self.table.columnCount()):
                for rownum in range(self.table.rowCount()):
                    if textindex < len(texts):
                        item = qtw.QTableWidgetItem(texts[textindex])
                        textindex += 1
                        self.table.setItem(rownum, colnum, item)
            return
        for text, scrpos in sorted(self.data.items(), key=lambda x: (x[1], x[0])):
            row, col = scrpos.split('x')
            item = qtw.QTableWidgetItem(text)
            self.table.setItem(int(row), int(col), item)

    def accept(self):
        """bij OK: de opgebouwde tabel via self.dialog_data doorgeven
        aan het mainwindow
        """
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        if rows * cols < len(self.data):
            qtw.QMessageBox.information(self, 'Reorder names', "not enough room for all entries")
            return
        for row in range(rows):
            for col in range(cols):
                # try:
                #     rowitems.append(str(self.table_table.item(row, col).text()))
                # except AttributeError:
                #     self._parent.meld('Graag nog even het laatste item bevestigen (...)')
                #     return
                item = self.table.item(row, col)
                if item:
                    self.data[item.text()] = f'{row}x{col}'
        self._parent.master.screenpos = self.data
        super().accept()
