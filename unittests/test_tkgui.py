"""unittests for ./src/tkgui.py
"""
import types
import pytest
from src import tkgui as testee
from mockgui import mockttkwidgets as mockttk

choice = """\
called Toplevel.__init__ with args ('root',) {{}}
called Frame.__init__ with args ChoiceDialog () {{'padding': 10}}
called Frame.grid with args () {{'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called Frame.columnconfigure with args (0,)
called Label.__init__ with args MockFrame () {{'text': 'a caption'}}
called Label.grid with args () {{'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called StringVar.__init__ with args ()
called ComboBox.__init__ with args MockFrame () {{'values': ['ons', 'op', 'ti'], 'textvariable': {testobj.dirname}}}
called StringVar.set with arg ''
called ComboBox.state with args (['readonly'],)
called ComboBox.bind with args ('<<ComboboxSelected>>', {testobj.enable_accept})
called ComboBox.grid with args () {{'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}}
called Frame.__init__ with args MockFrame () {{}}
called Frame.grid with args () {{'row': 2, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}}
called Button.__init__ with args MockFrame () {{'text': 'Ok', 'underline': 0, 'command': {testobj.accept}}}
called Button.state with args (['disabled'],)
called Button.grid with args () {{'row': 0, 'column': 0, 'sticky': ('e', 'w')}}
called Frame.columnconfigure with args (0,)
called Button.__init__ with args MockFrame () {{'text': 'Cancel', 'underline': 0, 'command': {testobj.close}}}
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


@pytest.fixture
def expected_output():
    "fixture returning output to be expected from (mostly) gui setup methods"
    results = {'choice': choice}
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


def test_get_shortcut_info():
    "unittest for tkgui.get_shortcut_info"
    with pytest.raises(ValueError):
        testee.get_shortcut_info('xyz')
    assert testee.get_shortcut_info('&xyz') == (0, 'xyz', 'x')
    assert testee.get_shortcut_info('x&yz') == (1, 'xyz', 'y')
    assert testee.get_shortcut_info('xy&z') == (2, 'xyz', 'z')


def test_show_message(monkeypatch, capsys):
    """unittests for tkgui.show_message
    """
    monkeypatch.setattr(testee.MessageBox, 'showinfo', mockttk.mock_show_info)
    testee.show_message('win', 'xxx')
    assert capsys.readouterr().out == ("called MessageBox.showinfo with args ()"
                                       " {'parent': 'win', 'message': 'xxx', 'title': 'SDVMM'}\n")
    testee.show_message('win', 'yyy', 'zzz')
    assert capsys.readouterr().out == ("called MessageBox.showinfo with args ()"
                                       " {'parent': 'win', 'message': 'yyy', 'title': 'zzz'}\n")


def test_show_dialog(capsys):
    """unittests for tkgui.show_dialog
    """
    class MockDialogGui:
        "stub"
        def __init__(self):
            print('called DialogGui.__init__')
        def focus_set(self):
            print("called DialogGui.focus_set")
        def grab_set(self):
            print("called DialogGui.grab_set")
        def wait_window(self):
            print("called DialogGui.wait_window")
    class MockDialog:
        "stub"
        def __init__(self, *args, **kwargs):
            print('called Dialog.__init__ with args', args, kwargs)
            self.doit = MockDialogGui()
    cls = MockDialog
    parent = types.SimpleNamespace()
    modnames = ['x', 'y']
    assert testee.show_dialog(cls, parent, modnames, True)
    assert capsys.readouterr().out == (
        "called Dialog.__init__ with args (namespace(), ['x', 'y'], True) {}\n"
        "called DialogGui.__init__\n"
        "called DialogGui.focus_set\n"
        "called DialogGui.grab_set\n"
        "called DialogGui.wait_window\n")


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
        def mock_add(self, *args):
            print('called ShowMods.root.add_option with args', args)
        def mock_title(self, *args):
            """stub
            """
            print('called ShowMods.root.__title__ with args', args)
        monkeypatch.setattr(testee.ImageTk, 'PhotoImage', mockttk.MockPhotoImage)
        monkeypatch.setattr(testee.tk.Tk, '__init__', mock_init)
        monkeypatch.setattr(testee.tk.Tk, 'option_add', mock_add)
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
                "called ShowMods.root.add_option with args ('*tearOff', False)\n"
                "called PhotoImage.__init__ with args ('ecimage',)\n"
                "called ShowMods.root.__title__ with args ('SDV Mod Manager',)\n"
                "called Frame.__init__ with args Tk () {}\n"
                "called Frame.grid with args"
                " () {'column': 0, 'row': 0, 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_create_selectables_title(self, monkeypatch, capsys):
        """unittest for ShowMods.create_selectables_title
        """
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.main = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args NoneType () {}\n")
        testobj.create_selectables_title('xxxx')
        assert capsys.readouterr().out == (
                "called Label.__init__ with args MockFrame () {'text': 'xxxx', 'padding': 10}\n"
                "called Label.grid with args () {'column': 0, 'row': 0, 'sticky': ('n', 'w')}\n")

    def test_create_selectables_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.create_selectables_grid
        """
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.main = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args NoneType () {}\n")
        testobj.create_selectables_grid()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args MockFrame"
                " () {'padding': (10, 0)}\n"
                "called Frame.grid with args () {'column': 0, 'row': 1}\n")

    def test_create_dependencies_title(self, monkeypatch, capsys):
        """unittest for ShowMods.create_dependencies_title
        """
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.main = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args NoneType () {}\n")
        testobj.create_dependencies_title('yyyy')
        assert capsys.readouterr().out == (
                "called Label.__init__ with args MockFrame"
                " () {'text': 'yyyy', 'padding': 10}\n"
                "called Label.grid with args () {'column': 0, 'row': 2, 'sticky': ('n', 'w')}\n")

    def test_create_dependencies_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.create_dependencies_grid
        """
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.main = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args NoneType () {}\n")
        testobj.create_dependencies_grid()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args MockFrame"
                " () {'padding': (10, 0)}\n"
                "called Frame.grid with args () {'column': 0, 'row': 3}\n")

    def test_create_buttons(self, monkeypatch, capsys):
        """unittest for ShowMods.create_buttons
        """
        def mock_refresh(*args, **kwargs):
            """stub
            """
            print('called ShowMods.refresh_widgets with args', args, kwargs)
        def callback1():
            "dummy callback function"
        def callback2():
            "dummy callback function"
        def callback3():
            "dummy callback function"
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args NoneType () {}\n")
        testobj.buttons = {}
        testobj.refresh_widgets = mock_refresh
        testobj.create_buttons([
            {'name': 'xxx', 'text': '&xxxxxx', 'tooltip': 'xxxxxxxxx', 'callback': callback1},
            {'name': 'actv', 'text': 'yyy&yyy', 'tooltip': 'yyyyyyyyy', 'callback': callback2},
            {'name': 'close', 'text': '&Close', 'tooltip': 'close', 'callback': callback3}])
        assert len(testobj.buttons) == 3
        assert isinstance(testobj.buttons['xxx'], mockttk.MockButton)
        assert isinstance(testobj.buttons['actv'], mockttk.MockButton)
        assert isinstance(testobj.buttons['close'], mockttk.MockButton)
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args MockFrame () {'padding': 10}\n"
                "called Frame.grid with args () {'column': 0, 'row': 3, 'sticky': 's'}\n"
                "called Button.__init__ with args MockFrame"
                f" () {{'text': 'xxxxxx', 'command': {callback1}, 'underline': 0}}\n"
                "called Button.grid with args () {'column': 0, 'row': 0}\n"
                "called Button.__init__ with args MockFrame"
                f" () {{'text': 'yyyyyy', 'command': {callback2}, 'underline': 3}}\n"
                "called Button.grid with args () {'column': 1, 'row': 0}\n"
                "called Button.state with args (['disabled'],)\n"
                "called Button.__init__ with args MockFrame"
                f" () {{'text': 'Close', 'command': {callback3}, 'underline': 2}}\n"
                "called Button.grid with args () {'column': 2, 'row': 0}\n")

    def test_setup_actions(self, monkeypatch, capsys):
        """unittest for ShowMods.setup_actions
        """
        def mock_bind(*args):
            print('called ShowMods.root.bind with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = types.SimpleNamespace(bind=mock_bind)
        testobj.setup_actions()
        assert capsys.readouterr().out == (
                f"called ShowMods.root.bind with args ('<Alt-d>', {testobj.manage_defaults})\n"
                f"called ShowMods.root.bind with args ('<Alt-i>', {testobj.update_mods})\n"
                f"called ShowMods.root.bind with args ('<Alt-r>', {testobj.manage_deletions})\n"
                f"called ShowMods.root.bind with args ('<Alt-m>', {testobj.manage_attributes})\n"
                f"called ShowMods.root.bind with args ('<Alt-a>', {testobj.confirm})\n"
                f"called ShowMods.root.bind with args ('<Control-Return>', {testobj.confirm})\n"
                f"called ShowMods.root.bind with args ('<Alt-s>', {testobj.manage_savefiles})\n"
                f"called ShowMods.root.bind with args ('<Alt-x>', {testobj.close})\n"
                f"called ShowMods.root.bind with args ('<Alt-o>', {testobj.close})\n"
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
                "called Button.__init__ with args NoneType () {}\n"
                "called Button.__init__ with args NoneType () {}\n")
        testobj.refresh_widgets()
        assert capsys.readouterr().out == (
                "called Button.state with args (['disabled'],)\n"
                "called Button.state with args (['disabled'],)\n"
                "called Manager.order_widgets with args ('activatables', 'dependencies', False)\n")
        testobj.master.screeninfo = {'x': 'y'}
        testobj.refresh_widgets(True)
        assert capsys.readouterr().out == (
                "called Button.state with args (['!disabled'],)\n"
                "called Button.state with args (['!disabled'],)\n"
                "called Manager.order_widgets with args ('activatables', 'dependencies', True)\n")

    def test_remove_widgets(self, monkeypatch, capsys):
        """unittest for ShowMods.remove_widgets
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widgetlist = ['', mockttk.MockLabel(), mockttk.MockCheckBox()]
        container = mockttk.MockFrame()
        assert capsys.readouterr().out == (
                "called Label.__init__ with args NoneType () {}\n"
                "called CheckBox.__init__ with args NoneType () {}\n"
                "called StringVar.__init__ with args ()\n"
                "called Frame.__init__ with args NoneType () {}\n")
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
            "called Frame.__init__ with args str () {'padding': (5, 0, 5, 0)}\n"
            "called IntVar.__init__ with args ()\n"
            "called CheckBox.__init__ with args MockFrame"
            f" () {{'variable': {widgetlist[4]}, 'command': {testobj.enable_button}}}\n"
            "called CheckBox.state with args (['disabled', '!selected'],)\n"
            "called CheckBox.grid with args () {'column': 1, 'row': 0}\n"
            "called StringVar.__init__ with args ()\n"
            "called Label.__init__ with args MockFrame"
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
            "called Frame.__init__ with args str () {'padding': (5, 0, 5, 0)}\n"
            "called IntVar.__init__ with args ()\n"
            "called CheckBox.__init__ with args MockFrame"
            f" () {{'variable': {widgetlist[4]}, 'command': {testobj.enable_button}}}\n"
            "called CheckBox.state with args (['!disabled', '!selected'],)\n"
            "called CheckBox.grid with args () {'column': 1, 'row': 0}\n"
            "called StringVar.__init__ with args ()\n"
            "called Label.__init__ with args MockFrame"
            f" () {{'textvariable': {widgetlist[3]}}}\n"
            "called Label.grid with args () {'column': 2, 'row': 0}\n"
            "called Frame.grid with args () {'row': 1, 'column': 2, 'sticky': 'w'}\n")

    def test_set_label_text(self, monkeypatch, capsys):
        """unittest for ShowMods.set_label_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widgetlist = ['frame', mockttk.MockLabel(), 'check', mockttk.MockStringVar(), 'intvar']
        assert widgetlist[3].get() is None
        assert capsys.readouterr().out == (
                "called Label.__init__ with args NoneType () {}\n"
                "called StringVar.__init__ with args ()\n"
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
        assert widgetlist[3].get() == 'xxxx'
        assert capsys.readouterr().out == (
                f"called Label.bind with args ('<Button-1>', {testobj.open_browser})\n"
                "called Label.configure with args {'foreground': 'blue', 'cursor': 'hand2'}\n"
                "called StringVar.set with arg 'xxxx'\n"
                "called StringVar.get\n")
        testobj.set_label_text(widgetlist, 'xxxx', 'zz', 'yyy')
        assert widgetlist[3].get() == 'xxxx yyy'
        assert capsys.readouterr().out == (
                f"called Label.bind with args ('<Button-1>', {testobj.open_browser})\n"
                "called Label.configure with args {'foreground': 'blue', 'cursor': 'hand2'}\n"
                "called StringVar.set with arg 'xxxx yyy'\n"
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

    def test_open_browser(self, monkeypatch, capsys):
        """unittest for ShowMods.open_browser
        """
        def mock_get(arg):
            print('called event.widget.cget with arg', arg)
            return "name (number)"
        def mock_build(*args):
            print('called Manager.build_link_text with args', args)
            return '<a href="xxxxx">yyyy</a>'
        def mock_open(arg):
            print("called webbrowser.open_new with arg", arg)
        monkeypatch.setattr(testee.webbrowser, 'open_new', mock_open)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(build_link_text=mock_build)
        event = types.SimpleNamespace(widget=types.SimpleNamespace(cget=mock_get))
        testobj.open_browser(event)
        assert capsys.readouterr().out == (
                "called event.widget.cget with arg text\n"
                "called Manager.build_link_text with args ('name ', 'number')\n"
                "called webbrowser.open_new with arg xxxxx\n")

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
        assert capsys.readouterr().out == "called Button.__init__ with args NoneType () {}\n"
        testobj.enable_button()
        assert capsys.readouterr().out == "called Button.state with args (['!disabled'],)\n"

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
        assert capsys.readouterr().out == "called Button.__init__ with args NoneType () {}\n"
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

    def test_manage_deletions(self, monkeypatch, capsys):
        """unittest for ShowMods.manage_deletions
        """
        def mock_manage():
            print('called Manager.manage_deletions')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(manage_deletions=mock_manage)
        testobj.manage_deletions('event')
        assert capsys.readouterr().out == "called Manager.manage_deletions\n"

    def test_manage_savefiles(self, monkeypatch, capsys):
        """unittest for ShowMods.manage_savefiles
        """
        def mock_manage():
            print('called Manager.manage_savefiles')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(manage_savefiles=mock_manage)
        testobj.manage_savefiles('event')
        assert capsys.readouterr().out == "called Manager.manage_savefiles\n"


class TestSettingsDialogGui:
    """unittests for qtgui.SettingsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SettingsDialogGui objeict

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called SettingsDialogGui.__init__ with args', args)
            # self._w = ' (mocked)'
        def mock_bind_all(self, *args):
            print('called SettingsDialogGui.bind_all with args', args)
        monkeypatch.setattr(testee.SettingsDialogGui, '__init__', mock_init)
        monkeypatch.setattr(testee.SettingsDialogGui, 'bind_all', mock_bind_all)
        testobj = testee.SettingsDialogGui()
        # print(testobj)
        assert capsys.readouterr().out == 'called SettingsDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):  # , expected_output):
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
        maingui = types.SimpleNamespace()
        parent = types.SimpleNamespace(root='root')
        testobj = testee.SettingsDialogGui(maingui, parent)
        assert testobj.maingui == maingui
        assert testobj.parent == parent
        assert isinstance(testobj.frm, testee.ttk.Frame)
        assert capsys.readouterr().out == (
                "called Toplevel.__init__ with args ('root',) {}\n"
                "called Frame.__init__ with args SettingsDialogGui () {'padding': 10}\n"
                "called Frame.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n"
                "called Frame.columnconfigure with args (0,)\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.add_label
        """
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.add_label('xxx')
        assert capsys.readouterr().out == (
                "called Label.__init__ with args MockFrame () {'text': 'xxx'}\n"
                "called Label.grid with args () {'row': 1, 'column': 0, 'sticky': 'w'}\n")

    def test_add_line_entry(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.add_line_entry
        """
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.ttk, 'Entry', mockttk.MockEntry)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.textvars = {}
        result = testobj.add_line_entry('xxx')
        assert isinstance(result, testee.ttk.Entry)
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called Entry.__init__ with args MockFrame ()"
                f" {{'width': 48, 'textvariable': {testobj.textvars[result]}}}\n"
                "called StringVar.set with arg 'xxx'\n"
                "called Entry.grid with args () {'row': 0, 'column': 1}\n")

    def test_add_browse_button(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.add_browse_button
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.ttk, 'Checkbutton', mockttk.MockCheckBox)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        result = testobj.add_browse_button(callback)
        assert isinstance(result, testee.ttk.Button)
        assert capsys.readouterr().out == (
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'Browse', 'command': {callback}}}\n"
                "called Button.grid with args () {'row': 0, 'column': 2, 'sticky': 'w'}\n")

    def test_add_spinbox(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.add_spinbox
        """
        monkeypatch.setattr(testee.tk, 'IntVar', mockttk.MockIntVar)
        monkeypatch.setattr(testee.ttk, 'Spinbox', mockttk.MockSpinBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.textvars = {}
        result = testobj.add_spinbox('xxx')
        assert isinstance(result, testee.ttk.Spinbox)
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called IntVar.__init__ with args ()\n"
                "called IntVar.set with arg xxx\n"
                "called SpinBox.__init__ with args MockFrame () {'width': 5, 'from_': 0,"
                f" 'to': 5, 'textvariable': {testobj.textvars[result]}}}\n"
                "called SpinBox.grid with args () {'row': 0, 'column': 1, 'sticky': 'w'}\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.add_buttonbox
        """
        def mock_get_info(text):
            "stub"
            return 0, text, 'q'
        def mock_bind(*args):
            print('called SettingsDialogGui.bind with args', args)
        def mock_confirm(*args):
            "dummy stub for callback"
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee, 'get_shortcut_info', mock_get_info)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.bind = mock_bind
        testobj.confirm = mock_confirm
        testobj.add_buttonbox([('xxx', callback)])
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args SettingsDialogGui () {'padding': 10}\n"
                "called Frame.grid with args () {'row': 1, 'column': 0}\n"
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'xxx', 'underline': 0, 'command': {callback}}}\n"
                "called Button.grid with args () {'row': 0, 'column': 0}\n"
                f"called SettingsDialogGui.bind with args ('<Alt-q>', {callback})\n"
                f"called SettingsDialogGui.bind with args ('<Escape>', {testobj.confirm})\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.set_focus
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus(widget)
        assert capsys.readouterr().out == ("called Entry.focus_set\n")

    def test_get_widget_text(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.get_widget_text
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widget: wvar}
        # breakpoint()
        testobj.get_widget_text(widget)
        assert capsys.readouterr().out == "called StringVar.get\n"

    def test_set_widget_text(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.set_widget_text
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widget: wvar}
        testobj.set_widget_text(widget, 'xxx')
        assert capsys.readouterr().out == "called StringVar.set with arg 'xxx'\n"

    def test_select_directory(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.select_directory
        """
        monkeypatch.setattr(testee.FileDialog, 'askdirectory', mockttk.mock_askopen_nofile)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.select_directory('xxx', 'yyy') == ''
        assert capsys.readouterr().out == (
                "called FileDialog.askopenfilename with args"
                " {'title': 'xxx', 'initialdir': 'yyy', 'mustexist': True}\n")
        monkeypatch.setattr(testee.FileDialog, 'askdirectory', mockttk.mock_askopen_file)
        assert testobj.select_directory('xxx', 'yyy') == 'filename'
        assert capsys.readouterr().out == (
                "called FileDialog.askopenfilename with args"
                " {'title': 'xxx', 'initialdir': 'yyy', 'mustexist': True}\n")

    def test_reject(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.reject
        """
        def mock_focus():
            print('called ShowMods.focus_set')
        def mock_destroy(self):
            print('called SettingsDialogGui.destroy')
        monkeypatch.setattr(testee.SettingsDialogGui, 'destroy', mock_destroy)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(root=types.SimpleNamespace(focus_set=mock_focus))
        testobj.reject()
        assert capsys.readouterr().out == ("called ShowMods.focus_set\n"
                                           "called SettingsDialogGui.destroy\n")
        testobj.parent = None
        testobj.reject()
        assert capsys.readouterr().out == "called SettingsDialogGui.destroy\n"

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.confirm
        """
        def mock_focus():
            print('called ShowMods.focus_set')
        def mock_destroy(self):
            print('called SettingsDialogGui.destroy')
        monkeypatch.setattr(testee.SettingsDialogGui, 'destroy', mock_destroy)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(root=types.SimpleNamespace(focus_set=mock_focus))
        testobj.confirm()
        assert capsys.readouterr().out == ("called ShowMods.focus_set\n"
                                           "called SettingsDialogGui.destroy\n")
        testobj.parent = None
        testobj.confirm()
        assert capsys.readouterr().out == "called SettingsDialogGui.destroy\n"


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
        assert capsys.readouterr().out == "called Button.__init__ with args NoneType () {}\n"
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


class TestDeleteDialogGui:
    """unittests for tkgui.DeleteDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for tkgui.DeleteDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called DeleteDialogGui.__init__ with args', args)
            old_init(self, *args, **kwargs)
        def mock_bind_all(self, *args):
            print('called SettingsDialogGui.bind_all with args', args)
        monkeypatch.setattr(testee.DeleteDialogGui, '__init__', mock_init)
        monkeypatch.setattr(testee.SettingsDialogGui, 'bind_all', mock_bind_all)
        testobj = testee.DeleteDialogGui()
        assert capsys.readouterr().out == 'called DeleteDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for DeleteDialog.__init__
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            print('called Toplevel.__init__ with args', args, kwargs)
            old_init(self, *kwargs, **kwargs)
        def mock_bind(self, *args, **kwargs):
            print('called Toplevel.bind_all with args', args, kwargs)
        monkeypatch.setattr(testee.tk.Toplevel, 'bind_all', mock_bind)
        monkeypatch.setattr(testee.tk.Toplevel, '__init__', mock_init)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        maingui = types.SimpleNamespace()
        parent = types.SimpleNamespace(root='root')
        testobj = testee.DeleteDialogGui(maingui, parent)
        assert testobj.maingui == maingui
        assert testobj.parent == parent
        assert isinstance(testobj.frm, testee.ttk.Frame)
        assert capsys.readouterr().out == (
                "called Toplevel.__init__ with args ('root',) {}\n"
                "called Frame.__init__ with args DeleteDialogGui () {'padding': 10}\n"
                "called Frame.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.add_combobox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.ttk, 'Combobox', mockttk.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.textvars = {}
        result = testobj.add_combobox(['x', 'y'], callback)
        assert isinstance(result, testee.ttk.Combobox)
        assert testobj.row == 1
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'x'\n"
                "called ComboBox.__init__ with args MockFrame ()"
                f" {{'values': ['y'], 'textvariable': {result.cget('textvariable')}, 'width': 40}}\n"
                "called ComboBox.state with args (['!readonly'],)\n"
                f"called ComboBox.bind with args ('<<ComboboxSelected>>', {callback})\n"
                "called ComboBox.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n")
        result = testobj.add_combobox(['x', 'y'], callback, False)
        assert isinstance(result, testee.ttk.Combobox)
        assert testobj.row == 2
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'x'\n"
                "called ComboBox.__init__ with args MockFrame ()"
                f" {{'values': ['y'], 'textvariable': {result.cget('textvariable')}, 'width': 40}}\n"
                "called ComboBox.state with args (['readonly'],)\n"
                f"called ComboBox.bind with args ('<<ComboboxSelected>>', {callback})\n"
                "called ComboBox.grid with args ()"
                " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.add_buttonbox
        """
        def mock_get_info(text):
            "stub"
            return 0, text, 'q'
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee, 'get_shortcut_info', mock_get_info)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.add_buttonbox([('xxx', callback, True), ('yyy', callback, False)])
        assert capsys.readouterr().out == (
                # "called Frame.__init__ with args SettingsDialogGui () {'padding': 10}\n"
                "called Frame.__init__ with args MockFrame () {}\n"
                "called Frame.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'xxx', 'underline': 0, 'command': {callback}}}\n"
                "called Button.state with args (['!disabled'],)\n"
                "called Button.grid with args () {'row': 0, 'column': 0, 'sticky': ('e', 'w')}\n"
                "called Frame.columnconfigure with args (0,)\n"
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'yyy', 'underline': 0, 'command': {callback}}}\n"
                "called Button.state with args (['disabled'],)\n"
                "called Button.grid with args () {'row': 0, 'column': 1, 'sticky': ('e', 'w')}\n"
                "called Frame.columnconfigure with args (1,)\n")
                # "called SettingsDialogGui.bind_all with args ('<Alt-q>', None)\n")

    def test_get_combobox_entry(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.get_combobox_entry
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockComboBox(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called ComboBox.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widget: wvar}
        testobj.get_combobox_entry(widget)
        assert capsys.readouterr().out == "called StringVar.get\n"

    def test_set_combobox_entry(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.set_combobox_entry
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockComboBox(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called ComboBox.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widget: wvar}
        testobj.set_combobox_entry(widget, 'xxx')
        assert capsys.readouterr().out == "called StringVar.set with arg 'xxx'\n"

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.set_focus
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus(widget)
        assert capsys.readouterr().out == ("called Entry.focus_set\n")

    def test_enable_button(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.enable_button
        """
        btn = mockttk.MockButton()
        assert capsys.readouterr().out == "called Button.__init__ with args NoneType () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_button(btn, True)
        assert capsys.readouterr().out == "called Button.state with args (['!disabled'],)\n"
        testobj.enable_button(btn, False)
        assert capsys.readouterr().out == "called Button.state with args (['disabled'],)\n"

    def test_confirm(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.confirm
        """
        def mock_focus():
            print('called ShowMods.focus_set')
        def mock_destroy():
            print('called DeleteDialogGui.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.destroy = mock_destroy
        testobj.parent = types.SimpleNamespace(root=types.SimpleNamespace(focus_set=mock_focus))
        testobj.confirm()
        assert capsys.readouterr().out == ("called ShowMods.focus_set\n"
                                           "called DeleteDialogGui.destroy\n")
        testobj.parent = None
        testobj.confirm()
        assert capsys.readouterr().out == "called DeleteDialogGui.destroy\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.accept
        """
        def mock_focus():
            print('called ShowMods.focus_set')
        def mock_destroy():
            print('called DeleteDialogGui.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.destroy = mock_destroy
        testobj.parent = types.SimpleNamespace(root=types.SimpleNamespace(focus_set=mock_focus))
        testobj.accept()
        assert capsys.readouterr().out == ("called ShowMods.focus_set\n"
                                           "called DeleteDialogGui.destroy\n")
        testobj.parent = None
        testobj.accept()
        assert capsys.readouterr().out == "called DeleteDialogGui.destroy\n"


class TestAttributesDialogGui:
    """unittests for tkgui.AttributesDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for tkgui.AttributesDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called AttributesDialogGui.__init__ with args', args)
            old_init(self, *args, **kwargs)
        monkeypatch.setattr(testee.AttributesDialogGui, '__init__', mock_init)
        testobj = testee.AttributesDialogGui()
        assert capsys.readouterr().out == 'called AttributesDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for AttributesDialog.__init__
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            print('called Toplevel.__init__ with args', args, kwargs)
            old_init(self, *kwargs, **kwargs)
        monkeypatch.setattr(testee.tk.Toplevel, '__init__', mock_init)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        maingui = types.SimpleNamespace()
        parent = types.SimpleNamespace(root='root')
        testobj = testee.AttributesDialogGui(maingui, parent)
        assert testobj.maingui == maingui
        assert testobj.parent == parent
        assert isinstance(testobj.frm, testee.ttk.Frame)
        assert testobj.row == 0
        assert capsys.readouterr().out == (
                "called Toplevel.__init__ with args ('root',) {}\n"
                "called Frame.__init__ with args AttributesDialogGui () {'padding': 10}\n"
                "called Frame.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_combobox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.ttk, 'Combobox', mockttk.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.textvars = {}
        result = testobj.add_combobox(['x', 'y'], callback)
        assert isinstance(result, testee.ttk.Combobox)
        assert testobj.row == 0
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'x'\n"
                "called ComboBox.__init__ with args MockFrame ()"
                f" {{'values': ['y'], 'textvariable': {result.cget('textvariable')}}}\n"
                "called ComboBox.state with args (['!readonly', '!disabled'],)\n"
                f"called ComboBox.bind with args ('<<ComboboxSelected>>', {callback})\n"
                "called ComboBox.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n")
        result = testobj.add_combobox(['x', 'y'], callback, False, False)
        assert isinstance(result, testee.ttk.Combobox)
        assert testobj.row == 0
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'x'\n"
                "called ComboBox.__init__ with args MockFrame ()"
                f" {{'values': ['y'], 'textvariable': {result.cget('textvariable')}}}\n"
                "called ComboBox.state with args (['readonly', 'disabled'],)\n"
                f"called ComboBox.bind with args ('<<ComboboxSelected>>', {callback})\n"
                "called ComboBox.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_label
        """
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.add_label('xxx')
        assert capsys.readouterr().out == (
                "called Label.__init__ with args MockFrame () {'text': 'xxx'}\n"
                "called Label.grid with args () "
                "{'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_start_line_with_clear_button(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.istart_line_with_clear_button
        """
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.start_line_with_clear_button()
        assert isinstance(testobj.hfrm, testee.ttk.Frame)
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args MockFrame () {}\n"
                "called Frame.grid with args ()"
                " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called Frame.columnconfigure with args (0,)\n")

    def test_add_clear_button(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_clear_button
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        # wvar = mockttk.MockStringVar()
        # widget = mockttk.MockEntry(textvariable=wvar)
        # assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
        #                                    "called Entry.__init__ with args NoneType ()"
        #                                    f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hfrm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.parent = types.SimpleNamespace(ecimage='ecimage')
        testobj.row = 0
        result = testobj.add_clear_button(callback)
        assert isinstance(result, testee.ttk.Button)
        assert capsys.readouterr().out == (
                # "called Frame.__init__ with args MockFrame () {}\n"
                # "called Frame.grid with args ()"
                # " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                # "called Frame.columnconfigure with args (0,)\n"
                # "called Entry.grid with args ()"
                # " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n"
                "called Button.__init__ with args MockFrame ()"
                f" {{'image': 'ecimage', 'command': {callback}}}\n"
                "called Button.state with args (['disabled'],)\n"
                "called Button.grid with args () {'row': 0, 'column': 1, 'sticky': 'w'}\n")

    def test_add_line_entry(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_line_entry
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.ttk, 'Entry', mockttk.MockEntry)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hfrm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.textvars = {}
        result = testobj.add_line_entry('xxx', callback)
        assert isinstance(result, testee.ttk.Entry)
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'xxx'\n"
                f"called StringVar.trace_add with args ('write', {testobj.monitor_textvar})\n"
                "called Entry.__init__ with args MockFrame ()"
                f" {{'textvariable': {result.getvar(result.cget('textvariable'))}}}\n"
                "called Entry.grid with args () {'row': 0, 'column': 0, 'sticky': ('e', 'w')}\n"
                "called Entry.state with args (['!disabled'],)\n")

    def test_add_line_entry_2(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_line_entry
        """
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.ttk, 'Entry', mockttk.MockEntry)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hfrm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.textvars = {}
        result = testobj.add_line_entry('xxx', None, False)
        assert isinstance(result, testee.ttk.Entry)
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'xxx'\n"
                "called Entry.__init__ with args MockFrame ()"
                f" {{'textvariable': {testobj.textvars[result]}}}\n"
                "called Entry.grid with args () {'row': 0, 'column': 0, 'sticky': ('e', 'w')}\n"
                "called Entry.state with args (['disabled'],)\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_checkbox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.tk, 'IntVar', mockttk.MockIntVar)
        monkeypatch.setattr(testee.ttk, 'Checkbutton', mockttk.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.textvars = {}
        result = testobj.add_checkbox('xxx', callback)
        assert isinstance(result, testee.ttk.Checkbutton)
        assert testobj.textvars[result] == result.getvar(result.cget('variable'))
        assert capsys.readouterr().out == (
                "called IntVar.__init__ with args ()\n"
                "called IntVar.set with arg 0\n"
                "called CheckBox.__init__ with args MockFrame () {'text': 'xxx',"
                f" 'variable': {testobj.textvars[result]}, 'command': {callback}}}\n"
                "called CheckBox.grid with args ()"
                " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called CheckBox.state with args (['!disabled'],)\n")

    def test_add_checkbox_2(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_checkbox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.tk, 'IntVar', mockttk.MockIntVar)
        monkeypatch.setattr(testee.ttk, 'Checkbutton', mockttk.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.textvars = {}
        result = testobj.add_checkbox('xxx', callback, False)
        assert isinstance(result, testee.ttk.Checkbutton)
        assert testobj.textvars[result] == result.getvar(result.cget('variable'))
        assert capsys.readouterr().out == (
                "called IntVar.__init__ with args ()\n"
                "called IntVar.set with arg 0\n"
                "called CheckBox.__init__ with args MockFrame () {'text': 'xxx',"
                f" 'variable': {testobj.textvars[result]}, 'command': {callback}}}\n"
                "called CheckBox.grid with args ()"
                " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called CheckBox.state with args (['disabled'],)\n")

    def test_add_button(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_button
        """
        def mock_get_info(text):
            "stub"
            return 0, text, 'q'
        def callback():
            """empty stub for callback function
            """
        def mock_bind(*args):
            "stub"
            print('called AttributesDialogGui.bind with args', args)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        monkeypatch.setattr(testee, 'get_shortcut_info', mock_get_info)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.bind = mock_bind
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        result = testobj.add_button('xxx', callback)
        assert testobj.row == 1
        assert isinstance(result, testee.ttk.Button)
        assert capsys.readouterr().out == (
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'xxx', 'underline': 0, 'command': {callback}}}\n"
                "called Button.grid with args ()"
                " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called Button.state with args (['!disabled'],)\n"
                f"called AttributesDialogGui.bind with args ('Alt-q', {callback})\n")
        result = testobj.add_button('xxx', callback, enabled=False)
        assert testobj.row == 2
        assert isinstance(result, testee.ttk.Button)
        assert capsys.readouterr().out == (
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'xxx', 'underline': 0, 'command': {callback}}}\n"
                "called Button.grid with args ()"
                " {'row': 2, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called Button.state with args (['disabled'],)\n"
                f"called AttributesDialogGui.bind with args ('Alt-q', {callback})\n")
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        result = testobj.add_button('xxx', callback, pos=1)
        assert testobj.row == 3
        assert isinstance(result, testee.ttk.Button)
        assert isinstance(testobj.localbuttonbox, testee.ttk.Frame)
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args MockFrame () {}\n"
                "called Frame.grid with args ()"
                " {'row': 3, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n"
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'xxx', 'underline': 0, 'command': {callback}}}\n"
                "called Button.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called Frame.columnconfigure with args (0,)\n"
                "called Button.state with args (['!disabled'],)\n"
                f"called AttributesDialogGui.bind with args ('Alt-q', {callback})\n")
        result = testobj.add_button('xxx', callback, 2, False)
        assert testobj.row == 4
        assert isinstance(result, testee.ttk.Button)
        assert capsys.readouterr().out == (
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'xxx', 'underline': 0, 'command': {callback}}}\n"
                "called Button.grid with args ()"
                " {'row': 0, 'column': 1, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called Frame.columnconfigure with args (1,)\n"
                "called Button.state with args (['disabled'],)\n"
                f"called AttributesDialogGui.bind with args ('Alt-q', {callback})\n")

    def test_add_menubutton(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_button
        """
        def mock_get_info(text):
            "stub"
            return 0, text, 'q'
        def callback1():
            """empty stub for callback function
            """
        def callback2():
            """empty stub for callback function
            """
        def mock_bind(*args):
            "stub"
            print('called AttributesDialogGui.bind with args', args)
        monkeypatch.setattr(testee.tk, 'Menubutton', mockttk.MockMenubutton)
        monkeypatch.setattr(testee.tk, 'Menu', mockttk.MockMenu)
        monkeypatch.setattr(testee, 'get_shortcut_info', mock_get_info)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.bind = mock_bind
        testobj.localbuttonbox = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        result = testobj.add_menubutton('xxx', ['xxx', 'yyy'], [callback1, callback2], 2)
        assert isinstance(result, testee.tk.Menubutton)
        assert capsys.readouterr().out == (
                "called Menubutton.__init__ with args MockFrame ()"
                " {'text': 'xxx', 'underline': 0}\n"
                "called Menubutton.configure with args {'relief': 'raised'}\n"
                "called Menubutton.grid with args ()"
                " {'row': 0, 'column': 1, 'sticky': ('n', 'e', 's', 'w')}\n"
                "called Frame.columnconfigure with args (1,)\n"
                "called Menu.__init__ with args MockMenubutton () {}\n"
                f"called Menubutton.configure with args {{'menu': {result.menu}}}\n"
                f"called Menu.add_command with args () {{'label': 'xxx', 'command': {callback1}}}\n"
                f"called Menu.add_command with args () {{'label': 'yyy', 'command': {callback2}}}\n"
                "called Menubutton.configure with args {'state': 'normal'}\n")
        result = testobj.add_menubutton('xxx', ['xxx', 'yyy'], [callback1, callback2], 1,
                                        enabled=False)
        assert isinstance(result, testee.tk.Menubutton)
        assert capsys.readouterr().out == (
                "called Menubutton.__init__ with args MockFrame ()"
                " {'text': 'xxx', 'underline': 0}\n"
                "called Menubutton.configure with args {'relief': 'raised'}\n"
                "called Menubutton.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n"
                "called Frame.columnconfigure with args (0,)\n"
                "called Menu.__init__ with args MockMenubutton () {}\n"
                f"called Menubutton.configure with args {{'menu': {result.menu}}}\n"
                f"called Menu.add_command with args () {{'label': 'xxx', 'command': {callback1}}}\n"
                f"called Menu.add_command with args () {{'label': 'yyy', 'command': {callback2}}}\n"
                "called Menubutton.configure with args {'state': 'disabled'}\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_buttonbox
        """
        def mock_get_info(text):
            "stub"
            return 0, text, 'q'
        def callback():
            """empty stub for callback function
            """
        def mock_bind(*args):
            "stub"
            print('called AttributesDialogGui.bind with args', args)
        monkeypatch.setattr(testee, 'get_shortcut_info', mock_get_info)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.bind = mock_bind
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.add_buttonbox([('xxx', callback, 'value')])
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args MockFrame () {}\n"
                "called Frame.grid with args ()"
                " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'xxx', 'underline': 0, 'command': {callback}}}\n"
                "called Button.state with args (['!disabled'],)\n"
                "called Button.grid with args () {'row': 0, 'column': 0, 'sticky': ('e', 'w')}\n"
                "called Frame.columnconfigure with args (0,)\n"
                f"called AttributesDialogGui.bind with args ('Alt-q', {callback})\n"
                f"called AttributesDialogGui.bind with args ('<Escape>', {testobj.close})\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.set_focus
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus(widget)
        assert capsys.readouterr().out == ("called Entry.focus_set\n")

    def test_monitor_textvar(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.monitor_textvar
        """
        def mock_enable():
            print('called AttributesDialog.enable_change')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.maingui = types.SimpleNamespace(enable_change=mock_enable)
        testobj.monitor_textvar()
        assert capsys.readouterr().out == ("called AttributesDialog.enable_change\n")

    def test_enable_button(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.enable_button
        """
        monkeypatch.setattr(testee.tk, 'Menubutton', mockttk.MockMenubutton)
        button = mockttk.MockButton()
        button2 = mockttk.MockMenubutton()
        assert capsys.readouterr().out == ("called Button.__init__ with args NoneType () {}\n"
                                           "called Menubutton.__init__ with args NoneType () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_button(button, False)
        assert capsys.readouterr().out == "called Button.state with args (['disabled'],)\n"
        testobj.enable_button(button, True)
        assert capsys.readouterr().out == "called Button.state with args (['!disabled'],)\n"
        testobj.enable_button(button2, False)
        assert capsys.readouterr().out == (
                "called Menubutton.configure with args {'state': 'disabled'}\n")
        testobj.enable_button(button2, True)
        assert capsys.readouterr().out == (
                "called Menubutton.configure with args {'state': 'normal'}\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.get_combobox_value
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockComboBox(textvariable=wvar)
        wvar.set('x')
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called ComboBox.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n"
                                           "called StringVar.set with arg 'x'\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widget: wvar}
        assert testobj.get_combobox_value(widget) == 'x'
        assert capsys.readouterr().out == "called StringVar.get\n"

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.get_checkbox_value
        """
        wvar = mockttk.MockIntVar()
        widget = mockttk.MockCheckBox(variable=wvar)
        wvar.set(1)
        assert capsys.readouterr().out == ("called IntVar.__init__ with args ()\n"
                                           "called CheckBox.__init__ with args NoneType ()"
                                           f" {{'variable': {wvar}}}\n"
                                           "called IntVar.set with arg 1\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widget: wvar}
        assert testobj.get_checkbox_value(widget) == 1
        assert capsys.readouterr().out == "called IntVar.get\n"

    def test_get_field_text(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.get_field_text
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        wvar.set('x')
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n"
                                           "called StringVar.set with arg 'x'\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widget: wvar}
        assert testobj.get_field_text(widget) == 'x'
        assert capsys.readouterr().out == "called StringVar.get\n"

    def _test_reset_all_fields(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.reset_all_fields
        """
        # niet geïmplementeerd, dus geen unittest

    def test_activate_and_populate_fields(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.activate_and_populate_fields
        """
        uvar = mockttk.MockStringVar()
        wvar = mockttk.MockStringVar()
        xvar = mockttk.MockIntVar()
        yvar = mockttk.MockIntVar()
        field_list = (mockttk.MockComboBox(), mockttk.MockButton(),
                      mockttk.MockEntry(textvariable=wvar), mockttk.MockButton(),
                      mockttk.MockCheckBox(textvariable=xvar),
                      mockttk.MockCheckBox(textvariable=yvar),
                      mockttk.MockButton(), mockttk.MockButton(), mockttk.MockButton(),
                      mockttk.MockButton(), mockttk.MockButton(), mockttk.MockButton())
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called StringVar.__init__ with args ()\n"
                                           "called IntVar.__init__ with args ()\n"
                                           "called IntVar.__init__ with args ()\n"
                                           "called ComboBox.__init__ with args NoneType () {}\n"
                                           "called StringVar.__init__ with args ()\n"
                                           "called Button.__init__ with args NoneType () {}\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n"
                                           "called Button.__init__ with args NoneType () {}\n"
                                           "called CheckBox.__init__ with args NoneType ()"
                                           f" {{'textvariable': {xvar}}}\n"
                                           "called StringVar.__init__ with args ()\n"
                                           "called CheckBox.__init__ with args NoneType ()"
                                           f" {{'textvariable': {yvar}}}\n"
                                           "called StringVar.__init__ with args ()\n"
                                           "called Button.__init__ with args NoneType () {}\n"
                                           "called Button.__init__ with args NoneType () {}\n"
                                           "called Button.__init__ with args NoneType () {}\n"
                                           "called Button.__init__ with args NoneType () {}\n"
                                           "called Button.__init__ with args NoneType () {}\n"
                                           "called Button.__init__ with args NoneType () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {field_list[0]: uvar, field_list[2]: wvar, field_list[4]: xvar,
                            field_list[5]: yvar}
        testobj.activate_and_populate_fields(field_list, ['x'], {'txt': 'TXT', 'sel': 'SEL',
                                                                 'opt': 'OPT'})
        assert capsys.readouterr().out == ("called ComboBox.configure with args {'values': ['x']}\n"
                                           "called StringVar.set with arg 'x'\n"
                                           "called ComboBox.state with args (['!disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           # f"called Entry.setvar with args {wvar}, TXT\n"
                                           # f"called Entry.getvar with arg {wvar}\n"
                                           "called StringVar.set with arg 'TXT'\n"
                                           "called Entry.state with args (['!disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           # f"called CheckBox.setvar with args {xvar}, SEL\n"
                                           # f"called CheckBox.getvar with arg {xvar}\n"
                                           "called IntVar.set with arg SEL\n"
                                           "called CheckBox.state with args (['!disabled'],)\n"
                                           # f"called CheckBox.setvar with args {yvar}, OPT\n"
                                           # f"called CheckBox.getvar with arg {yvar}\n"
                                           "called IntVar.set with arg OPT\n"
                                           "called CheckBox.state with args (['!disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           "called Button.state with args (['disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           "called Button.state with args (['!disabled'],)\n"
                                           "called Button.configure with args {'state': 'normal'}\n")

    def test_clear_field(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.clear_field
        """
        wvar = mockttk.MockStringVar()
        field = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {field: wvar}
        testobj.clear_field(field)
        assert capsys.readouterr().out == "called StringVar.set with arg ''\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for AttributesDilaog.accept
        """
        def mock_set():
            print('called ShowMods.root.focus_set')
        def mock_destroy():
            print('called AttributesDialog.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.destroy = mock_destroy
        testobj.parent = None
        testobj.accept()
        assert capsys.readouterr().out == "called AttributesDialog.destroy\n"
        testobj.parent = types.SimpleNamespace(root=types.SimpleNamespace(focus_set=mock_set))
        testobj.accept()
        assert capsys.readouterr().out == ("called ShowMods.root.focus_set\n"
                                           "called AttributesDialog.destroy\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for AttributesDilaog.close
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


class TestRestoreDialogGui:
    """unittests for qtgui.RestoreDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.RestoreDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            print('called RestoreDialogGui.__init__ with args', args)
            old_init(self, *args, **kwargs)
        monkeypatch.setattr(testee.RestoreDialogGui, '__init__', mock_init)
        testobj = testee.RestoreDialogGui()
        assert capsys.readouterr().out == 'called RestoreDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for RestoreDialog.__init__
        """
        def mock_init(self, *args, **kwargs):
            print('called Toplevel.__init__ with args', args, kwargs)
        monkeypatch.setattr(testee.tk.Toplevel, '__init__', mock_init)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        testobj = testee.RestoreDialogGui('maingui', 'parent')
        assert testobj.parent == 'parent'
        assert testobj.maingui == 'maingui'
        assert isinstance(testobj.frm, testee.ttk.Frame)
        assert testobj.row == 0
        assert testobj.textvars == {}
        assert capsys.readouterr().out == (
            "called Toplevel.__init__ with args ('parent',) {}\n"
            "called Frame.__init__ with args RestoreDialogGui () {'padding': 10}\n"
            "called Frame.grid with args () {'row': 0, 'column': 0,"
            " 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for RestoreDialogGui.add_checkbox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.tk, 'IntVar', mockttk.MockIntVar)
        monkeypatch.setattr(testee.ttk, 'Checkbutton', mockttk.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.textvars = {}
        result = testobj.add_checkbox('&xxx', callback)
        assert isinstance(result, testee.ttk.Checkbutton)
        assert testobj.textvars[result] == result.getvar(result.cget('variable'))
        assert capsys.readouterr().out == (
                "called IntVar.__init__ with args ()\n"
                "called IntVar.set with arg 0\n"
                "called CheckBox.__init__ with args MockFrame () {'text': 'xxx',"
                f" 'variable': {testobj.textvars[result]}, 'underline': 0, 'command': {callback}}}\n"
                "called CheckBox.grid with args ()"
                " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called CheckBox.state with args (['!disabled'],)\n")

    def test_add_checkbox_2(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_checkbox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.tk, 'IntVar', mockttk.MockIntVar)
        monkeypatch.setattr(testee.ttk, 'Checkbutton', mockttk.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.textvars = {}
        result = testobj.add_checkbox('&xxx', callback, False)
        assert isinstance(result, testee.ttk.Checkbutton)
        assert testobj.textvars[result] == result.getvar(result.cget('variable'))
        assert capsys.readouterr().out == (
                "called IntVar.__init__ with args ()\n"
                "called IntVar.set with arg 0\n"
                "called CheckBox.__init__ with args MockFrame () {'text': 'xxx',"
                f" 'variable': {testobj.textvars[result]}, 'underline': 0, 'command': {callback}}}\n"
                "called CheckBox.grid with args ()"
                " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called CheckBox.state with args (['disabled'],)\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for RestoreDialogGui.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        wvar = mockttk.MockIntVar()
        widget = mockttk.MockCheckBox(variable=wvar)
        wvar.set(1)
        assert capsys.readouterr().out == ("called IntVar.__init__ with args ()\n"
                                           "called CheckBox.__init__ with args NoneType ()"
                                           f" {{'variable': {wvar}}}\n"
                                           "called IntVar.set with arg 1\n")
        testobj.textvars = {widget: wvar}
        assert testobj.get_checkbox_value(widget) == 1
        assert capsys.readouterr().out == "called IntVar.get\n"

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for RestoreDialogGui.add_buttonbox
        """
        def mock_get_info(text):
            "stub"
            return 0, text, 'q'
        def callback():
            """empty stub for callback function
            """
        def mock_bind(*args):
            print('called RestoreDialogGui.bind with args', args)
        monkeypatch.setattr(testee, 'get_shortcut_info', mock_get_info)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.bind = mock_bind
        testobj.add_buttonbox([('xxx', callback())])
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args RestoreDialogGui () {'padding': 10}\n"
                "called Frame.grid with args () {'row': 1, 'column': 0}\n"
                "called Button.__init__ with args MockFrame ()"
                " {'text': 'xxx', 'underline': 0, 'command': None}\n"
                "called Button.grid with args () {'row': 0, 'column': 0}\n"
                "called RestoreDialogGui.bind with args ('<Alt-q>', None)\n"
                f"called RestoreDialogGui.bind with args ('<Escape>', {testobj.confirm})\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for RestoreDialogGui.set_focus
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus(widget)
        assert capsys.readouterr().out == ("called Entry.focus_set\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for RestoreDialogGui.confirm
        """
        def mock_focus():
            print('called ShowMods.focus_set')
        def mock_destroy():
            print('called RestoreDialogGui.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.destroy = mock_destroy
        testobj.parent = types.SimpleNamespace(focus_set=mock_focus)
        testobj.confirm()
        assert capsys.readouterr().out == ("called ShowMods.focus_set\n"
                                           "called RestoreDialogGui.destroy\n")
        testobj.parent = None
        testobj.confirm()
        assert capsys.readouterr().out == "called RestoreDialogGui.destroy\n"

    def test_reject(self, monkeypatch, capsys):
        """unittest for RestoreDialogGui.confirm
        """
        def mock_focus():
            print('called ShowMods.focus_set')
        def mock_destroy():
            print('called RestoreDialogGui.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.destroy = mock_destroy
        testobj.parent = types.SimpleNamespace(focus_set=mock_focus)
        testobj.reject()
        assert capsys.readouterr().out == ("called ShowMods.focus_set\n"
                                           "called RestoreDialogGui.destroy\n")
        testobj.parent = None
        testobj.reject()
        assert capsys.readouterr().out == "called RestoreDialogGui.destroy\n"


class TestDependencyDialogGui:
    """unittests for qtgui.DependencyDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.DependencyDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            print('called DependencyDialogGui.__init__ with args', args)
            old_init(self, *args, **kwargs)
        monkeypatch.setattr(testee.DependencyDialogGui, '__init__', mock_init)
        testobj = testee.DependencyDialogGui()
        assert capsys.readouterr().out == 'called DependencyDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for DeleteDialog.__init__
        """
        # old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            print('called Toplevel.__init__ with args', args, kwargs)
        monkeypatch.setattr(testee.tk.Toplevel, '__init__', mock_init)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        maingui = types.SimpleNamespace()
        parent = types.SimpleNamespace(root='root')
        testobj = testee.DependencyDialogGui(maingui, parent)
        assert testobj.maingui == maingui
        assert testobj.parent == parent
        assert isinstance(testobj.frm, testee.ttk.Frame)
        assert testobj.row == 0
        assert capsys.readouterr().out == (
                "called Toplevel.__init__ with args (namespace(root='root'),) {}\n"
                "called Frame.__init__ with args DependencyDialogGui () {'padding': 10}\n"
                "called Frame.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.add_label
        """
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.add_label('xxx')
        assert capsys.readouterr().out == (
                "called Label.__init__ with args MockFrame () {'text': 'xxx'}\n"
                "called Label.grid with args () "
                "{'row': 1, 'column': 0, 'sticky': 'w'}\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.add_combobox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.ttk, 'Combobox', mockttk.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.textvars = {}
        result = testobj.add_combobox(['x', 'y'], callback)
        assert isinstance(result, testee.ttk.Combobox)
        assert testobj.row == 1
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'x'\n"
                "called ComboBox.__init__ with args MockFrame ()"
                f" {{'values': ['y'], 'textvariable': {result.cget('textvariable')}}}\n"
                "called ComboBox.state with args (['!readonly', '!disabled'],)\n"
                f"called ComboBox.bind with args ('<<ComboboxSelected>>', {callback})\n"
                "called ComboBox.grid with args () {'row': 1, 'column': 0,"
                " 'sticky': ('n', 'e', 's', 'w')}\n")
        result = testobj.add_combobox(['x', 'y'], callback, False, False)
        assert isinstance(result, testee.ttk.Combobox)
        assert testobj.row == 2
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'x'\n"
                "called ComboBox.__init__ with args MockFrame ()"
                f" {{'values': ['y'], 'textvariable': {result.cget('textvariable')}}}\n"
                "called ComboBox.state with args (['readonly', 'disabled'],)\n"
                f"called ComboBox.bind with args ('<<ComboboxSelected>>', {callback})\n"
                "called ComboBox.grid with args () {'row': 2, 'column': 0,"
                " 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_set_field_enabled(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.set_field_enabled
        """
        button = mockttk.MockButton()
        assert capsys.readouterr().out == "called Button.__init__ with args NoneType () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_field_enabled(button, False)
        assert capsys.readouterr().out == "called Button.state with args (['disabled'],)\n"
        testobj.set_field_enabled(button, True)
        assert capsys.readouterr().out == "called Button.state with args (['!disabled'],)\n"

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.add_buttonbox
        """
        def mock_get_info(text):
            "stub"
            return 0, text, 'q'
        def callback():
            """empty stub for callback function
            """
        def mock_bind(*args):
            print('called DependencyDialogGui.bind with args', args)
        monkeypatch.setattr(testee, 'get_shortcut_info', mock_get_info)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.bind = mock_bind
        testobj.add_buttonbox([('xxx', callback())])
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args DependencyDialogGui () {'padding': 10}\n"
                "called Frame.grid with args () {'row': 1, 'column': 0}\n"
                "called Button.__init__ with args MockFrame ()"
                " {'text': 'xxx', 'underline': 0, 'command': None}\n"
                "called Button.grid with args () {'row': 0, 'column': 0}\n"
                "called DependencyDialogGui.bind with args ('<Alt-q>', None)\n"
                f"called DependencyDialogGui.bind with args ('<Escape>', {testobj.confirm})\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.set_focus
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus(widget)
        assert capsys.readouterr().out == ("called Entry.focus_set\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.get_combobox_value
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockComboBox(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called ComboBox.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widget: wvar}
        testobj.get_combobox_value(widget)
        assert capsys.readouterr().out == ("called StringVar.get\n")

    def test_reject(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.confirm
        """
        def mock_focus():
            print('called ShowMods.focus_set')
        def mock_destroy():
            print('called DependencyDialogGui.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.destroy = mock_destroy
        testobj.parent = types.SimpleNamespace(focus_set=mock_focus)
        testobj.reject()
        assert capsys.readouterr().out == ("called ShowMods.focus_set\n"
                                           "called DependencyDialogGui.destroy\n")
        testobj.parent = None
        testobj.reject()
        assert capsys.readouterr().out == "called DependencyDialogGui.destroy\n"

    def test_confirm(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.confirm
        """
        def mock_focus():
            print('called ShowMods.focus_set')
        def mock_destroy():
            print('called DependencyDialogGui.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.destroy = mock_destroy
        testobj.parent = types.SimpleNamespace(focus_set=mock_focus)
        testobj.confirm()
        assert capsys.readouterr().out == ("called ShowMods.focus_set\n"
                                           "called DependencyDialogGui.destroy\n")
        testobj.parent = None
        testobj.confirm()
        assert capsys.readouterr().out == "called DependencyDialogGui.destroy\n"


class TestSaveGamesDialogGui:
    """unittests for tkgui.SaveGamesDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for tkgui.SaveGamesDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called SaveGamesDialogGui.__init__ with args', args)
            old_init(self, *args, **kwargs)
        monkeypatch.setattr(testee.SaveGamesDialogGui, '__init__', mock_init)
        testobj = testee.SaveGamesDialogGui()
        assert capsys.readouterr().out == 'called SaveGamesDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.__init__
        """
        old_init = testee.tk.Toplevel.__init__
        def mock_init(self, *args, **kwargs):
            print('called Toplevel.__init__ with args', args, kwargs)
            old_init(self, *kwargs, **kwargs)
        monkeypatch.setattr(testee.tk.Toplevel, '__init__', mock_init)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        maingui = types.SimpleNamespace()
        parent = types.SimpleNamespace(root='root')
        testobj = testee.SaveGamesDialogGui(maingui, parent)
        assert testobj.maingui == maingui
        assert testobj.parent == parent
        assert isinstance(testobj.frm, testee.ttk.Frame)
        assert capsys.readouterr().out == (
                "called Toplevel.__init__ with args ('root',) {}\n"
                "called Frame.__init__ with args SaveGamesDialogGui () {'padding': 10}\n"
                "called Frame.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.add_combobox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.ttk, 'Combobox', mockttk.MockComboBox)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.msrow = 1
        testobj.msfrm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.textvars = {}
        result = testobj.add_combobox(['x', 'y'], callback)
        assert isinstance(result, testee.ttk.Combobox)
        assert testobj.row == 0
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'x'\n"
                "called ComboBox.__init__ with args MockFrame ()"
                f" {{'values': ['y'], 'textvariable': {result.cget('textvariable')}}}\n"
                "called ComboBox.state with args (['!readonly', '!disabled'],)\n"
                "called ComboBox.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n"
                f"called ComboBox.bind with args ('<<ComboboxSelected>>', {callback})\n")
        result = testobj.add_combobox(['x', 'y'], None, False)
        assert isinstance(result, testee.ttk.Combobox)
        assert testobj.row == 0
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        testobj.textvars = {}
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args MockFrame () {'padding': 10}\n"
                "called Frame.grid with args () {'row': 1, 'column': 0,"
                " 'sticky': ('n', 'e', 's', 'w')}\n"
                'called Frame.columnconfigure with args (0,)\n'
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'select a mod'\n"
                "called ComboBox.__init__ with args MockFrame ()"
                f" {{'values': ['x', 'y'], 'textvariable': {result.cget('textvariable')}}}\n"
                "called ComboBox.state with args (['readonly', '!disabled'],)\n"
                "called ComboBox.grid with args ()"
                " {'row': 0, 'column': 0, 'sticky': ('n', 'e', 's', 'w')}\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.get_combobox_value
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockComboBox(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called ComboBox.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widget: wvar}
        testobj.get_combobox_value(widget)
        assert capsys.readouterr().out == "called StringVar.get\n"

    def test_set_combobox_value(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.set_combobox_value
        """
        def mock_process(*args):
            print('called SaveGamesDialog.process_mod with args', args)
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockComboBox(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called ComboBox.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.maingui = types.SimpleNamespace(process_mod=mock_process)
        testobj.textvars = {widget: wvar}
        testobj.set_combobox_value(widget, 'xxx')
        assert capsys.readouterr().out == (
                "called StringVar.set with arg 'xxx'\n"
                f"called SaveGamesDialog.process_mod with args ({widget}, 'xxx')\n"
                "called ComboBox.state with args (['!disabled'],)\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.add_label
        """
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.add_label('xxx')
        assert isinstance(testobj.hfrm, mockttk.MockFrame)
        assert testobj.hrow == 0
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args MockFrame () {}\n"
                "called Frame.grid with args ()"
                " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called Frame.columnconfigure with args (1,)\n"
                "called Label.__init__ with args MockFrame () {'text': 'xxx'}\n"
                "called Label.grid with args () {'row': 0, 'column': 0}\n")
        testobj.row = 0
        testobj.add_label('xxx')
        assert capsys.readouterr().out == (
                "called Label.__init__ with args MockFrame () {'text': 'xxx'}\n"
                "called Label.grid with args () {'row': 0, 'column': 0}\n")

    def test_add_line_entry(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.add_line_entry
        """
        monkeypatch.setattr(testee.tk, 'StringVar', mockttk.MockStringVar)
        monkeypatch.setattr(testee.ttk, 'Entry', mockttk.MockEntry)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hfrm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.hrow = 0
        testobj.textvars = {}
        result = testobj.add_line_entry('xxx')
        assert isinstance(result, testee.ttk.Entry)
        assert testobj.textvars[result] == result.getvar(result.cget('textvariable'))
        assert capsys.readouterr().out == (
                "called StringVar.__init__ with args ()\n"
                "called StringVar.set with arg 'xxx'\n"
                "called Entry.__init__ with args MockFrame ()"
                f" {{'textvariable': {result.getvar(result.cget('textvariable'))}}}\n"
                "called Entry.state with args (['readonly'],)\n"
                "called Entry.grid with args () {'row': 0, 'column': 1}\n")

    def test_get_field_text(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.get_field_text
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        # breakpoint()
        testobj.textvars = {widget: wvar}
        testobj.get_field_text(widget)
        assert capsys.readouterr().out == "called StringVar.get\n"

    def test_set_field_text(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.set_field_text
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widget: wvar}
        testobj.set_field_text(widget, 'xxx')
        assert capsys.readouterr().out == "called StringVar.set with arg 'xxx'\n"

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.add_buttonbox
        """
        def mock_get_info(text):
            "stub"
            return 0, text, 'q'
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee, 'get_shortcut_info', mock_get_info)
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        result = testobj.add_buttonbox([('xxx', callback, True), ('yyy', callback, False)])
        assert isinstance(result[0], testee.ttk.Button)
        assert isinstance(result[1], testee.ttk.Button)
        assert capsys.readouterr().out == (
                "called Frame.__init__ with args MockFrame () {}\n"
                "called Frame.grid with args ()"
                " {'row': 1, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'xxx', 'underline': 0, 'command': {callback}}}\n"
                "called Button.state with args (['!disabled'],)\n"
                "called Button.grid with args () {'row': 0, 'column': 0, 'sticky': ('e', 'w')}\n"
                # "called SettingsDialogGui.bind_all with args ('<Alt-q>', None)\n"
                "called Frame.columnconfigure with args (0,)\n"
                "called Button.__init__ with args MockFrame ()"
                f" {{'text': 'yyy', 'underline': 0, 'command': {callback}}}\n"
                "called Button.state with args (['disabled'],)\n"
                "called Button.grid with args () {'row': 0, 'column': 1, 'sticky': ('e', 'w')}\n"
                # "called SettingsDialogGui.bind_all with args ('<Alt-q>', None)\n"
                "called Frame.columnconfigure with args (1,)\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.set_focus
        """
        wvar = mockttk.MockStringVar()
        widget = mockttk.MockEntry(textvariable=wvar)
        assert capsys.readouterr().out == ("called StringVar.__init__ with args ()\n"
                                           "called Entry.__init__ with args NoneType ()"
                                           f" {{'textvariable': {wvar}}}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus(widget)
        assert capsys.readouterr().out == ("called Entry.focus_set\n")

    def test_start_modselect_block(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.start_modselect_block
        """
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Label', mockttk.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.row = 0
        testobj.start_modselect_block('xxx')
        assert testobj.row == 2
        assert isinstance(testobj.msfrm, testee.ttk.Frame)
        assert testobj.msrow == 0
        assert capsys.readouterr().out == (
                "called Label.__init__ with args MockFrame () {'text': 'xxx'}\n"
                "called Label.grid with args () {'row': 1, 'column': 0, 'sticky': 'w'}\n"
                "called Frame.__init__ with args MockFrame () {}\n"
                "called Frame.grid with args ()"
                " {'row': 2, 'column': 0, 'sticky': ('n', 'e', 's', 'w'), 'pady': 2}\n"
                "called Frame.columnconfigure with args (0,)\n")

    def test_add_clear_button(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.add_clear_button
        """
        monkeypatch.setattr(testee.ttk, 'Frame', mockttk.MockFrame)
        monkeypatch.setattr(testee.ttk, 'Button', mockttk.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hmsfrm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.parent = types.SimpleNamespace(ecimage='ecimage')
        testobj.msrow = 0
        result = testobj.add_clear_button(True)
        assert isinstance(result[0], testee.ttk.Button)
        assert isinstance(result[1], testee.ttk.Frame)
        assert testobj.msrow == 1
        assert capsys.readouterr().out == (
                "called Button.__init__ with args MockFrame () {'image': 'ecimage'}\n"
                "called Button.state with args (['!disabled'],)\n"
                "called Button.grid with args () {'row': 0, 'column': 1}\n")
        result = testobj.add_clear_button(False)
        assert isinstance(result[0], testee.ttk.Button)
        assert isinstance(result[1], testee.ttk.Frame)
        assert testobj.msrow == 2
        assert capsys.readouterr().out == (
                "called Button.__init__ with args MockFrame () {'image': 'ecimage'}\n"
                "called Button.state with args (['disabled'],)\n"
                "called Button.grid with args () {'row': 0, 'column': 1}\n")
        assert testobj.msrow == 2

    def test_set_callbacks(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.set_callbacks
        """
        def callback1():
            """empty stub for callback function
            """
        def callback2():
            """empty stub for callback function
            """
        widgets = (mockttk.MockComboBox(), mockttk.MockButton(), mockttk.MockFrame())
        assert capsys.readouterr().out == ("called ComboBox.__init__ with args NoneType () {}\n"
                                           "called StringVar.__init__ with args ()\n"
                                           "called Button.__init__ with args NoneType () {}\n"
                                           "called Frame.__init__ with args NoneType () {}\n")
        callbacks = (callback1, callback2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_callbacks(widgets, callbacks)
        assert capsys.readouterr().out == (
                f"called ComboBox.bind with args ('<<ComboboxSelected>>', {callback1})\n"
                f"called Button.bind with args ('<Return>', {callback2})\n")

    def test_enable_widget(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.enable_widget
        """
        btn = mockttk.MockButton()
        assert capsys.readouterr().out == "called Button.__init__ with args NoneType () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_widget(btn, True)
        assert capsys.readouterr().out == "called Button.state with args (['!disabled'],)\n"
        testobj.enable_widget(btn, False)
        assert capsys.readouterr().out == "called Button.state with args (['disabled'],)\n"

    def test_remove_modselector(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.remove_modselector
        """
        widgets = (mockttk.MockComboBox(), mockttk.MockButton(), mockttk.MockFrame())
        assert capsys.readouterr().out == ("called ComboBox.__init__ with args NoneType () {}\n"
                                           "called StringVar.__init__ with args ()\n"
                                           "called Button.__init__ with args NoneType () {}\n"
                                           "called Frame.__init__ with args NoneType () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textvars = {widgets[1]: 'xxx'}
        testobj.remove_modselector(widgets)
        assert testobj.textvars == {}
        assert capsys.readouterr().out == ("called ComboBox.forget\n"
                                           "called ComboBox.destroy\n"
                                           "called Button.forget\n"
                                           "called Button.destroy\n"
                                           "called Frame.forget\n"
                                           "called Frame.destroy\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.accept
        """
        def mock_focus():
            print('called ShowMods.focus_set')
        def mock_destroy():
            print('called DeleteDialogGui.destroy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockttk.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__ with args NoneType () {}\n"
        testobj.destroy = mock_destroy
        testobj.parent = types.SimpleNamespace(root=types.SimpleNamespace(focus_set=mock_focus))
        testobj.accept()
        assert capsys.readouterr().out == ("called ShowMods.focus_set\n"
                                           "called DeleteDialogGui.destroy\n")
        testobj.parent = None
        testobj.accept()
        assert capsys.readouterr().out == "called DeleteDialogGui.destroy\n"
