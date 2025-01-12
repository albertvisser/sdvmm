"""Stardew Valley Expansion manager - gui toolkit specific code
"""
import sys
import os.path
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qgui
download_dir = ''
maxpercol = 10


# def show_dialog(cls, parent, modnames, first_time):
def show_dialog(cls, parent, *args, **kwargs):
    "generic function for handling a dialog (instead of calling it directly)"
    # parent.dialog_data = {'mods': [], 'deps': {}, 'set_active': []}
    # ok = cls(parent, modnames, first_time).exec()
    ok = cls(parent, *args, **kwargs).exec()
    # return ok == qtw.QDialog.DialogCode.Accepted, parent.dialog_data
    return ok == qtw.QDialog.DialogCode.Accepted  # , parent.dialog_data


class ShowMods(qtw.QWidget):
    "GUI presenting the available mods/extensions to make selection possible of mods to (de)activate"
    def __init__(self, master):
        self.master = master
        self.app = qtw.QApplication(sys.argv)
        super().__init__()

    def setup_screen(self):
        "define the screen elements"
        self.setWindowTitle('SDV Mod Manager')
        self.vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Dit overzicht toont de namen van expansies die je kunt activeren'
                                  ' (inclusief die al geactiveerd zijn).\n'
                                  'In de achterliggende configuratie is geregeld welke mods'
                                  ' hiervoor eventueel nog meer aangezet moeten worden\n'
                                  'De onderstreepte items zijn hyperlinks; ze leiden naar de pagina'
                                  ' waarvandaan ik ze van gedownload heb (doorgaans op Nexus)'))
        self.vbox.addLayout(hbox)
        self.widgets = {}
        self.containers = {}
        self.positions = {}
        self.gbox = qtw.QGridLayout()
        self.activate_button = qtw.QPushButton('&Activate changes', self)
        self.refresh_widgets(first_time=True)
        self.vbox.addLayout(self.gbox)
        self.vbox.addSpacing(10)
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
        # btn = qtw.QPushButton('add &Mod to config', self)
        # btn.clicked.connect(self.master.add_to_config)
        # hbox.addWidget(btn)
        btn = qtw.QPushButton('&Mod attributes', self)
        btn.clicked.connect(self.master.manage_attributes)
        hbox.addWidget(btn)
        # btn = qtw.QPushButton('&Edit config', self)
        # btn.clicked.connect(self.master.edit_config)
        # hbox.addWidget(btn)
        # btn = qtw.QPushButton('Re&Load config', self)
        # btn.clicked.connect(self.master.reload_config)
        # hbox.addWidget(btn)
        self.activate_button.clicked.connect(self.confirm)
        self.activate_button.setEnabled(False)
        hbox.addWidget(self.activate_button)
        btn = qtw.QPushButton('&Done', self)
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
        dont.setShortcuts(['Escape', 'Ctrl+Q'])
        self.addAction(dont)

    def show_screen(self):
        "show the screen and start the event loop"
        self.show()
        return self.app.exec()  # kan evt. ook weer via sys.exit()

    def confirm(self):
        "build a list from the checked entries and pass it back to the caller"
        # self.master.modnames = [x.text().split(">", 1)[1].split("<", 1)[0]
        #                        for x, y in self.widgets.values() if y.isChecked()]
        modnames = []
        for label, check in self.widgets.values():
            if check.isChecked():
                labeltext = label.text()
                if ">" in labeltext:
                    linktext = labeltext.split(">", 1)[1].split("<", 1)[0]
                else:
                    linktext = labeltext
                modnames.append(linktext)
        self.master.select_activations(modnames)
        if self.master.directories:   # alleen leeg als er niks aangevinkt is
            self.master.activate()
        self.refresh_widgets(reorder_widgets=False)  # is eigenlijk niet nodig?
        qtw.QMessageBox.information(self, 'Change Config', 'wijzigingen zijn doorgevoerd')
        self.activate_button.setEnabled(False)

    def refresh_widgets(self, first_time=False, reorder_widgets=True):
        "set the checkboxes to the right values (first time: also create them)"
        # on first-time we build all the checkbox containers
        if first_time:
            rownum, colnum = 0, 0
            highrow, highcol = 0, 0
            maxcol = 3
            unplotted = []
            for text, data in self.master.screeninfo.items():
                self.containers[text], self.widgets[text] = self.add_checkbox(text, data)
                if data['pos']:
                    rownum, colnum = [int(y) for y in data['pos'].split('x', 1)]
                    highrow = rownum if rownum > highrow else highrow
                    highcol = colnum if colnum > highcol else highcol
                    self.positions[(rownum, colnum)] = text
                else:   # fallback voor nog niet geplotte teksten
                    unplotted.append(text)
                rownum, colnum = highrow + 1, -1
            self.positions[(rownum, colnum)] = "---"
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel('Hieronder volgen afhankelijkheden; deze zijn niet'
                                      ' apart te activeren maar je kunt wel zien of ze'
                                      ' actief zijn'))
            self.containers['---'] = hbox
            rownum += 1
            for text in sorted(unplotted):
                colnum += 1
                if colnum == maxcol:
                    rownum += 1
                    colnum = 0
                self.positions[(rownum, colnum)] = text

        # print(self.positions) # wordt deze misschien niet bijgewerkt na reorderen?
        if reorder_widgets:
            if not first_time:
                for layout in self.containers.values():
                    self.gbox.removeItem(layout)
            for pos, text in self.positions.items():
                self.gbox.addLayout(self.containers[text], pos[0], pos[1])
            if not first_time:
                self.gbox.update()  # werkt helaas niet om de nieuwe volgorde te laten zien
        for text, check in self.widgets.items():
            loc = os.path.join(self.master.modbase, self.master.screeninfo[text]['dir'])
            check[1].setChecked(os.path.exists(loc))

    def add_checkbox(self, text, data):
        "add a checkbox with the given text"
        hbox = qtw.QHBoxLayout()
        check = qtw.QCheckBox()
        check.setEnabled(data['sel'])
        check.stateChanged.connect(self.enable_button)
        label = qtw.QLabel()
        if data['key']:
            nexustext = '<a href="https://www.nexusmods.com/stardewvalley/mods/{}">{}</a>'
            text = nexustext.format(data['key'], text)
            label.setOpenExternalLinks(True)
        if data['txt']:
            text += ' ' + data['txt']
        label.setText(text)
        hbox.addSpacing(50)
        hbox.addWidget(check)
        hbox.addWidget(label)
        hbox.addStretch()
        hbox.addSpacing(50)
        return hbox, (label, check)

    def enable_button(self):
        "make activating mods possible"
        self.activate_button.setEnabled(True)

    def update(self):
        "(re)install downloaded mods"
        filenames, ok = qtw.QFileDialog.getOpenFileNames(self, caption="Install downloaded mods",
                                                         directory=self.master.downloads,
                                                         filter='Zip files (*.zip)')
        if ok:
            report = self.master.update_mods(filenames)
            qtw.QMessageBox.information(self, 'Change Config', '\n'.join(report))

    def add_entries_for_name(self, name):
        "add entries for managing the new mod in the gui"
        self.containers[name], self.widgets[name] = self.add_checkbox(name, '')
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
            # row += 1
        return maxrow + 1, 0

    def reorder_gui(self):
        "Bring up a dialog to reorder the names on the screen and process the results"
        ok = show_dialog(ReorderDialog, self)
        if ok:
            self.master.update_config_from_screenpos()
            self.refresh_widgets()

    def select_value(self, caption, options, editable=True, mandatory=False):
        "Select or enter a value in a dialog"
        ok = False
        while not ok:
            ok, item = qtw.QInputDialog.getItem(self, 'Stardew Valley Mod Manager', caption, options,
                                                editable=editable)
            if not ok:
                if mandatory:
                    qtw.QMessageBox.information(self, 'SDVMM', 'You *must* select or enter a value')
                else:
                    ok = True
        return item


