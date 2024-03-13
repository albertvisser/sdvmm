"""unittests for ./activate.py
"""
import pathlib
import activate as testee

def mock_init(self, *args):
    """stub for setting up activate.Activate class
    """
    self.conf = {}
    self.modnames = []
    self.modbase = 'modbase'
    self.directories = set()


class MockParser(dict):
    """testdouble object mimicking configparser.ConfigParser class
    """
    def __init__(self, *args, **kwargs):
        print('called ConfigParser() with args', args, kwargs)
    def read(self, *args):
        """stub
        """
        print('called ConfigParser.read with args', args)
    def set(*args):
        """stub
        """
        print("called ConfigParser.set with args", args)
    def add_section(*args):
        """stub
        """
        print("called ConfigParser.add_section with args", args)
        if args[1] == 'q':
            raise testee.configparser.DuplicateSectionError('q')
    def write(*args):
        """stub
        """
        print("called ConfigParser.write with args", args)


def test_init(monkeypatch, capsys):
    """unittest for activate.init
    """
    monkeypatch.setattr(testee.configparser, 'ConfigParser', MockParser)
    testobj = testee.Activate('config')
    assert capsys.readouterr().out == (
            "called ConfigParser() with args () {'delimiters': (':',), 'allow_no_value': True}\n"
            "called ConfigParser.read with args ('config',)\n")
    assert testobj.conf.optionxform == str
    assert not testobj.directories
    assert isinstance(testobj.directories, set)


def test_build_and_start_gui(monkeypatch, capsys):
    """unittest for activate.build_and_start_gui
    """
    class MockShowMods:
        """stub
        """
        def __init__(self, master):
            master.modnames = ['one', 'two', 'three']
        def setup_screen(self):
            """stub
            """
            print('called gui.ShowMods.setup_screen()')
        def setup_actions(self):
            """stub
            """
            print('called gui.ShowMods.setup_actions()')
        def show_screen(self):
            """stub
            """
            print('called gui.ShowMods.show_screen()')
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    monkeypatch.setattr(testee.gui, 'ShowMods', MockShowMods)
    testobj = testee.Activate('')
    testobj.conf = {}
    testobj.modnames = []
    testobj.build_and_start_gui()
    assert testobj.modnames == ['one', 'two', 'three']
    assert capsys.readouterr().out == ('called gui.ShowMods.setup_screen()\n'
                                       'called gui.ShowMods.setup_actions()\n'
                                       'called gui.ShowMods.show_screen()\n')


def test_select_activations(monkeypatch, capsys):
    """unittest for activate.select_activations
    """
    def mock_add(self, *args):
        """stub
        """
        print('called self.add_activations with args', args)
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    monkeypatch.setattr(testee.Activate, 'add_activations', mock_add)
    testobj = testee.Activate('')
    conf = ('[test]\nthis\n\n[other]\nthey\nthem\n\n[third]\noink\n\n'
            '[Mod Directories]\ntest: x\nthis: y\nother: z\nthey: a\nthem: b\n\nthird: c\noink: d')
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


def test_add_activations(monkeypatch):
    """unittest for activate.add_activations
    """
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    testobj = testee.Activate('')
    testobj.conf = {'test': {'this': '', 'that': ''}, 'this': {'those': ''},
                    'Mod Directories': {'this': 'that, another', 'those': 'thoze'}}
    testobj.directories.add('that')
    assert testobj.directories == {'that'}
    testobj.add_activations('test', 'this')
    assert testobj.directories == {'that', 'another', 'thoze'}


def test_activate(monkeypatch, capsys):
    """unittest for activate.activate
    """
    def mock_rename(*args):
        """stub
        """
        print('called os.rename() with args', args)
    def mock_isfile(arg):
        """stub
        """
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
    testobj = testee.Activate('')
    testobj.conf['Mod Directories'] = {'SMAPI': ['test']}
    testobj.directories |= {'yes', 'off'}
    assert testobj.directories == {'yes', 'off'}
    testobj.activate()
    assert capsys.readouterr().out == ("called os.rename() with args (PosixPath('modbase/on'),"
                                       " 'modbase/.on')\n"
                                       "called os.rename() with args (PosixPath('modbase/.off'),"
                                       " 'modbase/off')\n")


def test_edit_config(monkeypatch, capsys):
    """unittest for activate.edit_config
    """
    def mock_run(*args):
        print('called subprocess.run with args', args)
    monkeypatch.setattr(testee.subprocess, 'run', mock_run)
    monkeypatch.setattr(testee, 'CONFIG', 'mock_config')
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    testobj = testee.Activate('')
    testobj.edit_config()
    assert capsys.readouterr().out == ("called subprocess.run with args (['gnome-terminal',"
                                       " '--geometry=102x54+1072+0', '--', 'vim', 'mock_config'],)\n")


