"""unittests for ./gui.py
"""
import types
import pytest
import mockgui.mockqtwidgets as mockqtw
from src import gui as testee

showmods = """\
called QWidget.setWindowTitle()
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('Dit overzicht toont de namen van expansies die je kunt activeren (inclusief die al geactiveerd zijn).\\nIn de achterliggende configuratie is geregeld welke mods hiervoor eventueel nog meer aangezet moeten worden\\nDe onderstreepte items zijn hyperlinks; ze leiden naar de pagina waarvandaan ik ze van gedownload heb (doorgaans op Nexus)',)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Grid.__init__
called PushButton.__init__ with args ('&Activate changes', {testobj}) {{}}
called ShowMods.refresh_widgets with args () {{'first_time': True}}
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called VBox.addSpacing
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Install / update', {testobj}) {{}}
called PushButton.setToolTip with arg `Selecteer uit een lijst met recent gedownloade mods één of meer om te installeren`
called Signal.connect with args ({testobj.update},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Reorder mods on screen', {testobj}) {{}}
called Signal.connect with args ({testobj.reorder_gui},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Mod attributes', {testobj}) {{}}
called Signal.connect with args ({testobj.master.manage_attributes},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called Signal.connect with args ({testobj.confirm},)
called PushButton.setEnabled with arg `False`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Done', {testobj}) {{}}
called Signal.connect with args ({testobj.close},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called QWidget.setLayout()
"""
# called PushButton.__init__ with args ('add &Mod to config', {testobj}) {{}}
# called Signal.connect with args ({testobj.master.add_to_config},)
# called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
# called PushButton.__init__ with args ('&Edit config', {testobj}) {{}}
# called Signal.connect with args ({testobj.master.edit_config},)
# called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
# called PushButton.__init__ with args ('Re&Load config', {testobj}) {{}}
# called Signal.connect with args ({testobj.master.reload_config},)
# called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
# called PushButton.__init__ with args ('&Check config', {testobj}) {{}}
# called Signal.connect with args ({testobj.check},)
# called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
newmod = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Grid.__init__
called Label.__init__ with args ('Mod name:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)
called LineEdit.__init__
called LineEdit.setMinimumWidth with arg `200`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (0, 1)
called Label.__init__ with args ('Unpack directory:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 0)
called LineEdit.__init__
called LineEdit.setMinimumWidth with arg `200`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 1)
called PushButton.__init__ with args ('&Select\\nfrom Downloads', {testobj}) {{}}
called Signal.connect with args ({testobj.select_mod},)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'> at (0, 2, 2, 1)
called CheckBox.__init__ with text 'Activatable'{checked}
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'> at (2, 0)
called VBox.__init__
called PushButton.__init__ with args ('&Add dependency', {testobj}) {{}}
called Signal.connect with args ({testobj.add_depline},)
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'> at (3, 0, 1, 3)
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Update', {testobj}) {{}}
called Signal.connect with args ({testobj.update_deps},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (4, 0, 1, 3)
called Dialog.setLayout
"""
add_depline = """\
called CheckBox.__init__
called HBox.__init__
called ComboBox.__init__
called ComboBox.setEditable with arg `False`
called ComboBox.addItems with arg ['-- add a new mod --', '-- remove this mod --']
called ComboBox.addItems with arg ['x', 'y']
called Signal.connect with args (functools.partial({testobj.process_dep}, {testobj.deps[0][0]}),)
called CheckBox.setEnabled with arg False
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called NewModDialog.update
"""
remarks = """\
called Conf.list_all_mod_dirs
called Conf.get_diritem_data with args ('xxx', 'SCRNAM')
called Conf.get_diritem_data with args ('yyy', 'SCRNAM')
called Dialog.__init__ with args {testobj.parent} () {{}}
called VBox.__init__
called ComboBox.__init__
called ComboBox.setEditable with arg `False`
called ComboBox.addItem with arg `select a mod to change the screen text`
called ComboBox.addItems with arg ['xxx_name', 'yyy_name']
called Signal.connect with args ({testobj.enable_select},)
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called PushButton.__init__ with args ('View &Attributes',) {{}}
called Signal.connect with args ({testobj.process},)
called PushButton.setEnabled with arg `False`
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.__init__
called Label.__init__ with args ('Screen Name:\\n(the suggestions in the box below are taken from\\nthe mod components', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called ComboBox.__init__
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
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called PushButton.__init__ with args () {{}}
called Icon.fromTheme with args ()
called PushButton.setIcon with arg `None`
called PushButton.setFixedSize with args (24, 24)
called PushButton.setDisabled with arg `True`
called Signal.connect with args ({testobj.clear_text_text},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called CheckBox.__init__ with text 'This mod can be activated by itself'
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
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
reorder = """\
called Widget.__init__
called Dialog.__init__ with args {testobj.parent} () {{}}
called ReorderDialog.determine_rows_cols
called VBox.__init__
called Table.__init__ with args ({testobj},)
called Header.__init__
called Header.__init__
called Table.setRowCount with arg '1'
called Table.setColumnCount with arg '1'
called Table.setColumnWidth with args (-1, 200)
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockTable'>
called ReorderDialog.populate
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&> Add Column', {testobj}) {{}}
called Signal.connect with args ({testobj.add_column},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&< Remove Last Column', {testobj}) {{}}
called Signal.connect with args ({testobj.remove_column},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('(Re)&Position texts in grid', {testobj}) {{}}
called Signal.connect with args ({testobj.populate},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&+ Add Row', {testobj}) {{}}
called Signal.connect with args ({testobj.add_row},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&- Remove Last Row', {testobj}) {{}}
called Signal.connect with args ({testobj.remove_row},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called PushButton.__init__ with args ('&Save', {testobj}) {{}}
called Signal.connect with args ({testobj.accept},)
called PushButton.setDefault with arg `True`
called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""


@pytest.fixture
def expected_output():
    "fixture returning output to be expected from (mostly) gui setup methods"
    results = {'showmods': showmods, 'newmod': newmod, 'add_depline': add_depline,
               'reorder': reorder, 'remarks': remarks}
    return results


class MockManager:
    """stub for ./manager.Manager
    """
    def __init__(self):
        self.modbase = 'modbase'
        self.downloads = 'Downloads'
        self.conf = {}
        self.directories = ['x']
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
    def reorder_gui(self):
        """stub
        """
        print('called Manager.reorder_gui()')


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
        def mock_refresh(**kwargs):
            """stub
            """
            print('called Manager.refresh_widgets with args', kwargs)
        def mock_information(self, *args):
            """stub
            """
            print('called MessageBox.information with args', args)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_information)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh_widgets = mock_refresh
        testobj.activate_button = mockqtw.MockPushButton()
        label1 = testee.qtw.QLabel('check1')
        check1 = testee.qtw.QCheckBox('', testobj)
        check1.setChecked(True)
        label2 = testee.qtw.QLabel('check2')
        check2 = testee.qtw.QCheckBox('', testobj)
        label3 = testee.qtw.QLabel('<a>check3</a>')
        check3 = testee.qtw.QCheckBox('', testobj)
        check3.setChecked(True)
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called Label.__init__ with args ('check1',)\n"
                                           "called CheckBox.__init__ with text ''\n"
                                           'called CheckBox.setChecked with arg True\n'
                                           "called Label.__init__ with args ('check2',)\n"
                                           "called CheckBox.__init__ with text ''\n"
                                           "called Label.__init__ with args ('<a>check3</a>',)\n"
                                           "called CheckBox.__init__ with text ''\n"
                                           'called CheckBox.setChecked with arg True\n')
        testobj.widgets = {'check1': (label1, check1), 'check2': (label2, check2),
                           'check3': (label3, check3)}
        testobj.confirm()
        assert capsys.readouterr().out == (
                'called CheckBox.isChecked\n'
                'called CheckBox.isChecked\n'
                'called CheckBox.isChecked\n'
                "called Manager.select_activations with arg ['check1', 'check3']\n"
                'called Manager.activate\n'
                "called Manager.refresh_widgets with args {'reorder_widgets': False}\n"
                "called MessageBox.information with args"
                " ('Change Config', 'wijzigingen zijn doorgevoerd')\n"
                "called PushButton.setEnabled with arg `False`\n")
        testobj.master.directories = []
        testobj.confirm()
        assert capsys.readouterr().out == (
                'called CheckBox.isChecked\n'
                'called CheckBox.isChecked\n'
                'called CheckBox.isChecked\n'
                "called Manager.select_activations with arg ['check1', 'check3']\n"
                "called Manager.refresh_widgets with args {'reorder_widgets': False}\n"
                "called MessageBox.information with args"
                " ('Change Config', 'wijzigingen zijn doorgevoerd')\n"
                "called PushButton.setEnabled with arg `False`\n")

    def test_refresh_widgets(self, monkeypatch, capsys):
        """unittest for ShowMods.refresh_widgets
        """
        counter = 0
        def mock_path(*args):
            """stub
            """
            nonlocal counter
            counter += 1
            if counter % 2 == 1:
                return False
            return True
        def mock_add(text, linknum):
            print(f"called Manager.add_checkbox with arg '{text}'")
            hbox = mockqtw.MockHBoxLayout()
            check = mockqtw.MockCheckBox()
            label = mockqtw.MockLabel()
            assert capsys.readouterr().out == (f"called Manager.add_checkbox with arg '{text}'\n"
                                               "called HBox.__init__\n"
                                               "called CheckBox.__init__\n"
                                               "called Label.__init__\n")
            return hbox, (label, check)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        # monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee, 'maxpercol', 3)
        monkeypatch.setattr(testee.os.path, 'exists', mock_path)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_checkbox = mock_add
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"

        testobj.master.screeninfo = {'mod 1': {'dir': 'moddir1', 'sel': True, 'pos': '0x0',
                                               'key': '', 'txt': ''},
                                     'mod 2': {'dir': 'moddir2', 'sel': True, 'pos': '1x1',
                                               'key': '12', 'txt': ''},
                                     'mod 3': {'dir': 'moddir3', 'sel': False, 'pos': '',
                                               'key': '9', 'txt': '(hmm)'},
                                     'mod 4': {'dir': 'moddir4', 'sel': False, 'pos': '0x1',
                                               'key': '', 'txt': ''}}
        testobj.widgets = {}
        testobj.containers = {}
        testobj.positions = {}
        testobj.refresh_widgets(first_time=True)
        assert len(testobj.widgets) == len(testobj.master.screeninfo)
        assert list(testobj.widgets.keys()) == list(testobj.master.screeninfo.keys())
        for x, y in testobj.widgets.values():
            assert isinstance(x, mockqtw.MockLabel)
            assert isinstance(y, mockqtw.MockCheckBox)
        assert len(testobj.containers) == len(testobj.master.screeninfo) + 1
        assert list(testobj.containers.keys()) == list(testobj.master.screeninfo.keys()) + ['---']
        for x in testobj.containers.values():
            assert isinstance(x, mockqtw.MockHBoxLayout)
        assert len(testobj.positions) == len(testobj.master.screeninfo) + 1
        assert list(testobj.positions.keys()) == [(0, 0), (1, 1), (0, 1), (2, -1), (3, 0)]
        assert list(testobj.positions.values()) == ['mod 1', 'mod 2', 'mod 4', '---', 'mod 3']
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called Label.__init__ with args ('Hieronder volgen afhankelijkheden;"
                " deze zijn niet apart te activeren maar je kunt wel zien of ze actief zijn',)\n"
                "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 0)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 1)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 1)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (2, -1)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (3, 0)\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n")

        testobj.master.screeninfo = {'mod 1': {'dir': 'moddir1', 'sel': True, 'pos': '',
                                               'key': '', 'txt': ''},
                                     'mod 2': {'dir': 'moddir2', 'sel': True, 'pos': '1x1',
                                               'key': '12', 'txt': ''},
                                     'mod 3': {'dir': 'moddir3', 'sel': False, 'pos': '',
                                               'key': '9', 'txt': '(hmm)'},
                                     'mod 4': {'dir': 'moddir4', 'sel': False, 'pos': '',
                                               'key': '9', 'txt': '(hmm)'},
                                     'mod 5': {'dir': 'moddir5', 'sel': False, 'pos': '',
                                               'key': '', 'txt': ''}}
        testobj.widgets = {}
        testobj.containers = {}
        testobj.positions = {}
        testobj.refresh_widgets(first_time=True, reorder_widgets=False)
        assert len(testobj.widgets) == len(testobj.master.screeninfo)
        assert list(testobj.widgets.keys()) == list(testobj.master.screeninfo.keys())
        for x, y in testobj.widgets.values():
            assert isinstance(x, mockqtw.MockLabel)
            assert isinstance(y, mockqtw.MockCheckBox)
        assert len(testobj.containers) == len(testobj.master.screeninfo) + 1
        assert list(testobj.containers.keys()) == list(testobj.master.screeninfo.keys()) + ['---']
        for x in testobj.containers.values():
            assert isinstance(x, mockqtw.MockHBoxLayout)
        assert len(testobj.positions) == len(testobj.master.screeninfo) + 1
        assert list(testobj.positions.keys()) == [(1, 1), (2, -1), (3, 0), (3, 1), (3, 2), (4, 0)]
        assert list(testobj.positions.values()) == ['mod 2', '---', 'mod 1', 'mod 3', 'mod 4',
                                                    'mod 5']
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called Label.__init__ with args ('Hieronder volgen afhankelijkheden;"
                " deze zijn niet apart te activeren maar je kunt wel zien of ze actief zijn',)\n"
                "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setChecked with arg False\n")

        testobj.master.screeninfo = {'mod 1': {'dir': 'moddir1', 'sel': True, 'pos': '0x0',
                                               'key': '', 'txt': ''},
                                     'mod 2': {'dir': 'moddir2', 'sel': True, 'pos': '1x1',
                                               'key': '12', 'txt': ''},
                                     'mod 3': {'dir': 'moddir3', 'sel': False, 'pos': '',
                                               'key': '9', 'txt': '(hmm)'},
                                     'mod 4': {'dir': 'moddir4', 'sel': False, 'pos': '0x1',
                                               'key': '', 'txt': ''}}
        testobj.widgets = {}
        hbox1 = mockqtw.MockHBoxLayout()
        hbox2 = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\ncalled HBox.__init__\n"
        testobj.containers = {'mod 1': hbox1, 'mod 2': hbox2}
        testobj.positions = {(0, 1): 'mod 1', (1, 1): 'mod 2'}
        testobj.refresh_widgets()
        assert capsys.readouterr().out == (
                f"called Grid.removeItem with args ({hbox1},)\n"
                f"called Grid.removeItem with args ({hbox2},)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 1)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 1)\n"
                "called Grid.update\n")
        return
        testobj.widgets = {}
        testobj.containers = {}
        testobj.positions = {}
        testobj.refresh_widgets(reorder_widgets=False)
        assert capsys.readouterr().out == (
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for ShowMods.add_checkbox
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.screentext = {}
        obj1, obj2 = testobj.add_checkbox('xxxx', {'sel': False, 'key': '1', 'txt': ''})
        assert isinstance(obj1, testee.qtw.QHBoxLayout)
        assert isinstance(obj2[0], testee.qtw.QLabel)
        assert isinstance(obj2[1], testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            "called HBox.__init__\n"
            "called CheckBox.__init__\n"
            "called CheckBox.setEnabled with arg False\n"
            f"called Signal.connect with args ({testobj.enable_button},)\n"
            "called Label.__init__\n"
            "called Label.setOpenExternalLinks with arg 'True'\n"
            "called Label.setText with arg"
            ' `<a href="https://www.nexusmods.com/stardewvalley/mods/1">xxxx</a>`\n'
            "called HBox.addSpacing\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called HBox.addStretch\n"
            "called HBox.addSpacing\n")
        obj1, obj2 = testobj.add_checkbox('xxxx', {'sel': True, 'key': '', 'txt': 'yyy'})
        assert isinstance(obj1, testee.qtw.QHBoxLayout)
        assert isinstance(obj2[0], testee.qtw.QLabel)
        assert isinstance(obj2[1], testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            "called HBox.__init__\n"
            "called CheckBox.__init__\n"
            "called CheckBox.setEnabled with arg True\n"
            f"called Signal.connect with args ({testobj.enable_button},)\n"
            "called Label.__init__\n"
            "called Label.setText with arg `xxxx yyy`\n"
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

    def test_add_entries_for_name(self, monkeypatch, capsys):
        """unittest for ShowMods.add_entries_for_name
        """
        def mock_add(*args):
            print("called Manager.add_checkbox with args", args)
            return 'hbox', ('label', 'check')
        def mock_determine():
            print('called Manager.determine_newt_row_col')
            return 1, 2
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.containers, testobj.widgets, testobj.positions = {}, {}, {}
        testobj.add_checkbox = mock_add
        testobj.determine_next_row_col = mock_determine
        testobj.add_entries_for_name('name')
        assert testobj.containers['name'] == 'hbox'
        assert testobj.widgets['name'] == ('label', 'check')
        assert testobj.positions[1, 2] == 'name'
        assert capsys.readouterr().out == ("called Manager.add_checkbox with args ('name', '')\n"
                                           'called Manager.determine_newt_row_col\n')

    def test_determine_next_row_col(self, monkeypatch, capsys):
        """unittest for ShowMods.deteremine_next_row_col
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.positions = {(0, 0): '', (0, 1): '', (0, 2): '', (1, 0): '', (1, 1): ''}
        assert testobj.determine_next_row_col() == (1, 2)
        # heb ik hier nou alweer row en col omgedraaid?
        testobj.positions = {(0, 0): '', (0, 1): '', (0, 2): '', (1, 0): '', (1, 1): '', (1, 2): ''}
        assert testobj.determine_next_row_col() == (2, 0)

    def test_reorder_gui(self, monkeypatch, capsys):
        """unittest for ShowMods.reorder_gui
        """
        def mock_show(*args, **kwargs):
            print("called gui.show_dialog with args", args, kwargs)
            return False  # , {}
        def mock_show_2(*args, **kwargs):
            print("called gui.show_dialog with args", args, kwargs)
            return True  # , {r'reordered': 'widgets'}
        def mock_refresh():
            print('called ActivateGui.refresh_widgets')
        def mock_update():
            print('called Manager.update_config_from_screenpos')
        monkeypatch.setattr(testee, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh_widgets = mock_refresh
        testobj.master.update_config_from_screenpos = mock_update
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.reorder_gui()
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" (<class 'src.gui.ReorderDialog'>, {testobj}) {{}}\n")
        monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
        testobj.reorder_gui()
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" (<class 'src.gui.ReorderDialog'>, {testobj}) {{}}\n"
                "called Manager.update_config_from_screenpos\n"
                "called ActivateGui.refresh_widgets\n")

    def test_select_value(self, monkeypatch, capsys):
        """unittest for ShowMods.select_value
        """
        def mock_get(*args, **kwargs):
            nonlocal counter
            print('called InputDialog.getItem with args', args, kwargs)
            counter += 1
            return counter != 1, f'item{counter}'
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
    SCRNAM = 'SCRNAM'
    NAME = 'Name'
    DEPS = 'Deps'
    VRS = 'Version'
    def list_all_mod_dirs(self):
        "stub"
        print('called Conf.list_all_mod_dirs')
        return ['xxx', 'yyy']
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
        """unittest for NewModDialog.__init__
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
        assert testobj.modnames == {'xxx_name': 'xxx', 'yyy_name': 'yyy'}
        assert isinstance(testobj.lbox, testee.qtw.QComboBox)
        assert isinstance(testobj.select_button, testee.qtw.QPushButton)
        assert isinstance(testobj.name, testee.qtw.QComboBox)
        assert isinstance(testobj.clear_name_button, testee.qtw.QPushButton)
        assert isinstance(testobj.text, testee.qtw.QLineEdit)
        assert isinstance(testobj.clear_text_button, testee.qtw.QPushButton)
        assert isinstance(testobj.activate_button, testee.qtw.QCheckBox)
        assert isinstance(testobj.comps_button, testee.qtw.QPushButton)
        assert isinstance(testobj.deps_button, testee.qtw.QPushButton)
        assert isinstance(testobj.change_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['remarks'].format(testobj=testobj)

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
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n")

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
                    screeninfo={'current text': {'txt': 'xxx', 'sel': True}}))
        testobj.modnames = {'current text': {'aaa'}}
        testobj.select_button = mockqtw.MockPushButton()
        testobj.lbox = mockqtw.MockComboBox()
        testobj.name = mockqtw.MockComboBox()
        testobj.clear_name_button = mockqtw.MockPushButton()
        testobj.text = mockqtw.MockLineEdit()
        testobj.clear_text_button = mockqtw.MockPushButton()
        testobj.activate_button = mockqtw.MockCheckBox()
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
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.process()
        assert testobj.choice == 'current text'
        assert capsys.readouterr().out == (
                "called PushButton.setDisabled with arg `True`\n"
                "called ComboBox.currentText\n"
                "called ComboBox.clear\n"
                "called ComboBox.addItem with arg `current text`\n"
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called Conf.get_component_data with args ('xxx', 'Name')\n"
                "called Conf.get_component_data with args ('yyy', 'Name')\n"
                "called ComboBox.addItems with arg ['xxx_compname', 'yyy_compname']\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called LineEdit.setText with arg `xxx`\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called CheckBox.setChecked with arg True\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called PushButton.setDisabled with arg `False`\n")
        monkeypatch.setattr(MockConf, 'list_components_for_dir', mock_list)
        testobj.process()
        assert testobj.choice == 'current text'
        assert capsys.readouterr().out == (
                "called PushButton.setDisabled with arg `True`\n"
                "called ComboBox.currentText\n"
                "called ComboBox.clear\n"
                "called ComboBox.addItem with arg `current text`\n"
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called ComboBox.addItems with arg []\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called LineEdit.setText with arg `xxx`\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called CheckBox.setChecked with arg True\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called PushButton.setDisabled with arg `False`\n"
                "called PushButton.setDisabled with arg `False`\n")

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
        """unittest for AttributesDialog.change_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.conf = MockConf()
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(
                    screeninfo={'current text': {'txt': 'xxx', 'sel': True}}))
        # testobj.modnames = {'current text': {'aaa'}}
        # testobj.select_button = mockqtw.MockPushButton()
        # testobj.lbox = mockqtw.MockComboBox()
        testobj.name = mockqtw.MockComboBox()
        testobj.clear_name_button = mockqtw.MockPushButton()
        testobj.text = mockqtw.MockLineEdit()
        testobj.clear_text_button = mockqtw.MockPushButton()
        testobj.activate_button = mockqtw.MockCheckBox()
        # testobj.comps_button = mockqtw.MockPushButton()
        # testobj.deps_button = mockqtw.MockPushButton()
        testobj.change_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called LineEdit.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called CheckBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.choice = 'current text'
        testobj.parent.master.attr_changes = []
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': '', 'sel': False}}
        assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == ("called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called CheckBox.isChecked\n"
                                           "called LineEdit.text\n"
                                           "called ComboBox.currentText\n")
        testobj.choice = 'xxx'
        testobj.parent.master.screeninfo = {'xxx': {'txt': 'yyy', 'sel': True}}
        testobj.parent.master.attr_changes = []
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': '', 'sel': False}}
        assert testobj.parent.master.attr_changes == [('current text', 'xxx')]
        assert capsys.readouterr().out == ("called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called CheckBox.isChecked\n"
                                           "called LineEdit.text\n"
                                           "called ComboBox.currentText\n")


class TestReorderDialog:
    """unittest for gui.ReorderDialog
    """
    populate_text = ("called TableItem.__init__ with arg {}\n"
                     "called Table.setItem with args ({},"
                     " item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n")
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui.ReorderDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called ReorderDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ReorderDialog, '__init__', mock_init)
        testobj = testee.ReorderDialog()
        assert capsys.readouterr().out == 'called ReorderDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ReorderDialog.__init__
        """
        def mock_determine(self):
            print('called ReorderDialog.determine_rows_cols')
            return 1, 1
        def mock_populate(self):
            print('called ReorderDialog.populate')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.ReorderDialog, 'determine_rows_cols', mock_determine)
        monkeypatch.setattr(testee.ReorderDialog, 'populate', mock_populate)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        parent = mockqtw.MockWidget()
        # parent.appicon = 'appicon'
        parent.master = MockManager()
        parent.master.screenpos = {'screen': 'positions'}
        testobj = testee.ReorderDialog(parent)
        assert testobj.parent == parent
        assert testobj.data == {'screen': 'positions'}
        assert isinstance(testobj.table, testee.qtw.QTableWidget)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['reorder'].format(testobj=testobj)

    def setup_table(self, testobj, capsys):
        """stub for table widget
        """
        testobj.table = mockqtw.MockTable(testobj)
        assert capsys.readouterr().out == (f"called Table.__init__ with args ({testobj},)\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        return testobj.table

    def test_determine_rows_cols(self, monkeypatch, capsys):
        """unittest for ReorderDialog.determine_rows_cols
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.data = {'xxx': ('', ''), 'yyy': ('', ''), 'zzz': ('', ''), 'qqq': ('', ''),
                        'rrr': ('', '')}
        assert testobj.determine_rows_cols() == (2, 3)
        testobj.data = {'xxx': ('', ''), 'yyy': ('', ''), 'zzz': ('', ''), 'qqq': ('', ''),
                        'rrr': ('', ''), 'sss': ('', '')}
        assert testobj.determine_rows_cols() == (2, 3)
        testobj.data = {'xxx': ('', ''), 'yyy': ('', ''), 'zzz': ('', ''), 'qqq': ('', ''),
                        'rrr': ('', ''), 'sss': ('', ''), 'ttt': ('', '')}
        assert testobj.determine_rows_cols() == (3, 3)
        testobj.data = {'xxx': ('1x1', ''), 'yyy': ('2x1', ''), 'zzz': ('0x0', '')}
        assert testobj.determine_rows_cols() == (3, 2)

    def test_add_column(self, monkeypatch, capsys):
        """unittest for ReorderDialog.add_column
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.table = self.setup_table(testobj, capsys)
        testobj.colwidth = 100
        testobj.add_column()
        assert capsys.readouterr().out == ("called Table.columnCount\n"
                                           "called Table.insertColumn with arg '0'\n"
                                           "called Table.columnCount\n"
                                           "called Table.setColumnWidth with args (0, 100)\n")

    def test_remove_column(self, monkeypatch, capsys):
        """unittest for ReorderDialog.remove_column
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.table = self.setup_table(testobj, capsys)
        testobj.remove_column()
        assert capsys.readouterr().out == ("called Table.columnCount\n"
                                           "called Table.removeColumn with arg '-1'\n")

    def test_add_row(self, monkeypatch, capsys):
        """unittest for ReorderDialog.add_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.table = self.setup_table(testobj, capsys)
        testobj.add_row()
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.insertRow with arg '0'\n")

    def test_remove_row(self, monkeypatch, capsys):
        """unittest for ReorderDialog.remove_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.table = self.setup_table(testobj, capsys)
        testobj.remove_row()
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.removeRow with arg '-1'\n")

    def test_populate(self, monkeypatch, capsys):
        """unittest for ReorderDialog.populate
        """
        monkeypatch.setattr(testee.qtw, 'QTableWidgetItem', mockqtw.MockTableItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.data = {'aaa': '', 'bbb': '', 'ccc': '', 'ddd': '', 'eee': '', 'fff': '', 'ggg': ''}
        testobj.table = self.setup_table(testobj, capsys)
        testobj.table.setRowCount(3)
        testobj.table.setColumnCount(2)
        assert capsys.readouterr().out == ("called Table.setRowCount with arg '3'\n"
                                           "called Table.setColumnCount with arg '2'\n")
        testobj.populate()
        assert capsys.readouterr().out == ("called Table.clear\n"
                                           "called Table.columnCount\n"
                                           "called Table.rowCount\n"
                                           + self.populate_text.format('aaa', '0, 0')
                                           + self.populate_text.format('bbb', '1, 0')
                                           + self.populate_text.format('ccc', '2, 0')
                                           + "called Table.rowCount\n"
                                           + self.populate_text.format('ddd', '0, 1')
                                           + self.populate_text.format('eee', '1, 1')
                                           + self.populate_text.format('fff', '2, 1'))
        testobj.table.setColumnCount(3)
        assert capsys.readouterr().out == ("called Table.setColumnCount with arg '3'\n")
        testobj.populate()
        assert capsys.readouterr().out == ("called Table.clear\n"
                                           "called Table.columnCount\n"
                                           "called Table.rowCount\n"
                                           + self.populate_text.format('aaa', '0, 0')
                                           + self.populate_text.format('bbb', '1, 0')
                                           + self.populate_text.format('ccc', '2, 0')
                                           + "called Table.rowCount\n"
                                           + self.populate_text.format('ddd', '0, 1')
                                           + self.populate_text.format('eee', '1, 1')
                                           + self.populate_text.format('fff', '2, 1')
                                           + "called Table.rowCount\n"
                                           + self.populate_text.format('ggg', '0, 2'))
        testobj.data = {'aaa': ('1x1', ''), 'bbb': ('0x0', ''), 'ccc': ('0x1', ''),
                        'ddd': ('2x1', ''), 'eee': ('3x1', ''),
                        'fff': ('1x0', ''), 'ggg': ('', '')}
        testobj.populate()
        assert capsys.readouterr().out == ("called Table.clear\n"
                                           "called Table.rowCount\n"
                                           "called Table.insertRow with arg '3'\n"
                                           + self.populate_text.format('ggg', '3, 0')
                                           + self.populate_text.format('bbb', '0, 0')
                                           + self.populate_text.format('ccc', '0, 1')
                                           + self.populate_text.format('fff', '1, 0')
                                           + self.populate_text.format('aaa', '1, 1')
                                           + self.populate_text.format('ddd', '2, 1')
                                           + self.populate_text.format('eee', '3, 1'))

    def test_accept(self, monkeypatch, capsys):
        """unittest for ReorderDialog.accept
        """
        def mock_accept(self):
            print('called Dialog.accept')
        def mock_information(self, *args):
            print('called MessageBox.information with args', args)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = mockqtw.MockWidget()
        testobj._parent.master = MockManager()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj.data = {'aaa': '', 'bbb': '', 'ccc': '', 'ddd': '', 'eee': '', 'fff': '', 'ggg': ''}
        testobj.table = self.setup_table(testobj, capsys)
        testobj.table.setRowCount(2)
        testobj.table.setColumnCount(2)
        assert capsys.readouterr().out == ("called Table.setRowCount with arg '2'\n"
                                           "called Table.setColumnCount with arg '2'\n")
        testobj.accept()
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.columnCount\n"
                                           "called MessageBox.information with args"
                                           " ('Reorder names', 'not enough room for all entries')\n")
        testobj.table.setRowCount(3)
        testobj.table.setColumnCount(3)
        testobj.table.setItem(0, 0, mockqtw.MockTableItem('bbb'))
        testobj.table.setItem(1, 0, mockqtw.MockTableItem('fff'))
        testobj.table.setItem(2, 0, mockqtw.MockTableItem('ddd'))
        testobj.table.setItem(0, 1, mockqtw.MockTableItem('ccc'))
        testobj.table.setItem(1, 1, mockqtw.MockTableItem('aaa'))
        testobj.table.setItem(2, 1, mockqtw.MockTableItem('eee'))
        testobj.table.setItem(0, 2, mockqtw.MockTableItem('ggg'))
        assert capsys.readouterr().out == ("called Table.setRowCount with arg '3'\n"
                                           "called Table.setColumnCount with arg '3'\n"
                                           + self.populate_text.format('bbb', '0, 0')
                                           + self.populate_text.format('fff', '1, 0')
                                           + self.populate_text.format('ddd', '2, 0')
                                           + self.populate_text.format('ccc', '0, 1')
                                           + self.populate_text.format('aaa', '1, 1')
                                           + self.populate_text.format('eee', '2, 1')
                                           + self.populate_text.format('ggg', '0, 2'))
        testobj.accept()
        assert testobj.data == {'aaa': '1x1', 'bbb': '0x0', 'ccc': '0x1', 'ddd': '2x0', 'eee': '2x1',
                                'fff': '1x0', 'ggg': '0x2'}
        assert testobj._parent.master.screenpos == testobj.data
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.columnCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Table.item with args (0, 1)\n"
                                           "called Table.item with args (0, 2)\n"
                                           "called Table.item with args (1, 0)\n"
                                           "called Table.item with args (1, 1)\n"
                                           "called Table.item with args (1, 2)\n"
                                           "called Table.item with args (2, 0)\n"
                                           "called Table.item with args (2, 1)\n"
                                           "called Table.item with args (2, 2)\n"
                                           "called Dialog.accept\n")
