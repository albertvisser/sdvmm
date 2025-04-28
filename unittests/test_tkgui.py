"""unittests for ./src/tkgui.py
"""
import types
import pytest
from src import tkgui as testee
from mockgui import mockttkwidgets as mockttk

sett = """\
called Toplevel.__init__ with args ('root',) {{}}
called Frame.__init__ with args <class 'src.tkgui.SettingsDialog'> () {{'padding': 10}}
called Frame.grid with args () {{'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called Frame.columnconfigure with args (0,)
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Base location for mods:'}}
called Label.grid with args () {{'row': 0, 'column': 0, 'sticky': 'w'}}
called StringVar.__init__ with args ()
called StringVar.set with arg 'xxx'
called Entry.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'width': 48, 'textvariable': {testobj.modbase_text}}}
called Entry.grid with args () {{'row': 0, 'column': 1}}
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Browse', 'command': {testobj.select_modbase}}}
called Button.grid with args () {{'row': 0, 'column': 2, 'sticky': 'w'}}
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Name of configuration file:'}}
called Label.grid with args () {{'row': 1, 'column': 0, 'sticky': 'w'}}
called StringVar.__init__ with args ()
called StringVar.set with arg 'yyy'
called Entry.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'width': 48, 'textvariable': {testobj.config_text}}}
called Entry.grid with args () {{'row': 1, 'column': 1}}
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Location for downloads:'}}
called Label.grid with args () {{'row': 2, 'column': 0, 'sticky': 'w'}}
called StringVar.__init__ with args ()
called StringVar.set with arg 'zzz'
called Entry.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'width': 48, 'textvariable': {testobj.download_text}}}
called Entry.grid with args () {{'row': 2, 'column': 1}}
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Browse', 'command': {testobj.select_download_path}}}
called Button.grid with args () {{'row': 2, 'column': 2, 'sticky': 'w'}}
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Number of columns on screen:'}}
called Label.grid with args () {{'row': 3, 'column': 0, 'sticky': 'w'}}
called IntVar.__init__ with args ()
called IntVar.set with arg 1
called SpinBox.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'width': 5, 'from_': 0, 'to': 5, 'textvariable': {testobj.columncount}}}
called SpinBox.grid with args () {{'row': 3, 'column': 1, 'sticky': 'w'}}
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Location for save files:'}}
called Label.grid with args () {{'row': 4, 'column': 0, 'sticky': 'w'}}
called StringVar.__init__ with args ()
called StringVar.set with arg 'qqq'
called Entry.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'width': 48, 'textvariable': {testobj.savepath_text}}}
called Entry.grid with args () {{'row': 4, 'column': 1}}
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Browse', 'command': {testobj.select_savepath}}}
called Button.grid with args () {{'row': 4, 'column': 2, 'sticky': 'w'}}
called Frame.__init__ with args <class 'src.tkgui.SettingsDialog'> () {{'padding': 10}}
called Frame.grid with args () {{'row': 1, 'column': 0}}
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Save', 'underline': 0, 'command': {testobj.update}}}
called Button.grid with args () {{'row': 0, 'column': 0}}
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Cancel', 'underline': 0, 'command': {testobj.close}}}
called Button.grid with args () {{'row': 0, 'column': 1}}
called Toplevel.bind_all with args ('<Alt-s>', <bound method TestSettingsDialog.test_init.<locals>.<lambda> of <src.tkgui.SettingsDialog object .!settingsdialog>>) {{}}
called Toplevel.bind_all with args ('<Alt-c>', <bound method TestSettingsDialog.test_init.<locals>.<lambda> of <src.tkgui.SettingsDialog object .!settingsdialog>>) {{}}
called Toplevel.bind_all with args ('<Escape>', <bound method TestSettingsDialog.test_init.<locals>.<lambda> of <src.tkgui.SettingsDialog object .!settingsdialog>>) {{}}
"""
choice = """\
called Toplevel.__init__ with args ('root',) {{}}
called Frame.__init__ with args <class 'src.tkgui.ChoiceDialog'> () {{'padding': 10}}
called Frame.grid with args () {{'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called Frame.columnconfigure with args (0,)
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'a caption'}}
called Label.grid with args () {{'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called StringVar.__init__ with args ()
called ComboBox.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'values': ['ons', 'op', 'ti'], 'textvariable': {testobj.dirname}}}
called StringVar.set with arg ''
called ComboBox.state with args (['readonly'],)
called ComboBox.bind with args ('<<ComboboxSelected>>', {testobj.enable_accept})
called ComboBox.grid with args () {{'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{}}
called Frame.grid with args () {{'row': 2, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Ok', 'underline': 0, 'command': {testobj.accept}}}
called Button.state with args (['disabled'],)
called Button.grid with args () {{'row': 0, 'column': 0, 'sticky': ('e', 'w')}}
called Frame.columnconfigure with args (0,)
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Cancel', 'underline': 0, 'command': {testobj.close}}}
called Button.grid with args () {{'row': 0, 'column': 1, 'sticky': ('e', 'w')}}
called Frame.columnconfigure with args (1,)
called Toplevel.bind with args ('<Alt-o>', {testobj.accept})
called Toplevel.bind with args ('<Alt-c>', {testobj.close})
called Toplevel.bind with args ('<Escape>', {testobj.close})
called ComboBox.focus_set
called Toplevel.focus_set
called Toplevel.grab_set
called Toplevel.wait_window
"""
attrs = """\
called Conf.list_all_mod_dirs
called Conf.get_diritem_data with args ('xxx', 'SCRNAM')
called Conf.get_diritem_data with args ('yyy', 'SCRNAM')
called Toplevel.__init__ with args ('root',) {{}}
called Frame.__init__ with args <class 'src.tkgui.AttributesDialog'> () {{'padding': 10}}
called Frame.grid with args () {{'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called StringVar.__init__ with args ()
called ComboBox.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'values': ['xxx_name', 'yyy_name'], 'textvariable': {testobj.modname}}}
called StringVar.set with arg 'Select a mod to change the screen text etc.'
called ComboBox.state with args (['readonly'],)
called ComboBox.bind with args ('<<ComboboxSelected>>', {testobj.process})
called ComboBox.grid with args () {{'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Screen Name:\\n(the suggestions in the box below are taken from\\nthe mod components'}}
called Label.grid with args () {{'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{}}
called Frame.grid with args () {{'row': 2, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called StringVar.__init__ with args ()
called StringVar.set with arg ''
called StringVar.trace_add
called ComboBox.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'textvariable': {testobj.scrname}}}
called ComboBox.state with args (['!readonly', 'disabled'],)
called ComboBox.bind with args ('<<ComboboxSelected>>', {testobj.enable_change})
called ComboBox.grid with args () {{'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called Frame.columnconfigure with args (0,)
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'image': 'ecimage', 'command': {testobj.clear_name_text}}}
called Button.state with args (['disabled'],)
called Button.grid with args () {{'row': 0, 'column': 1, 'sticky': 'w'}}
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Screen Text:\\n(to add some information e.q. if the mod is broken)'}}
called Label.grid with args () {{'row': 3, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{}}
called Frame.grid with args () {{'row': 4, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called Frame.columnconfigure with args (0,)
called StringVar.__init__ with args ()
called StringVar.set with arg ''
called StringVar.trace_add
called Entry.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'textvariable': {testobj.scrtext}}}
called Entry.grid with args () {{'row': 0, 'column': 0, 'sticky': ('e', 'w')}}
called Entry.state with args (['disabled'],)
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'image': 'ecimage', 'command': {testobj.clear_text_text}}}
called Button.state with args (['disabled'],)
called Button.grid with args () {{'row': 0, 'column': 1, 'sticky': 'w'}}
called IntVar.__init__ with args ()
called IntVar.set with arg 0
called CheckBox.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'This mod can be activated by itself', 'variable': {testobj.activate}, 'command': {testobj.enable_change}}}
called CheckBox.grid with args () {{'row': 5, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called CheckBox.state with args (['disabled'],)
called IntVar.__init__ with args ()
called IntVar.set with arg 0
called CheckBox.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Do not touch when (de)activating for a save', 'variable': {testobj.exempt}, 'command': {testobj.enable_change}}}
called CheckBox.grid with args () {{'row': 6, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called CheckBox.state with args (['disabled'],)
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'View Components', 'underline': 5, 'command': {testobj.view_components}}}
called Button.grid with args () {{'row': 7, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called Button.state with args (['disabled'],)
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'View Dependencies', 'underline': 5, 'command': {testobj.view_dependencies}}}
called Button.grid with args () {{'row': 8, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called Button.state with args (['disabled'],)
called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{}}
called Frame.grid with args () {{'row': 9, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Update', 'underline': 0, 'command': {testobj.update}}}
called Button.state with args (['disabled'],)
called Button.grid with args () {{'row': 0, 'column': 0, 'sticky': ('e', 'w')}}
called Frame.columnconfigure with args (0,)
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Close', 'underline': 2, 'command': {testobj.close}}}
called Button.grid with args () {{'row': 0, 'column': 1, 'sticky': ('e', 'w')}}
called Frame.columnconfigure with args (1,)
called ComboBox.focus_set
"""
saves = """\
called Conf.list_all_mod_savetemitems
called Conf.list_all_mod_dirs
called Conf.get_diritem_data with args ('xxx', 'SCRNAM')
called Conf.get_diritem_data with args ('yyy', 'SCRNAM')
called Toplevel.__init__ with args ('root',) {{}}
called Frame.__init__ with args <class 'src.tkgui.SaveGamesDialog'> () {{'padding': 10}}
called Frame.grid with args () {{'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called ComboBox.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'values': ['qqq', 'rrr'], 'textvariable': {testobj.savegame_selector_text!r}}}
called ComboBox.state with args (['readonly'],)
called ComboBox.bind with args ('<<ComboboxSelected>>', {testobj.get_savedata})
called ComboBox.grid with args () {{'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{}}
called Frame.grid with args () {{'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called Frame.columnconfigure with args (1,)
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Player name:'}}
called Label.grid with args () {{'row': 0, 'column': 0}}
called Entry.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'textvariable': {testobj.pname_text!r}}}
called Entry.grid with args () {{'row': 0, 'column': 1}}
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Farm name:'}}
called Label.grid with args () {{'row': 1, 'column': 0}}
called Entry.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'textvariable': {testobj.fname_text!r}}}
called Entry.grid with args () {{'row': 1, 'column': 1}}
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'In-game date:'}}
called Label.grid with args () {{'row': 2, 'column': 0}}
called Entry.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'textvariable': {testobj.gdate_text!r}}}
called Entry.grid with args () {{'row': 2, 'column': 1}}
called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{}}
called Frame.grid with args () {{'row': 2, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Uses:'}}
called Label.grid with args () {{'row': 0, 'column': 0}}
called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{}}
called Frame.grid with args () {{'row': 3, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called Frame.columnconfigure with args (0,)
called SaveGamesDialog.add_modselector
called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{}}
called Frame.grid with args () {{'row': 4, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Update config', 'underline': 0, 'command': {testobj.update}}}
called Button.state with args (['disabled'],)
called Button.grid with args () {{'row': 0, 'column': 0}}
called Toplevel.bind with args ('<Alt-u>', {testobj.update})
called Frame.columnconfigure with args (0,)
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Activate Mods', 'underline': 0, 'command': {testobj.confirm}}}
called Button.state with args (['disabled'],)
called Button.grid with args () {{'row': 0, 'column': 1}}
called Toplevel.bind with args ('<Alt-a>', {testobj.confirm})
called Frame.columnconfigure with args (1,)
called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {{'text': 'Close', 'underline': 0, 'command': {testobj.close}}}
called Button.grid with args () {{'row': 0, 'column': 2}}
called Toplevel.bind with args ('<Alt-c>', {testobj.close})
called Toplevel.bind with args ('<Escape>', {testobj.close})
called Frame.columnconfigure with args (2,)
called ComboBox.focus_set
"""


