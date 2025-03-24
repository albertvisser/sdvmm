"""Stardew Valley Expansion manager - gui toolkit specific code
"""
import sys
import os.path
import functools
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qgui
download_dir = ''


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
        self.attr_button = qtw.QPushButton('&Mod attributes', self)
        self.activate_button = qtw.QPushButton('&Activate changes', self)
        self.select_button = qtw.QPushButton('&Select Savefile', self)
        self.refresh_widgets(first_time=True)
        self.vbox.addSpacing(10)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('Set &Defaults', self)
        btn.clicked.connect(self.master.manage_defaults)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Install / update', self)
        btn.setToolTip('Selecteer uit een lijst met recent gedownloade mods één of meer om te'
                       ' installeren')
        btn.clicked.connect(self.update)
        hbox.addWidget(btn)
        self.attr_button.clicked.connect(self.master.manage_attributes)
        hbox.addWidget(self.attr_button)
        self.activate_button.clicked.connect(self.confirm)
        self.activate_button.setEnabled(False)
        hbox.addWidget(self.activate_button)
        self.select_button.clicked.connect(self.master.manage_savefiles)
        hbox.addWidget(self.select_button)
        btn = qtw.QPushButton('&Close', self)
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

    def refresh_widgets(self, first_time=False):  # , reorder_widgets=True):
        "set the checkboxes to the right values (first time: also create them)"
        # on first-time we build all the checkbox containers
        # otherwise we remove the variable elements from the gridboxes
        self.attr_button.setEnabled(bool(self.master.screeninfo))
        self.select_button.setEnabled(bool(self.master.screeninfo))
        self.master.order_widgets(first_time, self.gbox1, self.gbox2)

    def remove_widgets(self, *args):
        """remove the widgets from the screen before replacing them
        """
        widgetlist, container, row, col = args
        label, check = widgetlist[1:]
        check.close()
        label.close()
        container.removeItem(container.itemAtPosition(row, col))

    def add_checkbox(self, grid, rownum, colnum, selectable):
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
        grid.addLayout(hbox, rownum, colnum)
        return hbox, label, check

    def set_label_text(self, widgets, name, updateid, text):
        """change the text on a label
        """
        label = widgets[1]
        if updateid:
            name = self.master.build_link_text(name, updateid)
            label.setOpenExternalLinks(True)
        if text:
            name += ' ' + text
        label.setText(name)
        widgets = (widgets[0], label, widgets[2])

    def set_checkbox_state(self, widgetlist, state):
        "check or uncheck a checkbox"
        check = widgetlist[2]
        check.setChecked(state)
        widgetlist = (widgetlist[0], widgetlist[1], check)

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

    def confirm(self):
        "build a list from the checked entries and pass it back to the caller"
        self.master.process_activations()
        qtw.QMessageBox.information(self, 'Change Config', 'wijzigingen zijn doorgevoerd')
        self.activate_button.setEnabled(False)

    def get_labeltext_if_checked(self, widgetlist):
        """return the name of the mod associated with a checkbox
        """
        label, check = widgetlist[1:]
        if check.isChecked():
            labeltext = label.text()
            if ">" in labeltext:
                linktext = labeltext.split(">", 1)[1].split("<", 1)[0]
            else:
                linktext = labeltext
            return linktext
        return ''

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


