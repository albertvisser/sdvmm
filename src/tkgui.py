"""SDVMM tkinter versie
"""
import os
import functools
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as MessageBox
import tkinter.filedialog as FileDialog
from PIL import ImageTk, Image
# ECIMAGE = Image.open('/usr/share/icons/HighContrast/16x16/actions/edit-clear.png')
ECIMAGE = Image.open(os.path.join(os.path.dirname(__file__), 'edit-clear.png'))


def show_dialog(cls, parent, *args, **kwargs):
    "generic function for handling a dialog (instead of calling it directly)"
    dlg = cls(parent, *args, **kwargs)
    dlg.focus_set()
    dlg.grab_set()
    dlg.wait_window()
    return True


class ShowMods():
    "Hoofdscherm van de applicatie"

    def __init__(self, master):
        self.master = master
        self.root = tk.Tk()
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

    def create_dependencies_title(self, text):
        "create the second block of text"
        mid_message = ttk.Label(self.main, text=text, padding=10)
        mid_message.grid(column=0, row=2, sticky=(tk.N, tk.W))  # pack(side=tk.LEFT)

    def create_dependencies_grid(self):
        "show the mods that are selected automatically when needed"
        self.dependencies = ttk.Frame(self.main, padding=(10, 0))
        self.dependencies.grid(column=0, row=3)  # pack()

    def create_buttons(self, buttondefs):
        "create the stuff that makes the application do things"
        bottomline = ttk.Frame(self.root, padding=10)
        bottomline.grid(column=0, row=3, sticky=tk.S)  # pack(side=tk.BOTTOM)
        pos = 0
        for bdef in buttondefs:
            underline_index = bdef["text"].index('&')
            newtext = bdef["text"].replace("&", '')
            self.buttons[bdef["name"]] = ttk.Button(bottomline, text=newtext,
                                                    command=bdef["callback"],
                                                    underline=underline_index)
            # self.buttons[key].setToolTip(bdef["tooltip"])
            self.buttons[bdef["name"]].grid(column=pos, row=0)  # .pack(side=tk.LEFT)\
            pos += 1
        self.refresh_widgets(first_time=True)

    def setup_actions(self):
        "define hotkey actions"
        self.root.bind('<Alt-d>', self.manage_defaults)
        self.root.bind('<Alt-i>', self.update_mods)
        self.root.bind('<Alt-r>', self.remove_mods)
        self.root.bind('<Alt-m>', self.manage_attributes)
        self.root.bind('<Alt-a>', self.confirm)
        self.root.bind('<Control-Return>', self.confirm)
        self.root.bind('<Alt-s>', self.manage_savefiles)
        self.root.bind('<Alt-x>', self.close)
        self.root.bind('<Control-q>', self.close)

    def show_screen(self):
        "show the screen and start the event loop"
        self.root.mainloop()

    def refresh_widgets(self, first_time=False):
        "set the checkboxes to the right values (first time: also create them)"
        self.buttons['attr'].state([f'{"!" if self.master.screeninfo else ""}disabled'])
        self.buttons['sel'].state([f'{"!" if self.master.screeninfo else ""}disabled'])
        self.master.order_widgets(first_time, self.activatables, self.dependencies)

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
        if updateid:
            name = f'{name} ({updateid})'
        if text:
            name += ' ' + text
        labeltext = widgetlist[3]
        labeltext.set(name)
        widgetlist = (widgetlist[0], widgetlist[1], widgetlist[2], labeltext, widgetlist[4])

    def set_checkbox_state(self, widgetlist, state):
        "check or uncheck a checkbox"
        widgetlist[4].set(int(state))
        widgetlist = (widgetlist[0], widgetlist[1], widgetlist[2], widgetlist[3], widgetlist[4])

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

    def remove_mods(self):
        "remove mods from screen and config"
        MessageBox.showinfo(parent=self.root, message='W.I.P. - Nog even geduld a.u.b.')

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

    def manage_savefiles(self, event=None):
        "relay to master, swallowing the event argument"
        self.master.manage_savefiles()


