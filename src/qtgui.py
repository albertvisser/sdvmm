"""Stardew Valley Expansion manager - gui toolkit specific code
"""
import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qgui
download_dir = ''


def show_message(win, message, title='SDVMM'):
    "display a message in a box"
    qtw.QMessageBox.information(win, title, message)


def show_dialog(cls, parent, *args, **kwargs):
    "generic function for handling a dialog (instead of calling it directly)"
    # parent.dialog_data = {'mods': [], 'deps': {}, 'set_active': []}
    # ok = cls(parent, modnames, first_time).exec()
    dlg = cls(parent, *args, **kwargs)
    ok = dlg.doit.exec()
    # return ok == qtw.QDialog.DialogCode.Accepted, parent.dialog_data
    return ok == qtw.QDialog.DialogCode.Accepted  # , parent.dialog_data


class ShowMods(qtw.QWidget):
    "GUI presenting the available mods/extensions to make selection possible of mods to (de)activate"

    def __init__(self, master):
        self.master = master
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle('SDV Mod Manager')
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        self.buttons = {}

    def create_selectables_title(self, text):
        "create the first block of text"
        self.vbox.addWidget(qtw.QLabel(text))

    def create_selectables_grid(self):
        "show the mods that can be selected"
        self.gbox1 = qtw.QGridLayout()
        self.vbox.addLayout(self.gbox1)
        return self.gbox1

    def create_dependencies_title(self, text):
        "create the second block of text"
        self.vbox.addWidget(qtw.QLabel(text))

    def create_dependencies_grid(self):
        "show the mods that are selected automatically when needed"
        self.gbox2 = qtw.QGridLayout()
        self.vbox.addLayout(self.gbox2)
        return self.gbox2

    def create_buttons(self, buttondefs):
        "create the stuff that makes the application do things"
        self.vbox.addSpacing(10)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        for bdef in buttondefs:
            btn = qtw.QPushButton(bdef["text"], self)
            btn.clicked.connect(bdef["callback"])
            btn.setToolTip(bdef["tooltip"])
            hbox.addWidget(btn)
            self.buttons[bdef["name"]] = btn
        hbox.addStretch()
        self.vbox.addLayout(hbox)
        self.buttons["actv"].setEnabled(False)

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
        self.buttons['attr'].setEnabled(bool(self.master.screeninfo))
        self.buttons['sel'].setEnabled(bool(self.master.screeninfo))
        self.master.order_widgets(self.gbox1, self.gbox2, first_time)

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
            # check.stateChanged.connect(self.enable_button)
            check.clicked.connect(self.enable_button)
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
        # if not self.master.initializing:
        self.buttons['actv'].setEnabled(True)

    def update_mods(self):
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
        self.buttons['actv'].setEnabled(False)

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


class SettingsDialogGui(qtw.QDialog):
    """Dialog for changing some application defaults
    """
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent)
        self.vbox = qtw.QVBoxLayout()
        self.gbox = qtw.QGridLayout()
        self.vbox.addLayout(self.gbox)
        self.setLayout(self.vbox)
        self.row = 0
        # self.col = 0

    def add_label(self, labeltext):
        "add a label on the next row"
        self.row += 1
        self.gbox.addWidget(qtw.QLabel(labeltext, self), self.row, 0)  # self.col)
        # self.col += 1

    def add_line_entry(self, text):
        "add a text field on the same row as the label"
        cb = qtw.QLineEdit(self)
        cb.setText(text)
        cb.setMinimumWidth(380)
        self.gbox.addWidget(cb, self.row, 1)  # self.col)
        # self.col += 1
        return cb

    def add_browse_button(self, callback):
        "add a browse button on the same line as the text field"
        btn = qtw.QPushButton('Browse', self)
        btn.clicked.connect(callback)
        self.gbox.addWidget(btn, self.row, 2)  # self.col)
        return btn

    def add_spinbox(self, initial):
        "add a spinbox on the same row as the label"
        sp = qtw.QSpinBox(self)
        sp.setValue(initial)
        self.gbox.addWidget(sp, self.row, 1)
        return sp

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        hbox = qtw.QHBoxLayout()
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text)
            btn.clicked.connect(callback)
            hbox.addWidget(btn)
        self.vbox.addLayout(hbox)

    def set_focus(self, field):
        "set focus to field"
        field.setFocus()

    def get_widget_text(self, field):
        "get text from a widget"
        try:
            return field.text()
        except AttributeError:
            return field.value()

    def set_widget_text(self, field, value):
        "set a widget's text"
        field.setText(value)

    def select_directory(self, caption, start):
        "open a dialog for selecting a directory"
        return qtw.QFileDialog.getExistingDirectory(self, caption=caption, directory=start)

    def confirm(self):
        "close the dialog"
        self.accept()


