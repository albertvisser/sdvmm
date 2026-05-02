"""SDVMM tkinter versie
"""
import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as MessageBox
import tkinter.filedialog as FileDialog
from PIL import ImageTk, Image
import webbrowser
# ECIMAGE = Image.open('/usr/share/icons/HighContrast/16x16/actions/edit-clear.png')
ECIMAGE = Image.open(os.path.join(os.path.dirname(__file__), 'edit-clear.png'))


def get_shortcut_info(text):
    "extract shortcut indicators (location and mnemonic) from (button) text"
    pos = text.index('&')
    text = text.replace('&', '')
    char = text[pos].lower()
    return pos, text, char


def show_message(win, message, title='SDVMM'):
    "display a message in a box"
    MessageBox.showinfo(parent=win, message=message, title=title)


def show_dialog(cls, parent, *args, **kwargs):
    "generic function for handling a dialog (instead of calling it directly)"
    dlg = cls(parent, *args, **kwargs)
    dlg.doit.focus_set()
    dlg.doit.grab_set()
    dlg.doit.wait_window()
    return True


class ShowMods():
    "Hoofdscherm van de applicatie"

    def __init__(self, master):
        self.master = master
        self.root = tk.Tk()
        self.root.option_add('*tearOff', False)
        self.ecimage = ImageTk.PhotoImage(ECIMAGE)
        self.root.title("SDV Mod Manager")
        self.main = ttk.Frame(self.root)
        self.main.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))  # main.pack()
        self.buttons = {}

    def create_selectables_title(self, text):
        "create the first block of text"
        toptext = ttk.Label(self.main, text=text, padding=10)
        toptext.grid(column=0, row=0, sticky=(tk.N, tk.W))  # toptext.pack()

    def create_selectables_grid(self):
        "show the mods that can be selected"
        self.activatables = ttk.Frame(self.main, padding=(10, 0))
        self.activatables.grid(column=0, row=1)  # pack()
        return self.activatables

    def create_dependencies_title(self, text):
        "create the second block of text"
        mid_message = ttk.Label(self.main, text=text, padding=10)
        mid_message.grid(column=0, row=2, sticky=(tk.N, tk.W))  # pack(side=tk.LEFT)

    def create_dependencies_grid(self):
        "show the mods that are selected automatically when needed"
        self.dependencies = ttk.Frame(self.main, padding=(10, 0))
        self.dependencies.grid(column=0, row=3)  # pack()
        return self.dependencies

    def create_buttons(self, buttondefs):
        "create the stuff that makes the application do things"
        bottomline = ttk.Frame(self.root, padding=10)
        bottomline.grid(column=0, row=3, sticky=tk.S)  # pack(side=tk.BOTTOM)
        pos = 0
        for bdef in buttondefs:
            if bdef["text"] == '&Close':
                underline_index = 2
            else:
                underline_index = bdef["text"].index('&')
            newtext = bdef["text"].replace("&", '')
            self.buttons[bdef["name"]] = ttk.Button(bottomline, text=newtext,
                                                    command=bdef["callback"],
                                                    underline=underline_index)
            # self.buttons[key].setToolTip(bdef["tooltip"])
            self.buttons[bdef["name"]].grid(column=pos, row=0)  # .pack(side=tk.LEFT)\
            if bdef['name'] == 'actv':
                self.buttons[bdef["name"]].state(['disabled'])
            pos += 1

    def setup_actions(self):
        "define hotkey actions"
        self.root.bind('<Alt-d>', self.manage_defaults)
        self.root.bind('<Alt-i>', self.update_mods)
        self.root.bind('<Alt-r>', self.manage_deletions)
        self.root.bind('<Alt-m>', self.manage_attributes)
        self.root.bind('<Alt-a>', self.confirm)
        self.root.bind('<Control-Return>', self.confirm)
        self.root.bind('<Alt-s>', self.manage_savefiles)
        self.root.bind('<Alt-x>', self.close)
        self.root.bind('<Alt-o>', self.close)
        self.root.bind('<Control-q>', self.close)

    def show_screen(self):
        "show the screen and start the event loop"
        self.root.mainloop()

    def refresh_widgets(self, first_time=False):
        "set the checkboxes to the right values (first time: also create them)"
        self.buttons['attr'].state([f'{"!" if self.master.screeninfo else ""}disabled'])
        self.buttons['sel'].state([f'{"!" if self.master.screeninfo else ""}disabled'])
        self.master.order_widgets(self.activatables, self.dependencies, first_time)

    def remove_widgets(self, *args):  # widgetlist, container, row, col):
        """remove the widgets from the screen before replacing them
        tk version doesn't need
        """
        widgetlist = args[0]
        label, check = widgetlist[1:3]
        check.destroy()
        label.destroy()

    def add_checkbox(self, root, rownum, colnum, selectable):
        "add a checkbox and keep a reference to it"
        frm = ttk.Frame(root, padding=(5, 0, 5, 0))
        # frm.grid(column=colnum, row=rownum, sticky=tk.W)
        checkstate = tk.IntVar()
        check = ttk.Checkbutton(frm, variable=checkstate, command=self.enable_button)
        check.state([f'{"!" if selectable else ""}disabled', '!selected'])
        check.grid(column=1, row=0)  # .pack(side=tk.LEFT)
        labeltext = tk.StringVar()
        label = ttk.Label(frm, textvariable=labeltext)
        label.grid(column=2, row=0)  # .pack(side=LEFT)
        frm.grid(row=rownum, column=colnum, sticky=tk.W)
        return frm, label, check, labeltext, checkstate

    def set_label_text(self, widgetlist, name, updateid, text):
        """change the text on a label
        """
        label = widgetlist[1]
        if updateid:
            name = f'{name} ({updateid})'
            # name = f'{name}'
            label.bind('<Button-1>', self.open_browser)
            label.configure(foreground="blue", cursor="hand2")
        if text:
            name += ' ' + text
        labeltext = widgetlist[3]
        labeltext.set(name)
        widgetlist = (widgetlist[0], widgetlist[1], widgetlist[2], labeltext, widgetlist[4])

    def set_checkbox_state(self, widgetlist, state):
        "check or uncheck a checkbox"
        widgetlist[4].set(int(state))
        widgetlist = (widgetlist[0], widgetlist[1], widgetlist[2], widgetlist[3], widgetlist[4])

    def open_browser(self, event):
        """go to web address in label
        """
        text = event.widget.cget('text')
        name, rest = text.split("(", 1)
        updateid = rest.split(')', 1)[0]
        webaddr = self.master.build_link_text(name, updateid).split('"', 1)[1].split('"', 1)[0]
        webbrowser.open_new(webaddr)

    def close(self, event=None):
        "button callback to close the application"
        self.root.quit()

    def enable_button(self):
        "make activating the selected mods possible"
        self.buttons['actv'].state(['!disabled'])

    def manage_defaults(self, event=None):
        "open dialog to change defaults"
        self.master.manage_defaults()

    def update_mods(self, event=None):
        "(re)install downloaded mods"
        filenames = FileDialog.askopenfilename(title="Install downloaded mods", multiple=True,
                                               initialdir=self.master.downloads,
                                               filetypes=[('Zip files', '.zip')])
        if filenames:
            report = self.master.update_mods(filenames)
            MessageBox.showinfo(parent=self.root, message='\n'.join(report))

    def confirm(self):
        "build a list from the checked entries and pass it back to the caller"
        self.master.process_activations()
        MessageBox.showinfo(parent=self.root, message='wijzigingen zijn doorgevoerd')
        self.buttons['actv'].state(['disabled'])

    def get_labeltext_if_checked(self, widgetlist):
        """return the name of the mod associated with a checkbox
        """
        checked = widgetlist[-1].get()
        labeltext = widgetlist[-2].get()
        return labeltext.split('(', 1)[0].strip() if checked else ''

    def select_value(self, caption, options, editable=True, mandatory=False):
        "Select or enter a value in a dialog"
        self.dialog_data = ''
        while True:
            ChoiceDialog(self, caption, options, editable=editable)
            if not self.dialog_data:
                if not mandatory:
                    break
                MessageBox.showinfo(parent=self.root, message='You *must* select or enter a value')
            else:
                break
        return self.dialog_data

    def manage_attributes(self, event=None):
        "relay to master, swallowing the event argument"
        self.master.manage_attributes()

    def manage_deletions(self, event=None):
        "relay to master, swallowing the event argument"
        self.master.manage_deletions()

    def manage_savefiles(self, event=None):
        "relay to master, swallowing the event argument"
        self.master.manage_savefiles()