@pytest.fixture
def expected_output():
    "fixture returning output to be expected from (mostly) gui setup methods"
    results = {'sett': sett, 'choice': choice, 'attrs': attrs, 'saves': saves}
    return results


class MockManager:
    """stub for ./manager.Manager
    """
    def __init__(self):
        self.modbase = 'modbase'
        self.downloads = 'Downloads'
        self.conf = {}
        self.directories = []
    def add_to_config(self):
        """stub
        """
    def edit_config(self):
        """stub
        """
    def order_widgets(self, *args):
        """stub
        """
        print('called Manager.order_widgets with args', args)
    def process_activations(self):
        """stub
        """
        print('called Manager.process_activations')
    def select_activations(self, names):
        """stub
        """
        print(f'called Manager.select_activations with arg {names}')
        self.directories = ['x', 'y']
    def activate(self):
        """stub
        """
        print('called Manager.activate')
    def reload_config(self):
        """stub
        """
        print('called Manager.reload_config()')
    def check_config(self):
        """stub
        """
        print('called Manager.check_config()')
        return ['result', 'another result']
    def manage_attributes(self):
        """stub
        """
        print('called Manager.manage_attributes()')
    def manage_savefiles(self):
        """stub
        """
        print('called Manager.manage_savefiles()')
    def reorder_gui(self):
        """stub
        """
        print('called Manager.reorder_gui()')
    def manage_defaults(self):
        """stub
        """
        print('called Manager.manage_savefiles()')


class MockConf:
    """stub for jsonconfig.JsonConf object
    """
    SCRNAM, NAME, DEPS, VRS = 'SCRNAM', 'Name', 'Deps', 'Version'
    PNAME, FNAME, GDATE, MODS = 'Pname', 'Fname', 'Gdate', 'Mods'
    OPTOUT, DIR = '_DoNotTouch', 'dirname'
    def save(self):
        "stub"
        print('called Conf.save')
    def list_all_mod_dirs(self):
        "stub"
        print('called Conf.list_all_mod_dirs')
        return ['xxx', 'yyy']
    def list_all_saveitems(self):
        "stub"
        print('called Conf.list_all_mod_savetemitems')
        return ['qqq', 'rrr']
    def list_components_for_dir(self, name):
        "stub"
        print(f"called Conf.list_components_for_dir with arg '{name}'")
        return ['xxx', 'yyy']
    def get_diritem_data(self, *args):
        "stub"
        print("called Conf.get_diritem_data with args", args)
        return f'{args[0]}_name'
    def get_component_data(self, *args):
        "stub"
        print("called Conf.get_component_data with args", args)
        if args[1] == self.NAME:
            return f'{args[0]}_compname'
        if args[1] == self.DEPS:
            return [f'{args[0]}_depname']
        if args[1] == self.VRS:
            return f'{args[0]}_version'
        return f'{args[0]}_name'
    def get_saveitem_attrs(self, value):
        "stub"
        print(f"called Conf.get_saveitem_attrs with arg {value}")
        return [], False
    def get_mods_for_saveitem(self, name):
        "stub"
        print(f"called Conf.get_mods_for_saveitem with arg {name}")
        return []
    def update_saveitem_data(self, *args):
        "stub"
        print('called Conf.update_saveitem_data with args', args)


def test_show_dialog(capsys):
    """unittests for tkgui.show_dialog
    """
    parent = types.SimpleNamespace()
    cls = mockttk.MockDialog
    modnames = ['x', 'y']
    assert testee.show_dialog(cls, parent, modnames, True)
    assert capsys.readouterr().out == (
        "called Toplevel.__init__ with args (namespace(), ['x', 'y'], True) {}\n"
        "called Toplevel.focus_set\n"
        "called Toplevel.grab_set\n"
        "called Toplevel.wait_window\n")