class SettingsDialog(tk.Toplevel):
    """Dialog for changing some application defaults
    """
    def __init__(self, parent):  # , conf):
        self.parent = parent
        self.choice = ''
        super().__init__(parent.root)

        data = self.parent.master.dialog_data
        origmodbase, origconfig, origdownload, origcolcount, origsavepath = data

        frm = ttk.Frame(self, padding=10)
        frm.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        frm.columnconfigure(0, weight=1)
        row = 0
        ttk.Label(frm, text='Base location for mods:').grid(row=row, column=0, sticky=tk.W)
        self.modbase_text = tk.StringVar()
        self.modbase_text.set(origmodbase)
        modbase = ttk.Entry(frm, width=48, textvariable=self.modbase_text)
        modbase.grid(row=row, column=1)
        sel_modbase_button = ttk.Button(frm, text='Browse', command=self.select_modbase)
        sel_modbase_button.grid(row=row, column=2, sticky=tk.W)
        row += 1
        ttk.Label(frm, text='Name of configuration file:').grid(row=row, column=0, sticky=tk.W)
        self.config_text = tk.StringVar()
        self.config_text.set(origconfig)
        config = ttk.Entry(frm, width=48, textvariable=self.config_text)
        config.grid(row=row, column=1)
        row += 1
        ttk.Label(frm, text='Location for downloads:').grid(row=row, column=0, sticky=tk.W)
        self.download_text = tk.StringVar()
        self.download_text.set(origdownload)
        download = ttk.Entry(frm, width=48, textvariable=self.download_text)
        download.grid(row=row, column=1)
        sel_download_button = ttk.Button(frm, text='Browse', command=self.select_download_path)
        sel_download_button.grid(row=row, column=2, sticky=tk.W)
        row += 1
        ttk.Label(frm, text='Number of columns on screen:').grid(row=row, column=0, sticky=tk.W)
        self.columncount = tk.IntVar()
        self.columncount.set(origcolcount)
        columns = ttk.Spinbox(frm, width=5, from_=0, to=5, textvariable=self.columncount)
        columns.grid(row=row, column=1, sticky=tk.W)
        row += 1
        ttk.Label(frm, text='Location for save files:').grid(row=row, column=0, sticky=tk.W)
        self.savepath_text = tk.StringVar()
        self.savepath_text.set(origsavepath)
        savepath = ttk.Entry(frm, width=48, textvariable=self.savepath_text)
        savepath.grid(row=row, column=1)
        sel_savepath_button = ttk.Button(frm, text='Browse', command=self.select_savepath)
        sel_savepath_button.grid(row=row, column=2, sticky=tk.W)
        row += 1
        bbox = ttk.Frame(self, padding=10)
        bbox.grid(row=1, column=0)
        ok_button = ttk.Button(bbox, text='Save', underline=0, command=self.update)
        ok_button.grid(row=0, column=0)
        cancel_button = ttk.Button(bbox, text='Cancel', underline=0, command=self.close)
        cancel_button.grid(row=0, column=1)
        self.bind_all('<Alt-s>', self.update)
        self.bind_all('<Alt-c>', self.close)
        self.bind_all('<Escape>', self.close)

    def select_modbase(self, event=None):
        "define mod location"
        oldmodbase = self.modbase_text.get() or '~'
        filename = FileDialog.askdirectory(title="Where to install downloaded mods?",
                                           initialdir=os.path.expanduser(oldmodbase),
                                           mustexist=True)
        if filename:
            self.modbase_text.set(filename.replace(os.path.expanduser('~'), '~'))

    def select_download_path(self, event=None):
        "define download location"
        olddownload = self.download_text.get() or '~'
        filename = FileDialog.askdirectory(title="Where to download mods to?",
                                           initialdir=os.path.expanduser(olddownload),
                                           mustexist=True)
        if filename:
            self.download_text.set(filename.replace(os.path.expanduser('~'), '~'))

    def select_savepath(self, event=None):
        "define savefile location"
        oldsavepath = self.savepath_text.get() or '~'
        filename = FileDialog.askdirectory(title="Where are the saved games stored?",
                                           initialdir=os.path.expanduser(oldsavepath),
                                           mustexist=True)
        if filename:
            self.savepath_text.set(filename.replace(os.path.expanduser('~'), '~'))

    def update(self, event=None):
        "update settings and exit"
        self.parent.master.dialog_data = (self.modbase_text.get(), self.config_text.get(),
                                          self.download_text.get(), self.columncount.get(),
                                          self.savepath_text.get())
        self.close()

    def close(self, event=None):
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


