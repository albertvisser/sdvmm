import pytest
import pathlib
import activate

def mock_init(self, *args):
    self.conf = {}
    self.directories = set()

def test_activate(monkeypatch, capsys):
    def mock_rename(*args):
        print('called os.rename() with args', args)
    monkeypatch.setattr(activate, 'MODBASE', 'test')
    monkeypatch.setattr(activate.os, 'scandir', lambda x: [pathlib.Path('test/test'),
                                                           pathlib.Path('test/.no'),
                                                           pathlib.Path('test/yes'),
                                                           pathlib.Path('test/on'),
                                                           pathlib.Path('test/.off')])
    monkeypatch.setattr(activate.os, 'rename', mock_rename)
    monkeypatch.setattr(activate.Activate, '__init__', mock_init)
    testobj = activate.Activate()
    testobj.conf['Mod Directories'] = {'SMAPI': ['test']}
    testobj.directories |= {'yes', 'off'}
    assert testobj.directories == {'yes', 'off'}
    testobj.activate()
    assert capsys.readouterr().out == ("called os.rename() with args (PosixPath('test/on'),"
                                       " 'test/.on')\n"
                                       "called os.rename() with args (PosixPath('test/.off'),"
                                       " 'test/off')\n")

def test_add_activations(monkeypatch):
    monkeypatch.setattr(activate.Activate, '__init__', mock_init)
    testobj = activate.Activate()
    testobj.conf = {'test': {'this': '', 'that': ''}, 'this': {'those': ''},
                    'Mod Directories': {'this': 'that, another', 'those': 'thoze'}}
    testobj.directories.add('that')
    assert testobj.directories == {'that'}
    testobj.add_activations('test', 'this')
    assert testobj.directories == {'this', 'that', 'those'}

def test_select_activations(monkeypatch, capsys):
    def mock_add(self, *args):
        print('called self.add_activations with args', args)
    monkeypatch.setattr(activate.Activate, '__init__', mock_init)
    monkeypatch.setattr(activate.Activate, 'add_activations', mock_add)
    testobj = activate.Activate()
    testobj.conf = {'test': ['this'], 'other': ['they', 'them'], 'third': ['oink']}
    testobj.select_activations(['test', 'other'])
    assert capsys.readouterr().out == ("called self.add_activations with args ('test', 'this')\n"
                                       "called self.add_activations with args ('other', 'they')\n"
                                       "called self.add_activations with args ('other', 'them')\n")

def test_select_expansions(monkeypatch, capsys):
    def mock_showmods(master):
        master.modnames = master.conf['Expansions']
    monkeypatch.setattr(activate.Activate, '__init__', mock_init)
    monkeypatch.setattr(activate.gui, 'ShowMods', mock_showmods)
    testobj = activate.Activate()
    testobj.conf = {'Expansions': ('one', 'two', 'three')}
    assert testobj.select_expansions() == ('one', 'two', 'three')


class MockParser:
    def __init__(self, *args, **kwargs):
        print('called ConfigParser() with args', args, kwargs)
    def read(self, *args):
        print('called ConfigParser.read() with args', args)

def test_init(monkeypatch, capsys):
    monkeypatch.setattr(activate.configparser, 'ConfigParser', MockParser)
    conf = activate.Activate('config')
    assert capsys.readouterr().out == (
            "called ConfigParser() with args () {'allow_no_value': True}\n"
            "called ConfigParser.read() with args ('config',)\n")
    assert conf.conf.optionxform == str
    assert not conf.directories
    assert type(conf.directories) == set

class MockActivate:
    def __init__(self, args):
        print('called Activate() with args', args)
    def select_expansions(self):
        print('called Activate.select_expansions()')
        return ['x']
    def select_activations(self, args):
        print('called Activate.select_activations() with args', args)
        return ['y', 'z']
    def activate(self):
        print('called Activate.activate()')

def test_main(monkeypatch, capsys):
    monkeypatch.setattr(activate, 'Activate', MockActivate)
    monkeypatch.setattr(activate, 'CONFIG', 'filename')
    activate.main()
    assert capsys.readouterr().out == ("called Activate() with args filename\n"
                                       'called Activate.select_expansions()\n'
                                       "called Activate.select_activations() with args ['x']\n"
                                       'called Activate.activate()\n')
