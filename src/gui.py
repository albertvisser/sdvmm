"""Stardew Valley Expansion manager - gui toolkit specific code
"""
import sys
import os.path
import functools
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qgui
download_dir = ''
maxpercol = 10


def show_dialog(cls, parent, *args, **kwargs):
    "generic function for handling a dialog (instead of calling it directly)"
    # parent.dialog_data = {'mods': [], 'deps': {}, 'set_active': []}
    # ok = cls(parent, modnames, first_time).exec()
    ok = cls(parent, *args, **kwargs).exec()
    # return ok == qtw.QDialog.DialogCode.Accepted, parent.dialog_data
    return ok == qtw.QDialog.DialogCode.Accepted  # , parent.dialog_data


class ShowMods(qtw.QWidget):
    "GUI presenting the available mods/extensions to make selection possible of mods to (de)activate"
    maxcol = 3

    def __init__(self, master):
        self.master = master
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        self.lastrow, self.lastcol = 0, 0
        self.unplotted = []
        self.not_selectable = []
        self.plotted_widgets = {}
        self.plotted_positions = {}
        self.unplotted_widgets = {}
        self.unplotted_positions = {}
        self.nonsel_widgets = {}
        self.nonsel_positions = {}

    def setup_screen(self):
        "define the screen elements"
        self.setWindowTitle('SDV Mod Manager')
        self.vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Dit overzicht toont de namen van mods die je kunt activeren'
                                  ' (inclusief die al geactiveerd zijn).\n'
                                  'In de achterliggende configuratie is geregeld welke mods'
                                  ' hiervoor eventueel nog meer aangezet moeten worden\n'
                                  'De onderstreepte items zijn hyperlinks; ze leiden naar de pagina'
                                  ' waarvandaan ik ze van gedownload heb (doorgaans op Nexus)'))
        self.vbox.addLayout(hbox)
        self.gbox1 = qtw.QGridLayout()  # activatable mods
        self.vbox.addLayout(self.gbox1)
        self.vbox.addWidget(qtw.QLabel('Hieronder volgen afhankelijkheden; deze zijn niet'
                                       ' apart te activeren maar je kunt wel zien of ze'
                                       ' actief zijn'))
        self.gbox2 = qtw.QGridLayout()  # dependencies
        self.vbox.addLayout(self.gbox2)
        self.activate_button = qtw.QPushButton('&Activate changes', self)
        self.refresh_widgets(first_time=True)
        self.vbox.addSpacing(10)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Install / update', self)
        btn.setToolTip('Selecteer uit een lijst met recent gedownloade mods één of meer om te'
                       ' installeren')
        btn.clicked.connect(self.update)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Mod attributes', self)
        btn.clicked.connect(self.master.manage_attributes)
        hbox.addWidget(btn)
        self.activate_button.clicked.connect(self.confirm)
        self.activate_button.setEnabled(False)
        hbox.addWidget(self.activate_button)
        select_button = qtw.QPushButton('&Select Savefile', self)
        select_button.clicked.connect(self.master.manage_savefiles)
        hbox.addWidget(select_button)
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
        modnames = []
        all_widgets = self.plotted_widgets | self.unplotted_widgets
        for hbox, label, check in all_widgets.values():
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
        self.refresh_widget_data()
        qtw.QMessageBox.information(self, 'Change Config', 'wijzigingen zijn doorgevoerd')
        self.activate_button.setEnabled(False)

    def refresh_widgets(self, first_time=False):  # , reorder_widgets=True):
        "set the checkboxes to the right values (first time: also create them)"
        # on first-time we build all the checkbox containers
        # otherwize we remove the variable elements from the gridboxes
        if first_time:
            rownum, colnum = 0, 0
            for text, data in self.master.screeninfo.items():
                if data['pos']:
                    rownum, colnum = [int(y) for y in data['pos'].split('x', 1)]
                    self.plotted_widgets[(rownum, colnum)] = self.add_checkbox(data['sel'])
                    self.plotted_positions[(rownum, colnum)] = text, data
                    self.gbox1.addLayout(self.plotted_widgets[(rownum, colnum)][0], rownum, colnum)
                    self.lastrow, self.lastcol = max((self.lastrow, self.lastcol), (rownum, colnum))
                elif data['sel']:
                    self.unplotted.append(text)
                else:
                    self.not_selectable.append(text)
        else:  # if reorder_widgets:
            for key, value in self.unplotted_widgets.items():
                label, check = value[1:]
                check.close()
                label.close()
                self.gbox1.removeItem(self.gbox1.itemAtPosition(key[0], key[1]))
            for key, value in self.nonsel_widgets.items():
                label, check = value[1:]
                check.close()
                label.close()
                self.gbox2.removeItem(self.gbox2.itemAtPosition(key[0], key[1]))
        self.unplotted_positions, self.unplotted_widgets = self.add_items_to_grid(
            self.gbox1, self.lastrow, self.lastcol, self.unplotted)
        self.nonsel_positions, self.nonsel_widgets = self.add_items_to_grid(
            self.gbox2, 0, -1, self.not_selectable)
        self.refresh_widget_data(texts_also=True)

    def refresh_widget_data(self, texts_also=False):
        """actually set the extra texts and checks
        """
        sel_positions = self.plotted_positions | self.unplotted_positions
        sel_widgets = self.plotted_widgets | self.unplotted_widgets
        if texts_also:
            self.set_texts_for_grid(sel_positions, sel_widgets)
            self.set_texts_for_grid(self.nonsel_positions, self.nonsel_widgets)
        self.set_checks_for_grid(sel_positions, sel_widgets)
        self.set_checks_for_grid(self.nonsel_positions, self.nonsel_widgets)

    def add_items_to_grid(self, grid, rownum, colnum, items):
        """create the screen widgets and and remember their positions
        """
        widgets = {}
        positions = {}
        for text in sorted(items):
            colnum += 1
            if colnum == self.maxcol:
                rownum += 1
                colnum = 0
            widgets[(rownum, colnum)] = self.add_checkbox(self.master.screeninfo[text]['sel'])
            # with contextlib.suppress(TypeError):
            #     widgets[(rownum, colnum)][-1].stateChanged.disconnect()
            # if self.master.screeninfo[text]['sel']:
            #     widgets[(rownum, colnum)][-1].setEnabled(True)
            #     widgets[(rownum, colnum)][-1].stateChanged.connect(self.enable_button)
            positions[(rownum, colnum)] = text, self.master.screeninfo[text]
            grid.addLayout(widgets[(rownum, colnum)][0], rownum, colnum)
            self.master.screeninfo[text]['pos'] = f'{rownum}x{colnum}'
        return positions, widgets

    def set_texts_for_grid(self, positions, widgets):
        """add texts to the widgets
        """
        for pos, info in positions.items():
            text, data = info
            label = widgets[pos][1]
            self.build_screen_text(label, text, data['txt'], data['key'])

    def set_checks_for_grid(self, positions, widgets):
        "determine what value to set the checkboxes to"
        for pos, info in positions.items():
            data = info[1]
            check = widgets[pos][2]
            loc = os.path.join(self.master.modbase, data['dir'])
            check.setChecked(os.path.exists(loc))

    def add_checkbox(self, selectable):
        "add a checkbox with the given text"
        hbox = qtw.QHBoxLayout()
        check = qtw.QCheckBox()
        check.setEnabled(False)
        # with contextlib.suppress(TypeError):
        #     check.stateChanged.disconnect()
        if selectable:
            check.setEnabled(True)
            check.stateChanged.connect(self.enable_button)
        label = qtw.QLabel()
        hbox.addSpacing(50)
        hbox.addWidget(check)
        hbox.addWidget(label)
        hbox.addStretch()
        hbox.addSpacing(50)
        return hbox, label, check

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

    # def add_entries_for_name(self, name):
    #     "add entries for managing the new mod in the gui"
    #     self.containers[name], self.widgets[name] = self.add_checkbox(name, '')[1:]
    #     row, col = self.determine_next_row_col()
    #     self.positions[row, col] = name

    # def determine_next_row_col(self):
    #     "calculate placement on screen for new mod"
    #     maxcol, maxrow = 0, 0
    #     for row, col in self.positions:
    #         maxcol = max(col, maxcol)
    #         maxrow = max(row, maxrow)
    #     for col in range(maxcol + 1):
    #         if (maxrow, col) not in self.positions:
    #             return maxrow, col
    #         # row += 1
    #     return maxrow + 1, 0

    def select_value(self, caption, options, editable=True, mandatory=False):
        "Select or enter a value in a dialog"
        ok = False
        while not ok:
            item, ok = qtw.QInputDialog.getItem(self, 'Stardew Valley Mod Manager', caption, options,
                                                editable=editable)
            if not ok:
                if mandatory:
                    qtw.QMessageBox.information(self, 'SDVMM', 'You *must* select or enter a value')
                else:
                    ok = True
        return item

    def build_screen_text(self, label, name, text, updateid):
        """optionally turn screen text into a link and add remark
        """
        if updateid:
            nexustext = '<a href="https://www.nexusmods.com/stardewvalley/mods/{}">{}</a>'
            name = nexustext.format(updateid, name)
            label.setOpenExternalLinks(True)
        if text:
            name += ' ' + text
        label.setText(name)


