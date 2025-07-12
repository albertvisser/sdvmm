"""unittests for ./qtgui.py
"""
import types
import mockgui.mockqtwidgets as mockqtw
from src import qtgui as testee


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
    def refresh_widget_data(self):
        """stub
        """
        print('called Manager.refresh_widget_data')
    def build_link_text(self, *args):
        """stub
        """
        print('called Manager.build_link_text with args', args)
        return ''.join(args)
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


def test_show_message(monkeypatch, capsys):
    """unittest for qtgui.show_message
    """
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testee.show_message('win', "hello world!")
    assert capsys.readouterr().out == (
            "called MessageBox.information with args `win` `SDVMM` `hello world!`\n")
    testee.show_message('win', "hello world!", 'title')
    assert capsys.readouterr().out == (
            "called MessageBox.information with args `win` `title` `hello world!`\n")


def test_show_dialog(capsys):
    """unittest for qtgui.show_dialog
    """
    class MockDialog:
        "testdouble for Dialog class"
        def __init__(self, *args, **kwargs):
            print('called Dialog.__init__ with args', args, kwargs)
            self.doit = MockDialogGui(*args, **kwargs)
    class MockDialog2:
        "testdouble for Dialog class"
        def __init__(self, *args, **kwargs):
            print('called Dialog.__init__ with args', args, kwargs)
            self.doit = MockDialog2Gui(*args, **kwargs)
    class MockDialogGui:
        "stub for DialogGui class"
        def __init__(self, *args, **kwargs):
            print('called DialogGui.__init__ with args', args, kwargs)
        def exec(self):
            print('called DialogGui.exec')
            return testee.qtw.QDialog.DialogCode.Rejected
    class MockDialog2Gui:
        "stub for DialogGui class"
        def __init__(self, *args, **kwargs):
            print('called DialogGui.__init__ with args', args, kwargs)
        def exec(self):
            print('called DialogGui.exec')
            return testee.qtw.QDialog.DialogCode.Accepted
    parent = types.SimpleNamespace()
    cls = MockDialog
    modnames = ['x', 'y']
    # assert testee.show_dialog(cls, parent, modnames, True) == (False, {'mods': [], 'deps': {},
    #                                                                    'set_active': []})
    assert not testee.show_dialog(cls, parent, modnames, True)
    assert capsys.readouterr().out == (
        "called Dialog.__init__ with args (namespace(), ['x', 'y'], True) {}\n"
        "called DialogGui.__init__ with args (namespace(), ['x', 'y'], True) {}\n"
        "called DialogGui.exec\n")
    cls = MockDialog2
    # assert testee.show_dialog(cls, parent, modnames, False) == (True, {'mods': [], 'deps': {},
    #                                                                    'set_active': []})
    assert testee.show_dialog(cls, parent, modnames, False)
    assert capsys.readouterr().out == (
        "called Dialog.__init__ with args (namespace(), ['x', 'y'], False) {}\n"
        "called DialogGui.__init__ with args (namespace(), ['x', 'y'], False) {}\n"
        "called DialogGui.exec\n")