class DeleteDialogGui(qtw.QDialog):
    """Dialog for viewing and optionally changing a mod's properties
    """
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_combobox(self, items, callback, editable=True):  # , enabled=True):
        "add a combobox on the next line"
        cb = qtw.QComboBox(self)
        cb.setEditable(editable)
        cb.addItems(items)
        cb.currentTextChanged.connect(callback)
        self.vbox.addWidget(cb)
        return cb

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        hbox = qtw.QHBoxLayout()
        buttons = []
        for text, callback, enabled in buttondefs:
            button = qtw.QPushButton(text)
            button.clicked.connect(callback)
            button.setEnabled(enabled)
            hbox.addWidget(button)
            buttons.append(button)
        self.vbox.addLayout(hbox)
        return buttons

    def set_focus(self, field):
        "set focus to field"
        field.setFocus()

    def get_combobox_entry(self, field):
        "get value from combobox"
        return field.currentText()

    def set_combobox_entry(self, field, value):
        "set the combobox entry (by index)"
        field.setCurrentIndex(value)

    def enable_button(self, field, value):
        "make a button usable or not"
        field.setEnabled(value)

    def confirm(self):
        "close the dialog"
        self.accept()


class AttributesDialogGui(qtw.QDialog):
    """Dialog for viewing and optionally changing a mod's properties
    """
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_combobox(self, items, callback, editable=True, enabled=True):
        "add a combobox on the next line"
        cb = qtw.QComboBox(self)
        cb.setEditable(editable)
        cb.setEnabled(enabled)
        cb.addItems(items)
        cb.currentTextChanged.connect(callback)
        if editable:
            cb.editTextChanged.connect(callback)
        if items:
            self.vbox.addWidget(cb)
        else:
            self.hbox.addWidget(cb)
        return cb

    def add_label(self, labeltext):
        "add a label on the next line"
        self.vbox.addWidget(qtw.QLabel(labeltext, self))

    def add_line_entry(self, text, callback, enabled=True):
        "add a text field on the next line"
        text = qtw.QLineEdit(self)
        text.textEdited.connect(callback)
        text.setEnabled(enabled)
        # self.vbox.addWidget(text)
        self.hbox.addWidget(text)
        return text

    def add_checkbox(self, text, callback, enabled=True):
        "add a checkbox on the next line"
        cb = qtw.QCheckBox(text, self)
        cb.checkStateChanged.connect(callback)
        cb.setEnabled(enabled)
        self.vbox.addWidget(cb)
        return cb

    def add_button(self, text, callback, pos=0, enabled=True):
        "add a button on the next line"
        if pos == 1:
            self.localbuttonbox = qtw.QHBoxLayout()
            self.vbox.addLayout(self.localbuttonbox)
        button = qtw.QPushButton(text)
        button.clicked.connect(callback)
        if pos > 0:
            self.localbuttonbox.addWidget(button)
        else:
            self.vbox.addWidget(button)
        button.setEnabled(enabled)
        return button

    def add_menubutton(self, text, options, callbacks, pos, enabled=True):
        "add a button with a popup menu on the next line"
        button = qtw.QPushButton(text)
        menu = qtw.QMenu()
        for ix, name in enumerate(options):
            menu.addAction(name).triggered.connect(callbacks[ix])
        button.setMenu(menu)
        button.setEnabled(enabled)
        self.localbuttonbox.addWidget(button)
        return button

    def start_line_with_clear_button(self):
        "prepare for adding a line with two widgets"
        self.hbox = qtw.QHBoxLayout()
        self.vbox.addLayout(self.hbox)

    def add_clear_button(self, clear_button_callback):
        "add a simple button to clear another widget's contents"
        # hbox = qtw.QHBoxLayout()
        # hbox.addWidget(widget)
        button = qtw.QPushButton()
        button.setIcon(qgui.QIcon.fromTheme(qgui.QIcon.ThemeIcon.EditClear))
        button.setFixedSize(24, 24)
        button.setDisabled(True)
        button.clicked.connect(clear_button_callback)
        self.hbox.addWidget(button)
        # hbox.addWidget(button)
        # self.vbox.addLayout(hbox)
        return button

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        hbox = qtw.QHBoxLayout()
        buttons = []
        for text, callback, enabled in buttondefs:
            button = qtw.QPushButton(text)
            button.setEnabled(enabled)
            button.clicked.connect(callback)
            hbox.addWidget(button)
            buttons.append(button)
        self.vbox.addLayout(hbox)
        return buttons

    def set_focus(self, field):
        "set focus to field"
        field.setFocus()

    def enable_button(self, field, value):
        "make a button (un)usable"
        field.setEnabled(value)

    def get_combobox_value(self, field):
        "retrieve the selected/entered value from a combobox"
        return field.currentText()

    def get_checkbox_value(self, field):
        "retrieve the value from a checkbox"
        return field.isChecked()

    def get_field_text(self, field):
        "retrieve a field's text value"
        return field.text()

    def reset_all_fields(self, fields):
        "set the specified fields to their default values / states"
        fields[0].clear()
        fields[0].setEnabled(False)
        fields[2].clear()
        fields[2].setEnabled(False)
        fields[4].setDisabled(True)
        fields[4].setChecked(False)
        fields[5].setDisabled(True)
        fields[5].setChecked(False)
        fields[6].setDisabled(True)
        fields[7].setDisabled(True)
        fields[8].setDisabled(True)
        fields[9].setDisabled(True)
        fields[10].setDisabled(True)
        fields[11].setDisabled(True)

    def activate_and_populate_fields(self, fields, items, screeninfo):
        "update the specified fields to be usable and enter some defaults"
        fields[0].clear()
        fields[0].addItems(items)
        fields[0].setEnabled(True)
        fields[1].setDisabled(False)
        fields[2].setText(screeninfo['txt'])
        fields[2].setEnabled(True)
        fields[3].setDisabled(False)
        fields[4].setChecked(screeninfo['sel'])
        fields[4].setEnabled(True)
        fields[5].setChecked(screeninfo['opt'])
        fields[5].setEnabled(True)
        fields[6].setDisabled(False)
        fields[7].setDisabled(False)
        fields[8].setDisabled(True)
        fields[9].setDisabled(False)
        fields[10].setDisabled(False)
        fields[11].setDisabled(False)

    def clear_field(self, field):
        "empty a field's (text) contents"
        field.clear()


