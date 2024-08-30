"""unittests for ./activate_gui.py
"""
import types
import configparser
import pytest
import mockgui.mockqtwidgets as mockqtw
import activate_gui as testee

showmods = """\
called QWidget.setWindowTitle()
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('Dit overzicht toont de namen van expansies die je kunt activeren (inclusief die al geactiveerd zijn).\\nIn de achterliggende configuratie is geregeld welke mods hiervoor eventueel nog meer aangezet moeten worden\\nDe onderstreepte items zijn hyperlinks; ze leiden naar de pagina waarvandaan ik ze van gedownload heb (doorgaans op Nexus)',)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Grid.__init__
called ShowMods.refresh_widgets with args () {{'first_time': True}}
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Install / update', {testobj}) {{}}
called PushButton.setToolTip with arg `Selecteer uit een lijst met recent gedownloade mods één of meer om te installeren`
called Signal.connect with args ({testobj.update},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Reorder mods on screen', {testobj}) {{}}
called Signal.connect with args ({testobj.reorder_gui},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('add &Mod to config', {testobj}) {{}}
called Signal.connect with args ({testobj.master.add_to_config},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Edit config', {testobj}) {{}}
called Signal.connect with args ({testobj.master.edit_config},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('Re&Load config', {testobj}) {{}}
called Signal.connect with args ({testobj.master.reload_config},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Check config', {testobj}) {{}}
called Signal.connect with args ({testobj.check},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Activeer wijzigingen', {testobj}) {{}}
called Signal.connect with args ({testobj.confirm},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Klaar', {testobj}) {{}}
called Signal.connect with args ({testobj.close},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called QWidget.setLayout()
"""
newmod = """\
called Widget.__init__
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
called CheckBox.__init__
called CheckBox.setChecked with arg True
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
reorder = """\
called Widget.__init__
called Dialog.__init__ with args {testobj.parent} () {{}}
called ReorderDialog.determine_rows_cols
called VBox.__init__
called Table.__init__ with arg {testobj}
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
populate = """\
called TableItem.__init__ with arg {}
called Table.setItem with args ({}, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)
"""


@pytest.fixture
def expected_output():
    "fixture returning output to be expected from (mostly) gui setup methods"
    results = {'showmods': showmods, 'newmod': newmod, 'add_depline': add_depline,
               'reorder': reorder}
    return results


