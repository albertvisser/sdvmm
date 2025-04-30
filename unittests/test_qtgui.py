"""unittests for ./qtgui.py
"""
import types
import pytest
import mockgui.mockqtwidgets as mockqtw
from src import qtgui as testee

sett = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called VBox.__init__
called Grid.__init__
called Label.__init__ with args ('Base location for mods:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)
called LineEdit.__init__
called LineEdit.setText with arg `xxx`
called LineEdit.setMinimumWidth with arg `380`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (0, 1)
called PushButton.__init__ with args ('Browse', {testobj}) {{}}
called Signal.connect with args ({testobj.select_modbase},)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'> at (0, 2)
called Label.__init__ with args ('Configuration file name:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 0)
called LineEdit.__init__
called LineEdit.setText with arg `yyy`
called LineEdit.setMinimumWidth with arg `380`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 1)
called Label.__init__ with args ('Location for downloads:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (2, 0)
called LineEdit.__init__
called LineEdit.setText with arg `zzz`
called LineEdit.setMinimumWidth with arg `380`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (2, 1)
called PushButton.__init__ with args ('Browse', {testobj}) {{}}
called Signal.connect with args ({testobj.select_download_path},)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'> at (2, 2)
called Label.__init__ with args ('Number of columns on screen:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (3, 0)
called SpinBox.__init__
called SpinBox.setValue with arg 'qqq'
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockSpinBox'> at (3, 1)
called Label.__init__ with args ('Location for save files:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (4, 0)
called LineEdit.__init__
called LineEdit.setText with arg `rrr`
called LineEdit.setMinimumWidth with arg `380`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (4, 1)
called PushButton.__init__ with args ('Browse', {testobj}) {{}}
called Signal.connect with args ({testobj.select_savepath},)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'> at (4, 2)
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called HBox.__init__
called PushButton.__init__ with args ('&Save',) {{}}
called Signal.connect with args ({testobj.update},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Cancel',) {{}}
called Signal.connect with args ({testobj.reject},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
called LineEdit.setFocus
"""
delete = """\
called Conf.list_all_mod_dirs
called Conf.get_diritem_data with args ('xxx', 'SCRNAM')
called Conf.get_diritem_data with args ('yyy', 'SCRNAM')
called Dialog.__init__ with args {testobj.parent} () {{}}
called VBox.__init__
called ComboBox.__init__
called ComboBox.setEditable with arg `False`
called ComboBox.addItem with arg `select a mod to remove`
called ComboBox.addItems with arg ['xxx_name', 'yyy_name']
called Signal.connect with args ({testobj.process},)
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called HBox.__init__
called PushButton.__init__ with args ('&Remove',) {{}}
called PushButton.setDisabled with arg `True`
called Signal.connect with args ({testobj.update},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Exit',) {{}}
called Signal.connect with args ({testobj.accept},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
called ComboBox.setFocus
"""
attrs = """\
called Conf.list_all_mod_dirs
called Conf.get_diritem_data with args ('xxx', 'SCRNAM')
called Conf.get_diritem_data with args ('yyy', 'SCRNAM')
called Dialog.__init__ with args {testobj.parent} () {{}}
called VBox.__init__
called ComboBox.__init__
called ComboBox.setEditable with arg `False`
called ComboBox.addItem with arg `select a mod to change the screen text`
called ComboBox.addItems with arg ['xxx_name', 'yyy_name']
called Signal.connect with args ({testobj.process},)
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called HBox.__init__
called Label.__init__ with args ('Screen Name:\\n(the suggestions in the box below are taken from\\nthe mod components', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called ComboBox.__init__
called ComboBox.setEditable with arg `True`
called Signal.connect with args ({testobj.enable_change},)
called ComboBox.setEnabled with arg False
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called PushButton.__init__ with args () {{}}
called Icon.fromTheme with args ()
called PushButton.setIcon with arg `None`
called PushButton.setFixedSize with args (24, 24)
called PushButton.setDisabled with arg `True`
called Signal.connect with args ({testobj.clear_name_text},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called Label.__init__ with args ('Screen Text:\\n(to add some information e.q. if the mod is broken)', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called LineEdit.__init__
called Signal.connect with args ({testobj.enable_change},)
called LineEdit.setEnabled with arg False
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called PushButton.__init__ with args () {{}}
called Icon.fromTheme with args ()
called PushButton.setIcon with arg `None`
called PushButton.setFixedSize with args (24, 24)
called PushButton.setDisabled with arg `True`
called Signal.connect with args ({testobj.clear_text_text},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called CheckBox.__init__ with text 'This mod can be activated by itself'
called Signal.connect with args ({testobj.enable_change},)
called CheckBox.setDisabled with arg True
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called CheckBox.__init__ with text 'Do not touch when (de)activating for a save'
called Signal.connect with args ({testobj.enable_change},)
called CheckBox.setDisabled with arg True
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called PushButton.__init__ with args ('View &Components',) {{}}
called Signal.connect with args ({testobj.view_components},)
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.setDisabled with arg `True`
called PushButton.__init__ with args ('View &Dependencies',) {{}}
called Signal.connect with args ({testobj.view_dependencies},)
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.setDisabled with arg `True`
called HBox.__init__
called PushButton.__init__ with args ('&Update',) {{}}
called PushButton.setDisabled with arg `True`
called Signal.connect with args ({testobj.update},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Exit',) {{}}
called Signal.connect with args ({testobj.accept},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
called ComboBox.setFocus
"""
saveitems = """\
called Conf.list_all_mod_savetemitems
called Conf.list_all_mod_dirs
called Conf.get_diritem_data with args ('xxx', 'SCRNAM')
called Conf.get_diritem_data with args ('yyy', 'SCRNAM')
called Dialog.__init__ with args {testobj.parent} () {{}}
called ComboBox.__init__
called ComboBox.setEditable with arg `False`
called ComboBox.addItem with arg `select a saved game`
called ComboBox.addItems with arg ['qqq', 'rrr']
called Signal.connect with args ({testobj.get_savedata},)
called LineEdit.__init__
called Signal.connect with args ({testobj.enable_change},)
called LineEdit.__init__
called Signal.connect with args ({testobj.enable_change},)
called LineEdit.__init__
called Signal.connect with args ({testobj.enable_change},)
called PushButton.__init__ with args ('&Update config',) {{}}
called PushButton.setDisabled with arg `True`
called Signal.connect with args ({testobj.update},)
called PushButton.__init__ with args ('&Activate Mods',) {{}}
called PushButton.setDisabled with arg `True`
called Signal.connect with args ({testobj.confirm},)
called PushButton.__init__ with args ('&Exit',) {{}}
called Signal.connect with args ({testobj.accept},)
called VBox.__init__
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called Grid.__init__
called Label.__init__ with args ('Player name:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (0, 1)
called Label.__init__ with args ('Farm name:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 0)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 1)
called Label.__init__ with args ('In-game date:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (2, 0)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (2, 1)
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called VBox.__init__
called Label.__init__ with args ('Uses:', {testobj})
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called SaveGamesDialog.add_modselector
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called VBox.addStretch
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
called ComboBox.setFocus
"""


@pytest.fixture
def expected_output():
    "fixture returning output to be expected from (mostly) gui setup methods"
    results = {'sett': sett, 'delete': delete, 'attrs': attrs, 'saves': saveitems}
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


def test_show_dialog(capsys):
    """unittest for qtgui.show_dialog
    """
    def mock_exec(self):
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Rejected
    def mock_exec_2(self):
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Accepted
    parent = types.SimpleNamespace()
    cls = mockqtw.MockDialog
    modnames = ['x', 'y']
    cls.exec = mock_exec
    # assert testee.show_dialog(cls, parent, modnames, True) == (False, {'mods': [], 'deps': {},
    #                                                                    'set_active': []})
    assert not testee.show_dialog(cls, parent, modnames, True)
    assert capsys.readouterr().out == (
        "called Dialog.__init__ with args"
        # " namespace(dialog_data={'mods': [], 'deps': {}, 'set_active': []}) (['x', 'y'], True) {}\n"
        " namespace() (['x', 'y'], True) {}\n"
        "called Dialog.exec\n")
    cls.exec = mock_exec_2
    # assert testee.show_dialog(cls, parent, modnames, False) == (True, {'mods': [], 'deps': {},
    #                                                                    'set_active': []})
    assert testee.show_dialog(cls, parent, modnames, False)
    assert capsys.readouterr().out == (
        "called Dialog.__init__ with args"
        # " namespace(dialog_data={'mods': [], 'deps': {}, 'set_active': []}) (['x', 'y'], False) {}\n"
        " namespace() (['x', 'y'], False) {}\n"
        "called Dialog.exec\n")


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
                                           "called VBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'>\n")

    def test_create_selectables_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.create_selectables_grid
        """
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.create_selectables_grid()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockGridLayout'>\n")

    def test_create_dependencies_title(self, monkeypatch, capsys):
        """unittest for ShowMods.create_dependencies_title
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.create_dependencies_title('yyyy')
        assert capsys.readouterr().out == ("called Label.__init__ with args ('yyyy',)\n"
                                           "called VBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'>\n")

    def test_create_dependencies_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.create_dependencies_grid
        """
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.create_dependencies_grid()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockGridLayout'>\n")

    def test_create_buttons(self, monkeypatch, capsys, expected_output):
        """unittest for ShowMods.create_buttons
        """
        def mock_refresh(*args, **kwargs):
            """stub
            """
            print('called ShowMods.refresh_widgets with args', args, kwargs)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        testobj.buttons = {}
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.refresh_widgets = mock_refresh
        callback1 = lambda: '0'
        callback2 = lambda: '1'
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
                "called HBox.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
                f"called PushButton.__init__ with args ('yyyyyy', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback2},)\n"
                "called PushButton.setToolTip with arg `yyyyyyyyy`\n"
                "called HBox.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
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
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called HBox.addStretch\n"
            "called HBox.addSpacing\n"
            "called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>"
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
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called HBox.addStretch\n"
            "called HBox.addSpacing\n"
            "called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>"
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
        def mock_accept(self):
            print('called SettingsDialog.accept')
        monkeypatch.setattr(testee.SettingsDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.SettingsDialog, 'accept', mock_accept)
        testobj = testee.SettingsDialog()
        assert capsys.readouterr().out == 'called SettingsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SettingsDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.SettingsDialog, 'select_modbase', lambda: 'dummy')
        monkeypatch.setattr(testee.SettingsDialog, 'select_download_path', lambda: 'dummy')
        monkeypatch.setattr(testee.SettingsDialog, 'select_savepath', lambda: 'dummy')
        monkeypatch.setattr(testee.SettingsDialog, 'update', lambda: 'dummy')
        parent = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        parent.master = types.SimpleNamespace(dialog_data=('xxx', 'yyy', 'zzz', 'qqq', 'rrr'))
        testobj = testee.SettingsDialog(parent)
        assert testobj.parent == parent
        # assert isinstance(testobj.lbox, testee.qtw.QComboBox)
        # assert isinstance(testobj.select_button, testee.qtw.QPushButton)
        # assert isinstance(testobj.name, testee.qtw.QComboBox)
        # assert isinstance(testobj.clear_name_button, testee.qtw.QPushButton)
        assert isinstance(testobj.modbase_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.select_modbase_button, testee.qtw.QPushButton)
        assert isinstance(testobj.config_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.download_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.select_download_button, testee.qtw.QPushButton)
        assert isinstance(testobj.savepath_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.select_savepath_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['sett'].format(testobj=testobj)

    def test_select_modbase(self, monkeypatch, capsys):
        """unittest for SettingsDialog.select_modbase
        """
        def mock_get(self, **kwargs):
            print('called FileDialog.getExistingDirectory with args', kwargs)
            return ''
        def mock_get_2(self, **kwargs):
            print('called FileDialog.getExistingDirectory with args', kwargs)
            return 'xxx'
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getExistingDirectory', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.modbase_text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.select_modbase()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called FileDialog.getExistingDirectory with args"
                " {'caption': 'Where to install downloaded mods?',"
                f" 'directory': '{testee.os.path.expanduser('~')}'}}\n")
        testobj.modbase_text = mockqtw.MockLineEdit('qqq')
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.select_modbase()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called FileDialog.getExistingDirectory with args"
                " {'caption': 'Where to install downloaded mods?', 'directory': 'qqq'}\n")
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getExistingDirectory', mock_get_2)
        testobj.select_modbase()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called FileDialog.getExistingDirectory with args"
                " {'caption': 'Where to install downloaded mods?', 'directory': 'qqq'}\n"
                "called LineEdit.setText with arg `xxx`\n")

    def test_select_download_path(self, monkeypatch, capsys):
        """unittest for SettingsDialog.select_modbase
        """
        def mock_get(self, **kwargs):
            print('called FileDialog.getExistingDirectory with args', kwargs)
            return ''
        def mock_get_2(self, **kwargs):
            print('called FileDialog.getExistingDirectory with args', kwargs)
            return 'xxx'
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getExistingDirectory', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.download_text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.select_download_path()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called FileDialog.getExistingDirectory with args"
                " {'caption': 'Where to download mods to?',"
                f" 'directory': '{testee.os.path.expanduser('~')}'}}\n")
        testobj.download_text = mockqtw.MockLineEdit('qqq')
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.select_download_path()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called FileDialog.getExistingDirectory with args"
                " {'caption': 'Where to download mods to?', 'directory': 'qqq'}\n")
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getExistingDirectory', mock_get_2)
        testobj.select_download_path()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called FileDialog.getExistingDirectory with args"
                " {'caption': 'Where to download mods to?', 'directory': 'qqq'}\n"
                "called LineEdit.setText with arg `xxx`\n")

    def test_select_savepath(self, monkeypatch, capsys):
        """unittest for SettingsDialog.select_modbase
        """
        def mock_get(self, **kwargs):
            print('called FileDialog.getExistingDirectory with args', kwargs)
            return ''
        def mock_get_2(self, **kwargs):
            print('called FileDialog.getExistingDirectory with args', kwargs)
            return 'xxx'
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getExistingDirectory', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.savepath_text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.select_savepath()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called FileDialog.getExistingDirectory with args"
                " {'caption': 'Where are the saved games stored?',"
                f" 'directory': '{testee.os.path.expanduser('~')}'}}\n")
        testobj.savepath_text = mockqtw.MockLineEdit('qqq')
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.select_savepath()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called FileDialog.getExistingDirectory with args"
                " {'caption': 'Where are the saved games stored?', 'directory': 'qqq'}\n")
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getExistingDirectory', mock_get_2)
        testobj.select_savepath()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called FileDialog.getExistingDirectory with args"
                " {'caption': 'Where are the saved games stored?', 'directory': 'qqq'}\n"
                "called LineEdit.setText with arg `xxx`\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for SettingsDialog.update
        """
        def mock_accept():
            print("called SettingsDialog.accept")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(master=types.SimpleNamespace())
        testobj.modbase_text = mockqtw.MockLineEdit('xx')
        testobj.config_text = mockqtw.MockLineEdit('yy')
        testobj.download_text = mockqtw.MockLineEdit('zz')
        testobj.columns = mockqtw.MockSpinBox()
        testobj.savepath_text = mockqtw.MockLineEdit('qq')
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled SpinBox.__init__\n"
                                           "called LineEdit.__init__\n")
        testobj.accept = mock_accept
        testobj.update()
        assert testobj.parent.master.dialog_data == ('xx', 'yy', 'zz', 0, 'qq')
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called SpinBox.value\n"
                                           "called LineEdit.text\n"
                                           "called SettingsDialog.accept\n")


class TestDeleteDialog:
    """unittests for qtgui.DeleteDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.DeleteDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called DeleteDialog.__init__ with args', args)
        def mock_accept(self):
            print('called DeleteDialog.accept')
        monkeypatch.setattr(testee.DeleteDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.DeleteDialog, 'accept', mock_accept)
        testobj = testee.DeleteDialog()
        assert capsys.readouterr().out == 'called DeleteDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for DeleteDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        # monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.DeleteDialog, 'process', lambda: 'dummy')
        monkeypatch.setattr(testee.DeleteDialog, 'update', lambda: 'dummy')
        parent = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        conf = MockConf()
        testobj = testee.DeleteDialog(parent, conf)
        assert testobj.parent == parent
        assert testobj.conf == conf
        assert testobj.modnames == {'xxx_name': 'xxx', 'yyy_name': 'yyy'}
        assert isinstance(testobj.lbox, testee.qtw.QComboBox)
        assert isinstance(testobj.change_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['delete'].format(testobj=testobj)

    def test_process(self, monkeypatch, capsys):
        """unittest for DeleteDialog.process
        """
        def mock_text(self):
            print('called ComboBox.currentText')
            return 'qqq'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.seltext = 'selected text'
        testobj.lbox = mockqtw.MockComboBox()
        testobj.change_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.process()
        assert testobj.choice == 'current text'
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called PushButton.setEnabled with arg `True`\n")
        testobj.seltext = 'qqq'
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', mock_text)
        testobj.process()
        assert testobj.choice == 'qqq'
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called PushButton.setEnabled with arg `False`\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for DeleteDialog.update
        """
        def mock_remove(*args):
            print('called Manager.remove_mod with args', args)
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(remove_mod=mock_remove))
        testobj.lbox = mockqtw.MockComboBox()
        testobj.change_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.choice = 'current text'
        testobj.update()
        assert capsys.readouterr().out == (
                "called Manager.remove_mod with args ('current text',)\n"
                "called MessageBox.information with args"
                f" `{testobj}` `SDVMM` `current text has been removed`\n"
                "called ComboBox.setCurrentIndex with arg `0`\n"
                "called PushButton.setDisabled with arg `True`\n")


class TestAttributesDialog:
    """unittests for qtgui.AttributesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.AttributesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called AttributesDialog.__init__ with args', args)
        def mock_accept(self):
            print('called AttributesDialog.accept')
        monkeypatch.setattr(testee.AttributesDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.AttributesDialog, 'accept', mock_accept)
        testobj = testee.AttributesDialog()
        assert capsys.readouterr().out == 'called AttributesDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for AttributesDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        # monkeypatch.setattr(mockqtw.MockComboBox, 'currentTextChanged', {str: mockqtw.MockSignal()})
        monkeypatch.setattr(testee.qgui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.AttributesDialog, 'process', lambda: 'dummy')
        monkeypatch.setattr(testee.AttributesDialog, 'clear_name_text', lambda: 'dummy')
        monkeypatch.setattr(testee.AttributesDialog, 'clear_text_text', lambda: 'dummy')
        monkeypatch.setattr(testee.AttributesDialog, 'update', lambda: 'dummy')
        parent = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        conf = MockConf()
        testobj = testee.AttributesDialog(parent, conf)
        assert testobj.parent == parent
        assert testobj.conf == conf
        assert testobj.modnames == {'xxx_name': 'xxx', 'yyy_name': 'yyy'}
        assert isinstance(testobj.lbox, testee.qtw.QComboBox)
        # assert isinstance(testobj.select_button, testee.qtw.QPushButton)
        assert isinstance(testobj.name, testee.qtw.QComboBox)
        assert isinstance(testobj.clear_name_button, testee.qtw.QPushButton)
        assert isinstance(testobj.text, testee.qtw.QLineEdit)
        assert isinstance(testobj.clear_text_button, testee.qtw.QPushButton)
        assert isinstance(testobj.activate_button, testee.qtw.QCheckBox)
        assert isinstance(testobj.comps_button, testee.qtw.QPushButton)
        assert isinstance(testobj.deps_button, testee.qtw.QPushButton)
        assert isinstance(testobj.change_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['attrs'].format(testobj=testobj)

    def test_enable_change(self, monkeypatch, capsys):
        """unittest for AttributesDialog.enable_change
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.change_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.enable_change()
        assert capsys.readouterr().out == "called PushButton.setEnabled with arg `True`\n"

    def test_process(self, monkeypatch, capsys):
        """unittest for AttributesDialog.process
        """
        def mock_list(self, name):
            "stub"
            print(f"called Conf.list_components_for_dir with arg '{name}'")
            return []
        def mock_text(self):
            print('called ComboBox.currentText')
            return 'qqq'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(
                    screeninfo={'current text': {'txt': 'xxx', 'sel': True, 'opt': False}}))
        testobj.modnames = {'current text': {'aaa'}}
        testobj.select_button = mockqtw.MockPushButton()
        testobj.lbox = mockqtw.MockComboBox()
        testobj.name = mockqtw.MockComboBox()
        testobj.clear_name_button = mockqtw.MockPushButton()
        testobj.text = mockqtw.MockLineEdit()
        testobj.clear_text_button = mockqtw.MockPushButton()
        testobj.activate_button = mockqtw.MockCheckBox()
        testobj.exempt_button = mockqtw.MockCheckBox()
        testobj.comps_button = mockqtw.MockPushButton()
        testobj.deps_button = mockqtw.MockPushButton()
        testobj.change_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called ComboBox.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called LineEdit.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.process()
        assert testobj.choice == 'current text'
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called ComboBox.clear\n"
                "called ComboBox.addItem with arg `current text`\n"
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called Conf.get_component_data with args ('xxx', 'Name')\n"
                "called Conf.get_component_data with args ('yyy', 'Name')\n"
                "called ComboBox.addItems with arg ['xxx_compname', 'yyy_compname']\n"
                "called ComboBox.setEnabled with arg True\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called LineEdit.setText with arg `xxx`\n"
                "called LineEdit.setEnabled with arg True\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setEnabled with arg True\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setEnabled with arg True\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called PushButton.setDisabled with arg `True`\n")
        monkeypatch.setattr(MockConf, 'list_components_for_dir', mock_list)
        testobj.process()
        assert testobj.choice == 'current text'
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called ComboBox.clear\n"
                "called ComboBox.addItem with arg `current text`\n"
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called ComboBox.addItems with arg []\n"
                "called ComboBox.setEnabled with arg True\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called LineEdit.setText with arg `xxx`\n"
                "called LineEdit.setEnabled with arg True\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setEnabled with arg True\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setEnabled with arg True\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called PushButton.setDisabled with arg `True`\n")
        testobj.seltext = 'qqq'
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', mock_text)
        testobj.process()
        assert testobj.choice == 'qqq'
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called ComboBox.clear\n"
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

    def test_clear_name_text(self, monkeypatch, capsys):
        """unittest for AttributesDialog.clear_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.name = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.clear_name_text()
        assert capsys.readouterr().out == "called LineEdit.clear\n"

    def test_clear_text_text(self, monkeypatch, capsys):
        """unittest for AttributesDialog.clear_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.clear_text_text()
        assert capsys.readouterr().out == "called LineEdit.clear\n"

    def test_view_components(self, monkeypatch, capsys):
        """unittest for AttributesDialog.view_components
        """
        def mock_get(name):
            "stub"
            print(f"called Manager.get_mod_components with arg '{name}'")
            return 'xxx'
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(get_mod_components=mock_get))
        # testobj.conf = MockConf()
        testobj.choice = 'xxx'
        testobj.modnames = {'xxx': {'aaa'}}
        testobj.view_components()
        assert capsys.readouterr().out == (
                # "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called Manager.get_mod_components with arg '{'aaa'}'\n"
                # "called Conf.get_component_data with args ('xxx', 'Name')\n"
                # "called Conf.get_component_data with args ('xxx', 'Version')\n"
                # "called Conf.get_component_data with args ('yyy', 'Name')\n"
                # "called Conf.get_component_data with args ('yyy', 'Version')\n"
                # f"called MessageBox.information with args `{testobj}` `SDVMM mod info`"
                # " `Components for xxx:\n  xxx_compname   xxx_version\n    (xxx)\n"
                # "  yyy_compname   yyy_version\n    (yyy)`\n")
                f"called MessageBox.information with args `{testobj}` `SDVMM mod info` `xxx`\n")

    def test_view_dependencies(self, monkeypatch, capsys):
        """unittest for AttributesDialog.view_dependencies
        """
        def mock_get(name):
            "stub"
            print(f"called Manager.get_mod_dependencies with arg '{name}'")
            return 'xxx'
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(get_mod_dependencies=mock_get))
        # testobj.conf = MockConf()
        testobj.choice = 'xxx'
        testobj.modnames = {'xxx': {'aaa'}}
        testobj.view_dependencies()
        assert capsys.readouterr().out == (
                # "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called Manager.get_mod_dependencies with arg '{'aaa'}'\n"
                # "called Conf.get_component_data with args ('xxx', 'Deps')\n"
                # "called Conf.get_component_data with args ('yyy', 'Deps')\n"
                # "called Conf.get_component_data with args ('xxx_depname', 'Name')\n"
                # "called Conf.get_component_data with args ('yyy_depname', 'Name')\n"
                # f"called MessageBox.information with args `{testobj}` `SDVMM mod info`"
                # " `Dependencies for xxx:\n"
                # " xxx_depname_compname (xxx_depname)\n"
                # " yyy_depname_compname (yyy_depname)`\n")
                f"called MessageBox.information with args `{testobj}` `SDVMM mod info` `xxx`\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for AttributesDialog.update
        """
        def mock_update(*args):
            print('called Manager.update_attributes with args', args)
            return False, 'xxxx'
        def mock_update_2(*args):
            print('called Manager.update_attributes with args', args)
            return True, ''
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(
                    # screeninfo={'current text': {'txt': 'xxx', 'sel': True, 'pos': '2x2'}},
                    # attr_changes=[],
                    update_attributes=mock_update))
                # refresh_widgets=mock_refresh,
                # build_screen_text=mock_build)
        testobj.name = mockqtw.MockComboBox()
        testobj.clear_name_button = mockqtw.MockPushButton()
        testobj.text = mockqtw.MockLineEdit()
        testobj.clear_text_button = mockqtw.MockPushButton()
        testobj.activate_button = mockqtw.MockCheckBox()
        testobj.exempt_button = mockqtw.MockCheckBox()
        testobj.change_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called LineEdit.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.choice = 'current text'
        testobj.update()
        # assert testobj.parent.master.screeninfo == {'current text': {'txt': '', 'sel': False,
        #                                                              'opt': False, 'pos': '2x2'}}
        # assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == (
                # "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called CheckBox.isChecked\n"
                "called LineEdit.text\n"
                "called ComboBox.currentText\n"
                "called CheckBox.isChecked\n"
                "called Manager.update_attributes with args"
                " (False, 'current text', 'current text', '', False)\n"
                f"called MessageBox.information with args `{testobj}` `SDVMM` `xxxx`\n")
                # "called AttributeDialog.switch_selectability with args"
                # " (False, 'current text', 'current text')\n"
                # f"called MessageBox.information with args `{testobj}` `SDVMM`"
                # " `Onselecteerbaar maken van mods met coordinaten in de config"
                # " is helaas nog niet mogelijk`\n")
        testobj.parent.master.update_attributes = mock_update_2
        testobj.update()
        assert capsys.readouterr().out == (
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called CheckBox.isChecked\n"
                "called LineEdit.text\n"
                "called ComboBox.currentText\n"
                "called CheckBox.isChecked\n"
                "called Manager.update_attributes with args"
                " (False, 'current text', 'current text', '', False)\n"
                "called PushButton.setDisabled with arg `True`\n")


class TestSaveGamesDialog:
    """unittests for qtgui.SaveGamesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SaveGamesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called SaveGamesDialog.__init__ with args', args)
        # def mock_accept(self):
        #     print('called SaveGamesDialog.accept')
        monkeypatch.setattr(testee.SaveGamesDialog, '__init__', mock_init)
        # monkeypatch.setattr(testee.SaveGamesDialog, 'accept', mock_accept)
        testobj = testee.SaveGamesDialog()
        assert capsys.readouterr().out == 'called SaveGamesDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SaveGamesDialog.__init__
        """
        def mock_add(self):
            print('called SaveGamesDialog.add_modselector')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        # monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        # monkeypatch.setattr(mockqtw.MockComboBox, 'currentTextChanged', {str: mockqtw.MockSignal()})
        # monkeypatch.setattr(testee.qgui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.SaveGamesDialog, 'confirm', lambda: 'dummy')
        monkeypatch.setattr(testee.SaveGamesDialog, 'update', lambda: 'dummy')
        monkeypatch.setattr(testee.SaveGamesDialog, 'add_modselector', mock_add)
        parent = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        conf = MockConf()
        testobj = testee.SaveGamesDialog(parent, conf)
        assert testobj.parent == parent
        assert testobj.conf == conf
        assert testobj.savenames == ['qqq', 'rrr']
        assert testobj.modnames == {'xxx_name': 'xxx', 'yyy_name': 'yyy'}
        assert isinstance(testobj.savegame_selector, testee.qtw.QComboBox)
        assert isinstance(testobj.pname, testee.qtw.QLineEdit)
        assert isinstance(testobj.fname, testee.qtw.QLineEdit)
        assert isinstance(testobj.gdate, testee.qtw.QLineEdit)
        assert isinstance(testobj.update_button, testee.qtw.QPushButton)
        assert isinstance(testobj.confirm_button, testee.qtw.QPushButton)
        assert testobj.oldsavename == ''
        assert testobj.widgets == []
        assert isinstance(testobj.vbox2, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == expected_output['saves'].format(testobj=testobj)

    def test_enable_change(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.enable_change
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.enable_change()
        assert capsys.readouterr().out == "called PushButton.setEnabled with arg `True`\n"

    def test_add_modselector(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.add_modselector
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qgui, 'QIcon', mockqtw.MockIcon)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox2 = mockqtw.MockVBoxLayout()
        testobj.modnames = ['yyy', 'xxx']
        testobj.widgets = []
        testobj.add_modselector()
        assert len(testobj.widgets) == 1
        assert isinstance(testobj.widgets[0][0], testee.qtw.QPushButton)
        assert isinstance(testobj.widgets[0][1], testee.qtw.QComboBox)
        assert isinstance(testobj.widgets[0][2], testee.qtw.QHBoxLayout)
        assert capsys.readouterr().out == (
            "called VBox.__init__\n"
            "called HBox.__init__\n"
            "called ComboBox.__init__\n"
            "called ComboBox.setEditable with arg `False`\n"
            "called ComboBox.addItems with arg ['select a mod']\n"
            "called ComboBox.addItems with arg ['xxx', 'yyy']\n"
            f"called Signal.connect with args (functools.partial({testobj.process_mod},"
            f" {testobj.widgets[0][1]}),)\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>\n"
            "called PushButton.__init__ with args () {}\n"
            "called Icon.fromTheme with args ()\n"
            "called PushButton.setIcon with arg `None`\n"
            "called PushButton.setFixedSize with args (24, 24)\n"
            "called PushButton.setEnabled with arg `False`\n"
            f"called Signal.connect with args (functools.partial({testobj.remove_mod},"
            f" {testobj.widgets[0][0]}),)\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            "called VBox.insertLayout with arg1 0 and arg2 of type"
            " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n")

    def test_process_mod(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.process_mod
        """
        def mock_add():
            print('called SaveGamesDialog.add_modselector')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_modselector = mock_add
        testobj.update_button = mockqtw.MockPushButton()
        testobj.widgets = []
        lbox = mockqtw.MockComboBox()
        btn = mockqtw.MockPushButton()
        lbox2 = mockqtw.MockComboBox()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called ComboBox.__init__\n")
        testobj.process_mod(lbox, 'select a mod')
        assert capsys.readouterr().out == ""
        with pytest.raises(IndexError):
            testobj.process_mod(lbox, 'xxxx')
        assert capsys.readouterr().out == "called PushButton.setEnabled with arg `True`\n"
        testobj.widgets = [['qq', 'rr', 'ss']]
        testobj.process_mod(lbox, 'xxxx')
        assert capsys.readouterr().out == "called PushButton.setEnabled with arg `True`\n"
        testobj.widgets = [['qq', lbox2, 'ss'], [btn, lbox, 'ss']]
        testobj.process_mod(lbox, 'xxxx')
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called SaveGamesDialog.add_modselector\n")

    def test_remove_mod(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.remove_mod
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.widgets = []
        lbox = mockqtw.MockComboBox()
        btn = mockqtw.MockPushButton()
        hbox = mockqtw.MockHBoxLayout()
        testobj.vbox2 = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called HBox.__init__\n"
                                           "called VBox.__init__\n")
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
        assert capsys.readouterr().out == (
                "called VBox.removeWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
                "called PushButton.close\n"
                "called VBox.removeWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockComboBox'>\n"
                "called ComboBox.close\n"
                "called VBox.removeItem\n")

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
        def mock_exists(*args):
            print('called os.path.exists with args', args)
            return False
        def mock_exists_2(*args):
            print('called os.path.exists with args', args)
            return True
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        monkeypatch.setattr(testee.os.path, 'exists', mock_exists)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        testobj.conf.get_diritem_data = mock_get_diritem_data
        testobj.conf.get_component_data = mock_get_component_data
        testobj.conf.get_mods_for_saveitem = mock_get_mods
        testobj.parent = mockqtw.MockWidget()
        # testobj.parent.refresh_widget_data = mock_refresh
        testobj.parent.master = MockManager()
        testobj.savegame_selector = mockqtw.MockComboBox()
        testobj.savegame_selector.setCurrentText('ppp')
        assert capsys.readouterr().out == ("called Widget.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called ComboBox.setCurrentText with arg `ppp`\n")
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called Conf.get_mods_for_saveitem with arg current text\n"
                "called Conf.list_all_mod_dirs\n"
                "called Conf.get_diritem_data with args ('xxx', '_DoNotTouch')\n"
                "called Conf.get_diritem_data with args ('yyy', '_DoNotTouch')\n"
                "called os.path.exists with args ('modbase/yyy',)\n"
                "called Manager.select_activations with arg ['qqq', 'rrr']\n"
                "called Manager.activate\n"
                "called Manager.refresh_widget_data\n"
                "called MessageBox.information with args"
                f" `{testobj}` `Change Config` `wijzigingen zijn doorgevoerd`\n")

        monkeypatch.setattr(MockManager, 'select_activations', mock_select)
        monkeypatch.setattr(testee.os.path, 'exists', mock_exists_2)
        testobj.conf.list_components_for_dir = mock_list_comps
        testobj.parent.master.directories = ['sss', 'ttt']
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called Conf.get_mods_for_saveitem with arg current text\n"
                "called Conf.list_all_mod_dirs\n"
                "called Conf.get_diritem_data with args ('xxx', '_DoNotTouch')\n"
                "called Conf.get_diritem_data with args ('yyy', '_DoNotTouch')\n"
                "called os.path.exists with args ('modbase/yyy',)\n"
                "called Conf.get_diritem_data with args ('yyy', 'SCRNAM')\n"
                "called Manager.select_activations with arg ['qqq', 'rrr', 'yyy']\n"
                "called Manager.refresh_widget_data\n"
                "called MessageBox.information with args"
                f" `{testobj}` `Change Config` `wijzigingen zijn doorgevoerd`\n")

        testobj.conf.list_all_mod_dirs = mock_list_dirs
        testobj.parent.master.directories = ['sss', 'ttt']
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called Conf.get_mods_for_saveitem with arg current text\n"
                "called Conf.list_all_mod_dirs\n"
                "called Manager.select_activations with arg ['qqq', 'rrr']\n"
                "called Manager.refresh_widget_data\n"
                "called MessageBox.information with args"
                f" `{testobj}` `Change Config` `wijzigingen zijn doorgevoerd`\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.update
        """
        def mock_update(arg):
            print(f"called SaveGameDialog.update_conf with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update_conf = mock_update
        # testobj.conf = MockConf()
        testobj.savegame_selector = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.update()
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called SaveGameDialog.update_conf with arg 'current text'\n")

    def test_update_conf(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.update
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pname = mockqtw.MockLineEdit('xxx')
        testobj.fname = mockqtw.MockLineEdit('yyy')
        testobj.gdate = mockqtw.MockLineEdit('zzz')
        testobj.update_button = mockqtw.MockPushButton()
        testobj.conf = MockConf()
        testobj.widgets = []
        lbox = mockqtw.MockComboBox()
        testobj.old_pname = 'xxx'
        testobj.old_fname = 'yyy'
        testobj.old_gdate = 'zzz'
        testobj.oldmods = []
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called ComboBox.__init__\n")
        testobj.update_conf('save_name')
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called Conf.save\n"
                                           "called PushButton.setDisabled with arg `True`\n")
        testobj.widgets = [lbox]
        testobj.oldmods = ['current text']
        testobj.update_conf('save_name')
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Mods', [])\n"
                "called Conf.save\n"
                "called PushButton.setDisabled with arg `True`\n")

        testobj.old_pname = 'aaa'
        testobj.old_fname = 'bbb'
        testobj.old_gdate = 'ccc'
        testobj.oldmods = ['qqq']
        testobj.update_conf('save_name')
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Pname', 'xxx')\n"
                "called LineEdit.text\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Fname', 'yyy')\n"
                "called LineEdit.text\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Gdate', 'zzz')\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Mods', [])\n"
                "called Conf.save\n"
                "called PushButton.setDisabled with arg `True`\n")

    def test_get_savedata(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.get_savedata
        """
        def mock_update(name):
            print(f'called SaveGamesDialog with arg {name}')
        def mock_add(self):
            print('called SaveGamesDialog.add_modselector')
            self.widgets = [[btn, lbox, hbox]]
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
        btn = mockqtw.MockPushButton()
        lbox = mockqtw.MockComboBox()
        hbox = mockqtw.MockHBoxLayout()
        testobj.vbox2 = mockqtw.MockVBoxLayout()
        testobj.pname = mockqtw.MockLineEdit()
        testobj.fname = mockqtw.MockLineEdit()
        testobj.gdate = mockqtw.MockLineEdit()
        testobj.update_button = mockqtw.MockPushButton()
        testobj.confirm_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called ComboBox.__init__\n"
                                           "called HBox.__init__\n"
                                           "called VBox.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.widgets = []

        testobj.get_savedata('select a saved game')
        assert capsys.readouterr().out == ""

        testobj.oldsavename = ''
        testobj.get_savedata('xxx')
        assert capsys.readouterr().out == ("called Conf.get_saveitem_attrs with arg xxx\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
        testobj.oldsavename = 'yyy'
        testobj.get_savedata('xxx')
        assert capsys.readouterr().out == ("called SaveGamesDialog with arg yyy\n"
                                           "called SaveGamesDialog.add_modselector\n"
                                           "called Conf.get_saveitem_attrs with arg xxx\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
        testobj.widgets = [[btn, lbox, hbox]]
        testobj.conf.get_saveitem_attrs = mock_get_attrs
        testobj.conf.get_mods_for_saveitem = mock_get_mods
        testobj.get_savedata('xxx')
        assert capsys.readouterr().out == ("called SaveGamesDialog with arg xxx\n"
                                           "called PushButton.close\n"
                                           "called ComboBox.close\n"
                                           "called VBox.removeItem\n"
                                           "called SaveGamesDialog.add_modselector\n"
                                           "called Conf.get_saveitem_attrs with arg xxx\n"
                                           "called LineEdit.setText with arg `oldpname`\n"
                                           "called LineEdit.setText with arg `oldfname`\n"
                                           "called LineEdit.setText with arg `oldgdate`\n"
                                           "called Conf.get_mods_for_saveitem with arg xxx\n"
                                           "called ComboBox.setCurrentText with arg `newmodname`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
        testobj.widgets = [[btn, lbox, hbox]]
        testobj.conf.get_saveitem_attrs = mock_get_attrs_2
        testobj.conf.get_mods_for_saveitem = mock_get_mods
        testobj.get_savedata('xxx')
        assert capsys.readouterr().out == ("called SaveGamesDialog with arg xxx\n"
                                           "called PushButton.close\n"
                                           "called ComboBox.close\n"
                                           "called VBox.removeItem\n"
                                           "called SaveGamesDialog.add_modselector\n"
                                           "called Conf.get_saveitem_attrs with arg xxx\n"
                                           "called LineEdit.setText with arg `oldpname`\n"
                                           "called LineEdit.setText with arg `oldfname`\n"
                                           "called LineEdit.setText with arg `oldgdate`\n"
                                           "called Conf.get_mods_for_saveitem with arg xxx\n"
                                           "called ComboBox.setCurrentText with arg `newmodname`\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
