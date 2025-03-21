"""unittests for ./qtgui.py
"""
import types
import pytest
import mockgui.mockqtwidgets as mockqtw
from src import qtgui as testee

showmods = """\
called QWidget.setWindowTitle()
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('Dit overzicht toont de namen van mods die je kunt activeren (inclusief die al geactiveerd zijn).\\nIn de achterliggende configuratie is geregeld welke mods hiervoor eventueel nog meer aangezet moeten worden\\nDe onderstreepte items zijn hyperlinks; ze leiden naar de pagina waarvandaan ik ze van gedownload heb (doorgaans op Nexus)',)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Grid.__init__
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called Label.__init__ with args ('Hieronder volgen afhankelijkheden; deze zijn niet apart te activeren maar je kunt wel zien of ze actief zijn',)
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called Grid.__init__
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called PushButton.__init__ with args ('&Mod attributes', {testobj}) {{}}
called PushButton.__init__ with args ('&Activate changes', {testobj}) {{}}
called PushButton.__init__ with args ('&Select Savefile', {testobj}) {{}}
called ShowMods.refresh_widgets with args () {{'first_time': True}}
called VBox.addSpacing
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('Set &Defaults', {testobj}) {{}}
called Signal.connect with args ({testobj.master.manage_defaults},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Install / update', {testobj}) {{}}
called PushButton.setToolTip with arg `Selecteer uit een lijst met recent gedownloade mods één of meer om te installeren`
called Signal.connect with args ({testobj.update},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called Signal.connect with args ({testobj.master.manage_attributes},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called Signal.connect with args ({testobj.confirm},)
called PushButton.setEnabled with arg `False`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called Signal.connect with args ({testobj.master.manage_savefiles},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Close', {testobj}) {{}}
called Signal.connect with args ({testobj.close},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called QWidget.setLayout()
"""
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
called Label.__init__ with args ('Location for save files:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (3, 0)
called LineEdit.__init__
called LineEdit.setText with arg `qqq`
called LineEdit.setMinimumWidth with arg `380`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (3, 1)
called PushButton.__init__ with args ('Browse', {testobj}) {{}}
called Signal.connect with args ({testobj.select_savepath},)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'> at (3, 2)
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
called Signal.connect with args ({testobj.update_all},)
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
    results = {'showmods': showmods, 'sett': sett, 'attrs': attrs, 'saves': saveitems}
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
    def select_activations(self, names):
        """stub
        """
        print(f'called Manager.select_activations with arg {names}')
        self.directories = ['x']
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
    """unittest for gui.show_dialog
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
    """unittest for gui.ShowMods
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui.ShowMods object

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
            print('called QWidget.__init__()')
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_app_init)
        monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
        testobj = testee.ShowMods(MockManager())
        assert capsys.readouterr().out == (
            'called QApplication.__init__()\n'
            'called QWidget.__init__()\n')
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
        master = types.SimpleNamespace()
        testobj = testee.ShowMods(master)
        assert isinstance(testobj, testee.qtw.QWidget)
        assert testobj.master == master
        # assert testobj.filenames == ['file', 'name']
        assert hasattr(testobj, 'app')
        assert isinstance(testobj.app, testee.qtw.QApplication)
        assert capsys.readouterr().out == (
            'called QApplication.__init__()\n'
            'called QWidget.__init__()\n')

    # 67-85
    def test_setup_screen(self, monkeypatch, capsys, expected_output):
        """unittest for ShowMods.setup_screen
        """
        def mock_setWindowTitle(self, *args):
            """stub
            """
            print('called QWidget.setWindowTitle()')
        def mock_refresh(*args, **kwargs):
            """stub
            """
            print('called ShowMods.refresh_widgets with args', args, kwargs)
        def mock_setLayout(self, *args):
            """stub
            """
            print('called QWidget.setLayout()')
        monkeypatch.setattr(testee.qtw.QWidget, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh_widgets = mock_refresh
        testobj.setup_screen()
        assert capsys.readouterr().out == expected_output['showmods'].format(testobj=testobj)

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
            print('called QApplication.exec()')
            return 'okcode'
        def mock_show(self, *args):
            """stub
            """
            print('called QWidget.show()')
        monkeypatch.setattr(testee.qtw.QApplication, 'exec', mock_app_exec)
        monkeypatch.setattr(testee.qtw.QWidget, 'show', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_screen() == "okcode"
        assert capsys.readouterr().out == ('called QWidget.show()\n'
                                          'called QApplication.exec()\n')

    def test_confirm(self, monkeypatch, capsys):
        """unittest for ShowMods.confirm
        """
        def mock_select(self, arg):
            """stub
            """
            print('called Manager.select_activations with arg', arg)
            self.directories = []
        def mock_refresh(**kwargs):
            """stub
            """
            print('called ShowMods.refresh_widgets with args', kwargs)
        def mock_information(self, *args):
            """stub
            """
            print('called MessageBox.information with args', args)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.plotted_widgets = {}
        testobj.unplotted_widgets = {}
        testobj.activate_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.refresh_widgets = mock_refresh
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called Manager.select_activations with arg []\n"
                'called Manager.activate\n'
                "called MessageBox.information with args"
                " ('Change Config', 'wijzigingen zijn doorgevoerd')\n"
                "called PushButton.setEnabled with arg `False`\n")
        check_on = mockqtw.MockCheckBox()
        check_on.setChecked(True)
        check_off = mockqtw.MockCheckBox()
        testobj.plotted_widgets = {'xxx': ('hbox1', mockqtw.MockLabel('Xxxxx'), check_on),
                                   'yyy': ('hbox2', mockqtw.MockLabel('tt>Yyyy<uu'), check_off)}
        testobj.unplotted_widgets = {'aaa': ('hbox3', mockqtw.MockLabel('Aaaaa'), check_off),
                                     'bbb': ('hbox4', mockqtw.MockLabel('tt>Bbbb<uu'), check_on)}
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.__init__\n"
                                           "called Label.__init__ with args ('Xxxxx',)\n"
                                           "called Label.__init__ with args ('tt>Yyyy<uu',)\n"
                                           "called Label.__init__ with args ('Aaaaa',)\n"
                                           "called Label.__init__ with args ('tt>Bbbb<uu',)\n")
        monkeypatch.setattr(MockManager, 'select_activations', mock_select)
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                "called Manager.select_activations with arg ['Xxxxx', 'Bbbb']\n"
                "called MessageBox.information with args"
                " ('Change Config', 'wijzigingen zijn doorgevoerd')\n"
                "called PushButton.setEnabled with arg `False`\n")

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
        testobj.master.screeninfo = {}
        testobj.plotted_widgets = {}
        testobj.plotted_positions = {}
        testobj.lastrow = 0
        testobj.lastcol = 0
        testobj.unplotted = []
        testobj.unplotted_widgets = {}
        # testobj.unplotted_positions = {}
        testobj.not_selectable = []
        testobj.nonsel_widgets = {}
        # testobj.nonsel_positions = {}
        testobj.gbox1 = mockqtw.MockGridLayout()
        testobj.gbox2 = mockqtw.MockGridLayout()
        testobj.attr_button = mockqtw.MockPushButton()
        testobj.select_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called Grid.__init__\ncalled Grid.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.add_checkbox = mock_add
        testobj.add_items_to_grid = mock_add_items
        testobj.refresh_widget_data = mock_refresh
        testobj.refresh_widgets()
        assert testobj.plotted_widgets == {}
        assert testobj.plotted_positions == {}
        assert testobj.lastrow == 0
        assert testobj.lastcol == 0
        assert testobj.unplotted == []
        assert testobj.unplotted_widgets == {}
        assert testobj.unplotted_positions == {}
        assert testobj.not_selectable == []
        assert testobj.nonsel_widgets == {}
        assert testobj.nonsel_positions == {}
        assert capsys.readouterr().out == (
                "called PushButton.setEnabled with arg `False`\n"
                "called PushButton.setEnabled with arg `False`\n"
                f"called Showmods.add_items_to_grid with args ({testobj.gbox1}, 0, 0, [])\n"
                f"called Showmods.add_items_to_grid with args ({testobj.gbox2}, 0, -1, [])\n"
                "called Showmods.refresh_widget_data with args {'texts_also': True}\n")
                # "called Showmods.set_texts_for_grid with args ({}, {})\n"
                # "called Showmods.set_texts_for_grid with args ({}, {})\n"
                # "called Showmods.set_checks_for_grid with args ({}, {})\n"
                # "called Showmods.set_checks_for_grid with args ({}, {})\n")
        label1 = mockqtw.MockLabel()
        check1 = mockqtw.MockCheckBox()
        label2 = mockqtw.MockLabel()
        check2 = mockqtw.MockCheckBox()
        testobj.unplotted_widgets = {(1, 1): ('', label1, check1)}
        testobj.nonsel_widgets = {(2, 2): ('', label2, check2)}
        assert capsys.readouterr().out == ("called Label.__init__\ncalled CheckBox.__init__\n"
                                           "called Label.__init__\ncalled CheckBox.__init__\n")
        testobj.refresh_widgets()
        assert testobj.plotted_widgets == {}
        assert testobj.plotted_positions == {}
        assert testobj.lastrow == 0
        assert testobj.lastcol == 0
        assert testobj.unplotted == []
        assert testobj.unplotted_widgets == {}
        assert testobj.unplotted_positions == {}
        assert testobj.not_selectable == []
        assert testobj.nonsel_widgets == {}
        assert testobj.nonsel_positions == {}
        assert capsys.readouterr().out == (
                "called PushButton.setEnabled with arg `False`\n"
                "called PushButton.setEnabled with arg `False`\n"
                "called CheckBox.close\n"
                "called Label.close\n"
                "called Grid.itemAtPosition with args (1, 1)\n"
                "called Grid.removeItem with args (None,)\n"
                "called CheckBox.close\n"
                "called Label.close\n"
                "called Grid.itemAtPosition with args (2, 2)\n"
                "called Grid.removeItem with args (None,)\n"
                f"called Showmods.add_items_to_grid with args ({testobj.gbox1}, 0, 0, [])\n"
                f"called Showmods.add_items_to_grid with args ({testobj.gbox2}, 0, -1, [])\n"
                "called Showmods.refresh_widget_data with args {'texts_also': True}\n")
                # "called Showmods.set_texts_for_grid with args ({}, {})\n"
                # "called Showmods.set_texts_for_grid with args ({}, {})\n"
                # "called Showmods.set_checks_for_grid with args ({}, {})\n"
                # "called Showmods.set_checks_for_grid with args ({}, {})\n")
        testobj.master.screeninfo = {'xx': {'pos': '1x1', 'sel': True},
                                     'yy': {'pos': '', 'sel': True},
                                     'zz': {'pos': '', 'sel': False}}
        testobj.refresh_widgets(first_time=True)
        assert testobj.plotted_widgets == {(1, 1): ('x', 'y', 'z')}
        assert testobj.plotted_positions == {(1, 1): ('xx', {'pos': '1x1', 'sel': True})}
        assert testobj.lastrow == 1
        assert testobj.lastcol == 1
        assert testobj.unplotted == ['yy']
        assert testobj.not_selectable == ['zz']
        assert capsys.readouterr().out == (
                "called PushButton.setEnabled with arg `True`\n"
                "called PushButton.setEnabled with arg `True`\n"
                "called ShowMods.add_checkbox\n"
                "called Grid.addLayout with arg of type <class 'str'> at (1, 1)\n"
                f"called Showmods.add_items_to_grid with args ({testobj.gbox1}, 1, 1, ['yy'])\n"
                f"called Showmods.add_items_to_grid with args ({testobj.gbox2}, 0, -1, ['zz'])\n"
                "called Showmods.refresh_widget_data with args {'texts_also': True}\n")

    def test_refresh_widget_data(self, monkeypatch, capsys):
        """unittest for ShowMods.refresh_widgets
        """
        def mock_set1(*args):
            print("called Showmods.set_texts_for_grid with args", args)
        def mock_set2(*args):
            print("called Showmods.set_checks_for_grid with args", args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_texts_for_grid = mock_set1
        testobj.set_checks_for_grid = mock_set2
        testobj.plotted_widgets = {'x': '1', 'y': '2'}
        testobj.plotted_positions = {'a': 1, 'b': 2}
        testobj.unplotted_widgets = {'x': '3', 'z': '4'}
        testobj.unplotted_positions = {'a': 3, 'c': 4}
        testobj.nonsel_widgets = {'q': 'r'}
        testobj.nonsel_positions = {'p': 's'}
        testobj.refresh_widget_data()
        assert capsys.readouterr().out == (
                "called Showmods.set_checks_for_grid with args"
                " ({'a': 3, 'b': 2, 'c': 4}, {'x': '3', 'y': '2', 'z': '4'})\n"
                "called Showmods.set_checks_for_grid with args ({'p': 's'}, {'q': 'r'})\n")
        testobj.refresh_widget_data(texts_also=True)
        assert capsys.readouterr().out == (
                "called Showmods.set_texts_for_grid with args"
                " ({'a': 3, 'b': 2, 'c': 4}, {'x': '3', 'y': '2', 'z': '4'})\n"
                "called Showmods.set_texts_for_grid with args ({'p': 's'}, {'q': 'r'})\n"
                "called Showmods.set_checks_for_grid with args"
                " ({'a': 3, 'b': 2, 'c': 4}, {'x': '3', 'y': '2', 'z': '4'})\n"
                "called Showmods.set_checks_for_grid with args ({'p': 's'}, {'q': 'r'})\n")

    def test_add_items_to_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.add_items_to_grid
        """
        def mock_add(*args):
            print("called ShowMods.add_checkbox")
            return 'hbox', 'btn', cbox
        testobj = self.setup_testobj(monkeypatch, capsys)
        cbox = mockqtw.MockCheckBox()
        testobj.add_checkbox = mock_add
        testobj.master.screeninfo = {'x': {'sel': True}, 'y': {'sel': True}, 'z': {'sel': False}}
        gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called CheckBox.__init__\ncalled Grid.__init__\n"
        assert testobj.add_items_to_grid(gbox, 1, 1, []) == ({}, {})
        assert capsys.readouterr().out == ""
        assert testobj.add_items_to_grid(gbox, 1, 1, ['x', 'y', 'z']) == (
                {(1, 2): ('x', {'pos': '1x2', 'sel': True}),
                 (2, 0): ('y', {'pos': '2x0', 'sel': True}),
                 (2, 1): ('z', {'pos': '2x1', 'sel': False})},
                {(1, 2): ('hbox', 'btn', cbox), (2, 0): ('hbox', 'btn', cbox),
                 (2, 1): ('hbox', 'btn', cbox)})
        assert capsys.readouterr().out == (
                "called ShowMods.add_checkbox\n"
                "called Grid.addLayout with arg of type <class 'str'> at (1, 2)\n"
                "called ShowMods.add_checkbox\n"
                "called Grid.addLayout with arg of type <class 'str'> at (2, 0)\n"
                "called ShowMods.add_checkbox\n"
                "called Grid.addLayout with arg of type <class 'str'> at (2, 1)\n")

    def test_set_texts_for_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.set_texts_for_grid
        """
        def mock_build(*args):
            print('called ShowMods.build_screen_text with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.build_screen_text = mock_build
        widgets = {}
        positions = {}
        testobj.set_texts_for_grid(positions, widgets)
        assert capsys.readouterr().out == ""
        widgets = {(0, 1): ('', 'label1', ''), (1, 1): ('', 'label2', '')}
        positions = {(0, 1): ('aaa', {'txt': '', 'key': ''}),
                     (1, 1): ('bbb', {'txt': 'xxx', 'key': 'yyy'})}
        testobj.set_texts_for_grid(positions, widgets)
        assert capsys.readouterr().out == (
                "called ShowMods.build_screen_text with args ('label1', 'aaa', '', '')\n"
                "called ShowMods.build_screen_text with args ('label2', 'bbb', 'xxx', 'yyy')\n")

    def test_set_checks_for_grid(self, monkeypatch, capsys, tmp_path):
        """unittest for ShowMods.set_checks_for_grid
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj.master, 'modbase', tmp_path)
        (tmp_path / 'xxx').mkdir()
        testobj.enable_button = lambda x: 'dummy'
        widgets = {}
        positions = {}
        testobj.set_checks_for_grid(positions, widgets)
        assert capsys.readouterr().out == ""
        check1 = mockqtw.MockCheckBox()
        check2 = mockqtw.MockCheckBox()
        check3 = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\n")
        widgets = {(0, 1): ('', '', check1), (1, 1): ('', '', check2), (1, 2): ('', '', check3)}
        positions = {(0, 1): ('aaa', {'dir': 'qqq', 'sel': True}),
                     (1, 1): ('bbb', {'dir': 'xxx', 'sel': True}),
                     (1, 2): ('ccc', {'dir': 'rrr', 'sel': False})}
        testobj.set_checks_for_grid(positions, widgets)
        assert capsys.readouterr().out == (
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setChecked with arg False\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for ShowMods.add_checkbox
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.screentext = {}
        obj1, obj2, obj3 = testobj.add_checkbox(False)
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
            "called HBox.addSpacing\n")
        obj1, obj2, obj3 = testobj.add_checkbox(True)
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
            "called HBox.addSpacing\n")

    def test_enable_button(self, monkeypatch, capsys):
        """unittest for ShowMods.enable_button
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.activate_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == 'called PushButton.__init__ with args () {}\n'
        testobj.enable_button()
        assert capsys.readouterr().out == 'called PushButton.setEnabled with arg `True`\n'

    def test_update(self, monkeypatch, capsys):
        """unittest for ShowMods.update
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
        testobj.master.update_mods = mock_update
        testobj.update()
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileNames with args {testobj} ()"
                " {'caption': 'Install downloaded mods', 'directory': 'Downloads',"
                " 'filter': 'Zip files (*.zip)'}\n")

        monkeypatch.setattr(mockqtw.MockFileDialog, 'getOpenFileNames', mock_open)
        testobj.update()
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileNames with args {testobj} ()"
                " {'caption': 'Install downloaded mods', 'directory': 'Downloads',"
                " 'filter': 'Zip files (*.zip)'}\n"
                "called Manager.update_mods with arg ['name1', 'name2']\n"
                "called MessageBox.information with args ('Change Config', 'xxx\\nyyy')\n")

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

    def test_build_screen_text(self, monkeypatch, capsys):
        """unittest for ShowMods.build_screen_text
        """
        label = mockqtw.MockLabel()
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.build_screen_text(label, 'xxx', '', '')
        assert capsys.readouterr().out == ("called Label.setText with arg `xxx`\n")
        testobj.build_screen_text(label, 'xxx', 'yyy', 'zz')
        assert capsys.readouterr().out == (
                "called Label.setOpenExternalLinks with arg 'True'\n"
                'called Label.setText with arg'
                ' `<a href="https://www.nexusmods.com/stardewvalley/mods/zz">xxx</a> yyy`\n')


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
        return []
    def get_mods_for_saveitem(self, name):
        "stub"
        print(f"called Conf.get_mods_for_saveitem with arg {name}")
        return []
    def update_saveitem_data(self, *args):
        "stub"
        print('called Conf.update_saveitem_data with args', args)


class TestSettingsDialog:
    """unittest for gui.SettingsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui.SettingsDialog object

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
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.SettingsDialog, 'select_modbase', lambda: 'dummy')
        monkeypatch.setattr(testee.SettingsDialog, 'select_download_path', lambda: 'dummy')
        monkeypatch.setattr(testee.SettingsDialog, 'select_savepath', lambda: 'dummy')
        monkeypatch.setattr(testee.SettingsDialog, 'update', lambda: 'dummy')
        parent = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        parent.master = types.SimpleNamespace(dialog_data=('xxx', 'yyy', 'zzz', 'qqq'))
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
        testobj.savepath_text = mockqtw.MockLineEdit('qq')
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n")
        testobj.accept = mock_accept
        testobj.update()
        assert testobj.parent.master.dialog_data == ('xx', 'yy', 'zz', 'qq')
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called SettingsDialog.accept\n")


class TestAttributesDialog:
    """unittest for gui.AttributesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui.AttributesDialog object

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

    def test_enable_select(self, monkeypatch, capsys):
        """unittest for AttributesDialog.enable_select
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_button = mockqtw.MockPushButton()
        testobj.comps_button = mockqtw.MockPushButton()
        testobj.deps_button = mockqtw.MockPushButton()
        testobj.change_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.enable_select()
        assert capsys.readouterr().out == ("called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n")

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
                "called ComboBox.setEnabled with arg False\n"
                "called LineEdit.setEnabled with arg False\n"
                "called CheckBox.setDisabled with arg True\n"
                "called CheckBox.setDisabled with arg True\n"
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
        def mock_list(self, name):
            "stub"
            print(f"called Conf.list_components_for_dir with arg '{name}'")
            return []
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        testobj.choice = 'xxx'
        testobj.modnames = {'xxx': {'aaa'}}
        testobj.view_components()
        assert capsys.readouterr().out == (
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called Conf.get_component_data with args ('xxx', 'Name')\n"
                "called Conf.get_component_data with args ('xxx', 'Version')\n"
                "called Conf.get_component_data with args ('yyy', 'Name')\n"
                "called Conf.get_component_data with args ('yyy', 'Version')\n"
                f"called MessageBox.information with args `{testobj}` `SDVMM mod info`"
                " `Components for xxx:\n  xxx_compname   xxx_version\n    (xxx)\n"
                "  yyy_compname   yyy_version\n    (yyy)`\n")
        monkeypatch.setattr(MockConf, 'list_components_for_dir', mock_list)
        testobj.view_components()
        assert capsys.readouterr().out == (
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                f"called MessageBox.information with args `{testobj}` `SDVMM mod info`"
                " `Components for xxx:\n`\n")

    def test_view_dependencies(self, monkeypatch, capsys):
        """unittest for AttributesDialog.view_dependencies
        """
        def mock_list(self, name):
            "stub"
            print(f"called Conf.list_components_for_dir with arg '{name}'")
            return []
        def mock_get(self, *args):
            "stub"
            print("called Conf.get_component_data with args", args)
            if args[1] == self.DEPS:
                return [f'{args[0]}_compname']
            raise ValueError
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        testobj.choice = 'xxx'
        testobj.modnames = {'xxx': {'aaa'}}
        testobj.view_dependencies()
        assert capsys.readouterr().out == (
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called Conf.get_component_data with args ('xxx', 'Deps')\n"
                "called Conf.get_component_data with args ('yyy', 'Deps')\n"
                "called Conf.get_component_data with args ('xxx_depname', 'Name')\n"
                "called Conf.get_component_data with args ('yyy_depname', 'Name')\n"
                f"called MessageBox.information with args `{testobj}` `SDVMM mod info`"
                " `Dependencies for xxx:\n"
                " xxx_depname_compname (xxx_depname)\n"
                " yyy_depname_compname (yyy_depname)`\n")
        monkeypatch.setattr(MockConf, 'get_component_data', mock_get)
        testobj.view_dependencies()
        assert capsys.readouterr().out == (
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called Conf.get_component_data with args ('xxx', 'Deps')\n"
                "called Conf.get_component_data with args ('yyy', 'Deps')\n"
                "called Conf.get_component_data with args ('xxx_compname', 'Name')\n"
                "called Conf.get_component_data with args ('yyy_compname', 'Name')\n"
                f"called MessageBox.information with args `{testobj}` `SDVMM mod info`"
                " `Dependencies for xxx:\n"
                " unknown component: xxx_compname\n"
                " unknown component: yyy_compname`\n")
        monkeypatch.setattr(MockConf, 'list_components_for_dir', mock_list)
        testobj.view_dependencies()
        assert capsys.readouterr().out == (
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                f"called MessageBox.information with args `{testobj}` `SDVMM mod info`"
                " `Dependencies for xxx:\n None `\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for AttributesDialog.update
        """
        def mock_refresh(*args):
            print('called ShowMods.refresh_widgets with args', args)
        def mock_build(*args):
            print('called ShowMods.build_screen_text with args', args)
        def mock_switch(*args):
            print('called AttributeDialog.switch_selectability with args', args)
            return False
        def mock_switch_2(*args):
            print('called AttributeDialog.switch_selectability with args', args)
            return True
        def mock_get(*args):
            print('called AttributeDialog.get_widget_list with args', args)
            return ['widget', label]
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.switch_selectability = mock_switch
        testobj.get_widget_list = mock_get
        label = mockqtw.MockLabel()
        check = mockqtw.MockCheckBox()
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(
                    screeninfo={'current text': {'txt': 'xxx', 'sel': True, 'pos': '2x2'}},
                    attr_changes=[]),
                refresh_widgets=mock_refresh,
                build_screen_text=mock_build)
        testobj.name = mockqtw.MockComboBox()
        testobj.clear_name_button = mockqtw.MockPushButton()
        testobj.text = mockqtw.MockLineEdit()
        testobj.clear_text_button = mockqtw.MockPushButton()
        testobj.activate_button = mockqtw.MockCheckBox()
        testobj.exempt_button = mockqtw.MockCheckBox()
        testobj.change_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called Label.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called LineEdit.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.choice = 'current text'
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': '', 'sel': False,
                                                                     'opt': False, 'pos': '2x2'}}
        assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == (
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called CheckBox.isChecked\n"
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called ComboBox.currentText\n"
                "called AttributeDialog.switch_selectability with args"
                " (False, 'current text', 'current text')\n"
                f"called MessageBox.information with args `{testobj}` `SDVMM`"
                " `Onselecteerbaar maken van mods met coordinaten in de config"
                " is helaas nog niet mogelijk`\n")
        testobj.switch_selectability = mock_switch_2
        testobj.parent.master.attr_changes = []
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': '', 'sel': False,
                                                                     'opt': False, 'pos': '2x2'}}
        assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == ("called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called CheckBox.isChecked\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called ComboBox.currentText\n")
        testobj.activate_button.setChecked(True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"
        testobj.parent.master.attr_changes = []
        testobj.parent.nonsel_widgets = {(2, 2): ('', label, check)}
        testobj.parent.unplotted_widgets = {}
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': '', 'sel': True,
                                                                     'opt': False, 'pos': '2x2'}}
        assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == ("called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called CheckBox.isChecked\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called ComboBox.currentText\n"
                                           "called AttributeDialog.switch_selectability with args"
                                           " (True, 'current text', 'current text')\n"
                                           "called ShowMods.refresh_widgets with args ()\n")
        testobj.text.setText('qqq')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `qqq`\n"
        testobj.parent.master.attr_changes = []
        testobj.parent.master.screeninfo = {'current text': {'txt': 'yyy', 'sel': True,
                                                             'pos': '2x2', 'key': 'qq'}}
        testobj.parent.unplotted_widgets = {(2, 2): ('', label, check)}
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': 'qqq', 'sel': True,
                                                                     'opt': False, 'pos': '2x2',
                                                                     'key': 'qq'}}
        assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == (
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called CheckBox.isChecked\n"
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called ComboBox.currentText\n"
                "called AttributeDialog.get_widget_list with args (2, 2, True)\n"
                "called Label.setOpenExternalLinks with arg 'False'\n"
                "called ShowMods.build_screen_text with args "
                f"({label}, 'current text', 'qqq', 'qq')\n")
        testobj.choice = 'xxx'
        testobj.parent.master.screeninfo = {'xxx': {'txt': 'yyy', 'sel': True, 'pos': '2x2',
                                                    'key': 'qq'}}
        testobj.parent.master.attr_changes = []
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': 'qqq', 'sel': True,
                                                                     'opt': False, 'pos': '2x2',
                                                                     'key': 'qq'}}
        assert testobj.parent.master.attr_changes == [('current text', 'xxx')]
        assert capsys.readouterr().out == (
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called CheckBox.isChecked\n"
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called ComboBox.currentText\n"
                "called AttributeDialog.get_widget_list with args (2, 2, True)\n"
                "called Label.setOpenExternalLinks with arg 'False'\n"
                "called ShowMods.build_screen_text with args "
                f"({label}, 'current text', 'qqq', 'qq')\n")
        testobj.parent.master.screeninfo = {'asdf': {'txt': 'yyy', 'sel': True, 'pos': '2x2',
                                                     'key': 'qq'}}
        testobj.parent.master.attr_changes = []
        testobj.update()
        assert capsys.readouterr().out == (
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called CheckBox.isChecked\n"
                f"called MessageBox.information with args `{testobj}` `SDVMM`"
                " `Tweemaal schermnaam wijzigen van een mod zonder de dialoog af te breken"
                " en opnieuw te starten is helaas nog niet mogelijk`\n")
        # testobj.parent.master.screeninfo = {'xxx': {'txt': 'yyy', 'sel': True, 'pos': '2x2',
        #                                             'key': 'qq'}}
        # testobj.parent.master.attr_changes = []
        # testobj.activate_button.setChecked(False)
        # assert capsys.readouterr().out == "called CheckBox.setChecked with arg False\n"
        # testobj.parent.unplotted = []
        # testobj.update()
        # assert testobj.parent.master.screeninfo == {'current text': {'txt': 'qqq', 'sel': False,
        #                                                              'pos': '2x2', 'key': 'qq',
        #                                                              'opt': False}}
        # assert testobj.parent.master.attr_changes == [('current text', 'xxx')]
        # assert capsys.readouterr().out == (
        #         "called PushButton.setDisabled with arg `True`\n"
        #         "called PushButton.setDisabled with arg `True`\n"
        #         "called PushButton.setDisabled with arg `True`\n"
        #         "called CheckBox.isChecked\n"
        #         "called LineEdit.text\n"
        #         "called CheckBox.isChecked\n"
        #         "called ComboBox.currentText\n"
        #         f"called MessageBox.information with args `{testobj}` `SDVMM` `Onselecteerbaar"
        #         " maken van mods met coordinaten in de config is helaas nog niet mogelijk`\n")
        # testobj.choice = 'current text'
        # testobj.parent.master.screeninfo = {'current text': {'txt': 'yyy', 'sel': False,
        #                                                      'pos': '2x2', 'key': 'qq'}}
        # testobj.parent.master.attr_changes = []
        # testobj.parent.nonsel_widgets = {(2, 2): ('', label, check)}
        # testobj.text.setText('yyy')
        # assert capsys.readouterr().out == "called LineEdit.setText with arg `yyy`\n"
        # testobj.update()
        # assert testobj.parent.master.screeninfo == {'current text': {'txt': 'yyy', 'sel': False,
        #                                                              'pos': '2x2', 'key': 'qq',
        #                                                              'opt': False}}
        # assert testobj.parent.master.attr_changes == [('current text', '')]
        # assert capsys.readouterr().out == (
        #         "called PushButton.setDisabled with arg `True`\n"
        #         "called PushButton.setDisabled with arg `True`\n"
        #         "called PushButton.setDisabled with arg `True`\n"
        #         "called CheckBox.isChecked\n"
        #         "called LineEdit.text\n"
        #         "called CheckBox.isChecked\n"
        #         "called ComboBox.currentText\n")

    def test_switch_selectability(self, monkeypatch, capsys):
        """unittest for AttributesDialog.switch_selectability
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(unplotted=[], not_selectable=[])
        with pytest.raises(ValueError):
            testobj.switch_selectability(True, 'xxx', 'xxx')
        # testobj.parent.unplotted = []
        testobj.parent.not_selectable = ['xxx', 'yyy']
        assert testobj.switch_selectability(True, 'xxx', 'xxx')
        assert testobj.parent.unplotted == ['xxx']
        assert testobj.parent.not_selectable == ['yyy']
        testobj.parent.unplotted = []
        testobj.parent.not_selectable = ['xxx', 'yyy']
        assert testobj.switch_selectability(True, 'xxx', 'yyy')
        assert testobj.parent.unplotted == ['xxx']
        assert testobj.parent.not_selectable == ['xxx']
        testobj.parent.unplotted = []
        testobj.parent.not_selectable = []
        assert not testobj.switch_selectability(False, 'xxx', 'xxx')
        assert testobj.parent.unplotted == []
        assert testobj.parent.not_selectable == []
        testobj.parent.unplotted = ['xxx', 'yyy']
        testobj.parent.not_selectable = []
        assert testobj.switch_selectability(False, 'xxx', 'xxx')
        assert testobj.parent.unplotted == ['yyy']
        assert testobj.parent.not_selectable == ['xxx']
        testobj.parent.unplotted = ['xxx', 'yyy']
        testobj.parent.not_selectable = []
        assert testobj.switch_selectability(False, 'xxx', 'yyy')
        assert testobj.parent.unplotted == ['xxx']
        assert testobj.parent.not_selectable == ['xxx']

    def test_get_widget_list(self, monkeypatch, capsys):
        """unittest for AttributesDialog.get_widget_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(plotted_widgets={(1, 2): ['x']},
                                               unplotted_widgets={(1, 2): ['y']},
                                               nonsel_widgets={(1, 2): ['z']})
        assert testobj.get_widget_list(1, 2, True) == ['x']
        testobj.parent = types.SimpleNamespace(plotted_widgets={(1, 3): ['x']},
                                               unplotted_widgets={(1, 2): ['y']},
                                               nonsel_widgets={(1, 2): ['z']})
        assert testobj.get_widget_list(1, 2, True) == ['y']
        testobj.parent = types.SimpleNamespace(plotted_widgets={(1, 2): ['x']},
                                               unplotted_widgets={(1, 2): ['y']},
                                               nonsel_widgets={(1, 2): ['z']})
        assert testobj.get_widget_list(1, 2, False) == ['z']


class TestSaveGamesDialog:
    """unittest for gui.SaveGamesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui.SaveGamesDialog object

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
        monkeypatch.setattr(testee.SaveGamesDialog, 'update_all', lambda: 'dummy')
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
        def mock_refresh():
            print('called ShowMods.refresh_widget_data')
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
        testobj.parent.refresh_widget_data = mock_refresh
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
                "called ShowMods.refresh_widget_data\n"
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
                "called ShowMods.refresh_widget_data\n"
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
                "called ShowMods.refresh_widget_data\n"
                "called MessageBox.information with args"
                f" `{testobj}` `Change Config` `wijzigingen zijn doorgevoerd`\n")

    def test_update_all(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.update
        """
        def mock_update(arg):
            print(f'called SavedGamesDialog with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        testobj.update = mock_update
        testobj.savegame_selector = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.update_all()
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called SavedGamesDialog with arg current text\n"
                                           "called Conf.save\n")

    def test_update(self, monkeypatch, capsys):
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
        testobj.update('save_name')
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called PushButton.setDisabled with arg `True`\n")
        testobj.widgets = [lbox]
        testobj.oldmods = ['current text']
        testobj.update('save_name')
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Mods', [])\n"
                "called PushButton.setDisabled with arg `True`\n")

        testobj.old_pname = 'aaa'
        testobj.old_fname = 'bbb'
        testobj.old_gdate = 'ccc'
        testobj.oldmods = ['qqq']
        testobj.update('save_name')
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Pname', 'xxx')\n"
                "called LineEdit.text\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Fname', 'yyy')\n"
                "called LineEdit.text\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Gdate', 'zzz')\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Mods', [])\n"
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
            return 'oldpname', 'oldfname', 'oldgdate'
        def mock_get_mods(name):
            "stub"
            print(f"called Conf.get_mods_for_saveitem with arg {name}")
            return ['newmodname']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        testobj.update = mock_update
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
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
        testobj.oldsavename = 'yyy'
        testobj.get_savedata('xxx')
        assert capsys.readouterr().out == ("called SaveGamesDialog with arg yyy\n"
                                           "called SaveGamesDialog.add_modselector\n"
                                           "called Conf.get_saveitem_attrs with arg xxx\n"
                                           "called PushButton.setDisabled with arg `True`\n"
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
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