class TestShowMods:
    """unittests for tkgui.ShowMods
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for tkgui.ShowMods object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ShowMods.__init__ with args', args)
        monkeypatch.setattr(testee.ShowMods, '__init__', mock_init)
        testobj = testee.ShowMods()
        assert capsys.readouterr().out == 'called ShowMods.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ShowMods.__init__
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ShowMods.root.__init__')
        def mock_title(self, *args):
            """stub
            """
            print('called ShowMods.root.__title__ with args', args)
        monkeypatch.setattr(testee.ImageTk, 'PhotoImage', mockttk.MockPhotoImage)
        monkeypatch.setattr(testee.tk.Tk, '__init__', mock_init)
        monkeypatch.setattr(testee.tk.Tk, 'title', mock_title)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        master = types.SimpleNamespace()
        monkeypatch.setattr(testee, 'ECIMAGE', 'ecimage')
        testobj = testee.ShowMods(master)
        assert isinstance(testobj.root, testee.tk.Tk)
        assert isinstance(testobj.main, testee.ttk.Frame)
        assert testobj.master == master
        assert testobj.buttons == {}
        assert capsys.readouterr().out == (
                'called ShowMods.root.__init__\n'
                "called PhotoImage.__init__ with args ('ecimage',)\n"
                "called ShowMods.root.__title__ with args ('SDV Mod Manager',)\n"
                "called Frame.__init__ with args <class 'tkinter.Tk'> () {}\n"
                "called Frame.grid with args"
                " () {'column': 0, 'row': 0, 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_create_selectables_title(self, monkeypatch, capsys):
        """unittest for ShowMods.create_selectables_title
        """
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.main = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args <class 'NoneType'> () {}\n")
        testobj.create_selectables_title('xxxx')
        assert capsys.readouterr().out == (
                "called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'>"
                " () {'text': 'xxxx', 'padding': 10}\n"
                "called Label.grid with args () {'column': 0, 'row': 0, 'sticky': ('n', 'w')}\n")

    def test_create_selectables_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.create_selectables_grid
        """
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.main = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args <class 'NoneType'> () {}\n")
        testobj.create_selectables_grid()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'>"
                " () {'padding': (10, 0)}\n"
                "called Frame.grid with args () {'column': 0, 'row': 1}\n")

    def test_create_dependencies_title(self, monkeypatch, capsys):
        """unittest for ShowMods.create_dependencies_title
        """
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.main = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args <class 'NoneType'> () {}\n")
        testobj.create_dependencies_title('yyyy')
        assert capsys.readouterr().out == (
                "called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'>"
                " () {'text': 'yyyy', 'padding': 10}\n"
                "called Label.grid with args () {'column': 0, 'row': 2, 'sticky': ('n', 'w')}\n")

    def test_create_dependencies_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.create_dependencies_grid
        """
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.main = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args <class 'NoneType'> () {}\n")
        testobj.create_dependencies_grid()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'>"
                " () {'padding': (10, 0)}\n"
                "called Frame.grid with args () {'column': 0, 'row': 3}\n")

    def test_create_buttons(self, monkeypatch, capsys, expected_output):
        """unittest for ShowMods.create_buttons
        """
        def mock_refresh(*args, **kwargs):
            """stub
            """
            print('called ShowMods.refresh_widgets with args', args, kwargs)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args <class 'NoneType'> () {}\n")
        testobj.buttons = {}
        testobj.refresh_widgets = mock_refresh
        callback1 = lambda: '0'
        callback2 = lambda: '1'
        testobj.create_buttons([
            {'name': 'xxx', 'text': '&xxxxxx', 'tooltip': 'xxxxxxxxx', 'callback': callback1},
            {'name': 'actv', 'text': 'yyy&yyy', 'tooltip': 'yyyyyyyyy', 'callback': callback2}])
        assert len(testobj.buttons) == 2
        assert isinstance(testobj.buttons['xxx'], mockttk.MockButton)
        assert isinstance(testobj.buttons['actv'], mockttk.MockButton)
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args"
                " <class 'mockgui.mockttkwidgets.MockFrame'> () {'padding': 10}\n"
                "called Frame.grid with args () {'column': 0, 'row': 3, 'sticky': 's'}\n"
                "called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'>"
                f" () {{'text': 'xxxxxx', 'command': {callback1}, 'underline': 0}}\n"
                "called Button.grid with args () {'column': 0, 'row': 0}\n"
                "called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'>"
                f" () {{'text': 'yyyyyy', 'command': {callback2}, 'underline': 3}}\n"
                "called Button.grid with args () {'column': 1, 'row': 0}\n"
                "called ShowMods.refresh_widgets with args () {'first_time': True}\n")

    def test_setup_actions(self, monkeypatch, capsys):
        """unittest for ShowMods.setup_actions
        """
        def mock_bind(*args):
            print('called ShowMods.root.bind with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = types.SimpleNamespace(bind=mock_bind)
        # testobj.manage_defaults = lambda: 'dummy'
        # testobj.manage_attributes = lambda: 'dummy'
        # testobj.manage_savefiles = lambda: 'dummy'
        # testobj.update = lambda: 'dummy'
        # testobj.confirm = lambda: 'dummy'
        # testobj.stop = lambda: 'dummy'
        testobj.setup_actions()
        assert capsys.readouterr().out == (
                f"called ShowMods.root.bind with args ('<Alt-d>', {testobj.manage_defaults})\n"
                f"called ShowMods.root.bind with args ('<Alt-i>', {testobj.update_mods})\n"
                f"called ShowMods.root.bind with args ('<Alt-r>', {testobj.remove_mods})\n"
                f"called ShowMods.root.bind with args ('<Alt-m>', {testobj.manage_attributes})\n"
                f"called ShowMods.root.bind with args ('<Alt-a>', {testobj.confirm})\n"
                f"called ShowMods.root.bind with args ('<Control-Return>', {testobj.confirm})\n"
                f"called ShowMods.root.bind with args ('<Alt-s>', {testobj.manage_savefiles})\n"
                f"called ShowMods.root.bind with args ('<Alt-x>', {testobj.close})\n"
                f"called ShowMods.root.bind with args ('<Control-q>', {testobj.close})\n")

    def test_show_screen(self, monkeypatch, capsys):
        """unittest for ShowMods.show_screen
        """
        def mock_mainloop(*args):
            print('called ShowMods.root.mainloop')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = types.SimpleNamespace(mainloop=mock_mainloop)
        testobj.show_screen()
        assert capsys.readouterr().out == 'called ShowMods.root.mainloop\n'

    def test_refresh_widgets(self, monkeypatch, capsys):
        """unittest for ShowMods.refresh_widgets
        """
        def mock_order(*args):
            print('called Manager.order_widgets with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.activatables = 'activatables'
        testobj.dependencies = 'dependencies'
        testobj.master = types.SimpleNamespace(screeninfo={}, order_widgets=mock_order)
        testobj.buttons = {"attr": mockttk.MockButton(), "sel": mockttk.MockButton()}
        assert capsys.readouterr().out == (
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n")
        testobj.refresh_widgets()
        assert capsys.readouterr().out == (
                "called Button.state with args (['disabled'],)\n"
                "called Button.state with args (['disabled'],)\n"
                "called Manager.order_widgets with args (False, 'activatables', 'dependencies')\n")
        testobj.master.screeninfo = {'x': 'y'}
        testobj.refresh_widgets(True)
        assert capsys.readouterr().out == (
                "called Button.state with args (['!disabled'],)\n"
                "called Button.state with args (['!disabled'],)\n"
                "called Manager.order_widgets with args (True, 'activatables', 'dependencies')\n")

    def test_remove_widgets(self, monkeypatch, capsys):
        """unittest for ShowMods.remove_widgets
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widgetlist = ['', mockttk.MockLabel(), mockttk.MockCheckBox()]
        container = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Label.__init__ with args <class 'NoneType'> () {}\n"
                "called CheckBox.__init__ with args <class 'NoneType'> () {}\n"
                "called Frame.__init__ with args <class 'NoneType'> () {}\n")
        testobj.remove_widgets(widgetlist, container, 1, 2)
        assert capsys.readouterr().out == ("called CheckBox.destroy\n"
                                           "called Label.destroy\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for ShowMods.add_checkbox
        """
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Checkbutton', mockttk.MockCheckBox)
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        monkeypatch.setattr(testee.tk, 'IntVar', mockttk.MockIntVar)
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        testobj = self.setup_testobj(monkeypatch, capsys)
        widgetlist = testobj.add_checkbox('root', 1, 2, False)
        assert isinstance(widgetlist[0], testee.ttk.Frame)
        assert isinstance(widgetlist[1], testee.ttk.Label)
        assert isinstance(widgetlist[2], testee.ttk.Checkbutton)
        assert isinstance(widgetlist[3], testee.tk.StringVar)
        assert isinstance(widgetlist[4], testee.tk.IntVar)
        assert capsys.readouterr().out == (
            "called Frame.__init__ with args <class 'str'> () {'padding': (5, 0, 5, 0)}\n"
            "called IntVar.__init__ with args ()\n"
            "called CheckBox.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'>"
            f" () {{'variable': {widgetlist[4]}, 'command': {testobj.enable_button}}}\n"
            "called CheckBox.state with args (['disabled', '!selected'],)\n"
            "called CheckBox.grid with args () {'column': 1, 'row': 0}\n"
            "called StringVar.__init__ with args ()\n"
            "called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'>"
            f" () {{'textvariable': {widgetlist[3]}}}\n"
            "called Label.grid with args () {'column': 2, 'row': 0}\n"
            "called Frame.grid with args () {'row': 1, 'column': 2, 'sticky': 'w'}\n")
        widgetlist = testobj.add_checkbox('root', 1, 2, True)
        assert isinstance(widgetlist[0], testee.ttk.Frame)
        assert isinstance(widgetlist[1], testee.ttk.Label)
        assert isinstance(widgetlist[2], testee.ttk.Checkbutton)
        assert isinstance(widgetlist[3], testee.tk.StringVar)
        assert isinstance(widgetlist[4], testee.tk.IntVar)
        assert capsys.readouterr().out == (
            "called Frame.__init__ with args <class 'str'> () {'padding': (5, 0, 5, 0)}\n"
            "called IntVar.__init__ with args ()\n"
            "called CheckBox.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'>"
            f" () {{'variable': {widgetlist[4]}, 'command': {testobj.enable_button}}}\n"
            "called CheckBox.state with args (['!disabled', '!selected'],)\n"
            "called CheckBox.grid with args () {'column': 1, 'row': 0}\n"
            "called StringVar.__init__ with args ()\n"
            "called Label.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'>"
            f" () {{'textvariable': {widgetlist[3]}}}\n"
            "called Label.grid with args () {'column': 2, 'row': 0}\n"
            "called Frame.grid with args () {'row': 1, 'column': 2, 'sticky': 'w'}\n")

    def test_set_label_text(self, monkeypatch, capsys):
        """unittest for ShowMods.set_label_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widgetlist = ['frame', 'label', 'check', mockttk.MockStringVar(), 'intvar']
        assert widgetlist[3].get() is None
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called StringVar.get\n")
        testobj.set_label_text(widgetlist, 'xxxx', '', '')
        assert widgetlist[3].get() == 'xxxx'
        assert capsys.readouterr().out == ("called StringVar.set with arg 'xxxx'\n"
                                           "called StringVar.get\n")
        testobj.set_label_text(widgetlist, 'xxxx', '', 'yyy')
        assert widgetlist[3].get() == 'xxxx yyy'
        assert capsys.readouterr().out == ("called StringVar.set with arg 'xxxx yyy'\n"
                                           "called StringVar.get\n")
        testobj.set_label_text(widgetlist, 'xxxx', 'zz', '')
        assert widgetlist[3].get() == 'xxxx (zz)'
        assert capsys.readouterr().out == ("called StringVar.set with arg 'xxxx (zz)'\n"
                                           "called StringVar.get\n")
        testobj.set_label_text(widgetlist, 'xxxx', 'zz', 'yyy')
        assert widgetlist[3].get() == 'xxxx (zz) yyy'
        assert capsys.readouterr().out == ("called StringVar.set with arg 'xxxx (zz) yyy'\n"
                                           "called StringVar.get\n")

    def test_set_checkbox_state(self, monkeypatch, capsys):
        """unittest for showmods.set_checkbox_state
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widgetlist = ['frame', 'label', 'check', 'stringvar', mockttk.MockIntVar()]
        assert widgetlist[4].get() is None
        assert capsys.readouterr().out == ("called IntVar.__init__ with args ()\n"
                                           "called IntVar.get\n")
        testobj.set_checkbox_state(widgetlist, False)
        assert widgetlist[4].get() == 0
        assert capsys.readouterr().out == ("called IntVar.set with arg 0\n"
                                           "called IntVar.get\n")
        testobj.set_checkbox_state(widgetlist, True)
        assert widgetlist[4].get() == 1
        assert capsys.readouterr().out == ("called IntVar.set with arg 1\n"
                                           "called IntVar.get\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for ShowMods.close
        """
        def mock_quit():
            print('called root.quit')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = types.SimpleNamespace(quit=mock_quit)
        testobj.close('stopevent')
        assert capsys.readouterr().out == "called root.quit\n"

    def test_enable_button(self, monkeypatch, capsys):
        """unittest for ShowMods.enable_button
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.buttons = {'actv': mockttk.MockButton()}
        assert capsys.readouterr().out == (
                "called Button.__init__ with args <class 'NoneType'> () {}\n")
        testobj.enable_button()
        assert capsys.readouterr().out == ("called Button.state with args (['!disabled'],)\n")

    def test_manage_defaults(self, monkeypatch, capsys):
        """unittest for ShowMods.manage_defaults
        """
        def mock_manage():
            print('called Manager.manage_defaults')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(manage_defaults=mock_manage)
        testobj.manage_defaults('event')
        assert capsys.readouterr().out == "called Manager.manage_defaults\n"

    def test_update_mods(self, monkeypatch, capsys):
        """unittest for ShowMods.update
        """
        def mock_update(arg):
            print(f"called Manager.update_mods with arg {arg}")
            return ['xxx', 'yyy']
        monkeypatch.setattr(testee.tk.filedialog, 'askopenfilename', mockttk.mock_askopen_nofile)
        monkeypatch.setattr(testee.MessageBox, 'showinfo', mockttk.mock_show_info)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = 'root'
        testobj.master = types.SimpleNamespace(update_mods=mock_update, downloads='here')
        testobj.update_mods()
        assert capsys.readouterr().out == (
                "called FileDialog.askopenfilename with args"
                " {'title': 'Install downloaded mods', 'multiple': True,"
                " 'initialdir': 'here', 'filetypes': [('Zip files', '.zip')]}\n")

        monkeypatch.setattr(testee.tk.filedialog, 'askopenfilename', mockttk.mock_askopen_file)
        testobj.update_mods()
        assert capsys.readouterr().out == (
                "called FileDialog.askopenfilename with args"
                " {'title': 'Install downloaded mods', 'multiple': True,"
                " 'initialdir': 'here', 'filetypes': [('Zip files', '.zip')]}\n"
                "called Manager.update_mods with arg ['name1', 'name2']\n"
                "called MessageBox.showinfo with args ()"
                " {'parent': 'root', 'message': 'xxx\\nyyy'}\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for ShowMods.confirm
        """
        monkeypatch.setattr(testee.MessageBox, 'showinfo', mockttk.mock_show_info)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = 'root'
        testobj.master = MockManager()
        testobj.buttons = {'actv': mockttk.MockButton()}
        assert capsys.readouterr().out == (
                "called Button.__init__ with args <class 'NoneType'> () {}\n")
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called Manager.process_activations\n"
                "called MessageBox.showinfo with args"
                " () {'parent': 'root', 'message': 'wijzigingen zijn doorgevoerd'}\n"
                "called Button.state with args (['disabled'],)\n")

    def test_get_labeltext_if_checked(self, monkeypatch, capsys):
        """unittest for ShowMods.get_labeltext_if_checked
        """
        labeltext = mockttk.MockStringVar()
        labeltext.set('xxx')
        checkvar = mockttk.MockIntVar()
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called StringVar.set with arg 'xxx'\n"
                                           "called IntVar.__init__ with args ()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        widgetlist = ['hbox', 'label', 'check', labeltext, checkvar]
        assert testobj.get_labeltext_if_checked(widgetlist) == ''
        assert capsys.readouterr().out == ("called IntVar.get\n"
                                           "called StringVar.get\n")
        checkvar.set(0)
        assert capsys.readouterr().out == ("called IntVar.set with arg 0\n")
        assert testobj.get_labeltext_if_checked(widgetlist) == ''
        assert capsys.readouterr().out == ("called IntVar.get\n"
                                           "called StringVar.get\n")
        checkvar.set(1)
        assert capsys.readouterr().out == ("called IntVar.set with arg 1\n")
        assert testobj.get_labeltext_if_checked(widgetlist) == 'xxx'
        assert capsys.readouterr().out == ("called IntVar.get\n"
                                           "called StringVar.get\n")
        labeltext.set('xxx<yyy>zzz<qqq>rrr')
        assert capsys.readouterr().out == ("called StringVar.set with arg 'xxx<yyy>zzz<qqq>rrr'\n")
        assert testobj.get_labeltext_if_checked(widgetlist) == 'xxx<yyy>zzz<qqq>rrr'
        assert capsys.readouterr().out == ("called IntVar.get\n"
                                           "called StringVar.get\n")

    def test_select_value(self, monkeypatch, capsys):
        """unittest for ShowMods.select_value
        """
        def mock_dialog(parent, *args, **kwargs):
            nonlocal counter
            print('called ChoiceDialog with args', parent, args, kwargs)
            counter += 1
            if counter > 1:
                parent.dialog_data = 'qqq'
        monkeypatch.setattr(testee, 'ChoiceDialog', mock_dialog)
        monkeypatch.setattr(testee.MessageBox, 'showinfo', mockttk.mock_show_info)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = 'root'
        counter = 0
        assert testobj.select_value('xxx', ['yyy', 'zzz']) == ''
        assert capsys.readouterr().out == (f"called ChoiceDialog with args {testobj}"
                                           " ('xxx', ['yyy', 'zzz']) {'editable': True}\n")
        counter = 0
        assert testobj.select_value('xxx', ['yyy', 'zzz'], False, True) == 'qqq'
        assert capsys.readouterr().out == (
                f"called ChoiceDialog with args {testobj}"
                " ('xxx', ['yyy', 'zzz']) {'editable': False}\n"
                "called MessageBox.showinfo with args () {'parent': 'root',"
                " 'message': 'You *must* select or enter a value'}\n"
                f"called ChoiceDialog with args {testobj}"
                " ('xxx', ['yyy', 'zzz']) {'editable': False}\n")

    def test_manage_attributes(self, monkeypatch, capsys):
        """unittest for ShowMods.manage_attributes
        """
        def mock_manage():
            print('called Manager.manage_attributes')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(manage_attributes=mock_manage)
        testobj.manage_attributes('event')
        assert capsys.readouterr().out == "called Manager.manage_attributes\n"

    def test_manage_savefiles(self, monkeypatch, capsys):
        """unittest for ShowMods.manage_savefiles
        """
        def mock_manage():
            print('called Manager.manage_savefiles')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(manage_savefiles=mock_manage)
        testobj.manage_savefiles('event')
        assert capsys.readouterr().out == "called Manager.manage_savefiles\n"