class MockActivater:
    """stub for ./activate.Activater
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
    def select_activations(self):
        """stub
        """
        print('called Activater.select_activations')
    def activate(self):
        """stub
        """
        print('called Activater.activate')
    def reload_config(self):
        """stub
        """
        print('called Activater.reload_config()')
    def check_config(self):
        """stub
        """
        print('called Activater.check_config()')
        return ['result', 'another result']
    def reorder_gui(self):
        """stub
        """
        print('called Activater.reorder_gui()')


def test_show_dialog(capsys):
    """unittest for activate_gui.show_dialog
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
    """unittest for activate_gui.ShowMods
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for activate_gui.ShowMods object

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
        testobj = testee.ShowMods(MockActivater())
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
        assert master.modnames == []
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
            print('called Activater.refresh_widgets with args', kwargs)
        def mock_information(self, *args):
            """stub
            """
            print('called MessageBox.information with args', args)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_information)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh_widgets = mock_refresh
        check1 = testee.qtw.QCheckBox('check1', testobj)
        check1.setChecked(True)
        check2 = testee.qtw.QCheckBox('check2', testobj)
        testobj.widgets = {'check1': check1, 'check2': check2}
        testobj.confirm()
        assert testobj.master.modnames == ['check1']
        assert capsys.readouterr().out == ('called CheckBox.__init__\n'
                                           'called CheckBox.setChecked with arg True\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.isChecked\n'
                                           'called CheckBox.isChecked\n'
                                           'called Activater.select_activations\n'
                                           'called Activater.activate\n'
                                           'called Activater.refresh_widgets with'
                                           " args {'reorder_widgets': False}\n"
                                           "called MessageBox.information with args"
                                           " ('Change Config', 'wijzigingen zijn doorgevoerd')\n")

    def _test_refresh_widgets_old(self, monkeypatch, capsys):
        """unittest for ShowMods.refresh_widgets
        """
        counter = 0
        def mock_path(*args):
            """stub
            """
            nonlocal counter
            counter += 1
            if counter == 1:
                return False
            return True
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.os.path, 'exists', mock_path)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.conf = configparser.ConfigParser(allow_no_value=True)
        testobj.master.conf.optionxform = str
        testobj.master.conf.read_string('[Mod Directories]\noneone: one, eno\nonetwo: two\n'
                                        'twoone: three\ntwotwo: four\nfirst: first')
        testobj.master.screenpos = {'oneone': '0x0', 'onetwo': '0x1',
                                    'twoone': '1x0', 'twotwo': '1x1'}
        # assert list(testobj.master.conf['Mod Directories']) == []  # {}
        testobj.vbox = mockqtw.MockVBoxLayout()
        testobj.widgets = {}
        # breakpoint()
        testobj.refresh_widgets(first_time=True)
        # assert len(testobj.widgets) == len(testobj.master.conf.sections()) - 1
        assert isinstance(testobj.widgets['oneone'], testee.qtw.QCheckBox)
        assert isinstance(testobj.widgets['onetwo'], testee.qtw.QCheckBox)
        assert isinstance(testobj.widgets['twoone'], testee.qtw.QCheckBox)
        assert isinstance(testobj.widgets['twotwo'], testee.qtw.QCheckBox)
        assert capsys.readouterr().out == ('called VBox.__init__\n'
                                           'called HBox.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called HBox.addSpacing\n'
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           'called HBox.addStretch\n'
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                           'called CheckBox.setChecked with arg False\n'
                                           'called HBox.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called HBox.addSpacing\n'
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           'called HBox.addStretch\n'
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                           'called CheckBox.setChecked with arg True\n'
                                           'called HBox.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called HBox.addSpacing\n'
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           'called HBox.addStretch\n'
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                           'called CheckBox.setChecked with arg True\n'
                                           'called HBox.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called HBox.addSpacing\n'
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           'called HBox.addStretch\n'
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                           'called CheckBox.setChecked with arg True\n')
        counter = 0
        testobj.widgets = {'oneone': testee.qtw.QCheckBox(), 'onetwo': testee.qtw.QCheckBox(),
                           'twoone': testee.qtw.QCheckBox(), 'twotwo': testee.qtw.QCheckBox()}
        assert capsys.readouterr().out == ('called CheckBox.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.__init__\n'
                                           )
        testobj.refresh_widgets()
        assert capsys.readouterr().out == ('called CheckBox.setChecked with arg False\n'
                                           'called CheckBox.setChecked with arg True\n'
                                           'called CheckBox.setChecked with arg True\n'
                                           'called CheckBox.setChecked with arg True\n')

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
            print(f"called Activater.add_checkbox with arg '{text}'")
            hbox = mockqtw.MockHBoxLayout()
            check = mockqtw.MockCheckBox()
            label = mockqtw.MockLabel()
            assert capsys.readouterr().out == (f"called Activater.add_checkbox with arg '{text}'\n"
                                               "called HBox.__init__\n"
                                               "called CheckBox.__init__\n"
                                               "called Label.__init__\n")
            return hbox, check
        # monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        # monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee, 'maxpercol', 3)
        monkeypatch.setattr(testee.os.path, 'exists', mock_path)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_checkbox = mock_add
        testobj.master.conf = configparser.ConfigParser(allow_no_value=True)
        testobj.master.conf.optionxform = str
        testobj.master.conf.read_string('[Mod Directories]\noneone: one, eno\nonetwo: two\n'
                                        'twoone: three\ntwotwo: four\nfirst: first\n'
                                        '2neone: one, eno\n2netwo: two\n'
                                        '2woone: three\n2wotwo: four')
        testobj.master.screenpos = {'twoone': ['', ''], 'oneone': ['', ''],
                                    'onetwo': ['', ''], 'twotwo': ['', ''],
                                    '2woone': ['', ''], '2neone': ['', ''],
                                    '2netwo': ['', ''], '2wotwo': ['', '']}
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"

        testobj.widgets = {}
        testobj.containers = {}
        testobj.positions = {}
        testobj.refresh_widgets(first_time=True)
        assert len(testobj.widgets) == len(testobj.master.screenpos)
        assert list(testobj.widgets.keys()) == list(testobj.master.screenpos.keys())
        for x in testobj.widgets.values():
            assert isinstance(x, mockqtw.MockCheckBox)
        assert len(testobj.containers) == len(testobj.master.screenpos)
        assert list(testobj.containers.keys()) == list(testobj.master.screenpos.keys())
        for x in testobj.containers.values():
            assert isinstance(x, mockqtw.MockHBoxLayout)
        assert len(testobj.positions) == len(testobj.master.screenpos)
        assert list(testobj.positions.keys()) == [(0, 0), (0, 1), (0, 2), (1, 0),
                                                  (1, 1), (1, 2), (2, 0), (2, 1)]
        assert list(testobj.positions.values()) == list(testobj.master.screenpos.keys())
        assert capsys.readouterr().out == (
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 0)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 1)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 2)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 0)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 1)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 2)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (2, 0)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (2, 1)\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n")

        testobj.master.screenpos = {'oneone': ['0x0', '1'], 'onetwo': ['0x1', '3'],
                                    'twoone': ['1x0', '2'], 'twotwo': ['1x1', '4']}
        testobj.widgets = {}
        testobj.containers = {}
        testobj.positions = {}
        # breakpoint()
        testobj.refresh_widgets(first_time=True)
        assert len(testobj.widgets) == len(testobj.master.screenpos)
        assert list(testobj.widgets.keys()) == list(testobj.master.screenpos.keys())
        for x in testobj.widgets.values():
            assert isinstance(x, mockqtw.MockCheckBox)
        assert len(testobj.containers) == len(testobj.master.screenpos)
        assert list(testobj.containers.keys()) == list(testobj.master.screenpos.keys())
        for x in testobj.containers.values():
            assert isinstance(x, mockqtw.MockHBoxLayout)
        assert len(testobj.positions) == len(testobj.master.screenpos)
        assert list(testobj.positions.keys()) == [(0, 0), (0, 1), (1, 0), (1, 1)]
        assert list(testobj.positions.values()) == list(testobj.master.screenpos.keys())
        assert capsys.readouterr().out == (
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 0)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 1)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 0)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 1)\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n")
        texts = list(testobj.containers)
        testobj.refresh_widgets()
        assert capsys.readouterr().out == (
                f"called Grid.removeItem with args ({testobj.containers[texts[0]]},)\n"
                f"called Grid.removeItem with args ({testobj.containers[texts[1]]},)\n"
                f"called Grid.removeItem with args ({testobj.containers[texts[2]]},)\n"
                f"called Grid.removeItem with args ({testobj.containers[texts[3]]},)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 0)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 1)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 0)\n"
                "called Grid.addLayout with arg of type"
                " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 1)\n"
                "called Grid.update\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg True\n")
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
        obj1, obj2 = testobj.add_checkbox('xxxx', '123')
        assert isinstance(obj1, testee.qtw.QHBoxLayout)
        assert isinstance(obj2, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            "called HBox.__init__\n"
            "called CheckBox.__init__\n"
            "called Label.__init__\n"
            "called Label.setOpenExternalLinks with arg 'True'\n"
            "called Label.setText with arg"
            ' `<a href="https://www.nexusmods.com/stardewvalley/mods/123">xxxx</a>`\n'
            "called HBox.addSpacing\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called HBox.addStretch\n"
            "called HBox.addSpacing\n")

    def test_check(self, monkeypatch, capsys):
        """unittest for ShowMods.check
        """
        def mock_information(self, *args):
            """stub
            """
            print('called MessageBox.information with args', args)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.check()
        assert capsys.readouterr().out == ('called Activater.check_config()\n'
                                           "called MessageBox.information with args"
                                           " ('Check Config', 'result\\nanother result')\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for ShowMods.update
        """
        def mock_open(parent, *args, **kwargs):
            print('called FileDialog.getOpenFileNames with args', parent, args, kwargs)
            return ['name1', 'name2'], True
        def mock_update(arg):
            print(f"called Activater.update_mods with arg {arg}")
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
                "called Activater.update_mods with arg ['name1', 'name2']\n"
                "called MessageBox.information with args ('Change Config', 'xxx\\nyyy')\n")

    def test_add_entries_for_name(self, monkeypatch, capsys):
        """unittest for ShowMods.add_entries_for_name
        """
        def mock_add(text):
            print(f"called Activater.add_checkbox with arg '{text}'")
            return 'hbox', 'check'
        def mock_determine():
            print('called Activater.determine_newt_row_col')
            return 1, 2
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.containers, testobj.widgets, testobj.positions = {}, {}, {}
        testobj.add_checkbox = mock_add
        testobj.determine_next_row_col = mock_determine
        testobj.add_entries_for_name('name')
        assert testobj.containers['name'] == 'hbox'
        assert testobj.widgets['name'] == 'check'
        assert testobj.positions[1, 2] == 'name'
        assert capsys.readouterr().out == ("called Activater.add_checkbox with arg 'name'\n"
                                           'called Activater.determine_newt_row_col\n')

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
            print('called Activater.update_config_from_screenpos')
        monkeypatch.setattr(testee, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh_widgets = mock_refresh
        testobj.master.update_config_from_screenpos = mock_update
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.reorder_gui()
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" (<class 'activate_gui.ReorderDialog'>, {testobj}) {{}}\n")
        monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
        testobj.reorder_gui()
        assert testobj.widgets == {}
        assert testobj.containers == {}
        assert testobj.positions == {}
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" (<class 'activate_gui.ReorderDialog'>, {testobj}) {{}}\n"
                "called Activater.update_config_from_screenpos\n"
                "called ActivateGui.refresh_widgets\n")