class RestoreDialogGui(qtw.QDialog):
    """screen for dialog to select restore method
    """
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_checkbox(self, text, state):
        "add a checkbox on the next line"
        cb = qtw.QCheckBox(text, self)
        cb.setEnabled(state)
        self.vbox.addWidget(cb)
        return cb

    def get_checkbox_value(self, field):
        "retrieve the value from a checkbox"
        return field.isChecked()

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        hbox = qtw.QHBoxLayout()
        for text, callback in buttondefs:
            button = qtw.QPushButton(text)
            button.clicked.connect(callback)
            hbox.addWidget(button)
        self.vbox.addLayout(hbox)

    def set_focus(self, field):
        "set focus to field"
        field.setFocus()


class DependencyDialogGui(qtw.QDialog):
    """Dialog for manually defining a new dependency
    """
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_label(self, labeltext):
        "add a label to the next line"
        lbl = qtw.QLabel(labeltext, self)
        self.vbox.addWidget(lbl)
        return lbl

    def add_combobox(self, items, callback, editable=True, enabled=True):
        "add a combobox to the next line"
        cb = qtw.QComboBox(self)
        cb.setEditable(editable)
        cb.setEnabled(enabled)
        cb.addItems(items)
        if callback:
            cb.currentTextChanged.connect(callback)
        self.vbox.addWidget(cb)
        return cb

    def set_field_enabled(self, field, value):
        "make a fied usable"
        field.setEnabled(value)

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        hbox = qtw.QHBoxLayout()
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text)
            btn.clicked.connect(callback)
            hbox.addWidget(btn)
        self.vbox.addLayout(hbox)

    def set_focus(self, field):
        "set focus to field"
        field.setFocus()

    def get_combobox_value(self, field):
        "get the selected / entered value from a combobox"
        return field.currentText()

    def confirm(self):
        "close the dialog"
        super().accept()


