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
called Label.__init__ with args ('Dit overzicht toont de namen van expansies die je kunt activeren (inclusief die al geactiveerd zijn).\\nIn de achterliggende configuratie is geregeld welke mods hiervoor eventueel nog meer aangezet moeten worden',)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called ShowMods.refresh_widgets with args () {{'first_time': True}}
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('add &Mod', {testobj}) {{}}
called Signal.connect with args ({testobj.master.add_to_config},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Edit config', {testobj}) {{}}
called Signal.connect with args ({testobj.master.edit_config},)
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
called Dialog.__init__ with args {parent} () {{}}
called Grid.__init__
called Label.__init__ with args ('Mod name:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)
called LineEdit.__init__
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (0, 1)
called Label.__init__ with args ('Unpack directory:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 0)
called LineEdit.__init__
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 1)
called CheckBox.__init__
called CheckBox.setChecked with arg True
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'> at (2, 0, 1, 2)
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Add dependency', {testobj}) {{}}
called Signal.connect with args ({testobj.add_depline},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Update', {testobj}) {{}}
called Signal.connect with args ({testobj.update_deps},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (3, 0, 1, 2)
called VBox.__init__
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'> at (4, 0, 1, 2)
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


@pytest.fixture
def expected_output():
    "fixture returning output to be expected from (mostly) gui setup methods"
    results = {'showmods': showmods, 'newmod': newmod, 'add_depline': add_depline}
    return results


class MockActivate:
    """stub for ./activate.Activate
    """
    def __init__(self):
        self.modbase = 'modbase'
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
        print('called Activate.select_activations')
    def activate(self):
        """stub
        """
        print('called Activate.activate')
    def check_config(self):
        """stub
        """
        print('called Activate.check_config()')
        return ['result', 'another result']


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
    assert testee.show_dialog(cls, parent, modnames, True) == (False, {'mods': [], 'deps': {},
                                                                       'set_active': []})
    assert capsys.readouterr().out == (
        "called Dialog.__init__ with args"
        " namespace(dialog_data={'mods': [], 'deps': {}, 'set_active': []}) (['x', 'y'], True) {}\n"
        "called Dialog.exec\n")
    cls.exec = mock_exec_2
    assert testee.show_dialog(cls, parent, modnames, False) == (True, {'mods': [], 'deps': {},
                                                                       'set_active': []})
    assert capsys.readouterr().out == (
        "called Dialog.__init__ with args"
        " namespace(dialog_data={'mods': [], 'deps': {}, 'set_active': []}) (['x', 'y'], False) {}\n"
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
        testobj = testee.ShowMods(MockActivate())
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
                'called Action.setShortcut with arg `Escape`\n'
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
        def mock_refresh():
            """stub
            """
            print('called Activate.refresh_widgets')
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
                                           'called Activate.select_activations\n'
                                           'called Activate.activate\n'
                                           'called Activate.refresh_widgets\n'
                                           "called MessageBox.information with args"
                                           " ('Change Config', 'wijzigingen zijn doorgevoerd')\n")

    def test_refresh_widgets(self, monkeypatch, capsys):
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
        testobj.master.conf.read_string('[one]\nfirst\n\n[two]\n\n'
                                        '[Mod Directories]\none: one, eno\ntwo: two\nfirst: first')
        testobj.vbox = mockqtw.MockVBoxLayout()
        testobj.widgets = {}
        testobj.refresh_widgets(first_time=True)
        assert len(testobj.widgets) == len(testobj.master.conf.sections()) - 1
        assert isinstance(testobj.widgets['one'], testee.qtw.QCheckBox)
        assert isinstance(testobj.widgets['two'], testee.qtw.QCheckBox)
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
                                           'called CheckBox.setChecked with arg True\n')
        counter = 0
        testobj.widgets = {'one': testee.qtw.QCheckBox(), 'two': testee.qtw.QCheckBox()}
        assert capsys.readouterr().out == ('called CheckBox.__init__\n'
                                           'called CheckBox.__init__\n')
        testobj.refresh_widgets()
        assert capsys.readouterr().out == ('called CheckBox.setChecked with arg False\n'
                                           'called CheckBox.setChecked with arg True\n')

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
        assert capsys.readouterr().out == ('called Activate.check_config()\n'
                                           "called MessageBox.information with args"
                                           " ('Check Config', 'result\\nanother result')\n")


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
        assert capsys.readouterr().out == expected_output['newmod'].format(testobj=testobj,
                                                                           parent=parent)

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
        def mock_show(*args, **kwargs):
            print("called gui.show_dialog with args", args, kwargs)
            return False, {}
        def mock_show_2(*args, **kwargs):
            print("called gui.show_dialog with args", args, kwargs)
            return True, {'mods': [('x', 'y')], 'deps': {'a': 'b'}, 'set_active': ['q', 'r']}

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
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args (<class 'activate_gui.NewModDialog'>,"
                f" {testobj}, ['x', 'y']) {{'first_time': False}}\n")
        monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
        testobj.process_dep(lbox, 0)
        assert testobj.parent.dialog_data == {'mods': ['already, present', ('x', 'y')],
                                              'deps': {'a': 'b'}, 'set_active': ['xxx', 'q']}
        assert testobj.deps == [('lbox', 'text'), (lbox, 'a')]
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args (<class 'activate_gui.NewModDialog'>,"
                f" {testobj}, ['x', 'y']) {{'first_time': False}}\n"
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
                                              'set_active': ['xxx', '']}
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
