import pytest
import pathlib
import activate as testee

def mock_init(self, *args):
    self.conf = {}
    self.modnames = []
    self.modbase = 'modbase'
    self.directories = set()

def test_check_config(monkeypatch, capsys):
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    testobj = testee.Activate()
    conf_ok = '\n'.join(('[test]', 'this', 'these', '', '[this]', 'those', '',
                         '[Mod Directories]', 'test: x', 'this: that, another', 'those: thoze',
                         'these: theze'))
    testobj.conf = testee.configparser.ConfigParser(allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf_ok)
    assert testobj.check_config() == ['No errors']
    conf_nok = '\n'.join(('[test]', 'this', 'these', '', '[this]', 'those', '',
                         '[Mod Directories]', 'test: x', 'This: that, another', 'Those: thoze'))
    testobj.conf = testee.configparser.ConfigParser(allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf_nok)
    assert testobj.check_config() == ['Unknown mod name `this` for expansion/mod `test`',
                                      'Unknown mod name `these` for expansion/mod `test`',
                                      'Unknown expansion / mod name: `this`',
                                      'Unknown mod name `those` for expansion/mod `this`']


def test_activate(monkeypatch, capsys):
    def mock_rename(*args):
        print('called os.rename() with args', args)
    def mock_isfile(arg):
        return arg.stem == 'file'
    monkeypatch.setattr(testee.os, 'scandir', lambda x: [pathlib.Path('modbase/test'),
                                                         pathlib.Path('modbase/.no'),
                                                         pathlib.Path('modbase/yes'),
                                                         pathlib.Path('modbase/on'),
                                                         pathlib.Path('modbase/file'),
                                                         pathlib.Path('modbase/.off')])
    monkeypatch.setattr(testee.os, 'rename', mock_rename)
    monkeypatch.setattr(pathlib.Path, 'is_file', mock_isfile)
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    testobj = testee.Activate()
    testobj.conf['Mod Directories'] = {'SMAPI': ['test']}
    testobj.directories |= {'yes', 'off'}
    assert testobj.directories == {'yes', 'off'}
    testobj.activate()
    assert capsys.readouterr().out == ("called os.rename() with args (PosixPath('modbase/on'),"
                                       " 'modbase/.on')\n"
                                       "called os.rename() with args (PosixPath('modbase/.off'),"
                                       " 'modbase/off')\n")

def test_add_activations(monkeypatch):
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    testobj = testee.Activate()
    testobj.conf = {'test': {'this': '', 'that': ''}, 'this': {'those': ''},
                    'Mod Directories': {'this': 'that, another', 'those': 'thoze'}}
    testobj.directories.add('that')
    assert testobj.directories == {'that'}
    testobj.add_activations('test', 'this')
    assert testobj.directories == {'that', 'another', 'thoze'}

def test_select_activations(monkeypatch, capsys):
    def mock_add(self, *args):
        print('called self.add_activations with args', args)
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    monkeypatch.setattr(testee.Activate, 'add_activations', mock_add)
    testobj = testee.Activate()
    conf = '\n'.join(('[test]', 'this', '', '[other]', 'they', 'them', '', '[third]', 'oink', '',
                      '[Mod Directories]', 'test: x', 'this: y', 'other: z', 'they: a', 'them: b',
                      'third: c', 'oink: d'))
    testobj.conf = testee.configparser.ConfigParser(allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf)
    testobj.directories = {'a', 'b'}
    testobj.modnames = ['test', 'other']
    testobj.select_activations()
    assert testobj.directories == {'z', 'x'}
    assert capsys.readouterr().out == ("called self.add_activations with args ('test', 'this')\n"
                                       "called self.add_activations with args ('other', 'they')\n"
                                       "called self.add_activations with args ('other', 'them')\n")

def test_build_and_start_gui(monkeypatch, capsys):
    class MockShowMods:
        def __init__(self, master):
            master.modnames = ['one', 'two', 'three']
        def setup_screen(self):
            print('called gui.ShowMods.setup_screen()')
        def setup_actions(self):
            print('called gui.ShowMods.setup_actions()')
        def show_screen(self):
            print('called gui.ShowMods.show_screen()')
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    monkeypatch.setattr(testee.gui, 'ShowMods', MockShowMods)
    testobj = testee.Activate()
    testobj.conf = {}
    testobj.modnames = []
    testobj.build_and_start_gui()
    assert testobj.modnames == ['one', 'two', 'three']
    assert capsys.readouterr().out == ('called gui.ShowMods.setup_screen()\n'
                                       'called gui.ShowMods.setup_actions()\n'
                                       'called gui.ShowMods.show_screen()\n')


class MockParser:
    def __init__(self, *args, **kwargs):
        print('called ConfigParser() with args', args, kwargs)
    def read(self, *args):
        print('called ConfigParser.read() with args', args)

def test_init(monkeypatch, capsys):
    monkeypatch.setattr(testee.configparser, 'ConfigParser', MockParser)
    conf = testee.Activate('config')
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
    def build_and_start_gui(self):
        print('called Activate.build_and_start_gui()')
    def select_activations(self):
        print('called Activate.select_activations()')
    def activate(self):
        print('called Activate.activate()')

def test_main(monkeypatch, capsys):
    def mock_select(self):
        self.directories = 'anything'
    monkeypatch.setattr(testee, 'Activate', MockActivate)
    monkeypatch.setattr(testee, 'CONFIG', 'filename')
    testee.main()
    assert capsys.readouterr().out == ("called Activate() with args filename\n"
                                       'called Activate.build_and_start_gui()\n')