class AttributesDialog(tk.Toplevel):
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
        super().__init__(parent.root)

        # ecimage = ImageTk.PhotoImage(ECIMAGE)
        frm = ttk.Frame(self, padding=10)
        frm.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        row = 0
        # lbl = ttk.Label(frm, text='Select a mod to change the screen text etc.')
        # lbl.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        # row += 1
        self.modname = tk.StringVar()
        self.lbox = ttk.Combobox(frm, values=sorted(self.modnames), textvariable=self.modname)
        self.modname.set('Select a mod to change the screen text etc.')
        self.lbox.state(['readonly'])
        # self.lbox.bind('<<ComboboxSelected>>', self.enable_select)
        self.lbox.bind('<<ComboboxSelected>>', self.process)
        self.lbox.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        # row += 1
        # self.select_button = ttk.Button(frm, text='View Attributes', underline=5,
        #                                 command=self.process)
        # self.select_button.state(['disabled'])
        # self.select_button.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        row += 1
        lbl = ttk.Label(frm, text=('Screen Name:\n'
                                   '(the suggestions in the box below are taken from\n'
                                   'the mod components'))
        lbl.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        row += 1
        hfrm = ttk.Frame(frm)
        hfrm.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.scrname = tk.StringVar()
        self.scrname.set('')
        self.scrname.trace_add('write', self.monitor_textvar)
        self.name = ttk.Combobox(hfrm, textvariable=self.scrname)
        self.name.state(['!readonly', 'disabled'])
        self.name.bind('<<ComboboxSelected>>', self.enable_change)
        self.name.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        hfrm.columnconfigure(0, weight=1)
        self.clear_name_button = ttk.Button(hfrm, image=self.parent.ecimage,
                                            command=self.clear_name_text)
        self.clear_name_button.image = self.parent.ecimage
        self.clear_name_button.state(['disabled'])
        self.clear_name_button.grid(row=0, column=1, sticky=tk.W)
        row += 1
        lbl = ttk.Label(frm, text=('Screen Text:\n'
                                   '(to add some information e.q. if the mod is broken)'))
        lbl.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        row += 1
        hfrm = ttk.Frame(frm)
        hfrm.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        hfrm.columnconfigure(0, weight=1)
        self.scrtext = tk.StringVar()
        self.scrtext.set('')
        self.scrtext.trace_add('write', self.monitor_textvar)
        self.text = ttk.Entry(hfrm, textvariable=self.scrtext)
        self.text.grid(row=0, column=0, sticky=(tk.E, tk.W))
        self.text.state(['disabled'])
        self.clear_text_button = ttk.Button(hfrm, image=self.parent.ecimage,
                                            command=self.clear_text_text)
        # self.clear_text_button['image'] = ecimage
        # self.clear_button.resize(20, 20)
        # self.clear_text_button.setFixedSize(24, 24)
        self.clear_text_button.state(['disabled'])
        self.clear_text_button.grid(row=0, column=1, sticky=tk.W)
        row += 1
        self.activate = tk.IntVar()
        self.activate.set(0)
        self.activate_button = ttk.Checkbutton(frm, text='This mod can be activated by itself',
                                               variable=self.activate, command=self.enable_change)
        self.activate_button.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.activate_button.state(['disabled'])
        row += 1
        self.exempt = tk.IntVar()
        self.exempt.set(0)
        self.exempt_button = ttk.Checkbutton(frm, text='Do not touch when (de)activating for a save',
                                             variable=self.exempt, command=self.enable_change)
        self.exempt_button.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.exempt_button.state(['disabled'])
        row += 1
        self.comps_button = ttk.Button(frm, text='View Components', underline=5,
                                       command=self.view_components)
        self.comps_button.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.comps_button.state(['disabled'])
        row += 1
        self.deps_button = ttk.Button(frm, text='View Dependencies', underline=5,
                                      command=self.view_dependencies)
        self.deps_button.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.deps_button.state(['disabled'])

        row += 1
        hfrm = ttk.Frame(frm)
        hfrm.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.change_button = ttk.Button(hfrm, text="Update", underline=0, command=self.update)
        self.change_button.state(['disabled'])
        self.change_button.grid(row=0, column=0, sticky=(tk.E, tk.W))
        hfrm.columnconfigure(0, weight=1)
        close_button = ttk.Button(hfrm, text="Close", underline=2, command=self.close)
        close_button.grid(row=0, column=1, sticky=(tk.E, tk.W))
        hfrm.columnconfigure(1, weight=1)
        self.bind('<Alt-a>', self.process)
        self.bind('<Alt-c>', self.view_components)
        self.bind('<Alt-d>', self.view_dependencies)
        self.bind('<Alt-u>', self.update)
        self.bind('<Alt-o>', self.close)
        self.bind("<Escape>", self.close)
        self.lbox.focus_set()

    def monitor_textvar(self, *args):
        "callback for trace_add"
        self.enable_change()

    def enable_change(self, event=None):
        "enable change button"
        self.change_button.state(['!disabled'])

    # def enable_select(self, event=None):
    #     """disable buttons after selecting another mod
    #     """
    #     # self.select_button.state(['!disabled'])
    #     self.comps_button.state(['disabled'])
    #     self.deps_button.state(['disabled'])
    #     self.change_button.state(['disabled'])

    def process(self, event=None):
        "get description if any"
        # self.select_button.state(['disabled'])
        self.choice = self.modname.get()  # lbox.currentText()
        self.scrname.set(self.choice)
        items = set()
        for x in self.conf.list_components_for_dir(self.modnames[self.choice]):
            items.add(self.conf.get_component_data(x, self.conf.NAME))
        # self.name['values'] = [self.choice] + sorted(list(items))
        # self.name['values'] = sorted(list(items))
        self.name.configure(values=sorted(list(items)))
        self.name.state(['!disabled'])
        self.clear_name_button.state(['!disabled'])
        self.scrtext.set(self.parent.master.screeninfo[self.choice]['txt'])
        self.text.state(['!disabled'])
        self.clear_text_button.state(['!disabled'])
        # onoff = "" if self.parent.master.screeninfo[self.choice]['sel'] else "!"
        # self.activate_button.state([f'{onoff}selected'])
        self.activate.set(int(self.parent.master.screeninfo[self.choice]['sel']))
        self.activate_button.state(['!disabled'])
        # onoff = "" if self.parent.master.screeninfo[self.choice]['opt'] else "!"
        # self.exempt_button.state([f'{onoff}selected'])
        self.exempt.set(int(self.parent.master.screeninfo[self.choice]['opt']))
        self.exempt_button.state(['!disabled'])
        self.comps_button.state(['!disabled'])
        self.deps_button.state(['!disabled'])
        self.change_button.state(['disabled'])

    def clear_name_text(self, event=None):
        "visually delete screen text"
        self.scrname.set('')
        # self.name.delete(0, 'end')

    def clear_text_text(self, event=None):
        "visually delete additional text if any"
        self.scrtext.set('')
        # self.text.delete(0, 'end')

    def view_components(self, event=None):
        "list components for mod"
        message = self.parent.master.get_mod_components(self.modnames[self.choice])
        MessageBox.showinfo(parent=self, message=message)

    def view_dependencies(self, event=None):
        "list dependencies for mod"
        message = self.parent.master.get_mod_dependencies(self.modnames[self.choice])
        MessageBox.showinfo(parent=self, message=message)

    def update(self, event=None):
        "update screentext etc. in dictionary"
        # self.text.setReadOnly(True)
        self.clear_name_button.state(['disabled'])
        self.clear_text_button.state(['disabled'])
        selectable = self.activate_button.instate(['selected'])
        text = self.scrtext.get()
        name = self.scrname.get()
        is_exempt = self.exempt_button.instate(['selected'])
        ok, message = self.parent.master.update_attributes(selectable, name, self.choice,
                                                           text, is_exempt)
        if not ok:
            MessageBox.showinfo(parent=self, message=message)
        else:
            self.change_button.state(['disabled'])

    def close(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.root.focus_set()
        self.destroy()


class SaveGamesDialog(tk.Toplevel):
    """Dialog for defining and viewing which mods are used for a (to be selected) savefile
    and optionally activating them
    """
    def __init__(self, parent, conf):
        self.parent = parent
        self.conf = conf
        self.savenames = conf.list_all_saveitems()
        # for x in os.path.expanduser('~/.config/StardewValley/Saves').
        self.modnames = {}
        for x in conf.list_all_mod_dirs():
            self.modnames[conf.get_diritem_data(x, conf.SCRNAM)] = x
        super().__init__(parent.root)

        frm = ttk.Frame(self, padding=10)
        frm.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        row = 0
        self.savegame_selector_text = tk.StringVar()
        self.savegame_selector = ttk.Combobox(frm, values=sorted(self.savenames),
                                              textvariable=self.savegame_selector_text)
        self.savegame_selector_text.set('select a saved game')
        self.savegame_selector.state(['readonly'])
        self.savegame_selector.bind('<<ComboboxSelected>>', self.get_savedata)
        self.savegame_selector.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.oldsavename = ''
        row += 1
        hfrm = ttk.Frame(frm)
        hfrm.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        hfrm.columnconfigure(1, weight=1)
        ttk.Label(hfrm, text='Player name:').grid(row=0, column=0)
        self.pname_text = tk.StringVar()
        self.pname_text.set('')
        self.pname_text.trace_add('write', self.monitor_textvar)
        self.pname = ttk.Entry(hfrm, textvariable=self.pname_text)
        self.pname.grid(row=0, column=1)
        ttk.Label(hfrm, text='Farm name:').grid(row=1, column=0)
        self.fname_text = tk.StringVar()
        self.fname_text.set('')
        self.fname_text.trace_add('write', self.monitor_textvar)
        self.fname = ttk.Entry(hfrm, textvariable=self.fname_text)
        self.fname.grid(row=1, column=1)
        ttk.Label(hfrm, text='In-game date:').grid(row=2, column=0)
        self.gdate_text = tk.StringVar()
        self.gdate_text.set('')
        self.gdate_text.trace_add('write', self.monitor_textvar)
        self.gdate = ttk.Entry(hfrm, textvariable=self.gdate_text)
        self.gdate.grid(row=2, column=1)
        self.widgets = []

        row += 1
        hfrm = ttk.Frame(frm)
        hfrm.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        ttk.Label(hfrm, text='Uses:').grid(row=0, column=0)
        row += 1
        self.hfrm = ttk.Frame(frm)
        self.hfrm.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.hfrm.columnconfigure(0, weight=1)
        self.hfrmlen = 0
        # self.ecimage = ImageTk.PhotoImage(ECIMAGE)
        self.add_modselector()
        row += 1
        hfrm = ttk.Frame(frm)
        hfrm.grid(row=row, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        self.update_button = ttk.Button(hfrm, text='Update config', underline=0,
                                        command=self.update)
        self.update_button.state(['disabled'])
        self.update_button.grid(row=0, column=0)
        self.bind('<Alt-u>', self.update)
        hfrm.columnconfigure(0, weight=1)

        self.confirm_button = ttk.Button(hfrm, text='Activate Mods', underline=0,
                                         command=self.confirm)
        self.confirm_button.state(['disabled'])
        self.confirm_button.grid(row=0, column=1)
        self.bind('<Alt-a>', self.confirm)
        hfrm.columnconfigure(1, weight=1)

        self.close_button = ttk.Button(hfrm, text='Close', underline=0, command=self.close)
        self.close_button.grid(row=0, column=2)
        self.bind('<Alt-c>', self.close)
        self.bind('<Escape>', self.close)
        hfrm.columnconfigure(2, weight=1)

        self.savegame_selector.focus_set()

    def monitor_textvar(self, *args):
        "callback for trace_add - enable update button"
        self.update_button.state(['!disabled'])

    def add_modselector(self, name=''):
        "add a selector to make an association between a mod and the save file"
        self.hfrmlen += 1
        frm = ttk.Frame(self.hfrm)
        frm.grid(row=self.hfrmlen, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=2)
        lboxvar = tk.StringVar()
        lbox = ttk.Combobox(frm, values=sorted(self.modnames), textvariable=lboxvar)
        lbox.state(['readonly'])
        lboxvar.set('select a mod')
        lbox.bind('<<ComboboxSelected>>', functools.partial(self.process_mod, lbox))
        lbox.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        frm.columnconfigure(0, weight=1)
        btn = ttk.Button(frm, image=self.parent.ecimage)
        btn.configure(command=functools.partial(self.remove_mod, btn))
        btn.state([f'{"!" if name else ""}disabled'])
        btn.grid(row=0, column=1)
        self.widgets.append([btn, lbox, frm, lboxvar])

    def process_mod(self, lbox, event=None):
        "add an association between a mod and the save file"
        for item in self.widgets:
            if item[1] == lbox:
                to_enable = item[0]
                newvalue = item[3].get()
                break
        else:
            newvalue = ''
        if not newvalue or newvalue == 'select a mod':
            return
        # for item in self.widgets:
        #     if item[1] == lbox:
        #         item[0].state(['!disabled'])
        to_enable.state(['!disabled'])
        self.update_button.state(['!disabled'])
        # er moet alleen een nieuwe selector komen als dit de laatste combobox is en deze nog geen
        # waarde had
        if lbox == self.widgets[-1][1]:  # and len(self.widgets) > len(self.prevmods):
            self.add_modselector()
        # self.prevmods.append(newvalue)

    def remove_mod(self, btn):
        "delete an association between a mod and the save file"
        for item in self.widgets:
            if item[0] == btn:
                item[0].destroy()
                item[1].destroy()
                item[2].destroy()
                self.widgets.remove(item)

    def confirm(self):
        "activate the mods belonging to this save file"
        selected = self.savegame_selector_text.get()
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
        MessageBox.showinfo(parent=self, message='wijzigingen zijn doorgevoerd')

    def update(self):
        "callback for update button"
        self.update_conf(self.savegame_selector_text.get())

    def update_conf(self, savename):
        "save the mod associations in the config"
        new_pname = self.pname_text.get()
        if new_pname != self.old_pname:
            self.conf.update_saveitem_data(savename, self.conf.PNAME, new_pname)
        new_fname = self.fname_text.get()
        if new_fname != self.old_fname:
            self.conf.update_saveitem_data(savename, self.conf.FNAME, new_fname)
        new_gdate = self.gdate_text.get()
        if new_gdate != self.old_gdate:
            self.conf.update_saveitem_data(savename, self.conf.GDATE, new_gdate)
        newmods = [item[-1].get() for item in self.widgets[:-1]]
        if newmods != self.oldmods:
            self.conf.update_saveitem_data(savename, self.conf.MODS, newmods)
        self.conf.save()
        self.update_button.state(['disabled'])

    def get_savedata(self, event=None):
        "find and show existing configuration data for this save file"
        newvalue = self.savegame_selector_text.get()
        if newvalue == 'select a saved game':
            return
        if self.oldsavename:    # bestaande selectors eerst opruimen
            self.update_conf(self.oldsavename)
            for item in reversed(self.widgets):
                btn = item.pop(0)
                btn.destroy()
                lbox = item.pop(0)
                lbox.destroy()
                hfrm = item.pop(0)
                hfrm.destroy()
                self.widgets.remove(item)
            self.add_modselector()
        self.oldsavename = newvalue
        self.oldmods = []
        save_attrs, new_in_conf = self.conf.get_saveitem_attrs(newvalue)
        if save_attrs:
            self.old_pname, self.old_fname, self.old_gdate = save_attrs
            self.pname_text.set(self.old_pname)
            self.fname_text.set(self.old_fname)
            self.gdate_text.set(self.old_gdate)
            self.oldmods = self.conf.get_mods_for_saveitem(newvalue)
        for modname in self.oldmods:
            self.widgets[-1][3].set(modname)
            self.add_modselector()
        self.update_button.state([f'{"!" if new_in_conf else ""}disabled'])
        self.confirm_button.state(['!disabled'])

    def close(self, event=None):
        "close the dialog"
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.root.focus_set()
        self.destroy()