class SettingsDialog(qtw.QDialog):
    """Dialog for changing some application defaults
    """
    def __init__(self, parent):
        self.parent = parent
        origmodbase, origconfig, origdownload, origsavepath = self.parent.master.dialog_data
        super().__init__(parent)
        vbox = qtw.QVBoxLayout()
        gbox = qtw.QGridLayout()
        row = 0
        gbox.addWidget(qtw.QLabel('Base location for mods:', self), row, 0)
        self.modbase_text = qtw.QLineEdit(self)
        self.modbase_text.setText(origmodbase)
        self.modbase_text.setMinimumWidth(380)
        # self.modbase_text.setMaximumWidth(380)
        gbox.addWidget(self.modbase_text, row, 1)
        self.select_modbase_button = qtw.QPushButton('Browse', self)
        self.select_modbase_button.clicked.connect(self.select_modbase)
        gbox.addWidget(self.select_modbase_button, row, 2)
        row += 1
        gbox.addWidget(qtw.QLabel('Configuration file name:', self), row, 0)
        self.config_text = qtw.QLineEdit(self)
        self.config_text.setText(origconfig)
        self.config_text.setMinimumWidth(380)
        gbox.addWidget(self.config_text, row, 1)
        row += 1
        gbox.addWidget(qtw.QLabel('Location for downloads:', self), row, 0)
        self.download_text = qtw.QLineEdit(self)
        self.download_text.setText(origdownload)
        self.download_text.setMinimumWidth(380)
        # self.download_text.setMaximumWidth(220)
        gbox.addWidget(self.download_text, row, 1)
        self.select_download_button = qtw.QPushButton('Browse', self)
        self.select_download_button.clicked.connect(self.select_download_path)
        gbox.addWidget(self.select_download_button, row, 2)
        row += 1
        gbox.addWidget(qtw.QLabel('Location for save files:', self), row, 0)
        self.savepath_text = qtw.QLineEdit(self)
        self.savepath_text.setText(origsavepath)
        self.savepath_text.setMinimumWidth(380)
        # self.savepath_text.setMaximumWidth(120)
        gbox.addWidget(self.savepath_text, row, 1)
        self.select_savepath_button = qtw.QPushButton('Browse', self)
        self.select_savepath_button.clicked.connect(self.select_savepath)
        gbox.addWidget(self.select_savepath_button, row, 2)
        vbox.addLayout(gbox)
        # row += 1
        hbox = qtw.QHBoxLayout()
        save_button = qtw.QPushButton('&Save')
        save_button.clicked.connect(self.update)
        hbox.addWidget(save_button)
        close_button = qtw.QPushButton('&Cancel')
        close_button.clicked.connect(self.reject)
        hbox.addWidget(close_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.modbase_text.setFocus()

    def select_modbase(self):
        "define mod location"
        oldmodbase = self.modbase_text.text() or '~'
        filename = qtw.QFileDialog.getExistingDirectory(self,
                                                        caption="Where to install downloaded mods?",
                                                        directory=os.path.expanduser(oldmodbase))
        if filename:
            self.modbase_text.setText(filename.replace(os.path.expanduser('~'), '~'))

    def select_download_path(self):
        "define download location"
        olddownload = self.download_text.text() or '~'
        filename = qtw.QFileDialog.getExistingDirectory(self,
                                                        caption="Where to download mods to?",
                                                        directory=os.path.expanduser(olddownload))
        if filename:
            self.download_text.setText(filename.replace(os.path.expanduser('~'), '~'))

    def select_savepath(self):
        "define savefile location"
        oldsavepath = self.savepath_text.text() or '~'
        filename = qtw.QFileDialog.getExistingDirectory(self,
                                                        caption="Where are the saved games stored?",
                                                        directory=os.path.expanduser(oldsavepath))
        if filename:
            self.savepath_text.setText(filename.replace(os.path.expanduser('~'), '~'))

    def update(self):
        "update settings and exit"
        self.parent.master.dialog_data = (self.modbase_text.text(), self.config_text.text(),
                                          self.download_text.text(), self.savepath_text.text())
        self.accept()


class AttributesDialog(qtw.QDialog):
    """Dialog for viewing and optionally changing a mod's properties
    """
    seltext = 'select a mod to change the screen text'

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
        self.lbox.addItem(self.seltext)
        self.lbox.addItems(sorted(self.modnames))
        # self.lbox.currentTextChanged.connect(self.enable_select)
        self.lbox.currentTextChanged.connect(self.process)
        vbox.addWidget(self.lbox)
        # self.select_button = qtw.QPushButton('View &Attributes')
        # self.select_button.clicked.connect(self.process)
        # self.select_button.setEnabled(False)
        # vbox.addWidget(self.select_button)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Screen Name:\n'
                                  '(the suggestions in the box below are taken from\n'
                                  'the mod components', self))
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        self.name = qtw.QComboBox(self)
        self.name.setEditable(True)
        self.name.editTextChanged.connect(self.enable_change)
        self.name.setEnabled(False)
        hbox.addWidget(self.name)
        self.clear_name_button = qtw.QPushButton()
        self.clear_name_button.setIcon(qgui.QIcon.fromTheme(qgui.QIcon.ThemeIcon.EditClear))
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
        self.text.textEdited.connect(self.enable_change)
        self.text.setEnabled(False)
        hbox.addWidget(self.text)
        self.clear_text_button = qtw.QPushButton()
        self.clear_text_button.setIcon(qgui.QIcon.fromTheme(qgui.QIcon.ThemeIcon.EditClear))
        self.clear_text_button.setFixedSize(24, 24)
        self.clear_text_button.setDisabled(True)
        self.clear_text_button.clicked.connect(self.clear_text_text)
        hbox.addWidget(self.clear_text_button)
        vbox.addLayout(hbox)
        # hbox = qtw.QHBoxLayout()
        self.activate_button = qtw.QCheckBox('This mod can be activated by itself', self)
        self.activate_button.checkStateChanged.connect(self.enable_change)
        self.activate_button.setDisabled(True)
        # hbox.addWidget(self.activate_button)
        vbox.addWidget(self.activate_button)
        # vbox.addLayout(hbox)
        self.exempt_button = qtw.QCheckBox('Do not touch when (de)activating for a save', self)
        self.exempt_button.checkStateChanged.connect(self.enable_change)
        self.exempt_button.setDisabled(True)
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

    def enable_change(self):
        "enable change button"
        self.change_button.setEnabled(True)

    # def enable_select(self):
    #     """disable buttons after selecting another mod
    #     """
    #     # self.select_button.setEnabled(True)
    #     self.comps_button.setDisabled(True)
    #     self.deps_button.setDisabled(True)
    #     self.change_button.setDisabled(True)

    def process(self):
        "get description if any"
        # self.select_button.setDisabled(True)
        self.choice = self.lbox.currentText()
        if self.choice == self.seltext:
            self.name.setEnabled(False)
            self.text.setEnabled(False)
            self.activate_button.setDisabled(True)
            self.exempt_button.setDisabled(True)
            self.comps_button.setDisabled(True)
            self.deps_button.setDisabled(True)
            return
        self.name.clear()
        self.name.addItem(self.choice)
        items = set()
        for x in self.conf.list_components_for_dir(self.modnames[self.choice]):
            items.add(self.conf.get_component_data(x, self.conf.NAME))
        self.name.addItems(sorted(list(items)))
        self.name.setEnabled(True)
        self.clear_name_button.setDisabled(False)
        self.text.setText(self.parent.master.screeninfo[self.choice]['txt'])
        self.text.setEnabled(True)
        self.clear_text_button.setDisabled(False)
        self.activate_button.setChecked(self.parent.master.screeninfo[self.choice]['sel'])
        self.activate_button.setEnabled(True)
        self.exempt_button.setChecked(self.parent.master.screeninfo[self.choice]['opt'])
        self.exempt_button.setEnabled(True)
        self.comps_button.setDisabled(False)
        self.deps_button.setDisabled(False)
        self.change_button.setDisabled(True)

    def clear_name_text(self):
        "visually delete screen text"
        self.name.clear()

    def clear_text_text(self):
        "visually delete additional text if any"
        self.text.clear()

    def view_components(self):
        "list components for mod"
        message = self.parent.master.get_mod_components(self.modnames[self.choice])
        qtw.QMessageBox.information(self, 'SDVMM mod info', message)

    def view_dependencies(self):
        "list dependencies for mod"
        message = self.parent.master.get_mod_dependencies(self.modnames[self.choice])
        qtw.QMessageBox.information(self, 'SDVMM mod info', message)

    def update(self):
        "update screentext in dictionary"
        # self.text.setReadOnly(True)
        self.clear_name_button.setDisabled(True)
        self.clear_text_button.setDisabled(True)
        selectable = self.activate_button.isChecked()
        text = self.text.text()
        name = self.name.currentText()
        is_exempt = self.exempt_button.isChecked()
        ok, message = self.parent.master.update_attributes(selectable, name, self.choice,
                                                           text, is_exempt)
        if not ok:
            qtw.QMessageBox.information(self, 'SDVMM', message)
        else:
            self.change_button.setDisabled(True)


