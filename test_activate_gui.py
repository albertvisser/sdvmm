import types
import configparser
import pytest
import activate_gui as gui


class MockSignal:
    def __init__(self, *args):
        print('called signal.__init__()')
    def connect(self, *args):
        print('called signal.connect()')


class MockAction:
    triggered = MockSignal()
    def __init__(self, text, func):
        print('called action.__init__()')
        self.label = text
        self.callback = func
        self.shortcuts = []
        self.checkable = self.checked = False
        self.statustip = ''
    def setCheckable(self, state):
        self.checkable = state
    def setChecked(self, state):
        self.checked = state
    def setShortcut(self, data):
        print('call action.setShortcut with arg `{}`'.format(data))
    def setShortcuts(self, data):
        self.shortcuts = data
    def setStatusTip(self, data):
        self.statustip = data


class MockVBoxLayout:
    def __init__(self, *args):
        print('called MockVBoxLayout.__init__()')
    def addWidget(self, *args):
        print('called vbox.addWidget()')
    def addLayout(self, *args):
        print('called vbox.addLayout()')
    def addStretch(self, *args):
        print('called vbox.addStretch()')
    def addSpacing(self, *args):
        print('called vbox.addSpacing()')


class MockHBoxLayout:
    def __init__(self, *args):
        print('called MockHBoxLayout.__init__()')
    def addWidget(self, *args):
        print('called hbox.addWidget()')
    def addLayout(self, *args):
        print('called hbox.addLayout()')
    def addSpacing(self, *args):
        print('called hbox.addSpacing()')
    def addStretch(self, *args):
        print('called hbox.addStretch()')
    def insertStretch(self, *args):
        print('called hbox.insertStretch()')


class MockLabel:
    def __init__(self, *args):
        print('called MockLabel.__init__()')


class MockCheckBox:
    def __init__(self, *args):
        print('called MockCheckBox.__init__()')
        self.checked = None
        self.textvalue = args[0] if args else ''
    def setChecked(self, value):
        print('called check.setChecked({})'.format(value))
        self.checked = value
    def isChecked(self):
        print('called check.isChecked()')
        return self.checked
    def text(self):
        return self.textvalue


class MockPushButton:
    def __init__(self, *args):
        print('called MockPushButton.__init__()')
        self.clicked = MockSignal()