class TestNewModDialog:
    """unittest for activate_gui.NewModDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for activate_gui.NewModDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called NewModDialog.__init__ with args', args)
        def mock_accept(self):
            print('called NewModDialog.accept')
        monkeypatch.setattr(testee.NewModDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.NewModDialog, 'accept', mock_accept)
        testobj = testee.NewModDialog()
        assert capsys.readouterr().out == 'called NewModDialog.__init__ with args ()\n'
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
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        parent = mockqtw.MockWidget()
        modnames = ['x', 'y']
        first_time = True
        testobj = testee.NewModDialog(parent, modnames, first_time)
        assert testobj.parent == parent
        assert testobj.modnames == ['x', 'y']
        assert testobj.deps == []
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == expected_output['newmod'].format(testobj=testobj)

    def test_select_mod(self, monkeypatch, capsys):
        """unittest for NewModDialog.select_mod
        """
        def mock_open(*args, **kwargs):
            print('called FileDialog.getOpenFileName with args', args, kwargs)
            return [], False
        def mock_open_2(*args, **kwargs):
            print('called FileDialog.getOpenFileName with args', args, kwargs)
            return ['name'], True
        def mock_determine(name):
            print(f"called Activater.determine_unpack_directory with arg '{name}'")
            return ''
        def mock_determine_2(name):
            print(f"called Activater.determine_unpack_directory with arg '{name}'")
            return 'name'
        def mock_information(self, *args):
            print('called MessageBox.information with args', args)
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_open)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(master=MockActivater())
        testobj.parent.master.determine_unpack_directory = mock_determine
        testobj.first_name = mockqtw.MockLineEdit()
        testobj.last_name = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\ncalled LineEdit.__init__\n"
        testobj.select_mod()
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileName with args ({testobj},)"
                " {'caption': 'Select mod', 'directory': 'Downloads',"
                " 'filter': 'Zip files (*.zip)'}\n")
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_open_2)
        testobj.select_mod()
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileName with args ({testobj},)"
                " {'caption': 'Select mod', 'directory': 'Downloads',"
                " 'filter': 'Zip files (*.zip)'}\n"
                "called Activater.determine_unpack_directory with arg '['name']'\n"
                "called MessageBox.information with args ('Read mod name',"
                ' "Can\'t auto-determine;\\nzipfile contains more than one base directory")\n')
        testobj.parent.master.determine_unpack_directory = mock_determine_2
        testobj.select_mod()
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileName with args ({testobj},)"
                " {'caption': 'Select mod', 'directory': 'Downloads',"
                " 'filter': 'Zip files (*.zip)'}\n"
                "called Activater.determine_unpack_directory with arg '['name']'\n"
                "called LineEdit.setText with arg `name`\n"
                "called LineEdit.setText with arg `name`\n")

    def test_add_depline(self, monkeypatch, capsys, expected_output):
        """unittest for NewModDialog.add_depline
        """
        def mock_update():
            print('called NewModDialog.update')
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.process_dep = lambda x: x
        testobj.update = mock_update
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == 'called VBox.__init__\n'
        testobj.can_activate = mockqtw.MockCheckBox()
        testobj.deps = []
        testobj.modnames = ['x', 'y']
        testobj.add_depline()
        assert len(testobj.deps) == 1
        assert isinstance(testobj.deps[0][0], testee.qtw.QComboBox)
        assert testobj.deps[0][1] == ''
        assert capsys.readouterr().out == expected_output['add_depline'].format(testobj=testobj)

    def test_process_dep(self, monkeypatch, capsys):
        """unittest for NewModDialog.process_dep
        """
        def mock_remove(arg):
            print(f'called NewModDialog.remove_depline with arg {arg}')
        def mock_show(parent, *args, **kwargs):
            print("called gui.show_dialog with args", args, kwargs)
            parent.dialog_data = {}
            return False
        def mock_show_2(parent, *args, **kwargs):
            print("called gui.show_dialog with args", args, kwargs)
            parent.dialog_data = {'mods': [('x', 'y')], 'deps': {'a': 'b'}, 'set_active': ['q', 'r']}
            return True

        monkeypatch.setattr(testee, 'show_dialog', mock_show)
        lbox = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.modnames = ['x', 'y']
        testobj.remove_depline = mock_remove
        testobj.deps = [('lbox', 'text'), (lbox, 'text2')]

        testobj.parent = types.SimpleNamespace(dialog_data={'mods': [('already, present')],
                                                            'deps': {},
                                                            'set_active': ['xxx']})
        testobj.process_dep(lbox, 0)
        assert capsys.readouterr().out == ("called gui.show_dialog with args"
                                           f" ({testobj}, ['x', 'y']) {{'first_time': False}}\n")
        monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
        testobj.process_dep(lbox, 0)
        assert testobj.parent.dialog_data == {'mods': ['already, present', ('x', 'y')],
                                              'deps': {'a': 'b'}, 'set_active': ['xxx', 'q']}
        assert testobj.deps == [('lbox', 'text'), (lbox, 'a')]
        assert capsys.readouterr().out == ("called gui.show_dialog with args"
                                           f" ({testobj}, ['x', 'y']) {{'first_time': False}}\n"
                                           "called ComboBox.addItems with arg `a`\n"
                                           "called ComboBox.setCurrentText with arg `a`\n")

        testobj.deps = [('lbox1', 'text1'), ('lbox2', 'text2')]
        testobj.process_dep('lbox2', 1)
        assert capsys.readouterr().out == "called NewModDialog.remove_depline with arg lbox2\n"

        testobj.deps = [(lbox, 'xx')]
        testobj.process_dep(lbox, 2)
        assert testobj.deps == [(lbox, '2')]
        assert capsys.readouterr().out == "called ComboBox.itemText with value `2`\n"

    def test_remove_depline(self, monkeypatch, capsys):
        """unittest for NewModDialog.remove_depline
        """
        def mock_update():
            print('called NewModDialog.update')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update = mock_update
        testobj.vbox = mockqtw.MockVBoxLayout()
        testobj.can_activate = mockqtw.MockCheckBox()
        lbox1 = mockqtw.MockComboBox()
        lbox2 = mockqtw.MockComboBox()
        assert capsys.readouterr().out == ("called VBox.__init__\ncalled CheckBox.__init__\n"
                                           "called ComboBox.__init__\ncalled ComboBox.__init__\n")
        testobj.deps = [(lbox1, 'xxx'), (lbox2, 'yyy')]
        testobj.remove_depline(lbox1)
        assert capsys.readouterr().out == ("called VBox.removeWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockComboBox'>\n"
                                           "called ComboBox.close\n"
                                           "called NewModDialog.update\n")
        testobj.remove_depline(lbox2)
        assert capsys.readouterr().out == ("called VBox.removeWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockComboBox'>\n"
                                           "called CheckBox.setEnabled with arg True\n"
                                           "called ComboBox.close\n"
                                           "called NewModDialog.update\n")

    def test_update_deps(self, monkeypatch, capsys):
        """unittest for NewModDialog.update_deps
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.first_name = mockqtw.MockLineEdit('aaa')
        testobj.last_name = mockqtw.MockLineEdit('bbb')
        testobj.can_activate = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == (
                "called LineEdit.__init__\ncalled LineEdit.__init__\ncalled CheckBox.__init__\n")
        testobj.deps = [('x', 'dep1'), ('y', 'dep2')]
        testobj.parent = types.SimpleNamespace(dialog_data={'mods': [('already, present')],
                                                            'deps': {},
                                                            'set_active': ['xxx']})
        testobj.update_deps()
        assert testobj.parent.dialog_data == {'mods': [('aaa', 'bbb'), 'already, present'],
                                              'deps': {'aaa': ['dep1', 'dep2']},
                                              'set_active': ['xxx']}
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called NewModDialog.accept\n")
        testobj.deps = [('x', 'dep1'), ('y', 'dep2')]
        testobj.parent = types.SimpleNamespace(dialog_data={'mods': [('already, present')],
                                                            'deps': {},
                                                            'set_active': ['xxx']})
        testobj.can_activate.setChecked(True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"
        testobj.update_deps()
        assert testobj.parent.dialog_data == {'mods': [('aaa', 'bbb'), 'already, present'],
                                              'deps': {'aaa': ['dep1', 'dep2']},
                                              'set_active': ['xxx', 'aaa']}
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called NewModDialog.accept\n")


class TestReorderDialog:
    """unittest for activate_gui.ReorderDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for activate_gui.ReorderDialog object

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
        parent.master = MockActivater()
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
        assert capsys.readouterr().out == (f"called Table.__init__ with arg {testobj}\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        return testobj.table

    def test_determine_rows_cols(self, monkeypatch, capsys):
        """unittest for ReorderDialog.determine_rows_cols
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.data = {'xxx': '', 'yyy': '', 'zzz': '', 'qqq': '', 'rrr': ''}
        assert testobj.determine_rows_cols() == (2, 3)
        testobj.data = {'xxx': '', 'yyy': '', 'zzz': '', 'qqq': '', 'rrr': '', 'sss': ''}
        assert testobj.determine_rows_cols() == (2, 3)
        testobj.data = {'xxx': '', 'yyy': '', 'zzz': '', 'qqq': '', 'rrr': '', 'sss': '', 'ttt': ''}
        assert testobj.determine_rows_cols() == (3, 3)
        testobj.data = {'xxx': '1x1', 'yyy': '2x1', 'zzz': '0x0'}
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
                                           + populate.format('aaa', '0, 0')
                                           + populate.format('bbb', '1, 0')
                                           + populate.format('ccc', '2, 0')
                                           + "called Table.rowCount\n"
                                           + populate.format('ddd', '0, 1')
                                           + populate.format('eee', '1, 1')
                                           + populate.format('fff', '2, 1'))
        testobj.table.setColumnCount(3)
        assert capsys.readouterr().out == ("called Table.setColumnCount with arg '3'\n")
        testobj.populate()
        assert capsys.readouterr().out == ("called Table.clear\n"
                                           "called Table.columnCount\n"
                                           "called Table.rowCount\n"
                                           + populate.format('aaa', '0, 0')
                                           + populate.format('bbb', '1, 0')
                                           + populate.format('ccc', '2, 0')
                                           + "called Table.rowCount\n"
                                           + populate.format('ddd', '0, 1')
                                           + populate.format('eee', '1, 1')
                                           + populate.format('fff', '2, 1')
                                           + "called Table.rowCount\n"
                                           + populate.format('ggg', '0, 2'))
        testobj.data = {'aaa': '1x1', 'bbb': '0x0', 'ccc': '0x1', 'ddd': '1x2', 'eee': '3x1',
                        'fff': '1x0', 'ggg': '2x2'}
        testobj.populate()
        assert capsys.readouterr().out == ("called Table.clear\n"
                                           + populate.format('bbb', '0, 0')
                                           + populate.format('ccc', '0, 1')
                                           + populate.format('fff', '1, 0')
                                           + populate.format('aaa', '1, 1')
                                           + populate.format('ddd', '1, 2')
                                           + populate.format('ggg', '2, 2')
                                           + populate.format('eee', '3, 1'))

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
        testobj._parent.master = MockActivater()
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
                                           + populate.format('bbb', '0, 0')
                                           + populate.format('fff', '1, 0')
                                           + populate.format('ddd', '2, 0')
                                           + populate.format('ccc', '0, 1')
                                           + populate.format('aaa', '1, 1')
                                           + populate.format('eee', '2, 1')
                                           + populate.format('ggg', '0, 2'))
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