def test_check_config(monkeypatch):
    """unittest for activate.check_config
    """
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    testobj = testee.Activate('')
    conf_ok = ('[test]\nthis\nthese\n\n[this]\nthose\n\n'
               '[Mod Directories]\ntest: x\nthis: that, another\nthose: thoze\nthese: theze')
    testobj.conf = testee.configparser.ConfigParser(allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf_ok)
    assert testobj.check_config() == ['No errors']
    conf_nok = ('[test]\nthis\nthese\n\n[this]\nthose\n\n'
                '[Mod Directories]\ntest: x\nThis: that, another\nThose: thoze')
    testobj.conf = testee.configparser.ConfigParser(allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf_nok)
    assert testobj.check_config() == ['Unknown mod name `this` for expansion/mod `test`',
                                      'Unknown mod name `these` for expansion/mod `test`',
                                      'Unknown expansion / mod name: `this`',
                                      'Unknown mod name `those` for expansion/mod `this`']


def test_add_to_config(monkeypatch, capsys, tmp_path):
    """unittest for activate.add_to_config
    """
    class MockShow:
        "stub for testee.ShowMods"
        def add_checkbox(self, arg):
            print(f"called ShowMods.add_checkbox with arg '{arg}'")
        def refresh_widgets(self):
            print("called ShowMods.refresh_widgets")
    def mock_show(*args, **kwargs):
        print("called gui.show_dialog with args", args, kwargs)
        return False, {}
    def mock_show_2(*args, **kwargs):
        print("called gui.show_dialog with args", args, kwargs)
        return True, {'mods': [('x', 'y')], 'deps': {'a': 'b'}, 'set_active': ['q', 'r']}
    def mock_copyfile(*args):
        print('called shutil.copyfile with args', args)
    conffile = tmp_path / 'sdvmm' / 'config'
    conffile.parent.mkdir()
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copyfile)
    # monkeypatch.setattr(testee.gui, 'NewModDialog', MockDialog)
    monkeypatch.setattr(testee.Activate, '__init__', mock_init)
    testobj = testee.Activate('')
    testobj.conf = MockParser()
    testobj.conf['Mod Directories'] = 'mods'
    showmods = MockShow()
    testobj.doit = showmods
    testobj.config = str(conffile)
    testobj.add_to_config()
    assert capsys.readouterr().out == (
            "called ConfigParser() with args () {}\n"
            "called gui.show_dialog with args"
            f" (<class 'activate_gui.NewModDialog'>, {showmods}, 'mods') {{'first_time': True}}\n")
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
    testobj = testee.Activate('')
    testobj.conf = MockParser()
    testobj.conf['Mod Directories'] = 'mods'
    testobj.doit = showmods
    testobj.config = str(conffile)
    testobj.add_to_config()
    assert capsys.readouterr().out == (
            "called ConfigParser() with args () {}\n"
            "called gui.show_dialog with args"
            f" (<class 'activate_gui.NewModDialog'>, {showmods}, 'mods') {{'first_time': True}}\n"
            "called ConfigParser.set with args"
            " ({'Mod Directories': 'mods'}, 'Mod Directories', 'x', 'y')\n"
            "called ConfigParser.add_section with args ({'Mod Directories': 'mods'}, 'a')\n"
            "called ConfigParser.set with args ({'Mod Directories': 'mods'}, 'a', 'b', '')\n"
            "called ConfigParser.add_section with args ({'Mod Directories': 'mods'}, 'q')\n"
            "called ConfigParser.add_section with args ({'Mod Directories': 'mods'}, 'r')\n"
            "called ShowMods.add_checkbox with arg 'r'\n"
            f"called shutil.copyfile with args ('{conffile}', '{conffile}~')\n"
            "called ConfigParser.write with args ({'Mod Directories': 'mods'},"
            f" <_io.TextIOWrapper name='{conffile}' mode='w' encoding='UTF-8'>)\n"
            "called ShowMods.refresh_widgets\n")


class MockActivate:
    """testdouble object mimicking activate.Activate class
    """
    def __init__(self, args):
        print('called Activate() with args', args)
        self.directories = []
        self.modnames = []
    def build_and_start_gui(self):
        """stub
        """
        print('called Activate.build_and_start_gui()')
    def select_activations(self):
        """stub
        """
        print('called Activate.select_activations()')
    def activate(self):
        """stub
        """
        print('called Activate.activate()')


def test_main(monkeypatch, capsys):
    """unittest for activate.main
    """
    monkeypatch.setattr(testee, 'Activate', MockActivate)
    monkeypatch.setattr(testee, 'CONFIG', 'filename')
    testee.main()
    assert capsys.readouterr().out == ("called Activate() with args filename\n"
                                       'called Activate.build_and_start_gui()\n')