class TestSettingsDialog:
    """unittests for qtgui.SettingsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SettingsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called SettingsDialog.__init__ with args', args)
        # def mock_accept(self):
        #     print('called SettingsDialog.accept')
        monkeypatch.setattr(testee.SettingsDialog, '__init__', mock_init)
        # monkeypatch.setattr(testee.SettingsDialog, 'accept', mock_accept)
        testobj = testee.SettingsDialog()
        assert capsys.readouterr().out == 'called SettingsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SettingsDialog.__init__
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            print('called Toplevel.__init__ with args', args, kwargs)
            old_init(self, *kwargs, **kwargs)
        def mock_bind(self, *args, **kwargs):
            print('called Toplevel.bind_all with args', args, kwargs)
        monkeypatch.setattr(testee.tk.Toplevel, '__init__', mock_init)
        monkeypatch.setattr(testee.tk.Toplevel, 'bind_all', mock_bind)

        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        monkeypatch.setattr(testee.ttk, 'Entry', mockttk.MockEntry)
        monkeypatch.setattr(testee.ttk, 'Checkbutton', mockttk.MockCheckBox)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        monkeypatch.setattr(testee.ttk, 'Spinbox', mockttk.MockSpinBox)
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.tk, 'IntVar', mockttk.MockIntVar)

        monkeypatch.setattr(testee.SettingsDialog, 'select_modbase', lambda: 'dummy')
        monkeypatch.setattr(testee.SettingsDialog, 'select_download_path', lambda: 'dummy')
        monkeypatch.setattr(testee.SettingsDialog, 'select_savepath', lambda: 'dummy')
        monkeypatch.setattr(testee.SettingsDialog, 'update', lambda: 'dummy')
        monkeypatch.setattr(testee.SettingsDialog, 'close', lambda: 'dummy')
        parent = types.SimpleNamespace(root='root')
        parent.master = types.SimpleNamespace(dialog_data=('xxx', 'yyy', 'zzz', 1, 'qqq'))
        # breakpoint()
        testobj = testee.SettingsDialog(parent)
        assert testobj.parent == parent
        assert isinstance(testobj.modbase_text, testee.tk.StringVar)
        assert isinstance(testobj.config_text, testee.tk.StringVar)
        assert isinstance(testobj.download_text, testee.tk.StringVar)
        assert isinstance(testobj.columncount, testee.tk.IntVar)
        assert isinstance(testobj.savepath_text, testee.tk.StringVar)
        assert capsys.readouterr().out == expected_output['sett'].format(testobj=testobj)

    def test_select_modbase(self, monkeypatch, capsys):
        """unittest for SettingsDialog.select_modbase
        """
        def mock_get(**kwargs):
            print('called FileDialog.askdirectory with args', kwargs)
            return ''
        def mock_get_2(**kwargs):
            print('called FileDialog.askdirectory with args', kwargs)
            return 'xxx'
        monkeypatch.setattr(testee.FileDialog, 'askdirectory', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.modbase_text = mockttk.MockStringVar()
        assert capsys.readouterr().out == "called StringVar.__init__ with args ()\n"
        testobj.select_modbase()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called FileDialog.askdirectory with args"
                " {'title': 'Where to install downloaded mods?',"
                f" 'initialdir': '{testee.os.path.expanduser('~')}',"
                " 'mustexist': True}\n")
        testobj.modbase_text.set('qqq')
        assert capsys.readouterr().out == "called StringVar.set with arg 'qqq'\n"
        testobj.select_modbase()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called FileDialog.askdirectory with args"
                " {'title': 'Where to install downloaded mods?', 'initialdir': 'qqq',"
                " 'mustexist': True}\n")
        monkeypatch.setattr(testee.FileDialog, 'askdirectory', mock_get_2)
        testobj.select_modbase()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called FileDialog.askdirectory with args"
                " {'title': 'Where to install downloaded mods?', 'initialdir': 'qqq',"
                " 'mustexist': True}\n"
                "called StringVar.set with arg 'xxx'\n")

    def test_select_download_path(self, monkeypatch, capsys):
        """unittest for SettingsDialog.select_modbase
        """
        def mock_get(**kwargs):
            print('called FileDialog.askdirectory with args', kwargs)
            return ''
        def mock_get_2(**kwargs):
            print('called FileDialog.askdirectory with args', kwargs)
            return 'xxx'
        monkeypatch.setattr(testee.FileDialog, 'askdirectory', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.download_text = mockttk.MockStringVar()
        assert capsys.readouterr().out == "called StringVar.__init__ with args ()\n"
        testobj.select_download_path()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called FileDialog.askdirectory with args"
                " {'title': 'Where to download mods to?',"
                f" 'initialdir': '{testee.os.path.expanduser('~')}',"
                " 'mustexist': True}\n")
        testobj.download_text.set('qqq')
        assert capsys.readouterr().out == "called StringVar.set with arg 'qqq'\n"
        testobj.select_download_path()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called FileDialog.askdirectory with args"
                " {'title': 'Where to download mods to?', 'initialdir': 'qqq',"
                " 'mustexist': True}\n")
        monkeypatch.setattr(testee.FileDialog, 'askdirectory', mock_get_2)
        testobj.select_download_path()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called FileDialog.askdirectory with args"
                " {'title': 'Where to download mods to?', 'initialdir': 'qqq',"
                " 'mustexist': True}\n"
                "called StringVar.set with arg 'xxx'\n")

    def test_select_savepath(self, monkeypatch, capsys):
        """unittest for SettingsDialog.select_modbase
        """
        def mock_get(**kwargs):
            print('called FileDialog.askdirectory with args', kwargs)
            return ''
        def mock_get_2(**kwargs):
            print('called FileDialog.askdirectory with args', kwargs)
            return 'xxx'
        monkeypatch.setattr(testee.FileDialog, 'askdirectory', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.savepath_text = mockttk.MockStringVar()
        assert capsys.readouterr().out == "called StringVar.__init__ with args ()\n"
        testobj.select_savepath()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called FileDialog.askdirectory with args"
                " {'title': 'Where are the saved games stored?',"
                f" 'initialdir': '{testee.os.path.expanduser('~')}',"
                " 'mustexist': True}\n")
        testobj.savepath_text.set('qqq')
        assert capsys.readouterr().out == "called StringVar.set with arg 'qqq'\n"
        testobj.select_savepath()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called FileDialog.askdirectory with args"
                " {'title': 'Where are the saved games stored?', 'initialdir': 'qqq',"
                " 'mustexist': True}\n")
        monkeypatch.setattr(testee.FileDialog, 'askdirectory', mock_get_2)
        testobj.select_savepath()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called FileDialog.askdirectory with args"
                " {'title': 'Where are the saved games stored?', 'initialdir': 'qqq',"
                " 'mustexist': True}\n"
                "called StringVar.set with arg 'xxx'\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for SettingsDialog.update
        """
        def mock_close():
            print("called SettingsDialog.close")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(master=types.SimpleNamespace())
        testobj.modbase_text = mockttk.MockStringVar()
        testobj.modbase_text.set('xx')
        testobj.config_text = mockttk.MockStringVar()
        testobj.config_text.set('yy')
        testobj.download_text = mockttk.MockStringVar()
        testobj.download_text.set('zz')
        testobj.columncount = mockttk.MockIntVar()
        testobj.columncount.set(2)
        testobj.savepath_text = mockttk.MockStringVar()
        testobj.savepath_text.set('qq')
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called StringVar.set with arg 'xx'\n"
                                           "called StringVar.__init__ with args ()\n"
                                           "called StringVar.set with arg 'yy'\n"
                                           "called StringVar.__init__ with args ()\n"
                                           "called StringVar.set with arg 'zz'\n"
                                           "called IntVar.__init__ with args ()\n"
                                           "called IntVar.set with arg 2\n"
                                           "called StringVar.__init__ with args ()\n"
                                           "called StringVar.set with arg 'qq'\n")
        testobj.close = mock_close
        testobj.update()
        assert testobj.parent.master.dialog_data == ('xx', 'yy', 'zz', 2, 'qq')
        assert capsys.readouterr().out == ("called StringVar.get\n"
                                           "called StringVar.get\n"
                                           "called StringVar.get\n"
                                           "called IntVar.get\n"
                                           "called StringVar.get\n"
                                           "called SettingsDialog.close\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for SettingsDialog.close
        """
        def mock_set():
            print('called ShowMods.root.focus_set')
        def mock_destroy():
            print('called SettingsDialog.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.destroy = mock_destroy
        testobj.parent = None
        testobj.close()
        assert capsys.readouterr().out == "called SettingsDialog.destroy\n"
        testobj.parent = types.SimpleNamespace(root=types.SimpleNamespace(focus_set=mock_set))
        testobj.close()
        assert capsys.readouterr().out == ("called ShowMods.root.focus_set\n"
                                           "called SettingsDialog.destroy\n")


class TestChoiceDialog:
    """unittests for tkgui.ChoiceDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for tkgui.ChoiceDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ChoiceDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ChoiceDialog, '__init__', mock_init)
        testobj = testee.ChoiceDialog()
        assert capsys.readouterr().out == 'called ChoiceDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ChoiceDialog.__init__
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            print('called Toplevel.__init__ with args', args, kwargs)
            old_init(self, *kwargs, **kwargs)
        monkeypatch.setattr(testee.tk.Toplevel, '__init__', mock_init)
        monkeypatch.setattr(testee.tk.Toplevel, 'bind', mockttk.MockDialog.bind)
        monkeypatch.setattr(testee.tk.Toplevel, 'focus_set', mockttk.MockDialog.focus_set)
        monkeypatch.setattr(testee.tk.Toplevel, 'grab_set', mockttk.MockDialog.grab_set)
        monkeypatch.setattr(testee.tk.Toplevel, 'wait_window', mockttk.MockDialog.wait_window)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        monkeypatch.setattr(testee.ttk, 'Combobox', mockttk.MockComboBox)
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.ChoiceDialog, 'enable_accept', lambda: 'dummy')
        monkeypatch.setattr(testee.ChoiceDialog, 'accept', lambda: 'dummy')
        monkeypatch.setattr(testee.ChoiceDialog, 'close', lambda: 'dummy')
        parent = types.SimpleNamespace(root='root')
        testobj = testee.ChoiceDialog(parent, 'a caption', ['op', 'ti', 'ons'], False)
        assert capsys.readouterr().out == expected_output['choice'].format(testobj=testobj)
        assert testobj.parent == parent
        assert isinstance(testobj.dirname, testee.tk.StringVar)
        assert testobj.dirname.get() == ''
        assert capsys.readouterr().out == "called StringVar.get\n"
        assert isinstance(testobj.lbox, testee.ttk.Combobox)
        assert isinstance(testobj.ok_button, testee.ttk.Button)

    def test_enable_accept(self, monkeypatch, capsys):
        """unittest for ChoiceDialog.__enable_accept__
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ok_button = mockttk.MockButton()
        assert capsys.readouterr().out == (
                "called Button.__init__ with args <class 'NoneType'> () {}\n")
        testobj.enable_accept('buttonpressevent')
        assert capsys.readouterr().out == "called Button.state with args (['!disabled'],)\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for ChoiceDialog.__accept__
        """
        def mock_close():
            print('called ChoiceDialog.close')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace()
        testobj.dirname = mockttk.MockStringVar()
        testobj.dirname.set('xxx')
        testobj.close = mock_close
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called StringVar.set with arg 'xxx'\n")
        testobj.accept()
        assert capsys.readouterr().out == ("called StringVar.get\n"
                                           "called ChoiceDialog.close\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for ChoiceDialog.__close__
        """
        def mock_set():
            print('called ShowMods.root.focus_set')
        def mock_destroy():
            print('called ChoiceDialog.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.destroy = mock_destroy
        testobj.parent = None
        testobj.close()
        assert capsys.readouterr().out == "called ChoiceDialog.destroy\n"
        testobj.parent = types.SimpleNamespace(root=types.SimpleNamespace(focus_set=mock_set))
        testobj.close()
        assert capsys.readouterr().out == ("called ShowMods.root.focus_set\n"
                                           "called ChoiceDialog.destroy\n")


class TestAttributesDialog:
    """unittests for tkgui.AttributesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for tkgui.AttributesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called AttributesDialog.__init__ with args', args)
            old_init(self, *args, **kwargs)
        monkeypatch.setattr(testee.AttributesDialog, '__init__', mock_init)
        testobj = testee.AttributesDialog()
        assert capsys.readouterr().out == 'called AttributesDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for AttributesDialog.__init__
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            print('called Toplevel.__init__ with args', args, kwargs)
            old_init(self, *kwargs, **kwargs)
        monkeypatch.setattr(testee.tk.Toplevel, '__init__', mock_init)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        monkeypatch.setattr(testee.ttk, 'Entry', mockttk.MockEntry)
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.ttk, 'Combobox', mockttk.MockComboBox)
        monkeypatch.setattr(testee.tk, 'IntVar', mockttk.MockIntVar)
        monkeypatch.setattr(testee.ttk, 'Checkbutton', mockttk.MockCheckBox)
        # monkeypatch.setattr(testee.ImageTk, 'PhotoImage', mockttk.MockPhotoImage)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        monkeypatch.setattr(testee.AttributesDialog, 'process', lambda *x: 'dummy')
        monkeypatch.setattr(testee.AttributesDialog, 'clear_name_text', lambda *x: 'dummy')
        monkeypatch.setattr(testee.AttributesDialog, 'clear_text_text', lambda *x: 'dummy')
        monkeypatch.setattr(testee.AttributesDialog, 'update', lambda *x: 'dummy')
        monkeypatch.setattr(testee.AttributesDialog, 'monitor_textvar', lambda *x: 'dummy')
        # parent = mockttk.MockToplevel()
        parent = types.SimpleNamespace(root='root', ecimage='ecimage')
        # assert capsys.readouterr().out == "called Widget.__init__\n"
        conf = MockConf()
        testobj = testee.AttributesDialog(parent, conf)
        assert testobj.parent == parent
        assert testobj.conf == conf
        assert testobj.modnames == {'xxx_name': 'xxx', 'yyy_name': 'yyy'}
        assert isinstance(testobj.lbox, testee.ttk.Combobox)
        # assert isinstance(testobj.select_button, testee.ttk.QPushButton)
        assert isinstance(testobj.name, testee.ttk.Combobox)
        assert isinstance(testobj.clear_name_button, testee.ttk.Button)
        assert isinstance(testobj.text, testee.ttk.Entry)
        assert isinstance(testobj.clear_text_button, testee.ttk.Button)
        assert isinstance(testobj.activate_button, testee.ttk.Checkbutton)
        assert isinstance(testobj.comps_button, testee.ttk.Button)
        assert isinstance(testobj.deps_button, testee.ttk.Button)
        assert isinstance(testobj.change_button, testee.ttk.Button)
        assert capsys.readouterr().out == expected_output['attrs'].format(
                testobj=testobj, image=testee.ImageTk.PhotoImage(testee.ECIMAGE))

    def test_monitor_textvar(self, monkeypatch, capsys):
        """unittest for AttributesDialog.monitor_textvar
        """
        def mock_enable(*args):
            print('called AttributesDialog.enable_change')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_change = mock_enable
        testobj.monitor_textvar()
        assert capsys.readouterr().out == "called AttributesDialog.enable_change\n"

    def test_enable_change(self, monkeypatch, capsys):
        """unittest for AttributesDialog.enable_change
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.change_button = mockttk.MockButton()
        assert capsys.readouterr().out == (
                "called Button.__init__ with args <class 'NoneType'> () {}\n")
        testobj.enable_change()
        assert capsys.readouterr().out == "called Button.state with args (['!disabled'],)\n"

    # def _test_enable_select(self, monkeypatch, capsys):
    #     """unittest for AttributesDialog.enable_select
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.select_button = mockttk.MockPushButton()
    #     testobj.comps_button = mockttk.MockPushButton()
    #     testobj.deps_button = mockttk.MockPushButton()
    #     testobj.change_button = mockttk.MockPushButton()
    #     assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
    #                                        "called PushButton.__init__ with args () {}\n"
    #                                        "called PushButton.__init__ with args () {}\n"
    #                                        "called PushButton.__init__ with args () {}\n")
    #     testobj.enable_select()
    #     assert capsys.readouterr().out == ("called PushButton.setDisabled with arg `True`\n"
    #                                        "called PushButton.setDisabled with arg `True`\n"
    #                                        "called PushButton.setDisabled with arg `True`\n")

    def test_process(self, monkeypatch, capsys):
        """unittest for AttributesDialog.process
        """
        def mock_list(self, name):
            "stub"
            print(f"called Conf.list_components_for_dir with arg '{name}'")
            return []
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(
                    screeninfo={'current text': {'txt': 'xxx', 'sel': True, 'opt': False}}))
        testobj.modnames = {'current text': {'aaa'}}
        # testobj.select_button = mockttk.MockPushButton()
        testobj.lbox = mockttk.MockComboBox()
        testobj.modname = mockttk.MockStringVar()
        testobj.modname.set('current text')
        testobj.name = mockttk.MockComboBox()
        testobj.scrname = mockttk.MockStringVar()
        testobj.clear_name_button = mockttk.MockButton()
        testobj.text = mockttk.MockEntry()
        testobj.scrtext = mockttk.MockStringVar()
        testobj.clear_text_button = mockttk.MockButton()
        testobj.activate_button = mockttk.MockCheckBox()
        testobj.activate = mockttk.MockIntVar()
        testobj.exempt_button = mockttk.MockCheckBox()
        testobj.exempt = mockttk.MockIntVar()
        testobj.comps_button = mockttk.MockButton()
        testobj.deps_button = mockttk.MockButton()
        testobj.change_button = mockttk.MockButton()
        assert capsys.readouterr().out == (
                "called ComboBox.__init__ with args <class 'NoneType'> () {}\n"
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'current text'\n"
                "called ComboBox.__init__ with args <class 'NoneType'> () {}\n"
                "called StringVar.__init__ with args ()\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called Entry.__init__ with args <class 'NoneType'> () {}\n"
                "called StringVar.__init__ with args ()\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called CheckBox.__init__ with args <class 'NoneType'> () {}\n"
                "called IntVar.__init__ with args ()\n"
                "called CheckBox.__init__ with args <class 'NoneType'> () {}\n"
                "called IntVar.__init__ with args ()\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n")
        testobj.process()
        assert testobj.choice == 'current text'
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called StringVar.set with arg 'current text'\n"
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called Conf.get_component_data with args ('xxx', 'Name')\n"
                "called Conf.get_component_data with args ('yyy', 'Name')\n"
                "called ComboBox.configure with args {'values': ['xxx_compname', 'yyy_compname']}\n"
                "called ComboBox.state with args (['!disabled'],)\n"
                "called Button.state with args (['!disabled'],)\n"
                "called StringVar.set with arg 'xxx'\n"
                "called Entry.state with args (['!disabled'],)\n"
                "called Button.state with args (['!disabled'],)\n"
                "called IntVar.set with arg 1\n"
                "called CheckBox.state with args (['!disabled'],)\n"
                "called IntVar.set with arg 0\n"
                "called CheckBox.state with args (['!disabled'],)\n"
                "called Button.state with args (['!disabled'],)\n"
                "called Button.state with args (['!disabled'],)\n"
                "called Button.state with args (['disabled'],)\n")
        monkeypatch.setattr(MockConf, 'list_components_for_dir', mock_list)
        testobj.process()
        assert testobj.choice == 'current text'
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called StringVar.set with arg 'current text'\n"
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called ComboBox.configure with args {'values': []}\n"
                "called ComboBox.state with args (['!disabled'],)\n"
                "called Button.state with args (['!disabled'],)\n"
                "called StringVar.set with arg 'xxx'\n"
                "called Entry.state with args (['!disabled'],)\n"
                "called Button.state with args (['!disabled'],)\n"
                "called IntVar.set with arg 1\n"
                "called CheckBox.state with args (['!disabled'],)\n"
                "called IntVar.set with arg 0\n"
                "called CheckBox.state with args (['!disabled'],)\n"
                "called Button.state with args (['!disabled'],)\n"
                "called Button.state with args (['!disabled'],)\n"
                "called Button.state with args (['disabled'],)\n")

    def test_clear_name_text(self, monkeypatch, capsys):
        """unittest for AttributesDialog.clear_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.scrname = mockttk.MockStringVar()
        assert capsys.readouterr().out == "called StringVar.__init__ with args ()\n"
        testobj.clear_name_text()
        assert capsys.readouterr().out == "called StringVar.set with arg ''\n"

    def test_clear_text_text(self, monkeypatch, capsys):
        """unittest for AttributesDialog.clear_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.scrtext = mockttk.MockStringVar()
        assert capsys.readouterr().out == "called StringVar.__init__ with args ()\n"
        testobj.clear_text_text()
        assert capsys.readouterr().out == "called StringVar.set with arg ''\n"

    def test_view_components(self, monkeypatch, capsys):
        """unittest for AttributesDialog.view_components
        """
        def mock_get(name):
            "stub"
            print(f"called Manager.get_mod_components with arg '{name}'")
            return 'xxx'
        monkeypatch.setattr(testee.MessageBox, 'showinfo', mockttk.mock_show_info)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(get_mod_components=mock_get))
        testobj.choice = 'xxx'
        testobj.modnames = {'xxx': {'aaa'}}
        testobj.view_components()
        assert capsys.readouterr().out == (
                "called Manager.get_mod_components with arg '{'aaa'}'\n"
                f"called MessageBox.showinfo with args () {{'parent': {testobj!r},"
                " 'message': 'xxx'}\n")

    def test_view_dependencies(self, monkeypatch, capsys):
        """unittest for AttributesDialog.view_dependencies
        """
        def mock_get(name):
            "stub"
            print(f"called Manager.get_mod_dependencies with arg '{name}'")
            return 'xxx'
        monkeypatch.setattr(testee.MessageBox, 'showinfo', mockttk.mock_show_info)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(get_mod_dependencies=mock_get))
        # testobj.conf = MockConf()
        testobj.choice = 'xxx'
        testobj.modnames = {'xxx': {'aaa'}}
        testobj.view_dependencies()
        assert capsys.readouterr().out == (
                "called Manager.get_mod_dependencies with arg '{'aaa'}'\n"
                f"called MessageBox.showinfo with args () {{'parent': {testobj!r},"
                " 'message': 'xxx'}\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for AttributesDialog.update
        """
        def mock_update(*args):
            print('called Manager.update_attributes with args', args)
            return False, 'xxxx'
        def mock_update_2(*args):
            print('called Manager.update_attributes with args', args)
            return True, ''
        monkeypatch.setattr(testee.MessageBox, 'showinfo', mockttk.mock_show_info)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(
                    # screeninfo={'current text': {'txt': 'xxx', 'sel': True, 'pos': '2x2'}},
                    # attr_changes=[],
                    update_attributes=mock_update))
                # refresh_widgets=mock_refresh,
                # build_screen_text=mock_build)
        testobj.scrname = mockttk.MockStringVar()
        testobj.scrname.set('current text')
        testobj.clear_name_button = mockttk.MockButton()
        testobj.scrtext = mockttk.MockStringVar()
        testobj.scrname.set('')
        testobj.clear_text_button = mockttk.MockButton()
        testobj.activate_button = mockttk.MockCheckBox()
        testobj.exempt_button = mockttk.MockCheckBox()
        testobj.change_button = mockttk.MockButton()
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'current text'\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg ''\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called CheckBox.__init__ with args <class 'NoneType'> () {}\n"
                "called CheckBox.__init__ with args <class 'NoneType'> () {}\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n")
        testobj.choice = 'current text'
        testobj.update()
        # assert testobj.parent.master.screeninfo == {'current text': {'txt': '', 'sel': False,
        #                                                              'opt': False, 'pos': '2x2'}}
        # assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == (
                "called Button.state with args (['disabled'],)\n"
                "called Button.state with args (['disabled'],)\n"
                "called CheckBox.instate with args (['selected'],)\n"
                "called StringVar.get\n"
                "called StringVar.get\n"
                "called CheckBox.instate with args (['selected'],)\n"
                "called Manager.update_attributes with args"
                " (None, '', 'current text', None, None)\n"
                f"called MessageBox.showinfo with args () {{'parent': {testobj!r},"
                " 'message': 'xxxx'}\n")
        testobj.parent.master.update_attributes = mock_update_2
        testobj.update()
        assert capsys.readouterr().out == (
                "called Button.state with args (['disabled'],)\n"
                "called Button.state with args (['disabled'],)\n"
                "called CheckBox.instate with args (['selected'],)\n"
                "called StringVar.get\n"
                "called StringVar.get\n"
                "called CheckBox.instate with args (['selected'],)\n"
                "called Manager.update_attributes with args"
                " (None, '', 'current text', None, None)\n"
                "called Button.state with args (['disabled'],)\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for AttributesDialog.close
        """
        def mock_set():
            print('called ShowMods.root.focus_set')
        def mock_destroy():
            print('called AttributesDialog.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.destroy = mock_destroy
        testobj.parent = None
        testobj.close()
        assert capsys.readouterr().out == "called AttributesDialog.destroy\n"
        testobj.parent = types.SimpleNamespace(root=types.SimpleNamespace(focus_set=mock_set))
        testobj.close()
        assert capsys.readouterr().out == ("called ShowMods.root.focus_set\n"
                                           "called AttributesDialog.destroy\n")


class TestSaveGamesDialog:
    """unittests for tkgui.SaveGamesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for tkgui.SaveGamesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called SaveGamesDialog.__init__ with args', args)
            old_init(self, *args, **kwargs)
        monkeypatch.setattr(testee.SaveGamesDialog, '__init__', mock_init)
        testobj = testee.SaveGamesDialog()
        assert capsys.readouterr().out == 'called SaveGamesDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SaveGamesDialog.__init__
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            print('called Toplevel.__init__ with args', args, kwargs)
            old_init(self, *kwargs, **kwargs)
        def mock_add(self):
            print('called SaveGamesDialog.add_modselector')
        monkeypatch.setattr(testee.tk.Toplevel, '__init__', mock_init)
        monkeypatch.setattr(testee.tk.Toplevel, 'bind', mockttk.MockDialog.bind)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        monkeypatch.setattr(testee.ttk, 'Entry', mockttk.MockEntry)
        monkeypatch.setattr(testee.ttk, 'Combobox', mockttk.MockComboBox)
        # monkeypatch.setattr(testee.ttk, 'QCheckBox', mockttk.MockCheckBox)
        # monkeypatch.setattr(testee.qgui, 'QIcon', mockttk.MockIcon)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        monkeypatch.setattr(testee.SaveGamesDialog, 'confirm', lambda: 'dummy')
        monkeypatch.setattr(testee.SaveGamesDialog, 'update', lambda: 'dummy')
        monkeypatch.setattr(testee.SaveGamesDialog, 'add_modselector', mock_add)
        parent = types.SimpleNamespace(root='root')
        conf = MockConf()
        testobj = testee.SaveGamesDialog(parent, conf)
        assert testobj.parent == parent
        assert testobj.conf == conf
        assert testobj.savenames == ['qqq', 'rrr']
        assert testobj.modnames == {'xxx_name': 'xxx', 'yyy_name': 'yyy'}
        assert isinstance(testobj.savegame_selector, testee.ttk.Combobox)
        assert isinstance(testobj.pname, testee.ttk.Entry)
        assert isinstance(testobj.fname, testee.ttk.Entry)
        assert isinstance(testobj.gdate, testee.ttk.Entry)
        assert isinstance(testobj.update_button, testee.ttk.Button)
        assert isinstance(testobj.confirm_button, testee.ttk.Button)
        assert isinstance(testobj.close_button, testee.ttk.Button)
        assert testobj.oldsavename == ''
        assert testobj.widgets == []
        assert isinstance(testobj.hfrm, testee.ttk.Frame)
        assert testobj.hfrmlen == 0
        assert capsys.readouterr().out == expected_output['saves'].format(testobj=testobj)

    def test_monitor_textvar(self, monkeypatch, capsys):
        """unittest for sDialog.monitor_textvar
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update_button = mockttk.MockButton()
        assert capsys.readouterr().out == (
                "called Button.__init__ with args <class 'NoneType'> () {}\n")
        testobj.monitor_textvar()
        assert capsys.readouterr().out == "called Button.state with args (['!disabled'],)\n"

    def test_add_modselector(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.add_modselector
        """
        def mock_init(self, master, *args, **kwargs):
            kwargs['textvariable'] = f"item of type {type(kwargs['textvariable'])}"
            print('called ComboBox.__init__ with args', type(master), args, kwargs)
        def mock_bind(self, *args):
            args = (args[0], f"item of type {type(args[1])}")
            print('called ComboBox.bind with args', args)
        def mock_configure(self, **kwargs):
            kwargs['command'] = f"item of type {type(kwargs['command'])}"
            print('called Button.configure with args', kwargs)

        monkeypatch.setattr(mockttk.MockComboBox, '__init__', mock_init)
        monkeypatch.setattr(mockttk.MockComboBox, 'bind', mock_bind)
        monkeypatch.setattr(mockttk.MockButton, 'configure', mock_configure)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Combobox', mockttk.MockComboBox)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(ecimage='ecimage')
        testobj.hfrm = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args <class 'NoneType'> () {}\n")
        testobj.hfrmlen = 0
        testobj.modnames = ['yyy', 'xxx']
        testobj.widgets = []
        testobj.add_modselector()
        assert len(testobj.widgets) == 1
        assert isinstance(testobj.widgets[0][0], testee.ttk.Button)
        assert isinstance(testobj.widgets[0][1], testee.ttk.Combobox)
        assert isinstance(testobj.widgets[0][2], testee.ttk.Frame)
        assert isinstance(testobj.widgets[0][3], testee.tk.StringVar)
        assert capsys.readouterr().out == (
            "called Frame.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> () {}\n"
            "called Frame.grid with args ()"
            " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
            "called ComboBox.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> ()"
            f" {{'values': ['xxx', 'yyy'],"
            " 'textvariable': \"item of type <class 'tkinter.StringVar'>\"}\n"
            "called ComboBox.state with args (['readonly'],)\n"
            f"called ComboBox.bind with args ('<<ComboboxSelected>>',"
            " \"item of type <class 'functools.partial'>\")\n"
            "called ComboBox.grid with args ()"
            " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n"
            "called Frame.columnconfigure with args (0,)\n"
            "called Button.__init__ with args <class 'mockgui.mockttkwidgets.MockFrame'> ()"
            f" {{'image': '{testobj.parent.ecimage}'}}\n"
            "called Button.configure with args"
            " {'command': \"item of type <class 'functools.partial'>\"}\n"
            "called Button.state with args (['disabled'],)\n"
            "called Button.grid with args () {'row': 0, 'column': 1}\n")

    def test_process_mod(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.process_mod
        """
        def mock_add():
            print('called SaveGamesDialog.add_modselector')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_modselector = mock_add
        testobj.update_button = mockttk.MockButton()
        lbox = mockttk.MockComboBox()
        btn = mockttk.MockButton()
        lboxvar = mockttk.MockStringVar()
        lboxvar.set('select a mod')
        assert capsys.readouterr().out == (
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called ComboBox.__init__ with args <class 'NoneType'> () {}\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'select a mod'\n")
        testobj.widgets = []
        testobj.process_mod(lbox)
        assert capsys.readouterr().out == ""
        testobj.widgets = [[btn, lbox, 'frm', lboxvar]]
        testobj.process_mod(lbox)
        assert capsys.readouterr().out == "called StringVar.get\n"
        lboxvar.set('any value')
        assert capsys.readouterr().out == "called StringVar.set with arg 'any value'\n"
        testobj.process_mod(lbox)
        assert capsys.readouterr().out == ("called StringVar.get\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           "called SaveGamesDialog.add_modselector\n")
        lbox2 = mockttk.MockComboBox()
        btn2 = mockttk.MockButton()
        lbox2var = mockttk.MockStringVar()
        lbox2var.set('xxx')
        assert capsys.readouterr().out == (
                "called ComboBox.__init__ with args <class 'NoneType'> () {}\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'xxx'\n")
        testobj.widgets.append([btn2, lbox2, 'frm', lbox2var])
        testobj.process_mod(lbox)
        assert capsys.readouterr().out == ("called StringVar.get\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n")
        testobj.widgets[0], testobj.widgets[1] = testobj.widgets[1], testobj.widgets[0]
        testobj.process_mod(lbox)
        assert capsys.readouterr().out == ("called StringVar.get\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           "called SaveGamesDialog.add_modselector\n")

    def test_remove_mod(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.remove_mod
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.widgets = []
        lbox = mockttk.MockComboBox()
        btn = mockttk.MockButton()
        hbox = mockttk.MockFrame()
        # testobj.vbox2 = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called ComboBox.__init__ with args <class 'NoneType'> () {}\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called Frame.__init__ with args <class 'NoneType'> () {}\n")
                # "called VBox.__init__\n")
        testobj.remove_mod(btn)
        assert not testobj.widgets
        assert capsys.readouterr().out == ""
        testobj.widgets = [('x', 'y', 'z')]
        testobj.remove_mod(btn)
        assert len(testobj.widgets) == 1
        assert capsys.readouterr().out == ""
        testobj.widgets = [(btn, lbox, hbox)]
        testobj.remove_mod(btn)
        assert not testobj.widgets
        assert capsys.readouterr().out == ("called Button.destroy\n"
                                           "called ComboBox.destroy\n"
                                           "called Frame.destroy\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.confirm
        """
        def mock_list_dirs():
            print('called Conf.list_all_mod_dirs')
            return []
        def mock_list_comps(arg):
            print(f"called Conf.list_components_for_dir with arg '{arg}'")
            return []
        def mock_get_diritem_data(*args):
            print("called Conf.get_diritem_data with args", args)
            if args == ('xxx', '_DoNotTouch'):
                return False
            if args == ('yyy', '_DoNotTouch'):
                return True
            if args == ('zzz', '_DoNotTouch'):
                return True
        def mock_get_component_data(*args):
            print("called Conf.get_component_data with args", args)
            if args[0] == 'xxx':
                return 'aaa'
            if args[0] == 'yyy':
                return '.bbb'
        def mock_get_mods(name):
            print(f"called Conf.get_mods_for_saveitem with arg {name}")
            return ['qqq', 'rrr']
        def mock_select(self, names):
            print(f'called Manager.select_activations with arg {names}')
            self.directories = []
        def mock_refresh():
            print('called ShowMods.refresh_widget_data')
        def mock_exists(*args):
            print('called os.path.exists with args', args)
            return False
        def mock_exists_2(*args):
            print('called os.path.exists with args', args)
            return True
        monkeypatch.setattr(testee.MessageBox, 'showinfo', mockttk.mock_show_info)
        monkeypatch.setattr(testee.os.path, 'exists', mock_exists)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        testobj.conf.get_diritem_data = mock_get_diritem_data
        testobj.conf.get_component_data = mock_get_component_data
        testobj.conf.get_mods_for_saveitem = mock_get_mods
        testobj.parent = types.SimpleNamespace()
        testobj.parent.refresh_widget_data = mock_refresh
        testobj.parent.master = MockManager()
        # testobj.savegame_selector = mockttk.MockComboBox()
        # testobj.savegame_selector.setCurrentText('ppp')
        testobj.savegame_selector_text = mockttk.MockStringVar()
        testobj.savegame_selector_text.set('ppp')
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called StringVar.set with arg 'ppp'\n")
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called Conf.get_mods_for_saveitem with arg ppp\n"
                "called Conf.list_all_mod_dirs\n"
                "called Conf.get_diritem_data with args ('xxx', '_DoNotTouch')\n"
                "called Conf.get_diritem_data with args ('yyy', '_DoNotTouch')\n"
                "called os.path.exists with args ('modbase/yyy',)\n"
                "called Manager.select_activations with arg ['qqq', 'rrr']\n"
                "called Manager.activate\n"
                "called ShowMods.refresh_widget_data\n"
                "called MessageBox.showinfo with args ()"
                f" {{'parent': {testobj!r}, 'message': 'wijzigingen zijn doorgevoerd'}}\n")

        monkeypatch.setattr(MockManager, 'select_activations', mock_select)
        monkeypatch.setattr(testee.os.path, 'exists', mock_exists_2)
        testobj.conf.list_components_for_dir = mock_list_comps
        testobj.parent.master.directories = ['sss', 'ttt']
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called Conf.get_mods_for_saveitem with arg ppp\n"
                "called Conf.list_all_mod_dirs\n"
                "called Conf.get_diritem_data with args ('xxx', '_DoNotTouch')\n"
                "called Conf.get_diritem_data with args ('yyy', '_DoNotTouch')\n"
                "called os.path.exists with args ('modbase/yyy',)\n"
                "called Conf.get_diritem_data with args ('yyy', 'SCRNAM')\n"
                "called Manager.select_activations with arg ['qqq', 'rrr', 'yyy']\n"
                "called ShowMods.refresh_widget_data\n"
                "called MessageBox.showinfo with args ()"
                f" {{'parent': {testobj!r}, 'message': 'wijzigingen zijn doorgevoerd'}}\n")

        testobj.conf.list_all_mod_dirs = mock_list_dirs
        testobj.parent.master.directories = ['sss', 'ttt']
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called Conf.get_mods_for_saveitem with arg ppp\n"
                "called Conf.list_all_mod_dirs\n"
                "called Manager.select_activations with arg ['qqq', 'rrr']\n"
                "called ShowMods.refresh_widget_data\n"
                "called MessageBox.showinfo with args ()"
                f" {{'parent': {testobj!r}, 'message': 'wijzigingen zijn doorgevoerd'}}\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.update
        """
        def mock_update(arg):
            print(f"called SaveGameDialog.update_conf with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update_conf = mock_update
        # testobj.conf = MockConf()
        testobj.savegame_selector_text = mockttk.MockStringVar()
        testobj.savegame_selector_text.set('current text')
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called StringVar.set with arg 'current text'\n")
        testobj.update()
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called SaveGameDialog.update_conf with arg 'current text'\n")

    def test_update_conf(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.update
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pname_text = mockttk.MockStringVar()
        testobj.pname_text.set('xxx')
        testobj.fname_text = mockttk.MockStringVar()
        testobj.fname_text.set('yyy')
        testobj.gdate_text = mockttk.MockStringVar()
        testobj.gdate_text.set('zzz')
        testobj.update_button = mockttk.MockButton()
        testobj.conf = MockConf()
        testobj.widgets = []
        lbox = mockttk.MockComboBox()
        testobj.old_pname = 'xxx'
        testobj.old_fname = 'yyy'
        testobj.old_gdate = 'zzz'
        testobj.oldmods = []
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\ncalled StringVar.set with arg 'xxx'\n"
                "called StringVar.__init__ with args ()\ncalled StringVar.set with arg 'yyy'\n"
                "called StringVar.__init__ with args ()\ncalled StringVar.set with arg 'zzz'\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called ComboBox.__init__ with args <class 'NoneType'> () {}\n")
        testobj.update_conf('save_name')
        assert capsys.readouterr().out == ("called StringVar.get\n"
                                           "called StringVar.get\n"
                                           "called StringVar.get\n"
                                           "called Conf.save\n"
                                           "called Button.state with args (['disabled'],)\n")
        testobj.widgets = [lbox]
        testobj.oldmods = ['current text']
        testobj.update_conf('save_name')
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called StringVar.get\n"
                "called StringVar.get\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Mods', [])\n"
                "called Conf.save\n"
                "called Button.state with args (['disabled'],)\n")

        testobj.old_pname = 'aaa'
        testobj.old_fname = 'bbb'
        testobj.old_gdate = 'ccc'
        testobj.oldmods = ['qqq']
        testobj.update_conf('save_name')
        assert capsys.readouterr().out == (
                "called StringVar.get\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Pname', 'xxx')\n"
                "called StringVar.get\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Fname', 'yyy')\n"
                "called StringVar.get\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Gdate', 'zzz')\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Mods', [])\n"
                "called Conf.save\n"
                "called Button.state with args (['disabled'],)\n")

    def test_get_savedata(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.get_savedata
        """
        def mock_update(name):
            print(f'called SaveGamesDialog with arg {name}')
        def mock_add(self):
            print('called SaveGamesDialog.add_modselector')
            self.widgets = [[btn, lbox, hbox, lvar]]
        def mock_get_attrs(value):
            "stub"
            print(f"called Conf.get_saveitem_attrs with arg {value}")
            return ('oldpname', 'oldfname', 'oldgdate'), True
        def mock_get_attrs_2(value):
            "stub"
            print(f"called Conf.get_saveitem_attrs with arg {value}")
            return ('oldpname', 'oldfname', 'oldgdate'), False
        def mock_get_mods(name):
            "stub"
            print(f"called Conf.get_mods_for_saveitem with arg {name}")
            return ['newmodname']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        testobj.update_conf = mock_update
        monkeypatch.setattr(testee.SaveGamesDialog, 'add_modselector', mock_add)
        testobj.savegame_selector_text = mockttk.MockStringVar()
        btn = mockttk.MockButton()
        lbox = mockttk.MockComboBox()
        hbox = mockttk.MockFrame()
        lvar = mockttk.MockStringVar()
        testobj.pname_text = mockttk.MockStringVar()
        testobj.fname_text = mockttk.MockStringVar()
        testobj.gdate_text = mockttk.MockStringVar()
        testobj.update_button = mockttk.MockButton()
        testobj.confirm_button = mockttk.MockButton()
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called ComboBox.__init__ with args <class 'NoneType'> () {}\n"
                "called Frame.__init__ with args <class 'NoneType'> () {}\n"
                "called StringVar.__init__ with args ()\n"
                "called StringVar.__init__ with args ()\n"
                "called StringVar.__init__ with args ()\n"
                "called StringVar.__init__ with args ()\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n"
                "called Button.__init__ with args <class 'NoneType'> () {}\n")
        testobj.widgets = []

        testobj.savegame_selector_text.set('select a saved game')
        assert capsys.readouterr().out == "called StringVar.set with arg 'select a saved game'\n"
        testobj.get_savedata()
        assert capsys.readouterr().out == "called StringVar.get\n"

        testobj.oldsavename = ''
        testobj.savegame_selector_text.set('xxx')
        assert capsys.readouterr().out == "called StringVar.set with arg 'xxx'\n"
        testobj.get_savedata()
        assert capsys.readouterr().out == ("called StringVar.get\n"
                                           "called Conf.get_saveitem_attrs with arg xxx\n"
                                           "called Button.state with args (['disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n")
        testobj.oldsavename = 'yyy'
        # testobj.savegame_selector_text.set('xxx')
        testobj.get_savedata()
        assert capsys.readouterr().out == ("called StringVar.get\n"
                                           "called SaveGamesDialog with arg yyy\n"
                                           "called SaveGamesDialog.add_modselector\n"
                                           "called Conf.get_saveitem_attrs with arg xxx\n"
                                           "called Button.state with args (['disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n")
        testobj.widgets = [[btn, lbox, hbox]]
        testobj.conf.get_saveitem_attrs = mock_get_attrs
        testobj.conf.get_mods_for_saveitem = mock_get_mods
        testobj.get_savedata('xxx')
        assert capsys.readouterr().out == ("called StringVar.get\n"
                                           "called SaveGamesDialog with arg xxx\n"
                                           "called Button.destroy\n"
                                           "called ComboBox.destroy\n"
                                           "called Frame.destroy\n"
                                           "called SaveGamesDialog.add_modselector\n"
                                           "called Conf.get_saveitem_attrs with arg xxx\n"
                                           "called StringVar.set with arg 'oldpname'\n"
                                           "called StringVar.set with arg 'oldfname'\n"
                                           "called StringVar.set with arg 'oldgdate'\n"
                                           "called Conf.get_mods_for_saveitem with arg xxx\n"
                                           "called StringVar.set with arg 'newmodname'\n"
                                           "called SaveGamesDialog.add_modselector\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n")
        testobj.conf.get_saveitem_attrs = mock_get_attrs_2
        testobj.get_savedata('xxx')
        assert capsys.readouterr().out == ("called StringVar.get\n"
                                           "called SaveGamesDialog with arg xxx\n"
                                           "called Button.destroy\n"
                                           "called ComboBox.destroy\n"
                                           "called Frame.destroy\n"
                                           "called SaveGamesDialog.add_modselector\n"
                                           "called Conf.get_saveitem_attrs with arg xxx\n"
                                           "called StringVar.set with arg 'oldpname'\n"
                                           "called StringVar.set with arg 'oldfname'\n"
                                           "called StringVar.set with arg 'oldgdate'\n"
                                           "called Conf.get_mods_for_saveitem with arg xxx\n"
                                           "called StringVar.set with arg 'newmodname'\n"
                                           "called SaveGamesDialog.add_modselector\n"
                                           "called Button.state with args (['disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for SettingsDialog.close
        """
        def mock_set():
            print('called ShowMods.root.focus_set')
        def mock_destroy():
            print('called SaveGamesDialog.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.destroy = mock_destroy
        testobj.parent = None
        testobj.close()
        assert capsys.readouterr().out == "called SaveGamesDialog.destroy\n"
        testobj.parent = types.SimpleNamespace(root=types.SimpleNamespace(focus_set=mock_set))
        testobj.close()
        assert capsys.readouterr().out == ("called ShowMods.root.focus_set\n"
                                           "called SaveGamesDialog.destroy\n")
