import pytest
import types
import activate_gui as gui


def test_showmods_init(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called qtw.QApplication.__init__() with args', args)
    def mock_setup(self, *args):
        print('called ShowMods.setup_screen()')
    def mock_show(self, *args):
        print('called ShowMods.show_screen()')
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_init)
    monkeypatch.setattr(gui.ShowMods, 'setup_screen', mock_setup)
    monkeypatch.setattr(gui.ShowMods, 'show_screen', mock_show)
    me = types.SimpleNamespace()
    testobj = gui.ShowMods(me)
    assert type(testobj) == gui.qtw.QWidget
    assert testobj.master == me
    assert me.filedata == []
    assert testobj.filenames == ['file', 'name']
    assert hasattr(testobj, 'app')
    assert type(testobj.app) == gui.qtw.QApplication
    assert capsys.readouterr().out == (
        'called qtw.QApplication.__init__() with args ()\n'
        'called Gui.setup_screen()\n'
        'called Gui.show_screen()\n')