class AttributesDialog(qtw.QDialog):
    """Dialog for viewing and optionally changing a mod's properties
    """
    def __init__(self, parent, conf):
        self.parent = parent
        self.conf = conf
        self.choice = ''
        self.modnames = {}
        for x in conf.list_all_mod_dirs():
            name = conf.get_diritem_data(x, conf.SCRNAM) or x
            self.modnames[name] = x
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
        self.name = qtw.QComboBox(self)
        self.name.setEditable(True)
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
        # hbox = qtw.QHBoxLayout()
        self.activate_button = qtw.QCheckBox('This mod can be activated by itself', self)
        # hbox.addWidget(self.activate_button)
        vbox.addWidget(self.activate_button)
        # vbox.addLayout(hbox)
        self.exempt_button = qtw.QCheckBox('Do not touch when (de)activating for a save', self)
        # hbox.addWidget(self.exempt_button)
        vbox.addWidget(self.exempt_button)
        # vbox.addLayout(hbox)
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
        self.exempt_button.setChecked(self.parent.master.screeninfo[self.choice]['opt'])
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

    def update(self):
        "update screentext in dictionary"
        # self.text.setReadOnly(True)
        self.clear_name_button.setDisabled(True)
        self.clear_text_button.setDisabled(True)
        self.change_button.setDisabled(True)
        selectable = self.activate_button.isChecked()
        oldselect = self.parent.master.screeninfo[self.choice]['sel']
        self.parent.master.screeninfo[self.choice]['sel'] = selectable
        text = self.text.text()
        oldtext = self.parent.master.screeninfo[self.choice]['txt']
        self.parent.master.screeninfo[self.choice]['txt'] = text
        # old_exempt = self.parent.master.screeninfo[self.choice]['opt']
        self.parent.master.screeninfo[self.choice]['opt'] = self.exempt_button.isChecked()
        # is_exempt = self.exempt_button.isChecked()
        name = self.name.currentText()
        if name != self.choice:
            self.parent.master.screeninfo[name] = self.parent.master.screeninfo.pop(self.choice)
            self.parent.master.attr_changes.append((name, self.choice))
        else:
            self.parent.master.attr_changes.append((self.choice, ''))

        rownum, colnum = [int(y) for y in self.parent.master.screeninfo[name]['pos'].split('x', 1)]
        if oldselect:
            try:
                label = self.parent.plotted_widgets[(rownum, colnum)][1]
            except KeyError:
                label = self.parent.unplotted_widgets[(rownum, colnum)][1]
        else:
            label = self.parent.nonsel_widgets[(rownum, colnum)][1]
        if selectable != oldselect:
            if selectable:
                self.parent.not_selectable.remove(name)
                self.parent.unplotted.append(name)
            else:
                if name in self.parent.unplotted:
                    self.parent.unplotted.remove(name)
                    self.parent.not_selectable.append(name)
                else:
                    message = ("Onselecteerbaar maken van mods met coordinaten in de config"
                               " is helaas nog niet mogelijk")
                    qtw.QMessageBox.information(self, 'SDVMM', message)
                    return
            self.parent.refresh_widgets()  # not first_time
        elif text != oldtext or name != self.choice:
            # alleen schermtekst wijzigen
            label.setOpenExternalLinks(False)
            self.parent.build_screen_text(label, name, text,
                                          self.parent.master.screeninfo[name]['key'])