class TestShowMods:
    """unittest for qtgui.ShowMods
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.ShowMods object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_app_init(self, *args):
            """stub
            """
            print('called QApplication.__init__()')
        def mock_init(self, *args):
            """stub
            """
            print('called ShowMods.__init__()')
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_app_init)
        monkeypatch.setattr(testee.ShowMods, '__init__', mock_init)
        testobj = testee.ShowMods(MockManager())
        assert capsys.readouterr().out == (
            # 'called QApplication.__init__()\n'
            'called ShowMods.__init__()\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ShowMods.__init__
        """
        def mock_app_init(self, *args):
            """stub
            """
            print('called QApplication.__init__()')
        def mock_init(self, *args):
            """stub
            """
            print('called QWidget.__init__()')
        # def mock_setup(self, *args):
        #     print('called ShowMods.setup_screen()')
        # def mock_show(self, *args):
        #     """stub
        #     """
        #     print('called ShowMods.show_screen()')
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_app_init)
        monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QWidget, 'setWindowTitle', mockqtw.MockWidget.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mockqtw.MockWidget.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        master = types.SimpleNamespace()
        testobj = testee.ShowMods(master)
        assert isinstance(testobj, testee.qtw.QWidget)
        assert testobj.master == master
        # assert testobj.filenames == ['file', 'name']
        assert hasattr(testobj, 'app')
        assert isinstance(testobj.app, testee.qtw.QApplication)
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert testobj.buttons == {}
        assert capsys.readouterr().out == (
            'called QApplication.__init__()\n'
            'called QWidget.__init__()\n'
            "called Widget.setWindowTitle with arg `SDV Mod Manager`\n"
            "called VBox.__init__\n"
            'called Widget.setLayout\n')

    def test_create_selectables_title(self, monkeypatch, capsys):
        """unittest for ShowMods.create_selectables_title
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.create_selectables_title('xxxx')
        assert capsys.readouterr().out == ("called Label.__init__ with args ('xxxx',)\n"
                                           "called VBox.addWidget with arg MockLabel\n")

    def test_create_selectables_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.create_selectables_grid
        """
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.create_selectables_grid()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called VBox.addLayout with arg MockGridLayout\n")

    def test_create_dependencies_title(self, monkeypatch, capsys):
        """unittest for ShowMods.create_dependencies_title
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.create_dependencies_title('yyyy')
        assert capsys.readouterr().out == ("called Label.__init__ with args ('yyyy',)\n"
                                           "called VBox.addWidget with arg MockLabel\n")

    def test_create_dependencies_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.create_dependencies_grid
        """
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.create_dependencies_grid()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called VBox.addLayout with arg MockGridLayout\n")

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
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        testobj.buttons = {}
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.refresh_widgets = mock_refresh
        testobj.create_buttons([
            {'name': 'xxx', 'text': 'xxxxxx', 'tooltip': 'xxxxxxxxx', 'callback': callback1},
            {'name': 'actv', 'text': 'yyyyyy', 'tooltip': 'yyyyyyyyy', 'callback': callback2}])
        assert len(testobj.buttons) == 2
        assert isinstance(testobj.buttons['xxx'], mockqtw.MockPushButton)
        assert isinstance(testobj.buttons['actv'], mockqtw.MockPushButton)
        assert capsys.readouterr().out == (
                "called VBox.addSpacing\n"
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xxxxxx', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback1},)\n"
                "called PushButton.setToolTip with arg `xxxxxxxxx`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yyyyyy', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback2},)\n"
                "called PushButton.setToolTip with arg `yyyyyyyyy`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n"
                "called PushButton.setEnabled with arg `False`\n")

    def test_setup_actions(self, monkeypatch, capsys):
        """unittest for ShowMods.setup_actions
        """
        def mock_addAction(self, *args):
            """stub
            """
            print('called QWidget.addAction()')
        def mock_confirm(self, *args):
            """stub
            """
        def mock_close(self, *args):
            """stub
            """
        monkeypatch.setattr(testee.qtw.QWidget, 'addAction', mock_addAction)
        monkeypatch.setattr(testee.qgui, 'QAction', mockqtw.MockAction)
        monkeypatch.setattr(testee.ShowMods, 'confirm', mock_confirm)
        monkeypatch.setattr(testee.ShowMods, 'close', mock_close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setup_actions()
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('Done', {testobj})\n"
                f"called Signal.connect with args ({testobj.confirm},)\n"
                'called Action.setShortcut with arg `Ctrl+Enter`\n'
                'called QWidget.addAction()\n'
                f"called Action.__init__ with args ('Cancel', {testobj})\n"
                f"called Signal.connect with args ({testobj.close},)\n"
                "called Action.setShortcuts with arg `['Escape', 'Ctrl+Q']`\n"
                'called QWidget.addAction()\n')

    def test_show_screen(self, monkeypatch, capsys):
        """unittest for ShowMods.show_screen
        """
        def mock_app_exec(self, *args):
            """stub
            """
            print('called Application.exec')
            return 'okcode'
        def mock_show(self, *args):
            """stub
            """
            print('called QWidget.show()')
        monkeypatch.setattr(mockqtw.MockApplication, 'exec', mock_app_exec)
        monkeypatch.setattr(testee.qtw.QWidget, 'show', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockqtw.MockApplication()
        assert capsys.readouterr().out == "called Application.__init__\n"
        assert testobj.show_screen() == "okcode"
        assert capsys.readouterr().out == ('called QWidget.show()\n'
                                          'called Application.exec\n')

    def test_refresh_widgets(self, monkeypatch, capsys):
        """unittest for ShowMods.refresh_widgets
        """
        def mock_add(*args):
            print("called ShowMods.add_checkbox")
            return 'x', 'y', 'z'
        def mock_add_items(*args):
            print("called Showmods.add_items_to_grid with args", args)
            return {}, {}
        def mock_refresh(**kwargs):
            print("called Showmods.refresh_widget_data with args", kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockManager()
        testobj.master.screeninfo = {}
        testobj.gbox1 = mockqtw.MockGridLayout()
        testobj.gbox2 = mockqtw.MockGridLayout()
        testobj.buttons = {"attr": mockqtw.MockPushButton(), 'sel': mockqtw.MockPushButton()}
        assert capsys.readouterr().out == ("called Grid.__init__\ncalled Grid.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.add_checkbox = mock_add
        testobj.add_items_to_grid = mock_add_items
        testobj.refresh_widget_data = mock_refresh
        testobj.refresh_widgets()
        assert capsys.readouterr().out == (
                "called PushButton.setEnabled with arg `False`\n"
                "called PushButton.setEnabled with arg `False`\n"
                "called Manager.order_widgets with args"
                f" ({testobj.gbox1}, {testobj.gbox2}, False)\n")
        testobj.refresh_widgets()
        assert capsys.readouterr().out == (
                "called PushButton.setEnabled with arg `False`\n"
                "called PushButton.setEnabled with arg `False`\n"
                "called Manager.order_widgets with args"
                f" ({testobj.gbox1}, {testobj.gbox2}, False)\n")
        testobj.master.screeninfo = {'xx': {'pos': '1x1', 'sel': True},
                                     'yy': {'pos': '', 'sel': True},
                                     'zz': {'pos': '', 'sel': False}}
        testobj.refresh_widgets(first_time=True)
        assert capsys.readouterr().out == (
                "called PushButton.setEnabled with arg `True`\n"
                "called PushButton.setEnabled with arg `True`\n"
                "called Manager.order_widgets with args"
                f" ({testobj.gbox1}, {testobj.gbox2}, True)\n")

    def test_remove_widgets(self, monkeypatch, capsys):
        """unittest for ShowMods.remove_widgets
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockManager()
        widgetlist = ['', mockqtw.MockLabel(), mockqtw.MockCheckBox()]
        container = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == ("called Label.__init__\ncalled CheckBox.__init__\n"
                                           "called Grid.__init__\n")
        testobj.remove_widgets(widgetlist, container, 1, 2)
        assert capsys.readouterr().out == ("called CheckBox.close\n"
                                           "called Label.close\n"
                                           "called Grid.itemAtPosition with args (1, 2)\n"
                                           "called Grid.removeItem with args ('itematpos',)\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for ShowMods.add_checkbox
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockManager()
        testobj.master.screentext = {}
        grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        obj1, obj2, obj3 = testobj.add_checkbox(grid, 1, 2, False)
        assert isinstance(obj1, testee.qtw.QHBoxLayout)
        assert isinstance(obj2, testee.qtw.QLabel)
        assert isinstance(obj3, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            "called HBox.__init__\n"
            "called CheckBox.__init__\n"
            "called CheckBox.setEnabled with arg False\n"
            "called Label.__init__\n"
            "called HBox.addSpacing\n"
            "called HBox.addWidget with arg MockCheckBox\n"
            "called HBox.addWidget with arg MockLabel\n"
            "called HBox.addStretch\n"
            "called HBox.addSpacing\n"
            "called Grid.addLayout with arg MockHBoxLayout"
            " at (1, 2)\n")
        obj1, obj2, obj3 = testobj.add_checkbox(grid, 1, 2, True)
        assert isinstance(obj1, testee.qtw.QHBoxLayout)
        assert isinstance(obj2, testee.qtw.QLabel)
        assert isinstance(obj3, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            "called HBox.__init__\n"
            "called CheckBox.__init__\n"
            "called CheckBox.setEnabled with arg False\n"
            "called CheckBox.setEnabled with arg True\n"
            f"called Signal.connect with args ({testobj.enable_button},)\n"
            "called Label.__init__\n"
            "called HBox.addSpacing\n"
            "called HBox.addWidget with arg MockCheckBox\n"
            "called HBox.addWidget with arg MockLabel\n"
            "called HBox.addStretch\n"
            "called HBox.addSpacing\n"
            "called Grid.addLayout with arg MockHBoxLayout"
            " at (1, 2)\n")

    def test_set_label_text(self, monkeypatch, capsys):
        """unittest for ShowMods.set_label_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockManager()
        widgetlist = ['frame', mockqtw.MockLabel(), 'check']
        assert widgetlist[1].text() == ''
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj.set_label_text(widgetlist, 'xxxx', '', '')
        assert widgetlist[1].text() == 'xxxx'
        assert capsys.readouterr().out == "called Label.setText with arg `xxxx`\n"
        testobj.set_label_text(widgetlist, 'xxxx', '', 'yyy')
        assert widgetlist[1].text() == 'xxxx yyy'
        assert capsys.readouterr().out == "called Label.setText with arg `xxxx yyy`\n"
        testobj.set_label_text(widgetlist, 'xxxx', 'zz', '')
        assert widgetlist[1].text() == 'xxxxzz'
        assert capsys.readouterr().out == (
                "called Manager.build_link_text with args ('xxxx', 'zz')\n"
                "called Label.setOpenExternalLinks with arg 'True'\n"
                "called Label.setText with arg `xxxxzz`\n")
        testobj.set_label_text(widgetlist, 'xxxx', 'zz', 'yyy')
        assert widgetlist[1].text() == 'xxxxzz yyy'
        assert capsys.readouterr().out == (
                "called Manager.build_link_text with args ('xxxx', 'zz')\n"
                "called Label.setOpenExternalLinks with arg 'True'\n"
                "called Label.setText with arg `xxxxzz yyy`\n")

    def test_set_checkbox_state(self, monkeypatch, capsys):
        """unittest for showmods.set_checkbox_state
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widgetlist = ['frame', 'label', mockqtw.MockCheckBox()]
        assert not widgetlist[2].isChecked()
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.isChecked\n")
        testobj.set_checkbox_state(widgetlist, False)
        assert not widgetlist[2].isChecked()
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.isChecked\n")
        testobj.set_checkbox_state(widgetlist, True)
        assert widgetlist[2].isChecked() == 1
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.isChecked\n")

    def test_enable_button(self, monkeypatch, capsys):
        """unittest for ShowMods.enable_button
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.buttons = {'actv': mockqtw.MockPushButton()}
        assert capsys.readouterr().out == 'called PushButton.__init__ with args () {}\n'
        testobj.enable_button()
        assert capsys.readouterr().out == 'called PushButton.setEnabled with arg `True`\n'

    def test_update_mods(self, monkeypatch, capsys):
        """unittest for ShowMods.update_mods
        """
        def mock_open(parent, *args, **kwargs):
            print('called FileDialog.getOpenFileNames with args', parent, args, kwargs)
            return ['name1', 'name2'], True
        def mock_update(arg):
            print(f"called Manager.update_mods with arg {arg}")
            return ['xxx', 'yyy']
        def mock_information(self, *args):
            """stub
            """
            print('called MessageBox.information with args', args)
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockManager()
        testobj.master.update_mods = mock_update
        testobj.update_mods()
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileNames with args {testobj} ()"
                " {'caption': 'Install downloaded mods', 'directory': 'Downloads',"
                " 'filter': 'Zip files (*.zip)'}\n")

        monkeypatch.setattr(mockqtw.MockFileDialog, 'getOpenFileNames', mock_open)
        testobj.update_mods()
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileNames with args {testobj} ()"
                " {'caption': 'Install downloaded mods', 'directory': 'Downloads',"
                " 'filter': 'Zip files (*.zip)'}\n"
                "called Manager.update_mods with arg ['name1', 'name2']\n"
                "called MessageBox.information with args ('Change Config', 'xxx\\nyyy')\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for ShowMods.confirm
        """
        def mock_information(self, *args):
            """stub
            """
            print('called MessageBox.information with args', args)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockManager()
        testobj.buttons = {'actv': mockqtw.MockPushButton()}
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called Manager.process_activations\n"
                "called MessageBox.information with args"
                " ('Change Config', 'wijzigingen zijn doorgevoerd')\n"
                "called PushButton.setEnabled with arg `False`\n")

    def test_get_labeltext_if_checked(self, monkeypatch, capsys):
        """unittest for ShowMods.get_labeltext_if_checked
        """
        label = mockqtw.MockLabel('xxx')
        check = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called Label.__init__ with args ('xxx',)\n"
                                           "called CheckBox.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        widgetlist = ['hbox', label, check]
        assert testobj.get_labeltext_if_checked(widgetlist) == ''
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")
        check.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n")
        assert testobj.get_labeltext_if_checked(widgetlist) == 'xxx'
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")
        label.setText('xxx<yyy>zzz<qqq>rrr')
        assert capsys.readouterr().out == ("called Label.setText with arg `xxx<yyy>zzz<qqq>rrr`\n")
        assert testobj.get_labeltext_if_checked(widgetlist) == 'zzz'
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")

    def test_select_value(self, monkeypatch, capsys):
        """unittest for ShowMods.select_value
        """
        def mock_get(*args, **kwargs):
            nonlocal counter
            print('called InputDialog.getItem with args', args, kwargs)
            counter += 1
            return f'item{counter}', counter != 1
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get)
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        counter = 0
        assert testobj.select_value('xxx', ['yyy', 'zzz']) == 'item1'
        assert capsys.readouterr().out == (
                f"called InputDialog.getItem with args ({testobj},"
                " 'Stardew Valley Mod Manager', 'xxx', ['yyy', 'zzz']) {'editable': True}\n")
        counter = 0
        assert testobj.select_value('xxx', ['yyy', 'zzz'], False, True) == 'item2'
        assert capsys.readouterr().out == (
                f"called InputDialog.getItem with args ({testobj},"
                " 'Stardew Valley Mod Manager', 'xxx', ['yyy', 'zzz']) {'editable': False}\n"
                f"called MessageBox.information with args `{testobj}` `SDVMM`"
                " `You *must* select or enter a value`\n"
                f"called InputDialog.getItem with args ({testobj},"
                " 'Stardew Valley Mod Manager', 'xxx', ['yyy', 'zzz']) {'editable': False}\n")


class TestSettingsDialogGui:
    """unittests for qtgui.SettingsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SettiingsDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called SettingsDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.SettingsDialogGui, '__init__', mock_init)
        testobj = testee.SettingsDialogGui()
        assert capsys.readouterr().out == 'called SettingsDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SettingsDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        master = types.SimpleNamespace()
        parent = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = testee.SettingsDialogGui(master, parent)
        assert testobj.master == master
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.gbox, testee.qtw.QGridLayout)
        assert testobj.row == 0
        assert capsys.readouterr().out == (
            f"called Dialog.__init__ with args {parent} () {{}}\n"
            "called VBox.__init__\n"
            "called Grid.__init__\n"
            "called VBox.addLayout with arg MockGridLayout\n"
            "called Dialog.setLayout\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.add_label
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.add_label('xxx')
        assert testobj.row == 1
        assert capsys.readouterr().out == (f"called Label.__init__ with args ('xxx', {testobj})\n"
                                           "called Grid.addWidget with arg MockLabel at (1, 0)\n")

    def test_add_line_entry(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.add_line_entry
        """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        result = testobj.add_line_entry('text')
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                "called LineEdit.__init__\n"
                "called LineEdit.setText with arg `text`\n"
                "called LineEdit.setMinimumWidth with arg `380`\n"
                "called Grid.addWidget with arg MockLineEdit at (0, 1)\n")

    def test_add_browse_button(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.add_browse_button
        """
        def callback():
            return 'dummy'
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        result = testobj.add_browse_button(callback)
        assert isinstance(result, testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
                f"called PushButton.__init__ with args ('Browse', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called Grid.addWidget with arg MockPushButton at (0, 2)\n")

    def test_add_spinbox(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.add_spinbox
        """
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        result = testobj.add_spinbox('xxx')
        assert isinstance(result, testee.qtw.QSpinBox)
        assert capsys.readouterr().out == (
                "called SpinBox.__init__\n"
                "called SpinBox.setValue with arg 'xxx'\n"
                "called Grid.addWidget with arg MockSpinBox at (0, 1)\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.add_buttonbox
        """
        def callback():
            return 'dummy'
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttonbox([('text', callback)])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called PushButton.__init__ with args ('text',) {}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.set_focus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.set_focus(field)
        assert capsys.readouterr().out == ("called LineEdit.setFocus\n")

    def test_get_widget_text(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.get_widget_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        assert testobj.get_widget_text(widget) == ''
        assert capsys.readouterr().out == ("called LineEdit.text\n")
        widget = mockqtw.MockSpinBox()
        assert capsys.readouterr().out == "called SpinBox.__init__\n"
        assert testobj.get_widget_text(widget) == 0
        assert capsys.readouterr().out == ("called SpinBox.value\n")

    def test_set_widget_text(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.set_widget_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockLabel()
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj.set_widget_text(widget, 'xxx')
        assert capsys.readouterr().out == ("called Label.setText with arg `xxx`\n")
        widget = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.set_widget_text(widget, 'xxx')
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `xxx`\n")

    def test_select_directory(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.select_directory
        """
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_directory('caption', 'start')
        assert capsys.readouterr().out == (
                f"called FileDialog.getExistingDirectory with args {testobj}"
                " () {'caption': 'caption', 'directory': 'start'}\n")
        return ''

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SettingsDialogGui.confirm
        """
        def mock_accept():
            print('called Dialog.accept')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.accept = mock_accept
        testobj.confirm()
        assert capsys.readouterr().out == ("called Dialog.accept\n")


class TestDeleteDialogGui:
    """unittests for qtgui.DeleteDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.DeleteDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called DeleteDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.DeleteDialogGui, '__init__', mock_init)
        testobj = testee.DeleteDialogGui()
        assert capsys.readouterr().out == 'called DeleteDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for DeleteDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        master = types.SimpleNamespace()
        parent = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = testee.DeleteDialogGui(master, parent)
        assert testobj.parent == parent
        assert testobj.master == master
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
            f"called Dialog.__init__ with args {parent} () {{}}\n"
            "called VBox.__init__\n"
            "called Dialog.setLayout\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.add_combobox
        """
        def callback():
            return 'dummy'
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_combobox(['xxx', 'yyy'], callback)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.setEditable with arg `True`\n"
                "called ComboBox.addItems with arg ['xxx', 'yyy']\n"
                f"called Signal.connect with args ({callback},)\n"
                "called VBox.addWidget with arg MockComboBox\n")
        result = testobj.add_combobox(['xxx', 'yyy'], callback, False)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.setEditable with arg `False`\n"
                "called ComboBox.addItems with arg ['xxx', 'yyy']\n"
                f"called Signal.connect with args ({callback},)\n"
                "called VBox.addWidget with arg MockComboBox\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.add_buttonbox
        """
        def callback():
            return 'dummy'
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_buttonbox([('xxx', callback, False), ('yyy', callback, True)])
        assert len(result) == 2
        assert isinstance(result[0], testee.qtw.QPushButton)
        assert isinstance(result[1], testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called PushButton.__init__ with args ('xxx',) {}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called PushButton.setEnabled with arg `False`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called PushButton.__init__ with args ('yyy',) {}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called PushButton.setEnabled with arg `True`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.set_focus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.set_focus(field)
        assert capsys.readouterr().out == ("called LineEdit.setFocus\n")

    def test_get_combobox_entry(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.get_combobox_entry
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockComboBox()
        assert testobj.get_combobox_entry(field) == 'current text'
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.currentText\n")

    def test_set_combobox_entry(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.set_combobox_entry
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockComboBox()
        testobj.set_combobox_entry(field, 1)
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.setCurrentIndex with arg `1`\n")

    def test_enable_button(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.enable_button
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        button = mockqtw.MockPushButton()
        testobj.enable_button(button, 'value')
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called PushButton.setEnabled with arg `value`\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.confirm
        """
        def mock_accept():
            print('called Dialog.accept')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.accept = mock_accept
        testobj.confirm()
        assert capsys.readouterr().out == ("called Dialog.accept\n")


class TestAttributesDialogGui:
    """unittests for qtgui.AttributesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.AttributesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called AttributesDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.AttributesDialogGui, '__init__', mock_init)
        testobj = testee.AttributesDialogGui()
        assert capsys.readouterr().out == 'called AttributesDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for AttributesDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        master = types.SimpleNamespace()
        parent = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = testee.AttributesDialogGui(master, parent)
        assert testobj.parent == parent
        assert testobj.master == master
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
            f"called Dialog.__init__ with args {parent} () {{}}\n"
            "called VBox.__init__\n"
            "called Dialog.setLayout\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_combobox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        result = testobj.add_combobox(['xxx'], callback)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.setEditable with arg `True`\n"
                "called ComboBox.setEnabled with arg True\n"
                "called ComboBox.addItems with arg ['xxx']\n"
                f"called Signal.connect with args ({callback},)\n"
                f"called Signal.connect with args ({callback},)\n"
                "called VBox.addWidget with arg MockComboBox\n")
        result = testobj.add_combobox([], callback, False, False)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.setEditable with arg `False`\n"
                "called ComboBox.setEnabled with arg False\n"
                "called ComboBox.addItems with arg []\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockComboBox\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_label
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_label('xxx')
        assert capsys.readouterr().out == (f"called Label.__init__ with args ('xxx', {testobj})\n"
                                           "called VBox.addWidget with arg MockLabel\n")

    def test_add_line_entry(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_line_entry
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        result = testobj.add_line_entry('text', callback)
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                "called LineEdit.__init__\n"
                f"called Signal.connect with args ({callback},)\n"
                "called LineEdit.setEnabled with arg True\n"
                "called HBox.addWidget with arg MockLineEdit\n")
        result = testobj.add_line_entry('text', callback, False)
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                "called LineEdit.__init__\n"
                f"called Signal.connect with args ({callback},)\n"
                "called LineEdit.setEnabled with arg False\n"
                "called HBox.addWidget with arg MockLineEdit\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_checkbox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_checkbox('xxx', callback)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == ("called CheckBox.__init__ with text 'xxx'\n"
                                           f"called Signal.connect with args ({callback},)\n"
                                           "called CheckBox.setEnabled with arg True\n"
                                           "called VBox.addWidget with arg MockCheckBox\n")
        result = testobj.add_checkbox('xxx', callback, False)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == ("called CheckBox.__init__ with text 'xxx'\n"
                                           f"called Signal.connect with args ({callback},)\n"
                                           "called CheckBox.setEnabled with arg False\n"
                                           "called VBox.addWidget with arg MockCheckBox\n")

    def test_add_button(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_button
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_button('xxx', callback)
        assert isinstance(result, testee.qtw.QPushButton)
        assert capsys.readouterr().out == ("called PushButton.__init__ with args ('xxx',) {}\n"
                                           f"called Signal.connect with args ({callback},)\n"
                                           "called VBox.addWidget with arg MockPushButton\n"
                                           "called PushButton.setEnabled with arg `True`\n")
        result = testobj.add_button('xxx', callback, False)
        assert isinstance(result, testee.qtw.QPushButton)
        assert capsys.readouterr().out == ("called PushButton.__init__ with args ('xxx',) {}\n"
                                           f"called Signal.connect with args ({callback},)\n"
                                           "called VBox.addWidget with arg MockPushButton\n"
                                           "called PushButton.setEnabled with arg `False`\n")

    def test_start_line_with_clear_button(self, monkeypatch, capsys):
        """ unittest for test_start_line_with_clear_button
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = testee.qtw.QVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.row = 0
        testobj.start_line_with_clear_button()
        assert isinstance(testobj.hbox, testee.qtw.QHBoxLayout)
        assert testobj.row == 0
        assert capsys.readouterr().out == (
                "called VBox.addLayout with arg QHBoxLayout\n")

    def test_add_clear_button(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_clear_button
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qgui, 'QIcon', mockqtw.MockIcon)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        result = testobj.add_clear_button(callback)
        assert isinstance(result, testee.qtw.QPushButton)
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called Icon.fromTheme with args ()\n"
                                           "called PushButton.setIcon with arg `None`\n"
                                           "called PushButton.setFixedSize with args (24, 24)\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           f"called Signal.connect with args ({callback},)\n"
                                           "called HBox.addWidget with arg MockPushButton\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.add_buttonbox
        """
        def callback():
            "stub for callback function"
            return 'dummy'
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttonbox([('text', callback, 'value')])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called PushButton.__init__ with args ('text',) {}\n"
                "called PushButton.setEnabled with arg `value`\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.set_focus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.set_focus(field)
        assert capsys.readouterr().out == ("called LineEdit.setFocus\n")

    def test_enable_button(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.enable_button
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.enable_button(button, 'value')
        assert capsys.readouterr().out == "called PushButton.setEnabled with arg `value`\n"

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.get_combobox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_combobox_value(cb) == 'current text'
        assert capsys.readouterr().out == ("called ComboBox.currentText\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert not testobj.get_checkbox_value(cb)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")

    def test_get_field_text(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.get_field_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        assert testobj.get_field_text(widget) == ''
        assert capsys.readouterr().out == ("called LineEdit.text\n")

    def test_reset_all_fields(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.reset_all_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field_list = (mockqtw.MockComboBox(), mockqtw.MockPushButton(), mockqtw.MockLineEdit(),
                      mockqtw.MockPushButton(), mockqtw.MockCheckBox(), mockqtw.MockCheckBox(),
                      mockqtw.MockPushButton(), mockqtw.MockPushButton(), mockqtw.MockPushButton())
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called LineEdit.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.reset_all_fields(field_list)
        assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                           "called ComboBox.setEnabled with arg False\n"
                                           "called LineEdit.clear\n"
                                           "called LineEdit.setEnabled with arg False\n"
                                           "called CheckBox.setDisabled with arg True\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setDisabled with arg True\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n")

    def test_activate_and_populate_fields(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.activate_and_populate_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field_list = (mockqtw.MockComboBox(), mockqtw.MockPushButton(), mockqtw.MockLineEdit(),
                      mockqtw.MockPushButton(), mockqtw.MockCheckBox(), mockqtw.MockCheckBox(),
                      mockqtw.MockPushButton(), mockqtw.MockPushButton(), mockqtw.MockPushButton())
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called LineEdit.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.reset_all_fields(field_list)
        testobj.activate_and_populate_fields(field_list, ['x', 'y'], {'txt': 'xxx', 'sel': 'yyy',
                                                                      'opt': 'zzz'})
        assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                           "called ComboBox.setEnabled with arg False\n"
                                           "called LineEdit.clear\n"
                                           "called LineEdit.setEnabled with arg False\n"
                                           "called CheckBox.setDisabled with arg True\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setDisabled with arg True\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called ComboBox.clear\n"
                                           "called ComboBox.addItems with arg ['x', 'y']\n"
                                           "called ComboBox.setEnabled with arg True\n"
                                           "called PushButton.setDisabled with arg `False`\n"
                                           "called LineEdit.setText with arg `xxx`\n"
                                           "called LineEdit.setEnabled with arg True\n"
                                           "called PushButton.setDisabled with arg `False`\n"
                                           "called CheckBox.setChecked with arg yyy\n"
                                           "called CheckBox.setEnabled with arg True\n"
                                           "called CheckBox.setChecked with arg zzz\n"
                                           "called CheckBox.setEnabled with arg True\n"
                                           "called PushButton.setDisabled with arg `False`\n"
                                           "called PushButton.setDisabled with arg `False`\n"
                                           "called PushButton.setDisabled with arg `True`\n")

    def test_clear_field(self, monkeypatch, capsys):
        """unittest for AttributesDialogGui.clear_field
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.clear_field(cb)
        assert capsys.readouterr().out == ("called ComboBox.clear\n")


class TestDependencyDialogGui:
    """unittests for qtgui.DependencyDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.DependencyDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called DependencyDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.DependencyDialogGui, '__init__', mock_init)
        testobj = testee.DependencyDialogGui()
        assert capsys.readouterr().out == 'called DependencyDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for DeleteDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        master = types.SimpleNamespace()
        parent = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = testee.DependencyDialogGui(master, parent)
        assert testobj.master == master
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
            f"called Dialog.__init__ with args {parent} () {{}}\n"
            "called VBox.__init__\n"
            "called Dialog.setLayout\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.add_label
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_label('xxx')
        assert isinstance(result, testee.qtw.QLabel)
        assert capsys.readouterr().out == (f"called Label.__init__ with args ('xxx', {testobj})\n"
                                           "called VBox.addWidget with arg MockLabel\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.add_combobox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_combobox(['x', 'y'], callback)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.setEditable with arg `True`\n"
                                           "called ComboBox.setEnabled with arg True\n"
                                           "called ComboBox.addItems with arg ['x', 'y']\n"
                                           f"called Signal.connect with args ({callback},)\n"
                                           "called VBox.addWidget with arg MockComboBox\n")
        result = testobj.add_combobox(['x', 'y'], None, False, False)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.setEditable with arg `False`\n"
                                           "called ComboBox.setEnabled with arg False\n"
                                           "called ComboBox.addItems with arg ['x', 'y']\n"
                                           # f"called Signal.connect with args ({callback},)\n"
                                           "called VBox.addWidget with arg MockComboBox\n")

    def test_set_field_enabled(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.set_field_enabled
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.set_field_enabled(field, 'value')
        assert capsys.readouterr().out == "called PushButton.setEnabled with arg `value`\n"

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.add_buttonbox
        """
        def callback():
            return 'dummy'
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttonbox([('text', callback)])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called PushButton.__init__ with args ('text',) {}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.set_focus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.set_focus(field)
        assert capsys.readouterr().out == ("called LineEdit.setFocus\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.get_combobox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_combobox_value(cb) == 'current text'
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_confirm(self, monkeypatch, capsys):
        """unittest for DependencyDialogGui.confirm
        """
        def mock_accept(self):
            print('called Dialog.accept')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.confirm()
        assert capsys.readouterr().out == ("called Dialog.accept\n")


class TestSaveGamesDialogGui:
    """unittests for qtgui.SaveGamesDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SaveGamesDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called SaveGamesDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.SaveGamesDialogGui, '__init__', mock_init)
        testobj = testee.SaveGamesDialogGui()
        assert capsys.readouterr().out == 'called SaveGamesDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        master = types.SimpleNamespace()
        parent = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = testee.SaveGamesDialogGui(master, parent)
        assert testobj.master == master
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
            f"called Dialog.__init__ with args {parent} () {{}}\n"
            "called VBox.__init__\n"
            "called Dialog.setLayout\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.add_combobox
        """
        def callback():
            """empty stub for callback function
            """
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        testobj.msbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\ncalled VBox.__init__\n"
        result = testobj.add_combobox(['x'], callback)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.setEditable with arg `True`\n"
                "called ComboBox.setEnabled with arg True\n"
                "called ComboBox.addItems with arg ['x']\n"
                f"called Signal.connect with args ({callback},)\n"
                "called VBox.addWidget with arg MockComboBox\n")
        result = testobj.add_combobox(['x'], None, False, False)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.setEditable with arg `False`\n"
                "called ComboBox.setEnabled with arg False\n"
                "called ComboBox.addItems with arg ['x']\n"
                "called HBox.__init__\n"
                "called HBox.addWidget with arg MockComboBox\n"
                "called VBox.insertLayout with args (-1, MockHBoxLayout)\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.get_combobox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_combobox_value(cb) == 'current text'
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_set_combobox_value(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.set_combobox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.set_combobox_value(cb, 'xxx')
        assert capsys.readouterr().out == "called ComboBox.setCurrentText with arg `xxx`\n"

    def test_add_label(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.add_label
        """
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        # breakpoint()
        testobj.add_label('xxx')
        assert isinstance(testobj.gbox, testee.qtw.QGridLayout)
        assert testobj.row == 0
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called VBox.addLayout with arg MockGridLayout\n"
                                           f"called Label.__init__ with args ('xxx', {testobj})\n"
                                           "called Grid.addWidget with arg MockLabel at (0, 0)\n")
        testobj.row += 1
        testobj.add_label('xxx')
        assert capsys.readouterr().out == (f"called Label.__init__ with args ('xxx', {testobj})\n"
                                           "called Grid.addWidget with arg MockLabel at (1, 0)\n")

    def test_add_line_entry(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.add_line_entry
        """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        result = testobj.add_line_entry('text')
        assert testobj.row == 1
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                "called LineEdit.__init__\n"
                "called LineEdit.setText with arg `text`\n"
                "called LineEdit.setMinimumWidth with arg `380`\n"
                "called Grid.addWidget with arg MockLineEdit at (0, 1)\n")

    def test_set_field_text(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.set_field_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockLabel()
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj.set_field_text(widget, 'xxx')
        assert capsys.readouterr().out == ("called Label.setText with arg `xxx`\n")
        widget = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.set_field_text(widget, 'xxx')
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `xxx`\n")

    def test_get_field_text(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.get_field_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        assert testobj.get_field_text(widget) == ''
        assert capsys.readouterr().out == ("called LineEdit.text\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.add_buttonbox
        """
        def callback():
            return 'dummy'
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttonbox([('text', callback, 'value')])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called PushButton.__init__ with args ('text',) {}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called PushButton.setEnabled with arg `value`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.set_focus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.set_focus(field)
        assert capsys.readouterr().out == ("called LineEdit.setFocus\n")

    def test_start_modselect_block(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.start_modselect_block
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.start_modselect_block('xxx')
        assert isinstance(testobj.msbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ("called VBox.__init__\n"
                                           f"called Label.__init__ with args ('xxx', {testobj})\n"
                                           "called VBox.addWidget with arg MockLabel\n"
                                           "called VBox.addStretch\n"
                                           "called VBox.addLayout with arg MockVBoxLayout\n")

    def test_add_clear_button(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.add_clear_button
        """
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qgui, 'QIcon', mockqtw.MockIcon)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.msbox = mockqtw.MockVBoxLayout()
        testobj.hmsbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == ("called VBox.__init__\n"
                                           "called HBox.__init__\n")
        result = testobj.add_clear_button('value')
        assert isinstance(result[0], testee.qtw.QPushButton)
        assert isinstance(result[1], testee.qtw.QHBoxLayout)
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called Icon.fromTheme with args ()\n"
                                           "called PushButton.setIcon with arg `None`\n"
                                           "called PushButton.setFixedSize with args (24, 24)\n"
                                           "called PushButton.setEnabled with arg `value`\n"
                                           "called HBox.addWidget with arg MockPushButton\n")

    def test_set_callbacks(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.set_callbacks
        """
        def callback1():
            """empty stub for callback function
            """
        def callback2():
            """empty stub for callback function
            """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_callbacks((mockqtw.MockComboBox(), mockqtw.MockPushButton()),
                              (callback1, callback2))
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           f"called Signal.connect with args ({callback1},)\n"
                                           f"called Signal.connect with args ({callback2},)\n")

    def test_enable_change(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.enable_change
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(update_button=mockqtw.MockPushButton())
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.enable_change()
        assert capsys.readouterr().out == "called PushButton.setEnabled with arg `True`\n"

    def test_enable_widget(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.enable_widget
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.enable_widget(button, 'value')
        assert capsys.readouterr().out == "called PushButton.setEnabled with arg `value`\n"

    def test_remove_modselector(self, monkeypatch, capsys):
        """unittest for SaveGamesDialogGui.remove_modselector
        """
        def mock_itemat(rownum):
            print(f'called VBox.itemAt with arg {rownum}')
            return hbox
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.msbox = mockqtw.MockVBoxLayout()
        testobj.msbox.itemAt = mock_itemat
        cb = mockqtw.MockCheckBox()
        btn = mockqtw.MockPushButton()
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == ("called VBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called HBox.__init__\n")
        testobj.remove_modselector((cb, btn, hbox))
        assert capsys.readouterr().out == ("called HBox.removeWidget with arg MockCheckBox\n"
                                           "called CheckBox.close\n"
                                           "called HBox.removeWidget with arg MockPushButton\n"
                                           "called PushButton.close\n"
                                           "called VBox.removeItem\n")