def test_showmods_init(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called qtw.QApplication.__init__()')
    def mock_init(self, *args):
        print('called qtw.QWidget.__init__()')
    # def mock_setup(self, *args):
    #     print('called ShowMods.setup_screen()')
    def mock_show(self, *args):
        print('called ShowMods.show_screen()')
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    # monkeypatch.setattr(gui.ShowMods, 'setup_screen', mock_setup)
    me = types.SimpleNamespace()
    testobj = gui.ShowMods(me)
    assert isinstance(testobj, gui.qtw.QWidget)
    assert testobj.master == me
    assert me.modnames == []
    # assert testobj.filenames == ['file', 'name']
    assert hasattr(testobj, 'app')
    assert isinstance(testobj.app, gui.qtw.QApplication)
    assert capsys.readouterr().out == (
        'called qtw.QApplication.__init__()\n'
        'called qtw.QWidget.__init__()\n')
        # 'called ShowMods.setup_screen()\n')

def test_setup_screen(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        print('called QWidget.__init__()')
    def mock_setWindowTitle(self, *args):
        print('called QWidget.setWindowTitle()')
    def mock_refresh(*args, **kwargs):
        print('called ShowMods.refresh_widgets with args', args, kwargs)
    def mock_setLayout(self, *args):
        print('called QWidget.setLayout()')
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw.QWidget, 'setWindowTitle', mock_setWindowTitle)
    monkeypatch.setattr(gui.qtw.QWidget, 'setLayout', mock_setLayout)
    monkeypatch.setattr(gui.qtw, 'QVBoxLayout', MockVBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QHBoxLayout', MockHBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
    monkeypatch.setattr(gui.qtw, 'QCheckBox', MockCheckBox)
    monkeypatch.setattr(gui.qtw, 'QPushButton', MockPushButton)
    me = types.SimpleNamespace(modbase='modbase')
    testobj = gui.ShowMods(me)  # setup_screen wordt door deze aangeroepen
    monkeypatch.setattr(testobj, 'refresh_widgets', mock_refresh)
    testobj.setup_screen()
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called QWidget.setWindowTitle()\n'
                                       'called MockVBoxLayout.__init__()\n'
                                       'called MockHBoxLayout.__init__()\n'
                                       'called MockLabel.__init__()\n'
                                       'called hbox.addWidget()\n'
                                       'called vbox.addLayout()\n'
                                       'called ShowMods.refresh_widgets with args'
                                       " () {'first_time': True}\n"
                                       'called MockHBoxLayout.__init__()\n'
                                       'called hbox.addStretch()\n'
                                       'called MockPushButton.__init__()\n'
                                       'called signal.__init__()\n'
                                       'called signal.connect()\n'
                                       'called hbox.addWidget()\n'
                                       'called MockPushButton.__init__()\n'
                                       'called signal.__init__()\n'
                                       'called signal.connect()\n'
                                       'called hbox.addWidget()\n'
                                       'called MockPushButton.__init__()\n'
                                       'called signal.__init__()\n'
                                       'called signal.connect()\n'
                                       'called hbox.addWidget()\n'
                                       'called hbox.addStretch()\n'
                                       'called vbox.addLayout()\n'
                                       'called QWidget.setLayout()\n')

def test_refresh_widgets(monkeypatch, capsys):
    counter = 0
    def mock_path(*args):
        nonlocal counter
        counter += 1
        if counter == 1: return False
        return True
    monkeypatch.setattr(gui.qtw, 'QHBoxLayout', MockHBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QCheckBox', MockCheckBox)
    monkeypatch.setattr(gui.os.path, 'exists', mock_path)
    me = types.SimpleNamespace(modbase='modbase')
    me.conf = configparser.ConfigParser(allow_no_value=True)
    me.conf.optionxform = str
    me.conf.read_string( '\n'.join(('[one]', 'first', '', '[two]', '',
                                    '[Mod Directories]', 'one: one, eno', 'two: two',
                                    'first: first')))
    testobj = gui.ShowMods(me)  # setup_screen wordt door deze aangeroepen
    testobj.vbox  = MockVBoxLayout()
    testobj.widgets = {}
    testobj.refresh_widgets(first_time=True)
    assert len(testobj.widgets) == 2
    assert isinstance(testobj.widgets['one'], gui.qtw.QCheckBox)
    assert isinstance(testobj.widgets['two'], gui.qtw.QCheckBox)
    assert capsys.readouterr().out == ('called MockVBoxLayout.__init__()\n'
                                       'called MockHBoxLayout.__init__()\n'
                                       'called MockCheckBox.__init__()\n'
                                       'called hbox.addSpacing()\n'
                                       'called hbox.addWidget()\n'
                                       'called hbox.addStretch()\n'
                                       'called vbox.addLayout()\n'
                                       'called check.setChecked(False)\n'
                                       'called MockHBoxLayout.__init__()\n'
                                       'called MockCheckBox.__init__()\n'
                                       'called hbox.addSpacing()\n'
                                       'called hbox.addWidget()\n'
                                       'called hbox.addStretch()\n'
                                       'called vbox.addLayout()\n'
                                       'called check.setChecked(True)\n')
    counter = 0
    testobj.widgets = {'one': gui.qtw.QCheckBox(), 'two': gui.qtw.QCheckBox()}
    assert capsys.readouterr().out == ('called MockCheckBox.__init__()\n'
                                       'called MockCheckBox.__init__()\n')
    testobj.refresh_widgets()
    assert capsys.readouterr().out == ('called check.setChecked(False)\n'
                                       'called check.setChecked(True)\n')

def test_setup_actions(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        print('called QWidget.__init__()')
    def mock_addAction(self, *args):
        print('called QWidget.addAction()')
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw.QWidget, 'addAction', mock_addAction)
    monkeypatch.setattr(gui.qgui, 'QAction', MockAction)
    me = types.SimpleNamespace(conf={})
    testobj = gui.ShowMods(me)
    testobj.setup_actions()
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called action.__init__()\n'
                                       'called signal.connect()\n'
                                       'call action.setShortcut with arg `Ctrl+Enter`\n'
                                       'called QWidget.addAction()\n'
                                       'called action.__init__()\n'
                                       'called signal.connect()\n'
                                       'call action.setShortcut with arg `Escape`\n'
                                       'called QWidget.addAction()\n')

def test_show_screen(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called QApplication.__init__()')
    def mock_app_exec(self, *args):
        print('called QApplication.exec()')
        return 'okcode'
    def mock_init(self, *args):
        print('called QWidget.__init__()')
    def mock_show(self, *args):
        print('called QWidget.show()')
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QApplication, 'exec', mock_app_exec)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw.QWidget, 'show', mock_show)
    me = types.SimpleNamespace(conf={})
    testobj = gui.ShowMods(me)
    assert testobj.show_screen() == 'okcode'
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called QWidget.show()\n'
                                       'called QApplication.exec()\n')

def test_confirm(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        print('called QWidget.__init__()')
    def mock_select():
        print('called Activate.select_activations')
    def mock_activate():
        print('called Activate.activate')
    def mock_refresh():
        print('called Activate.refresh_widgets')
    def mock_information(self, *args):
        print('called MessageBox.information with args', args)
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw.QMessageBox, 'information', mock_information)
    monkeypatch.setattr(gui.qtw, 'QCheckBox', MockCheckBox)
    me = types.SimpleNamespace(conf={}, select_activations=mock_select, activate=mock_activate,
                               directories=['x'])
    testobj = gui.ShowMods(me)
    monkeypatch.setattr(testobj, 'refresh_widgets', mock_refresh)
    check1 = gui.qtw.QCheckBox('check1', testobj)
    check1.setChecked(True)
    check2 = gui.qtw.QCheckBox('check2', testobj)
    testobj.widgets = {'check1': check1, 'check2': check2}
    testobj.confirm()
    assert me.modnames == ['check1']
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called MockCheckBox.__init__()\n'
                                       'called check.setChecked(True)\n'
                                       'called MockCheckBox.__init__()\n'
                                       'called check.isChecked()\n'
                                       'called check.isChecked()\n'
                                       'called Activate.select_activations\n'
                                       'called Activate.activate\n'
                                       'called Activate.refresh_widgets\n'
                                       "called MessageBox.information with args"
                                       " ('Change Config', 'wijzigingen zijn doorgevoerd')\n")

def test_check(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        print('called QWidget.__init__()')
    def mock_information(self, *args):
        print('called MessageBox.information with args', args)
    def mock_check(): #  self, *args):
        print('called Activate.check_config()')
        return ['result', 'another result']
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw.QMessageBox, 'information', mock_information)
    me = types.SimpleNamespace(check_config=mock_check)
    testobj = gui.ShowMods(me)
    testobj.check()
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called Activate.check_config()\n'
                                       "called MessageBox.information with args"
                                       " ('Check Config', 'result\\nanother result')\n")