class SaveGamesDialog(qtw.QDialog):
    """Dialog for viewing and optionally changing a mod's properties
    """
    def __init__(self, parent, conf):
        self.parent = parent
        self.conf = conf
        self.choice = ''
        self.savenames = conf.list_all_saveitems()
        # for x in os.path.expanduser('~/.config/StardewValley/Saves').
        self.modnames = {}
        for x in conf.list_all_mod_dirs():
            self.modnames[conf.get_diritem_data(x, conf.SCRNAM)] = x
        super().__init__(parent)
        self.savegame_selector = qtw.QComboBox(self)
        self.savegame_selector.setEditable(False)
        self.savegame_selector.addItem('select a saved game')
        self.savegame_selector.addItems(sorted(self.savenames))
        self.savegame_selector.currentTextChanged.connect(self.get_savedata)
        self.oldsavename = ''
        self.pname = qtw.QLineEdit(self)
        self.fname = qtw.QLineEdit(self)
        self.gdate = qtw.QLineEdit(self)
        self.widgets = []
        self.update_button = qtw.QPushButton('&Update config')
        self.update_button.setDisabled(True)
        self.update_button.clicked.connect(self.update_all)
        self.confirm_button = qtw.QPushButton('&Activate Mods')
        self.confirm_button.setDisabled(True)
        self.confirm_button.clicked.connect(self.confirm)
        close_button = qtw.QPushButton('&Exit')
        close_button.clicked.connect(self.accept)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.savegame_selector)
        gbox = qtw.QGridLayout()
        gbox.addWidget(qtw.QLabel('Player name:', self), 0, 0)
        gbox.addWidget(self.pname, 0, 1)
        gbox.addWidget(qtw.QLabel('Farm name:', self), 1, 0)
        gbox.addWidget(self.fname, 1, 1)
        gbox.addWidget(qtw.QLabel('In-game date:', self), 2, 0)
        gbox.addWidget(self.gdate, 2, 1)
        vbox.addLayout(gbox)
        self.vbox2 = qtw.QVBoxLayout()
        self.vbox2.addWidget(qtw.QLabel('Uses:', self))
        self.add_modselector()
        vbox.addLayout(self.vbox2)
        vbox.addStretch()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.update_button)
        hbox.addWidget(self.confirm_button)
        hbox.addWidget(close_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.savegame_selector.setFocus()

    def add_modselector(self, name=''):
        "add a selector to make an association between a mod and the save file"
        hbox = qtw.QHBoxLayout()
        lbox = qtw.QComboBox(self)
        lbox.setEditable(False)
        lbox.addItems(['select a mod'])
        lbox.addItems(sorted(self.modnames))
        # if name:
        #     lbox.setCurrentText(name)
        lbox.currentTextChanged.connect(functools.partial(self.process_mod, lbox))
        hbox.addWidget(lbox)
        btn = qtw.QPushButton()
        btn.setIcon(qgui.QIcon.fromTheme(qgui.QIcon.ThemeIcon.EditClear))
        btn.setFixedSize(24, 24)
        btn.setEnabled(bool(name))
        btn.clicked.connect(functools.partial(self.remove_mod, btn))
        hbox.addWidget(btn)
        # self.vbox2.addLayout(hbox)
        self.vbox2.insertLayout(len(self.vbox2), hbox)
        self.widgets.append([btn, lbox, hbox])

    def process_mod(self, lbox, newvalue):
        "add an association between a mod and the save file"
        if newvalue == 'select a mod':
            return
        for item in self.widgets:
            if item[1] == lbox:
                item[0].setEnabled(True)
        self.update_button.setEnabled(True)
        # er moet alleen een nieuwe selector komen als dit de laatste combobox is en deze nog geen
        # waarde had
        if lbox == self.widgets[-1][1]:  # and len(self.widgets) > len(self.prevmods):
            self.add_modselector()
        # self.prevmods.append(newvalue)

    def remove_mod(self, btn):
        "delete an association between a mod and the save file"
        for item in self.widgets:
            if item[0] == btn:
                self.vbox2.removeWidget(item[0])
                item[0].close()
                self.vbox2.removeWidget(item[1])
                item[1].close()
                self.vbox2.removeItem(item[2])
                # item[2].close()
                self.widgets.remove(item)

    def confirm(self):
        "activate the mods belonging to this save file"
        selected = self.savegame_selector.currentText()
        modnames = self.conf.get_mods_for_saveitem(selected)
        # uitzetten gebeurt in activate(), hier moeten de mods die ongemoeid gelaten moeten worden
        # en aanstaan, toegevoegd worden aan de selectie
        for dirname in self.conf.list_all_mod_dirs():
            if (self.conf.get_diritem_data(dirname, self.conf.OPTOUT)
                    and os.path.exists(os.path.join(self.parent.master.modbase, dirname))):
                modnames.append(self.conf.get_diritem_data(dirname, self.conf.SCRNAM) or dirname)
        self.parent.master.select_activations(modnames)
        if self.parent.master.directories:   # alleen leeg als er niks geselecteerd is
            self.parent.master.activate()
        self.parent.refresh_widget_data()
        qtw.QMessageBox.information(self, 'Change Config', 'wijzigingen zijn doorgevoerd')

    def update_all(self):
        "save the mod associations in the config"
        # breakpoint()
        self.update(self.savegame_selector.currentText())
        self.conf.save()

    # def accept(self):
    #     "exit the dialog"
    #     if self.update_button.isEnabled():
    #         ok = qtw.QMessageBox.question(self, 'Change Config', '')

    # def reset(self):
    #     "undo the changes for this savefile in memory"
    #     self.pname.setText(self.old_pname)
    #     self.fname.setText(self.old_fname)
    #     self.gdate.setText(self.old_gdate)
    #     for item in self.widgets:

    def update(self, savename):
        "save the changes for this savefile in memory"
        new_pname = self.pname.text()
        if new_pname != self.old_pname:
            self.conf.update_saveitem_data(savename, self.conf.PNAME, new_pname)
        new_fname = self.fname.text()
        if new_fname != self.old_fname:
            self.conf.update_saveitem_data(savename, self.conf.FNAME, new_fname)
        new_gdate = self.gdate.text()
        if new_gdate != self.old_gdate:
            self.conf.update_saveitem_data(savename, self.conf.GDATE, new_gdate)
        newmods = [item[1].currentText() for item in self.widgets[:-1]]
        if newmods != self.oldmods:
            self.conf.update_saveitem_data(savename, self.conf.MODS, newmods)
        self.update_button.setDisabled(True)

    def get_savedata(self, newvalue):
        "find and show existing configuration data for this save file"
        if newvalue == 'select a saved game':
            return
        if self.oldsavename:
            self.update(self.oldsavename)
            for item in reversed(self.widgets):
                btn = item.pop(0)
                btn.close()
                lbox = item.pop(0)
                lbox.close()
                self.vbox2.removeItem(item[0])
                self.widgets.remove(item)
            self.add_modselector()
        self.oldsavename = newvalue
        self.oldmods = []
        save_attrs = self.conf.get_saveitem_attrs(newvalue)
        if save_attrs:
            self.old_pname, self.old_fname, self.old_gdate = save_attrs
            self.pname.setText(self.old_pname)
            self.fname.setText(self.old_fname)
            self.gdate.setText(self.old_gdate)
            self.oldmods = self.conf.get_mods_for_saveitem(newvalue)
        for modname in self.oldmods:
            self.widgets[-1][1].setCurrentText(modname)
        self.update_button.setDisabled(True)
        self.confirm_button.setEnabled(True)
