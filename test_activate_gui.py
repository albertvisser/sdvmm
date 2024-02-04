"""unittests for ./activate_gui.py
"""
import types
import configparser
# import mockqtwidgets as mockqtw
import mockgui.mockqtwidgets as mockqtw
import activate_gui as gui


def test_showmods_init(monkeypatch, capsys):
    """unittest for activate_gui.ShowMods.init
    """
    def mock_app_init(self, *args):
        """stub
        """
        print('called qtw.QApplication.__init__()')
    def mock_init(self, *args):
        """stub
        """
        print('called qtw.QWidget.__init__()')
    # def mock_setup(self, *args):
    #     print('called ShowMods.setup_screen()')
    def mock_show(self, *args):
        """stub
        """
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
    """unittest for activate_gui.ShowMods.setup_screen
    """
    def mock_app_init(self, *args):
        """stub
        """
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        """stub
        """
        print('called QWidget.__init__()')
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
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw.QWidget, 'setWindowTitle', mock_setWindowTitle)
    monkeypatch.setattr(gui.qtw.QWidget, 'setLayout', mock_setLayout)
    monkeypatch.setattr(gui.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(gui.qtw, 'QCheckBox', mockqtw.MockCheckBox)
    monkeypatch.setattr(gui.qtw, 'QPushButton', mockqtw.MockPushButton)
    me = types.SimpleNamespace(modbase='modbase')
    testobj = gui.ShowMods(me)  # setup_screen wordt door deze aangeroepen
    monkeypatch.setattr(testobj, 'refresh_widgets', mock_refresh)
    testobj.setup_screen()
    assert capsys.readouterr().out == (
            'called QApplication.__init__()\n'
            'called QWidget.__init__()\n'
            'called QWidget.setWindowTitle()\n'
            'called VBox.__init__\n'
            'called HBox.__init__\n'
            "called Label.__init__ with args"
            " ('Dit overzicht toont de namen van expansies die je"
            " kunt activeren\\n(inclusief die al geactiveerd zijn).\\nIn"
            " de achterliggende configuratie is geregeld welke mods\\n"
            "hiervoor eventueel nog meer aangezet moeten worden',)\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            "called ShowMods.refresh_widgets with args () {'first_time': True}\n"
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            f"called PushButton.__init__ with args ('&Check config', {testobj}) {{}}\n"
            f"called Signal.connect with args ({testobj.check},)\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            f"called PushButton.__init__ with args ('&Activeer wijzigingen', {testobj}) {{}}\n"
            f"called Signal.connect with args ({testobj.confirm},)\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            f"called PushButton.__init__ with args ('&Klaar', {testobj}) {{}}\n"
            f"called Signal.connect with args ({testobj.close},)\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            'called HBox.addStretch\n'
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called QWidget.setLayout()\n')

def test_refresh_widgets(monkeypatch, capsys):
    """unittest for activate_gui.ShowMods.refresh_widgets
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
    monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QCheckBox', mockqtw.MockCheckBox)
    monkeypatch.setattr(gui.os.path, 'exists', mock_path)
    me = types.SimpleNamespace(modbase='modbase')
    me.conf = configparser.ConfigParser(allow_no_value=True)
    me.conf.optionxform = str
    me.conf.read_string('[one]\nfirst\n\n[two]\n\n'
                        '[Mod Directories]\none: one, eno\ntwo: two\nfirst: first')
    testobj = gui.ShowMods(me)  # setup_screen wordt door deze aangeroepen
    testobj.vbox = mockqtw.MockVBoxLayout()
    testobj.widgets = {}
    testobj.refresh_widgets(first_time=True)
    assert len(testobj.widgets) == len(testobj.master.conf.sections()) - 1
    assert isinstance(testobj.widgets['one'], gui.qtw.QCheckBox)
    assert isinstance(testobj.widgets['two'], gui.qtw.QCheckBox)
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
    testobj.widgets = {'one': gui.qtw.QCheckBox(), 'two': gui.qtw.QCheckBox()}
    assert capsys.readouterr().out == ('called CheckBox.__init__\n'
                                       'called CheckBox.__init__\n')
    testobj.refresh_widgets()
    assert capsys.readouterr().out == ('called CheckBox.setChecked with arg False\n'
                                       'called CheckBox.setChecked with arg True\n')

def test_setup_actions(monkeypatch, capsys):
    """unittest for activate_gui.ShowMods.setup_actions
    """
    def mock_app_init(self, *args):
        """stub
        """
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        """stub
        """
        print('called QWidget.__init__()')
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
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw.QWidget, 'addAction', mock_addAction)
    monkeypatch.setattr(gui.qgui, 'QAction', mockqtw.MockAction)
    monkeypatch.setattr(gui.ShowMods, 'confirm', mock_confirm)
    monkeypatch.setattr(gui.ShowMods, 'close', mock_close)
    me = types.SimpleNamespace(conf={})
    testobj = gui.ShowMods(me)
    testobj.setup_actions()
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       f"called Action.__init__ with args ('Done', {testobj})\n"
                                       f"called Signal.connect with args ({testobj.confirm},)\n"
                                       'called Action.setShortcut with arg `Ctrl+Enter`\n'
                                       'called QWidget.addAction()\n'
                                       f"called Action.__init__ with args ('Cancel', {testobj})\n"
                                       f"called Signal.connect with args ({testobj.close},)\n"
                                       'called Action.setShortcut with arg `Escape`\n'
                                       'called QWidget.addAction()\n')

def test_show_screen(monkeypatch, capsys):
    """unittest for activate_gui.ShowMods.show_screen
    """
    def mock_app_init(self, *args):
        """stub
        """
        print('called QApplication.__init__()')
    def mock_app_exec(self, *args):
        """stub
        """
        print('called QApplication.exec()')
        return 'okcode'
    def mock_init(self, *args):
        """stub
        """
        print('called QWidget.__init__()')
    def mock_show(self, *args):
        """stub
        """
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
    """unittest for activate_gui.ShowMods.confirm
    """
    def mock_app_init(self, *args):
        """stub
        """
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        """stub
        """
        print('called QWidget.__init__()')
    def mock_select():
        """stub
        """
        print('called Activate.select_activations')
    def mock_activate():
        """stub
        """
        print('called Activate.activate')
    def mock_refresh():
        """stub
        """
        print('called Activate.refresh_widgets')
    def mock_information(self, *args):
        """stub
        """
        print('called MessageBox.information with args', args)
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw.QMessageBox, 'information', mock_information)
    monkeypatch.setattr(gui.qtw, 'QCheckBox', mockqtw.MockCheckBox)
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
                                       'called CheckBox.__init__\n'
                                       'called CheckBox.setChecked with arg True\n'
                                       'called CheckBox.__init__\n'
                                       'called CheckBox.isChecked\n'
                                       'called CheckBox.isChecked\n'
                                       'called Activate.select_activations\n'
                                       'called Activate.activate\n'
                                       'called Activate.refresh_widgets\n'
                                       "called MessageBox.information with args"
                                       " ('Change Config', 'wijzigingen zijn doorgevoerd')\n")

def test_check(monkeypatch, capsys):
    """unittest for activate_gui.ShowMods.check
    """
    def mock_app_init(self, *args):
        """stub
        """
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        """stub
        """
        print('called QWidget.__init__()')
    def mock_information(self, *args):
        """stub
        """
        print('called MessageBox.information with args', args)
    def mock_check():  # self, *args):
        """stub
        """
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