class SaveGamesDialogGui(qtw.QDialog):
    """Dialog for defining and viewing which mods are used for a (to be selected) savefile
    and optionally activating them
    """
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_combobox(self, items, callback, editable=True, enabled=True):
        "add a combobox to the next line"
        cb = qtw.QComboBox(self)
        cb.setEditable(editable)
        cb.setEnabled(enabled)
        cb.addItems(items)
        if callback:
            cb.currentTextChanged.connect(callback)
            self.vbox.addWidget(cb)
        else:
            self.hmsbox = qtw.QHBoxLayout()
            self.hmsbox.addWidget(cb)
            self.msbox.insertLayout(len(self.msbox) - 1, self.hmsbox)
        return cb

    def get_combobox_value(self, field):
        "get the selected / entered value from a combobox"
        return field.currentText()

    def set_combobox_value(self, field, value):
        "set the text value for a combobox"
        field.setCurrentText(value)

    def add_label(self, labeltext):
        "add a label to the next line in a grid, creating the grid if necessary"
        # if not hasattr(self, 'gbox'):
        try:
            test = self.__getattribute__('gbox')
        except AttributeError:
            self.gbox = qtw.QGridLayout()
            self.vbox.addLayout(self.gbox)
            self.row = 0
        self.gbox.addWidget(qtw.QLabel(labeltext, self), self.row, 0)  # self.col)

    def add_line_entry(self, text):
        "add a text field to the same line in the grid"
        lb = qtw.QLineEdit(self)
        lb.setText(text)
        lb.setMinimumWidth(380)
        self.gbox.addWidget(lb, self.row, 1)
        self.row += 1
        return lb

    def set_field_text(self, field, text):
        "set the vaule for a field"
        field.setText(text)

    def get_field_text(self, field):
        "get a field's (text) value"
        return field.text()

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        hbox = qtw.QHBoxLayout()
        buttons = []
        for text, callback, enabled in buttondefs:
            btn = qtw.QPushButton(text)
            btn.clicked.connect(callback)
            btn.setEnabled(enabled)
            hbox.addWidget(btn)
            buttons.append(btn)
        self.vbox.addLayout(hbox)
        return buttons

    def set_focus(self, field):
        "set focus to field"
        field.setFocus()

    def start_modselect_block(self, labeltext):
        "start the block containing the mod selection checkboxes"
        self.msbox = qtw.QVBoxLayout()
        self.msbox.addWidget(qtw.QLabel(labeltext, self))
        self.msbox.addStretch()
        self.vbox.addLayout(self.msbox)

    def add_clear_button(self, enabled):
        "add a simple button to clear another widget's contents"
        # hbox = qtw.QHBoxLayout()
        # hbox.addWidget(widget)
        button = qtw.QPushButton()
        button.setIcon(qgui.QIcon.fromTheme(qgui.QIcon.ThemeIcon.EditClear))
        button.setFixedSize(24, 24)
        button.setEnabled(enabled)
        # # button.clicked.connect(clear_button_callback)
        # hbox.addWidget(button)
        # # self.vbox2.addLayout(hbox)
        # self.msbox.insertLayout(len(self.msbox) - 1, hbox)
        container, self.hmsbox = self.hmsbox, None
        container.addWidget(button)
        return button, container

    def set_callbacks(self, widgets, callbacks):
        "set the variable callbacks for the fields"
        widgets[0].currentTextChanged.connect(callbacks[0])
        widgets[1].clicked.connect(callbacks[1])

    def enable_change(self):
        "enable change button"
        self.master.update_button.setEnabled(True)

    def enable_widget(self, widget, value):
        "make a widget (un)usable"
        widget.setEnabled(value)

    def remove_modselector(self, widgets):
        "remove a checkbox / button combination"
        button, lbox, container = widgets
        container.removeWidget(button)
        button.close()
        container.removeWidget(lbox)
        lbox.close()
        self.msbox.removeItem(container)
        # widgets[2].close()