class AttributesDialog(qtw.QDialog):
    """Dialog for viewing and optionally changing a mod's properties
    """
    def __init__(self, parent, conf):
        self.parent = parent
        self.conf = conf
        self.choice = ''
        self.modnames = {}
        for x in conf.list_all_mod_dirs():
            self.modnames[conf.get_diritem_data(x, conf.SCRNAM)] = x
        super().__init__(parent)
        vbox = qtw.QVBoxLayout()
        self.lbox = qtw.QComboBox(self)
        self.lbox.setEditable(False)
        self.lbox.addItem('select a mod to change the screen text')
        self.lbox.addItems(sorted(self.modnames))
        self.lbox.currentTextChanged.connect(self.enable_select)
        # self.lbox.activated.connect(self.enable_select)
        vbox.addWidget(self.lbox)
        self.select_button = qtw.QPushButton('View &Attributes')
        self.select_button.clicked.connect(self.process)
        self.select_button.setEnabled(False)
        vbox.addWidget(self.select_button)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Screen Name:\n'
                                  '(the suggestions in the box below are taken from\n'
                                  'the mod components', self))
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        # self.text = qtw.QLineEdit(self)
        self.name = qtw.QComboBox(self)
        # self.text.setMinimumWidth(200)
        # self.text.setReadOnly(True)
        hbox.addWidget(self.name)
        self.clear_name_button = qtw.QPushButton()
        self.clear_name_button.setIcon(qgui.QIcon.fromTheme(qgui.QIcon.ThemeIcon.EditClear))
        # self.clear_button.resize(20, 20)
        self.clear_name_button.setFixedSize(24, 24)
        self.clear_name_button.setDisabled(True)
        self.clear_name_button.clicked.connect(self.clear_name_text)
        hbox.addWidget(self.clear_name_button)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Screen Text:\n'
                                  '(to add some information e.q. if the mod is broken)', self))
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        self.text = qtw.QLineEdit(self)
        hbox.addWidget(self.text)
        self.clear_text_button = qtw.QPushButton()
        self.clear_text_button.setIcon(qgui.QIcon.fromTheme(qgui.QIcon.ThemeIcon.EditClear))
        # self.clear_button.resize(20, 20)
        self.clear_text_button.setFixedSize(24, 24)
        self.clear_text_button.setDisabled(True)
        self.clear_text_button.clicked.connect(self.clear_text_text)
        hbox.addWidget(self.clear_text_button)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        self.activate_button = qtw.QCheckBox('This mod can be activated by itself', self)
        hbox.addWidget(self.activate_button)
        vbox.addLayout(hbox)
        self.comps_button = qtw.QPushButton('View &Components')
        self.comps_button.clicked.connect(self.view_components)
        vbox.addWidget(self.comps_button)
        self.comps_button.setDisabled(True)
        self.deps_button = qtw.QPushButton('View &Dependencies')
        self.deps_button.clicked.connect(self.view_dependencies)
        vbox.addWidget(self.deps_button)
        self.deps_button.setDisabled(True)
        hbox = qtw.QHBoxLayout()
        self.change_button = qtw.QPushButton('&Update')
        self.change_button.setDisabled(True)
        self.change_button.clicked.connect(self.update)
        hbox.addWidget(self.change_button)
        close_button = qtw.QPushButton('&Exit')
        close_button.clicked.connect(self.accept)
        hbox.addWidget(close_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.lbox.setFocus()

    def enable_select(self):
        """disable buttons after selecting another mod
        """
        self.select_button.setEnabled(True)
        self.comps_button.setDisabled(True)
        self.deps_button.setDisabled(True)
        self.change_button.setDisabled(True)

    def process(self):
        "get description if any"
        self.select_button.setDisabled(True)
        self.choice = self.lbox.currentText()
        self.name.clear()
        self.name.addItem(self.choice)
        items = set()
        for x in self.conf.list_components_for_dir(self.modnames[self.choice]):
            items.add(self.conf.get_component_data(x, self.conf.NAME))
        self.name.addItems(sorted(list(items)))
        self.clear_name_button.setDisabled(False)
        self.text.setText(self.parent.master.screeninfo[self.choice]['txt'])
        self.clear_text_button.setDisabled(False)
        self.activate_button.setChecked(self.parent.master.screeninfo[self.choice]['sel'])
        self.comps_button.setDisabled(False)
        self.deps_button.setDisabled(False)
        self.change_button.setDisabled(False)

    def clear_name_text(self):
        "visually delete screen text"
        self.name.clear()

    def clear_text_text(self):
        "visually delete additional text if any"
        self.text.clear()

    def view_components(self):
        "list components for mod"
        complist = []
        # maxlen = 0
        for comp in self.conf.list_components_for_dir(self.modnames[self.choice]):
            text = (f'  {self.conf.get_component_data(comp, self.conf.NAME)} '
                    f'  {self.conf.get_component_data(comp, self.conf.VRS)}\n'
                    f'    ({comp})')
            # maxlen = max(maxlen, len(text))
            complist.append(text)
        message = f'Components for {self.choice}:\n' + '\n'.join(complist)
        qtw.QMessageBox.information(self, 'SDVMM mod info', message)
        # box = qtw.QMessageBox(self)
        # box.setWindowTitle('SDVMM mod info')
        # box.setText(f'Components for {self.choice}:\n' + '\n'.join(complist))
        # box.addButton(qtw.QMessageBox.StandardButton.Ok)
        # box.setFixedSize(len(complist) * 10, maxlen * 10)
        # box.resize(len(complist) * 10, maxlen * 10)
        # box.exec()

    def view_dependencies(self):
        "list dependencies for mod"
        deplist = set()
        for comp in self.conf.list_components_for_dir(self.modnames[self.choice]):
            for dep in self.conf.get_component_data(comp, self.conf.DEPS):
                deplist.add(dep)
        depnames = []
        # maxlen = 0
        for dep in sorted(deplist):
            try:
                depname = self.conf.get_component_data(dep, self.conf.NAME)
            except ValueError:
                depname = 'unknown component:'
                depnames.append((depname, dep))
            else:
                depnames.append((depname, f'({dep})'))
            # maxlen = max(maxlen, len(depname) + len(dep) + 4)
        if not depnames:
            depnames = [('None', '')]
        message = f'Dependencies for {self.choice}:\n' + "\n".join(f' {x} {y}'
                                                                   for (x, y) in sorted(depnames))
        qtw.QMessageBox.information(self, 'SDVMM mod info', message)
        # box = qtw.QMessageBox(self)
        # box.setWindowTitle('SDVMM mod info')
        # box.setText(f'Dependencies for {self.choice}:\n'
        #             + "\n".join(f' {x} {y}' for (x, y) in sorted(depnames)))
        # box.addButton(qtw.QMessageBox.StandardButton.Ok)
        # box.setFixedSize(len(depnames) * 10, maxlen * 10)
        # box.exec()

    def update(self):
        "update screentext in dictionary"
        # self.text.setReadOnly(True)
        self.clear_name_button.setDisabled(True)
        self.clear_text_button.setDisabled(True)
        self.change_button.setDisabled(True)
        selectable = self.activate_button.isChecked()
        self.parent.master.screeninfo[self.choice]['sel'] = selectable
        text = self.text.text()
        self.parent.master.screeninfo[self.choice]['txt'] = text
        name = self.name.currentText()
        if name != self.choice:
            self.parent.master.screeninfo[name] = self.parent.master.screeninfo.pop(self.choice)
            self.parent.master.attr_changes.append((name, self.choice))
        else:
            self.parent.master.attr_changes.append((self.choice, ''))


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
        for pos in [x[0] for x in self.data.values()]:
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
            if scrpos[0]:
                row, col = [int(x) for x in scrpos[0].split('x')]
            else:
                row, col = self.table.rowCount(), 0
                self.table.insertRow(row)
            item = qtw.QTableWidgetItem(text)
            self.table.setItem(row, col, item)

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