class SaveGamesDialog(qtw.QDialog):
    """Dialog for defining and viewing which mods are used for a (to be selected) savefile
    and optionally activating them
    """
    def __init__(self, parent, conf):
        self.parent = parent
        self.conf = conf
        self.savenames = conf.list_all_saveitems()
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
        self.pname.textEdited.connect(self.enable_change)
        self.fname = qtw.QLineEdit(self)
        self.fname.textEdited.connect(self.enable_change)
        self.gdate = qtw.QLineEdit(self)
        self.gdate.textEdited.connect(self.enable_change)
        self.widgets = []
        self.update_button = qtw.QPushButton('&Update config')
        self.update_button.setDisabled(True)
        self.update_button.clicked.connect(self.update)
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

    def enable_change(self):
        "enable change button"
        self.update_button.setEnabled(True)

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
        self.parent.master.refresh_widget_data()
        qtw.QMessageBox.information(self, 'Change Config', 'wijzigingen zijn doorgevoerd')

    def update(self):
        "callback for update button"
        self.update_conf(self.savegame_selector.currentText())

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

    def update_conf(self, savename):
        "save the mod associations in the config"
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
        self.conf.save()
        self.update_button.setDisabled(True)

    def get_savedata(self, newvalue):
        "find and show existing configuration data for this save file"
        if newvalue == 'select a saved game':
            return
        if self.oldsavename:
            self.update_conf(self.oldsavename)
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