class SettingsDialogGui(tk.Toplevel):
    """Dialog for changing some application defaults
    """
    def __init__(self, dialogmaster, parent):
        self.dialogmaster = dialogmaster
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent.root)
        self.frm = ttk.Frame(self, padding=10)
        self.frm.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.frm.columnconfigure(0, weight=1)
        self.textvars = {}
        self.row = 0
        # self.col = 0

    def add_label(self, labeltext):
        "add a label on the next row"
        self.row += 1
        ttk.Label(self.frm, text=labeltext).grid(row=self.row, column=0, sticky=tk.W)

    def add_line_entry(self, text):
        "add a text field on the same row as the label"
        textvar = tk.StringVar()
        textbox = ttk.Entry(self.frm, width=48, textvariable=textvar)
        textvar.set(text)
        self.textvars[textbox] = textvar
        textbox.grid(row=self.row, column=1)
        # textbox.delete(0, 'end')
        # textbox.insert(0, text)
        return textbox

    def add_browse_button(self, callback):
        "add a browse button on the same line as the text field"
        btn = ttk.Button(self.frm, text='Browse', command=callback)
        btn.grid(row=self.row, column=2, sticky=tk.W)
        return btn

    def add_spinbox(self, initial):
        "add a spinbox on the same row as the label"
        textvar = tk.IntVar()
        textvar.set(initial)
        sp = ttk.Spinbox(self.frm, width=5, from_=0, to=5, textvariable=textvar)
        self.textvars[sp] = textvar
        sp.grid(row=self.row, column=1, sticky=tk.W)
        return sp

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        self.row += 1
        bbox = ttk.Frame(self, padding=10)
        bbox.grid(row=self.row, column=0)
        for ix, bdef in enumerate(buttondefs):
            text, callback = bdef
            pos, text, char = get_shortcut_info(text)
            btn = ttk.Button(bbox, text=text, underline=pos, command=callback)
            btn.grid(row=0, column=ix)
            self.bind(f'<Alt-{char}>', callback)
        self.bind("<Escape>", self.confirm)

    def set_focus(self, field):
        "set focus to field"
        field.focus_set()

    def get_widget_text(self, field):
        "get text from a widget"
        # return field.getvar(field.cget('textvariable'))
        return self.textvars[field].get()

    def set_widget_text(self, field, value):
        "set a widget's text"
        # field.setvar(field.cget('textvariable'), value)
        self.textvars[field].set(value)

    def select_directory(self, caption, start):
        "open a dialog for selecting a directory"
        dirname = FileDialog.askdirectory(title=caption, initialdir=start, mustexist=True)
        return dirname

    def reject(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.root.focus_set()
        self.destroy()

    def confirm(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.root.focus_set()
        self.destroy()


class ChoiceDialog(tk.Toplevel):
    """Dialog for selecting a value from a list
    """
    def __init__(self, parent, caption, options, editable):  # , conf):
        self.parent = parent
        super().__init__(self.parent.root)
        frm = ttk.Frame(self, padding=10)
        frm.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        frm.columnconfigure(0, weight=1)
        row = 0
        ttk.Label(frm, text=caption).grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.dirname = tk.StringVar()
        row += 1
        self.lbox = ttk.Combobox(frm, values=sorted(options), textvariable=self.dirname)
        self.dirname.set('')
        self.lbox.state([f'{"!" if editable else ""}readonly'])
        self.lbox.bind('<<ComboboxSelected>>', self.enable_accept)
        self.lbox.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        row += 1
        hfrm = ttk.Frame(frm)
        hfrm.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.ok_button = ttk.Button(hfrm, text="Ok", underline=0, command=self.accept)
        self.ok_button.state(['disabled'])
        self.ok_button.grid(row=0, column=0, sticky=(tk.E, tk.W))
        hfrm.columnconfigure(0, weight=1)
        ttk.Button(hfrm, text="Cancel", underline=0, command=self.close).grid(row=0, column=1,
                                                                              sticky=(tk.E, tk.W))
        hfrm.columnconfigure(1, weight=1)
        self.bind("<Alt-o>", self.accept)
        self.bind("<Alt-c>", self.close)
        self.bind("<Escape>", self.close)
        self.lbox.focus_set()
        self.focus_set()
        self.grab_set()
        self.wait_window()

    def enable_accept(self, event):
        """make ok button usable
        """
        self.ok_button.state(['!disabled'])

    def accept(self, event=None):
        "close the dialog, returning the choice"
        self.parent.dialog_data = self.dirname.get()
        self.close()

    def close(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.root.focus_set()
        self.destroy()


class DeleteDialogGui(tk.Toplevel):
    """Dialog for viewing and optionally changing a mod's properties
    """
    def __init__(self, dialogmaster, parent):
        self.dialogmaster = dialogmaster
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent.root)
        self.frm = ttk.Frame(self, padding=10)
        self.frm.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.row = 0
        self.textvars = {}

    def add_combobox(self, items, callback, editable=True):
        "add a combobox on the next line"
        textvar = tk.StringVar()
        textvar.set(items.pop(0))   # 'Select a mod to remove from the config')
        cb = ttk.Combobox(self.frm, values=items, textvariable=textvar, width=40)
        self.textvars[cb] = textvar
        cb.state([f'{"!" if editable else ""}readonly'])
        cb.bind('<<ComboboxSelected>>', callback)
        cb.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.row += 1
        return cb

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        hfrm = ttk.Frame(self.frm)
        hfrm.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        buttons = []
        for ix, bdef in enumerate(buttondefs):
            text, callback, enabled = bdef
            pos, text, char = get_shortcut_info(text)
            button = ttk.Button(hfrm, text=text, underline=pos, command=callback)
            button.state([f'{"!" if enabled else ""}disabled'])
            button.grid(row=0, column=ix, sticky=(tk.E, tk.W))
            hfrm.columnconfigure(ix, weight=1)
            self.bind(f'Alt-{char}', callback)
            buttons.append(button)
        self.bind("<Escape>", self.accept)
        return buttons

    def set_focus(self, field):
        "set focus to field"
        field.focus_set()

    def get_combobox_entry(self, field):
        "get value from combobox"
        # return field.getvar(field.cget('textvariable'))
        return self.textvars[field].get()

    def set_combobox_entry(self, field, value):
        "set the combobox entry (by index)"
        # field.setvar(field.cget('textvariable'), value)
        self.textvars[field].set(value)

    def enable_button(self, field, value):
        "make a button usable or not"
        field.state([f'{"!" if value else ""}disabled'])

    def confirm(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.root.focus_set()
        self.destroy()

    def accept(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.root.focus_set()
        self.destroy()


class AttributesDialogGui(tk.Toplevel):
    """Dialog for viewing and optionally changing a mod's properties
    """
    def __init__(self, dialogmaster, parent):
        self.dialogmaster = dialogmaster
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent.root)
        self.frm = ttk.Frame(self, padding=10)
        self.frm.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.row = 0
        self.textvars = {}

    def add_combobox(self, items, callback, editable=True, enabled=True):
        "add a combobox on the next line"
        initial = items.pop(0) if items else ''
        textvar = tk.StringVar()
        textvar.set(initial)
        cb = ttk.Combobox(self.frm if items else self.hfrm, values=items, textvariable=textvar)
        cb.state([f'{"!" if editable else ""}readonly', f'{"!" if enabled else ""}disabled'])
        cb.bind('<<ComboboxSelected>>', callback)
        if editable:
            textvar.trace_add('write', self.monitor_textvar)
        #     cb.editTextChanged.connect(callback)
        cb.grid(row=self.row if items else 0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.textvars[cb] = textvar
        return cb

    def add_label(self, labeltext):
        "add a label on the next line"
        self.row += 1
        lbl = ttk.Label(self.frm, text=labeltext)
        lbl.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))

    def start_line_with_clear_button(self):
        "prepare for adding a line with two widgets"
        self.row += 1
        self.hfrm = ttk.Frame(self.frm)
        self.hfrm.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.hfrm.columnconfigure(0, weight=1)

    def add_clear_button(self, clear_button_callback):
        "add a simple button to clear another widget's contents"
        button = ttk.Button(self.hfrm, image=self.parent.ecimage, command=clear_button_callback)
        button.state(['disabled'])
        button.grid(row=0, column=1, sticky=tk.W)
        return button

    def add_line_entry(self, text, callback, enabled=True):
        "add a text field on the next line"
        textvar = tk.StringVar()
        textvar.set(text)
        if callback:
            textvar.trace_add('write', self.monitor_textvar)
        text = ttk.Entry(self.hfrm, textvariable=textvar)
        text.grid(row=0, column=0, sticky=(tk.E, tk.W))
        text.state([f'{"!" if enabled else ""}disabled'])
        self.textvars[text] = textvar
        return text

    def add_checkbox(self, text, callback, enabled=True):
        "add a checkbox on the next line"
        self.row += 1
        textvar = tk.IntVar()
        textvar.set(0)
        cb = ttk.Checkbutton(self.frm, text=text, variable=textvar, command=callback)
        cb.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        cb.state([f'{"!" if enabled else ""}disabled'])
        self.textvars[cb] = textvar
        return cb

    def add_button(self, text, callback, pos=0, enabled=True):
        "add a button on the next line"
        textpos, text, char = get_shortcut_info(text)
        self.row += 1
        if pos == 1:
            self.localbuttonbox = ttk.Frame(self.frm)
            self.localbuttonbox.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        if pos:
            button = ttk.Button(self.localbuttonbox, text=text, underline=textpos, command=callback)
            button.grid(row=0, column=pos - 1, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
            self.localbuttonbox.columnconfigure(pos - 1, weight=1)
        else:
            button = ttk.Button(self.frm, text=text, underline=textpos, command=callback)
            button.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        button.state([f'{"!" if enabled else ""}disabled'])
        self.bind(f'Alt-{char}', callback)
        return button

    def add_menubutton(self, text, options, callbacks, pos, enabled=True):
        "add a button with a popup menu on the next line"
        textpos, text, char = get_shortcut_info(text)
        button = tk.Menubutton(self.localbuttonbox, text=text, underline=textpos)
        # button['relief'] = 'raised'
        button.configure(relief='raised')
        button.grid(row=0, column=pos - 1, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.localbuttonbox.columnconfigure(pos - 1, weight=1)
        button.menu = tk.Menu(button)
        # button['menu'] = buttonmenu
        button.configure(menu=button.menu)
        for ix, name in enumerate(options):
            # menu.addAction(name).triggered.connect(callbacks[ix])
            button.menu.add_command(label=name, command=callbacks[ix])
        # button.state([f'{"!" if enabled else ""}disabled'])
        # button["state"] = "normal" if enabled else "disabled"
        button.configure(state="normal" if enabled else "disabled")
        return button

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        self.row += 1
        hfrm = ttk.Frame(self.frm)
        hfrm.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        buttons = []
        for ix, bdef in enumerate(buttondefs):
            text, callback, enabled = bdef
            pos, text, char = get_shortcut_info(text)
            button = ttk.Button(hfrm, text=text, underline=pos, command=callback)
            button.state([f'{"!" if enabled else ""}disabled'])
            button.grid(row=0, column=ix, sticky=(tk.E, tk.W))
            hfrm.columnconfigure(ix, weight=1)
            self.bind(f'Alt-{char}', callback)
            buttons.append(button)
        self.bind("<Escape>", self.close)
        return buttons

    def set_focus(self, field):
        "set focus to field"
        field.focus_set()

    def monitor_textvar(self, *args):
        "callback for trace_add"
        self.dialogmaster.enable_change()

    def enable_button(self, field, enabled):
        "make a button (un)usable"
        if isinstance(field, tk.Menubutton):
            # field["state"] = "normal" if enabled else "disabled"
            field.configure(state="normal" if enabled else "disabled")
        else:
            field.state([f'{"!" if enabled else ""}disabled'])

    def get_combobox_value(self, field):
        "retrieve the selected/entered value from a combobox"
        # return field.getvar(field.cget('textvariable'))
        return self.textvars[field].get()

    def get_checkbox_value(self, field):
        "retrieve the value from a checkbox"
        # return field.getvar(field.cget('textvariable'))
        return self.textvars[field].get()

    def get_field_text(self, field):
        "retrieve a field's text value"
        # return field.getvar(field.cget('textvariable'))
        return self.textvars[field].get()

    def reset_all_fields(self, fields):
        "set the specified fields to their default values / states"
        # deze methode is hier niet nodig, doet niks

    def activate_and_populate_fields(self, fields, items, screeninfo):
        "update the specified fields to be usable and enter some defaults"
        fields[0].configure(values=items)
        self.textvars[fields[0]].set(items[0])
        fields[0].state(['!disabled'])
        fields[1].state(['!disabled'])
        self.textvars[fields[2]].set(screeninfo['txt'])
        # fields[2].setvar(fields[2].cget('textvariable'), screeninfo['txt'])
        fields[2].state(['!disabled'])
        fields[3].state(['!disabled'])
        self.textvars[fields[4]].set(screeninfo['sel'])
        # fields[4].setvar(fields[4].cget('textvariable'), screeninfo['sel'])
        fields[4].state(['!disabled'])
        self.textvars[fields[5]].set(screeninfo['opt'])
        # fields[5].setvar(fields[5].cget('textvariable'), screeninfo['opt'])
        fields[5].state(['!disabled'])
        fields[6].state(['!disabled'])
        fields[7].state(['!disabled'])
        fields[8].state(['!disabled'])
        fields[9].state(['disabled'])
        fields[10].state(['!disabled'])
        fields[11].state(['!disabled'])
        fields[12].configure(state="normal")

    def clear_field(self, field):
        "empty a field's (text) contents"
        # field.setvar(field.cget('textvariable'), '')
        self.textvars[field].set('')

    def accept(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.root.focus_set()
        self.destroy()

    def close(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.root.focus_set()
        self.destroy()


class RestoreDialogGui(tk.Toplevel):
    """screen for dialog to select restore method
    """
    def __init__(self, dialogmaster, parent):
        self.dialogmaster = dialogmaster
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent)
        self.frm = ttk.Frame(self, padding=10)
        self.frm.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        # self.frm.columnconfigure(0, weight=1)
        self.row = 0
        self.textvars = {}

    def add_checkbox(self, text, callback, enabled=True):
        "add a checkbox on the next line"
        textpos, text, char = get_shortcut_info(text)
        self.row += 1
        textvar = tk.IntVar()
        textvar.set(0)
        cb = ttk.Checkbutton(self.frm, text=text, variable=textvar, underline=textpos,
                             command=callback)
        cb.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        cb.state([f'{"!" if enabled else ""}disabled'])
        self.bind(f'Alt-{char}', callback)
        self.textvars[cb] = textvar
        return cb

    def get_checkbox_value(self, field):
        "retrieve the value from a checkbox"
        # return field.getvar(field.cget('textvariable'))
        return self.textvars[field].get()

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        self.row += 1
        bbox = ttk.Frame(self, padding=10)
        bbox.grid(row=self.row, column=0)
        for ix, bdef in enumerate(buttondefs):
            text, callback = bdef
            pos, text, char = get_shortcut_info(text)
            btn = ttk.Button(bbox, text=text, underline=pos, command=callback)
            btn.grid(row=0, column=ix)
            self.bind(f'<Alt-{char}>', callback)
        self.bind('<Escape>', self.confirm)

    def set_focus(self, field):
        "set focus to field"
        field.focus_set()

    def confirm(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    def reject(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()


class DependencyDialogGui(tk.Toplevel):
    """Dialog for manually defining a new dependency
    """
    def __init__(self, dialogmaster, parent):
        self.dialogmaster = dialogmaster
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent)
        self.frm = ttk.Frame(self, padding=10)
        self.frm.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        # self.frm.columnconfigure(0, weight=1)
        self.row = 0
        self.textvars = {}

    def add_label(self, labeltext):
        "add a label to the next line"
        self.row += 1
        ttk.Label(self.frm, text=labeltext).grid(row=self.row, column=0, sticky=tk.W)

    def add_combobox(self, items, callback, editable=True, enabled=True):
        "add a combobox to the next line"
        self.row += 1
        textvar = tk.StringVar()
        textvar.set(items.pop(0))
        cb = ttk.Combobox(self.frm, values=items, textvariable=textvar)
        cb.state([f'{"!" if editable else ""}readonly', f'{"!" if enabled else ""}disabled'])
        cb.bind('<<ComboboxSelected>>', callback)
        cb.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.textvars[cb] = textvar
        return cb

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        self.row += 1
        bbox = ttk.Frame(self, padding=10)
        bbox.grid(row=self.row, column=0)
        for ix, bdef in enumerate(buttondefs):
            text, callback = bdef
            pos, text, char = get_shortcut_info(text)
            btn = ttk.Button(bbox, text=text, underline=pos, command=callback)
            btn.grid(row=0, column=ix)
            self.bind(f'<Alt-{char}>', callback)
        self.bind('<Escape>', self.confirm)

    def set_focus(self, field):
        "set focus to field"
        field.focus_set()

    def set_field_enabled(self, field, value):
        "make a fied usable"
        field.state([f'{"!" if value else ""}disabled'])

    def get_combobox_value(self, field):
        "get the selected / entered value from a combobox"
        return self.textvars[field].get()
        # return field.getvar(field.cget('textvariable'))

    def reject(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    def confirm(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()


class SaveGamesDialogGui(tk.Toplevel):
    """Dialog for defining and viewing which mods are used for a (to be selected) savefile
    and optionally activating them
    """
    def __init__(self, dialogmaster, parent):
        self.dialogmaster = dialogmaster
        self.parent = parent  # DialogGui heeft dezelfde parent als Dialog
        super().__init__(parent.root)
        self.frm = ttk.Frame(self, padding=10)
        self.frm.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.row = 0
        self.textvars = {}

    def add_combobox(self, items, callback, editable=True, enabled=True):
        "add a combobox to the next line"
        if callback:
            initial = items.pop(0)
            frame = self.frm
            rownum = self.row
        else:
            initial = 'select a mod'  # 'select a mod' if callback is None else items.pop(0)
            self.hmsfrm = ttk.Frame(self.msfrm, padding=10)
            self.hmsfrm.grid(row=self.msrow, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
            self.hmsfrm.columnconfigure(0, weight=1)
            frame = self.hmsfrm
            rownum = 0
        textvar = tk.StringVar()
        textvar.set(initial)
        cb = ttk.Combobox(frame, values=items, textvariable=textvar)
        cb.state([f'{"!" if editable else ""}readonly', f'{"!" if enabled else ""}disabled'])
        cb.grid(row=rownum, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        if callback:
            cb.bind('<<ComboboxSelected>>', callback)
        self.textvars[cb] = textvar
        return cb

    def get_combobox_value(self, field):
        "get the selected / entered value from a combobox"
        return self.textvars[field].get()
        # return field.getvar(field.cget('textvariable'))

    def set_combobox_value(self, field, value):
        "set the text value for a combobox"
        self.textvars[field].set(value)
        # dit is altijd een modselector checkbox
        # en dan moet ik de wijzig callback met de hand uitvoeren
        self.dialogmaster.process_mod(field, value)
        self.enable_widget(field, True)

    def add_label(self, labeltext):
        "add a label to the next line in a grid, creating the grid if necessary"
        self.row += 1
        if not hasattr(self, 'hfrm'):
            self.hfrm = ttk.Frame(self.frm)
            self.hfrm.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
            self.hfrm.columnconfigure(1, weight=1)
            self.hrow = 0
        ttk.Label(self.hfrm, text=labeltext).grid(row=self.hrow, column=0)

    def add_line_entry(self, text):
        "add a text field to the same line in the grid"
        textvar = tk.StringVar()
        textvar.set(text)
        cb = ttk.Entry(self.hfrm, textvariable=textvar)
        cb.state(['readonly'])
        cb.grid(row=self.hrow, column=1)
        self.textvars[cb] = textvar
        self.hrow += 1
        return cb

    def set_field_text(self, field, value):
        "set the vaule for a field"
        self.textvars[field].set(value)
        # field.setvar(field.cget('textvariable'), value)

    def get_field_text(self, field):
        "get a field's (text) value"
        return self.textvars[field].get()
        # return field.getvar(field.cget('textvariable'))

    def start_modselect_block(self, labeltext):
        "start the block containing the mod selection checkboxes"
        self.row += 1
        ttk.Label(self.frm, text=labeltext).grid(row=self.row, column=0, sticky=tk.W)
        self.row += 1
        self.msfrm = ttk.Frame(self.frm)
        self.msfrm.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.msfrm.columnconfigure(0, weight=1)
        self.msrow = 0

    def add_clear_button(self, enabled):
        "add a simple button to clear another widget's contents"
        # widget.grid(row=self.msrow, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        # btn = ttk.Button(self.msfrm, image=self.parent.ecimage)
        # btn.state([f'{"!" if disable_button else ""}disabled'])
        # btn.grid(row=self.msrow, column=1)
        # frm = ttk.Frame(self.msfrm, padding=10)
        # frm.grid(row=self.msrow, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        # frm.columnconfigure(0, weight=1)
        # widget.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        btn = ttk.Button(self.hmsfrm, image=self.parent.ecimage)
        btn.state([f'{"!" if enabled else ""}disabled'])
        btn.grid(row=0, column=1)
        self.msrow += 1
        return btn, self.hmsfrm

    def set_callbacks(self, widgets, callbacks):
        "set the variable callbacks for the fields"
        widgets[0].bind('<<ComboboxSelected>>', callbacks[0])
        widgets[1].bind('<Return>', callbacks[1])

    def add_buttonbox(self, buttondefs):
        "add a row of buttons at the bottom of the page"
        self.row += 1
        hfrm = ttk.Frame(self.frm)
        hfrm.grid(row=self.row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        buttons = []
        for ix, bdef in enumerate(buttondefs):
            text, callback, enabled = bdef
            pos, text, char = get_shortcut_info(text)
            button = ttk.Button(hfrm, text=text, underline=pos, command=callback)
            button.state([f'{"!" if enabled else ""}disabled'])
            button.grid(row=0, column=ix, sticky=(tk.E, tk.W))
            hfrm.columnconfigure(ix, weight=1)
            buttons.append(button)
            self.bind(f"<Alt-{char}>", callback)
        self.bind("<Escape>", self.accept)
        return buttons

    def set_focus(self, field):
        "set focus to field"
        field.focus_set()

    def enable_widget(self, widget, value):
        "make a widget (un)usable"
        widget.state([f'{"!" if value else ""}disabled'])

    def remove_modselector(self, widgets):
        "remove a checkbox / button combination"
        self.textvars.pop(widgets[1])
        widgets[0].forget()
        widgets[0].destroy()
        widgets[1].forget()
        widgets[1].destroy()
        widgets[2].forget()
        widgets[2].destroy()

    def accept(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.root.focus_set()
        self.destroy()
