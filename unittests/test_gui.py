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
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called Label.__init__ with args ('Hieronder volgen afhankelijkheden; deze zijn niet apart te activeren maar je kunt wel zien of ze actief zijn',)
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called Grid.__init__
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called PushButton.__init__ with args ('&Activate changes', {testobj}) {{}}
called ShowMods.refresh_widgets with args () {{'first_time': True}}
called VBox.addSpacing
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Install / update', {testobj}) {{}}
called PushButton.setToolTip with arg `Selecteer uit een lijst met recent gedownloade mods één of meer om te installeren`
called Signal.connect with args ({testobj.update},)
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
# called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
# called PushButton.__init__ with args ('&Reorder mods on screen', {testobj}) {{}}
# called Signal.connect with args ({testobj.reorder_gui},)
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
        def mock_set1(*args):
            print("called Showmods.set_texts_for_grid with args", args)
        def mock_set2(*args):
            print("called Showmods.set_checks_for_grid with args", args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.screeninfo = {}
        testobj.plotted_widgets = {}
        testobj.plotted_positions = {}
        testobj.lastrow = 0
        testobj.lastcol = 0
        testobj.unplotted = []
        testobj.unplotted_widgets = {}
        testobj.unplotted_positions = {}
        testobj.not_selectable = []
        testobj.nonsel_widgets = {}
        testobj.nonsel_positions = {}
        testobj.gbox1 = mockqtw.MockGridLayout()
        testobj.gbox2 = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\ncalled Grid.__init__\n"
        testobj.add_checkbox = mock_add
        testobj.add_items_to_grid = mock_add_items
        testobj.set_texts_for_grid = mock_set1
        testobj.set_checks_for_grid = mock_set2
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
                f"called Showmods.add_items_to_grid with args ({testobj.gbox1}, 0, 0, [])\n"
                f"called Showmods.add_items_to_grid with args ({testobj.gbox2}, 0, -1, [])\n"
                "called Showmods.set_texts_for_grid with args ({}, {})\n"
                "called Showmods.set_texts_for_grid with args ({}, {})\n"
                "called Showmods.set_checks_for_grid with args ({}, {})\n"
                "called Showmods.set_checks_for_grid with args ({}, {})\n")
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
                "called Showmods.set_texts_for_grid with args ({}, {})\n"
                "called Showmods.set_texts_for_grid with args ({}, {})\n"
                "called Showmods.set_checks_for_grid with args ({}, {})\n"
                "called Showmods.set_checks_for_grid with args ({}, {})\n")
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
                "called ShowMods.add_checkbox\n"
                "called Grid.addLayout with arg of type <class 'str'> at (1, 1)\n"
                f"called Showmods.add_items_to_grid with args ({testobj.gbox1}, 1, 1, ['yy'])\n"
                f"called Showmods.add_items_to_grid with args ({testobj.gbox2}, 0, -1, ['zz'])\n"
                "called Showmods.set_texts_for_grid with args"
                " ({(1, 1): ('xx', {'pos': '1x1', 'sel': True})}, {(1, 1): ('x', 'y', 'z')})\n"
                "called Showmods.set_texts_for_grid with args ({}, {})\n"
                "called Showmods.set_checks_for_grid with args"
                " ({(1, 1): ('xx', {'pos': '1x1', 'sel': True})}, {(1, 1): ('x', 'y', 'z')})\n"
                "called Showmods.set_checks_for_grid with args ({}, {})\n")

    def test_add_items_to_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.add_items_to_grid
        """
        def mock_add(*args):
            print("called ShowMods.add_checkbox")
            return 'a', 'b', 'c'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_checkbox = mock_add
        testobj.master.screeninfo = {'x': {}, 'y': {}, 'z': {}}
        gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        assert testobj.add_items_to_grid(gbox, 1, 1, []) == ({}, {})
        assert capsys.readouterr().out == ""
        assert testobj.add_items_to_grid(gbox, 1, 1, ['x', 'y', 'z']) == (
                {(1, 2): ('x', {'pos': '1x2'}), (2, 0): ('y', {'pos': '2x0'}),
                 (2, 1): ('z', {'pos': '2x1'})},
                {(1, 2): ('a', 'b', 'c'), (2, 0): ('a', 'b', 'c'), (2, 1): ('a', 'b', 'c')})
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
                "called Signal.disconnect\n"
                "called CheckBox.setEnabled with arg True\n"
                f"called Signal.connect with args ({testobj.enable_button},)\n"
                "called CheckBox.setChecked with arg False\n"
                "called Signal.disconnect\n"
                "called CheckBox.setEnabled with arg True\n"
                f"called Signal.connect with args ({testobj.enable_button},)\n"
                "called CheckBox.setChecked with arg True\n"
                "called Signal.disconnect\n"
                "called CheckBox.setChecked with arg False\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for ShowMods.add_checkbox
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.screentext = {}
        obj1, obj2, obj3 = testobj.add_checkbox()
        assert isinstance(obj1, testee.qtw.QHBoxLayout)
        assert isinstance(obj2, testee.qtw.QLabel)
        assert isinstance(obj3, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            "called HBox.__init__\n"
            "called CheckBox.__init__\n"
            "called CheckBox.setEnabled with arg False\n"
            # f"called Signal.connect with args ({testobj.enable_button},)\n"
            "called Label.__init__\n"
            # "called Label.setOpenExternalLinks with arg 'True'\n"
            # "called Label.setText with arg"
            # ' `<a href="https://www.nexusmods.com/stardewvalley/mods/1">xxxx</a>`\n'
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
        def mock_refresh(*args):
            print('called ShowMods.refresh_widgets with args', args)
        def mock_build(*args):
            print('called ShowMods.build_screen_text with args', args)
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        label = mockqtw.MockLabel()
        check = mockqtw.MockCheckBox()
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(
                    screeninfo={'current text': {'txt': 'xxx', 'sel': True, 'pos': '2x2'}},
                    attr_changes=[]),
                unplotted=['current text'], unplotted_widgets={(2, 2): ('', label, check)},
                not_selectable=[], nonsel_widgets={},
                refresh_widgets=mock_refresh,
                build_screen_text=mock_build)
        testobj.name = mockqtw.MockComboBox()
        testobj.clear_name_button = mockqtw.MockPushButton()
        testobj.text = mockqtw.MockLineEdit()
        testobj.clear_text_button = mockqtw.MockPushButton()
        testobj.activate_button = mockqtw.MockCheckBox()
        testobj.change_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called Label.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called LineEdit.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called CheckBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.choice = 'current text'
        testobj.update()
        assert testobj.parent.unplotted == []
        assert testobj.parent.not_selectable == ['current text']
        assert testobj.parent.master.screeninfo == {'current text': {'txt': '', 'sel': False,
                                                                     'pos': '2x2'}}
        assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == ("called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called CheckBox.isChecked\n"
                                           "called LineEdit.text\n"
                                           "called ComboBox.currentText\n"
                                           "called ShowMods.refresh_widgets with args ()\n")
        testobj.activate_button.setChecked(True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"
        testobj.parent.master.attr_changes = []
        testobj.parent.nonsel_widgets = {(2, 2): ('', label, check)}
        testobj.parent.unplotted_widgets = {}
        testobj.update()
        assert testobj.parent.unplotted == ['current text']
        assert testobj.parent.not_selectable == []
        assert testobj.parent.master.screeninfo == {'current text': {'txt': '', 'sel': True,
                                                                     'pos': '2x2'}}
        assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == ("called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called CheckBox.isChecked\n"
                                           "called LineEdit.text\n"
                                           "called ComboBox.currentText\n"
                                           "called ShowMods.refresh_widgets with args ()\n")

        testobj.text.setText('qqq')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `qqq`\n"
        testobj.parent.master.screeninfo = {'current text': {'txt': 'yyy', 'sel': True,
                                                             'pos': '2x2', 'key': 'qq'}}
        testobj.parent.unplotted_widgets = {(2, 2): ('', label, check)}
        testobj.parent.nonsel_widgets = {}
        testobj.parent.master.attr_changes = []
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': 'qqq', 'sel': True,
                                                                     'pos': '2x2', 'key': 'qq'}}
        assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == ("called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called CheckBox.isChecked\n"
                                           "called LineEdit.text\n"
                                           "called ComboBox.currentText\n"
                                           "called Label.setOpenExternalLinks with arg 'False'\n"
                                           "called ShowMods.build_screen_text with args "
                                           f"({label}, 'current text', 'qqq', 'qq')\n")
        testobj.choice = 'xxx'
        testobj.parent.master.screeninfo = {'xxx': {'txt': 'yyy', 'sel': True, 'pos': '2x2',
                                                    'key': 'qq'}}
        testobj.parent.master.attr_changes = []
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': 'qqq', 'sel': True,
                                                                     'pos': '2x2', 'key': 'qq'}}
        assert testobj.parent.master.attr_changes == [('current text', 'xxx')]
        assert capsys.readouterr().out == ("called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called PushButton.setDisabled with arg `True`\n"
                                           "called CheckBox.isChecked\n"
                                           "called LineEdit.text\n"
                                           "called ComboBox.currentText\n"
                                           "called Label.setOpenExternalLinks with arg 'False'\n"
                                           "called ShowMods.build_screen_text with args "
                                           f"({label}, 'current text', 'qqq', 'qq')\n")

        testobj.parent.master.screeninfo = {'xxx': {'txt': 'yyy', 'sel': True, 'pos': '2x2',
                                                    'key': 'qq'}}
        testobj.parent.master.attr_changes = []
        testobj.activate_button.setChecked(False)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg False\n"
        testobj.parent.unplotted = []
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': 'qqq', 'sel': False,
                                                                     'pos': '2x2', 'key': 'qq'}}
        assert testobj.parent.master.attr_changes == [('current text', 'xxx')]
        assert capsys.readouterr().out == (
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called CheckBox.isChecked\n"
                "called LineEdit.text\n"
                "called ComboBox.currentText\n"
                f"called MessageBox.information with args `{testobj}` `SDVMM` `Onselecteerbaar"
                " maken van mods met coordinaten in de config is helaas nog niet mogelijk`\n")
        testobj.choice = 'current text'
        testobj.parent.master.screeninfo = {'current text': {'txt': 'yyy', 'sel': False,
                                                             'pos': '2x2', 'key': 'qq'}}
        testobj.parent.master.attr_changes = []
        testobj.parent.nonsel_widgets = {(2, 2): ('', label, check)}
        testobj.text.setText('yyy')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `yyy`\n"
        testobj.update()
        assert testobj.parent.master.screeninfo == {'current text': {'txt': 'yyy', 'sel': False,
                                                                     'pos': '2x2', 'key': 'qq'}}
        assert testobj.parent.master.attr_changes == [('current text', '')]
        assert capsys.readouterr().out == (
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called CheckBox.isChecked\n"
                "called LineEdit.text\n"
                "called ComboBox.currentText\n")
