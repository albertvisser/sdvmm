import pytest
import pathlib
import activate

def mock_init(self, *args):
    self.conf = {}
    self.modnames = []
    self.modbase = 'modbase'
    self.directories = set()

def test_check_config(monkeypatch, capsys):
    monkeypatch.setattr(activate.Activate, '__init__', mock_init)
    testobj = activate.Activate()
    conf_ok = '\n'.join(('[test]', 'this', 'these', '', '[this]', 'those', '',
                         '[Mod Directories]', 'test: x', 'this: that, another', 'those: thoze',
                         'these: theze'))
    testobj.conf = activate.configparser.ConfigParser(allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf_ok)
    assert testobj.check_config() == ['No errors']
    conf_nok = '\n'.join(('[test]', 'this', 'these', '', '[this]', 'those', '',
                         '[Mod Directories]', 'test: x', 'This: that, another', 'Those: thoze'))
    testobj.conf = activate.configparser.ConfigParser(allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf_nok)
    assert testobj.check_config() == ['Unknown mod name `this` for expansion/mod `test`',
                                      'Unknown mod name `these` for expansion/mod `test`',
                                      'Unknown expansion / mod name: `this`',
                                      'Unknown mod name `those` for expansion/mod `this`']


def test_activate(monkeypatch, capsys):
    def mock_rename(*args):
        print('called os.rename() with args', args)
    monkeypatch.setattr(activate.os, 'scandir', lambda x: [pathlib.Path('modbase/test'),
                                                           pathlib.Path('modbase/.no'),
                                                           pathlib.Path('modbase/yes'),
                                                           pathlib.Path('modbase/on'),
                                                           pathlib.Path('modbase/.off')])
    monkeypatch.setattr(activate.os, 'rename', mock_rename)
    monkeypatch.setattr(activate.Activate, '__init__', mock_init)
    testobj = activate.Activate()
    testobj.conf['Mod Directories'] = {'SMAPI': ['test']}
    testobj.directories |= {'yes', 'off'}
    assert testobj.directories == {'yes', 'off'}
    testobj.activate()
    assert capsys.readouterr().out == ("called os.rename() with args (PosixPath('modbase/on'),"
                                       " 'modbase/.on')\n"
                                       "called os.rename() with args (PosixPath('modbase/.off'),"
                                       " 'modbase/off')\n")

def test_add_activations(monkeypatch):
    monkeypatch.setattr(activate.Activate, '__init__', mock_init)
    testobj = activate.Activate()
    testobj.conf = {'test': {'this': '', 'that': ''}, 'this': {'those': ''},
                    'Mod Directories': {'this': 'that, another', 'those': 'thoze'}}
    testobj.directories.add('that')
    assert testobj.directories == {'that'}
    testobj.add_activations('test', 'this')
    assert testobj.directories == {'that', 'another', 'thoze'}

def test_select_activations(monkeypatch, capsys):
    def mock_add(self, *args):
        print('called self.add_activations with args', args)
    monkeypatch.setattr(activate.Activate, '__init__', mock_init)
    monkeypatch.setattr(activate.Activate, 'add_activations', mock_add)
    testobj = activate.Activate()
    conf = '\n'.join(('[test]', 'this', '', '[other]', 'they', 'them', '', '[third]', 'oink', '',
                      '[Mod Directories]', 'test: x', 'this: y', 'other: z', 'they: a', 'them: b',
                      'third: c', 'oink: d'))
    testobj.conf = activate.configparser.ConfigParser(allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf)
    testobj.modnames = ['test', 'other']
    testobj.select_activations()
    assert capsys.readouterr().out == ("called self.add_activations with args ('test', 'this')\n"
                                       "called self.add_activations with args ('other', 'they')\n"
                                       "called self.add_activations with args ('other', 'them')\n")

def test_select_expansions(monkeypatch, capsys):
    class MockShowMods:
        def __init__(self, master):
            master.modnames = ['one', 'two', 'three']
        def show_screen(self):
            print('called gui.ShowMods.show_screen()')
    monkeypatch.setattr(activate.Activate, '__init__', mock_init)
    monkeypatch.setattr(activate.gui, 'ShowMods', MockShowMods)
    testobj = activate.Activate()
    testobj.conf = {}
    testobj.modnames = []
    testobj.select_expansions()
    assert testobj.modnames == ['one', 'two', 'three']
    assert capsys.readouterr().out == 'called gui.ShowMods.show_screen()\n'


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
        self.directories = []
        self.modnames = []
    def select_expansions(self):
        print('called Activate.select_expansions()')
    def select_activations(self):
        print('called Activate.select_activations()')
    def activate(self):
        print('called Activate.activate()')

def test_main(monkeypatch, capsys):
    def mock_select(self):
        self.directories = 'anything'
    monkeypatch.setattr(activate, 'Activate', MockActivate)
    monkeypatch.setattr(activate, 'CONFIG', 'filename')
    activate.main()
    assert capsys.readouterr().out == ("called Activate() with args filename\n"
                                       'called Activate.select_expansions()\n'
                                       "called Activate.select_activations()\n")
    monkeypatch.setattr(MockActivate, 'select_activations', mock_select)
    monkeypatch.setattr(activate, 'Activate', MockActivate)
    activate.main()
    assert capsys.readouterr().out == ("called Activate() with args filename\n"
                                       'called Activate.select_expansions()\n'
                                       'called Activate.activate()\n')
