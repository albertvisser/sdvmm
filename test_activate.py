"""unittests for ./activate.py
"""
import pathlib
import activate as testee

def mock_init(self, *args):
    """stub for setting up activate.Activater class
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


def test_get_archive_root():
    """unittest for get_archive_root
    """
    assert testee.get_archive_root([]) == set()
    assert testee.get_archive_root(['path/to/file', 'path/to/other/file', 'root/dir']) == {'path',
                                                                                           'root'}
    assert testee.get_archive_root(['path/to/file', '__MACOSX/dir', '__MACOSX/xxx']) == {'path'}


def test_init(monkeypatch, capsys):
    """unittest for Activater.init
    """
    monkeypatch.setattr(testee.configparser, 'ConfigParser', MockParser)
    testobj = testee.Activater('config')
    assert capsys.readouterr().out == (
            "called ConfigParser() with args () {'delimiters': (':',), 'allow_no_value': True}\n"
            "called ConfigParser.read with args ('config',)\n")
    assert isinstance(testobj.conf, testee.configparser.ConfigParser)
    assert testobj.conf.optionxform == str
    assert testobj.modnames == []
    assert testobj.modbase == testee.MODBASE
    assert testobj.downloads == testee.DOWNLOAD
    assert testobj.directories == set()
    assert testobj.screenpos == {}


def test_build_and_start_gui(monkeypatch, capsys):
    """unittest for Activater.build_and_start_gui
    """
    class MockShowMods:
        """stub
        """
        def __init__(self, master):
            print(f"called gui.ShowMods.__init__() with arg '{master}'")
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
    def mock_extract():
        print('called Activater.extract_screen_locations')
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    monkeypatch.setattr(testee.gui, 'ShowMods', MockShowMods)
    testobj = testee.Activater('')
    testobj.extract_screen_locations = mock_extract
    testobj.conf = {}
    testobj.modnames = []
    testobj.build_and_start_gui()
    assert testobj.modnames == ['one', 'two', 'three']
    assert capsys.readouterr().out == ('called Activater.extract_screen_locations\n'
                                       f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
                                       'called gui.ShowMods.setup_screen()\n'
                                       'called gui.ShowMods.setup_actions()\n'
                                       'called gui.ShowMods.show_screen()\n')


def test_extract_screen_locations(monkeypatch):
    """unittest for Activater.extract_screen_locations
    """
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    testobj = testee.Activater('')
    testobj.screenpos = {}
    conf = (f'[test]\nthis\n{testee.SCRPOS}: x,y\n\n[other]\nthey\nthem\n\n'
            '[Mod Directories]\ntest: x\nthis: y')
    testobj.conf = testee.configparser.ConfigParser(allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf)
    assert testobj.conf.sections() == ['test', 'other', 'Mod Directories']
    assert testobj.conf.options('test') == ['this', f'{testee.SCRPOS}']
    assert testobj.conf.options('other') == ['they', 'them']
    testobj.extract_screen_locations()
    assert testobj.conf.sections() == ['test', 'other', 'Mod Directories']
    assert testobj.conf.options('test') == ['this', '_ScreenPos']
    assert testobj.conf.options('other') == ['they', 'them']
    assert testobj.screenpos == {'test': 'x,y', 'other': ''}


def test_select_activations(monkeypatch, capsys):
    """unittest for Activater.select_activations
    """
    def mock_add(self, *args):
        """stub
        """
        print('called self.add_activations with args', args)
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    monkeypatch.setattr(testee.Activater, 'add_activations', mock_add)
    testobj = testee.Activater('')
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
    """unittest for Activater.add_activations
    """
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    testobj = testee.Activater('')
    testobj.conf = {'test': {'this': '', 'that': ''}, 'this': {'those': ''},
                    'Mod Directories': {'this': 'that, another', 'those': 'thoze'}}
    testobj.directories.add('that')
    assert testobj.directories == {'that'}
    testobj.add_activations('test', 'this')
    assert testobj.directories == {'that', 'another', 'thoze'}


def test_activate(monkeypatch, capsys):
    """unittest for Activater.activate
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
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    testobj = testee.Activater('')
    testobj.conf['Mod Directories'] = {'SMAPI': ['test']}
    testobj.directories |= {'yes', 'off'}
    assert testobj.directories == {'yes', 'off'}
    testobj.activate()
    assert capsys.readouterr().out == ("called os.rename() with args (PosixPath('modbase/on'),"
                                       " 'modbase/.on')\n"
                                       "called os.rename() with args (PosixPath('modbase/.off'),"
                                       " 'modbase/off')\n")


def test_edit_config(monkeypatch, capsys):
    """unittest for Activater.edit_config
    """
    def mock_run(*args):
        print('called subprocess.run with args', args)
    monkeypatch.setattr(testee.subprocess, 'run', mock_run)
    monkeypatch.setattr(testee, 'CONFIG', 'mock_config')
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    testobj = testee.Activater('')
    testobj.edit_config()
    assert capsys.readouterr().out == ("called subprocess.run with args (['gnome-terminal',"
                                       " '--geometry=102x54+1072+0', '--', 'vim', 'mock_config'],)\n")


def test_check_config(monkeypatch):
    """unittest for Activater.check_config
    """
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    testobj = testee.Activater('')
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
    """unittest for Activater.add_to_config
    """
    class MockShow:
        "stub for testee.ShowMods"
        def add_entries_for_name(self, arg):
            print(f"called ShowMods.add_entries_for_name with arg '{arg}'")
        def refresh_widgets(self):
            print("called ShowMods.refresh_widgets")
    def mock_show(*args, **kwargs):
        print("called gui.show_dialog with args", args, kwargs)
        return False
    def mock_show_2(*args, **kwargs):
        print("called gui.show_dialog with args", args, kwargs)
        args[1].dialog_data = {'mods': [('x', 'y')], 'deps': {'a': 'b'}, 'set_active': ['q', 'r']}
        return True
    def mock_copyfile(*args):
        print('called shutil.copyfile with args', args)
    conffile = tmp_path / 'sdvmm' / 'config'
    conffile.parent.mkdir()
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copyfile)
    # monkeypatch.setattr(testee.gui, 'NewModDialog', MockDialog)
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    testobj = testee.Activater('')
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
    testobj = testee.Activater('')
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
            "called ShowMods.add_entries_for_name with arg 'r'\n"
            f"called shutil.copyfile with args ('{conffile}', '{conffile}~')\n"
            "called ConfigParser.write with args ({'Mod Directories': 'mods'},"
            f" <_io.TextIOWrapper name='{conffile}' mode='w' encoding='UTF-8'>)\n"
            "called ShowMods.refresh_widgets\n")


def test_update_config_from_screenpos(monkeypatch, tmp_path):
    """unittest for Activater.update_config_from_screenpos
    """
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    testobj = testee.Activater('')
    testobj.screenpos = {}
    configfile = tmp_path / 'testconf'
    backupfile = tmp_path / 'testconf~'
    configfile.touch()
    testobj.config = str(configfile)
    conf = ('[test]\nthis\n\n[other]\nthey\nthem\n\n'
            '[Mod Directories]\ntest: x\nthis: y')
    testobj.conf = testee.configparser.ConfigParser(delimiters=(':',), allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf)
    oldconf = testobj.conf
    testobj.screenpos['test'] = 'x,y'
    testobj.screenpos['other'] = ''
    testobj.update_config_from_screenpos()
    assert testobj.conf == oldconf
    assert configfile.read_text() == ("[test]\nthis\n_ScreenPos : x,y\n\n[other]\nthey\nthem\n\n"
                                      "[Mod Directories]\ntest : x\nthis : y\n\n")
    assert backupfile.read_text() == ""


def test_update_mods(monkeypatch, capsys, tmp_path):
    """unittest for Activater.update_mods
    """
    class MockZipFile:
        """stub for zipfile.Zipfile
        """
        def __init__(self, *args):
            print('called ZipFile.__init__ with args', args)
            self._name = args[0].name
        def namelist(self):
            print('called ZipFile.namelist')
            return ['name', 'list']
        def extractall(self, *args):
            print('called ZipFile.extractall with args', args)
            (tmp_path / 'mods' / self._name).touch()
            if not (tmp_path / 'mods' / '__MACOSX').exists():
                (tmp_path / 'mods' / '__MACOSX').mkdir()
        def extract(self, *args):
            print('called ZipFile.extract with args', args)
            (tmp_path / 'mods' / self._name).touch()
        def close(self):
            print('called ZipFile.close')
    counter = 0
    def mock_get(arg):
        nonlocal counter
        print(f'called get_archive_root with arg {arg}')
        counter += 1
        if counter == 2:
            return {'two', 'roots'}
        if counter == 4:
            return set()
        return {f'root-{counter}'}
    monkeypatch.setattr(testee.zipfile, 'ZipFile', MockZipFile)
    (tmp_path / 'mods').mkdir()
    (tmp_path / 'dl').mkdir()
    (tmp_path / 'dl' / 'installed').mkdir()
    (tmp_path / 'dl' / 'root-1').touch()
    (tmp_path / 'mods' / 'root-1').touch()
    (tmp_path / 'dl' / 'root-3').touch()
    (tmp_path / 'mods' / '.root-3').touch()
    (tmp_path / 'dl' / 'root-5').touch()
    (tmp_path / 'dl' / 'root-6').touch()
    (tmp_path / 'mods' / 'root-6').touch()
    (tmp_path / 'mods' / '.root-6~').mkdir()
    (tmp_path / 'dl' / 'root-7').touch()
    (tmp_path / 'mods' / '.root-7').touch()
    (tmp_path / 'mods' / '.root-7~').mkdir()
    monkeypatch.setattr(testee, 'get_archive_root', mock_get)
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    testobj = testee.Activater('')
    testobj.modbase = str(tmp_path / 'mods')
    assert testobj.update_mods([]) == []
    assert capsys.readouterr().out == ''
    filelist = [tmp_path / 'dl' / 'root-1', tmp_path / 'dl' / 'root-2', tmp_path / 'dl' / 'root-3',
                tmp_path / 'dl' / 'root-4', tmp_path / 'dl' / 'root-5', tmp_path / 'dl' / 'root-6',
                tmp_path / 'dl' / 'root-7']
    assert testobj.update_mods(filelist) == [
            f"{tmp_path}/dl/root-1 is successfully installed",
            f"{tmp_path}/dl/root-2: zipfile should contain only one base directory",
            f"{tmp_path}/dl/root-3 is successfully installed",
            f"{tmp_path}/dl/root-4: zipfile should contain only one base directory",
            f"{tmp_path}/dl/root-5 is successfully installed",
            f"{tmp_path}/dl/root-6 is successfully installed",
            f"{tmp_path}/dl/root-7 is successfully installed"]
    # het is nog mooier als ik ook laat zien wat er nu in de diverse directories zit
    assert capsys.readouterr().out == (
            f"called ZipFile.__init__ with args ({filelist[0]!r},)\n"
            "called ZipFile.namelist\n"
            "called get_archive_root with arg ['name', 'list']\n"
            f"called ZipFile.extractall with args ({testobj.modbase!r},)\n"
            "called ZipFile.close\n"
            f"called ZipFile.__init__ with args ({filelist[1]!r},)\n"
            "called ZipFile.namelist\n"
            "called get_archive_root with arg ['name', 'list']\n"
            "called ZipFile.close\n"
            f"called ZipFile.__init__ with args ({filelist[2]!r},)\n"
            "called ZipFile.namelist\n"
            "called get_archive_root with arg ['name', 'list']\n"
            f"called ZipFile.extractall with args ({testobj.modbase!r},)\n"
            "called ZipFile.close\n"
            f"called ZipFile.__init__ with args ({filelist[3]!r},)\n"
            "called ZipFile.namelist\n"
            "called get_archive_root with arg ['name', 'list']\n"
            "called ZipFile.close\n"
            f"called ZipFile.__init__ with args ({filelist[4]!r},)\n"
            "called ZipFile.namelist\n"
            "called get_archive_root with arg ['name', 'list']\n"
            f"called ZipFile.extractall with args ({testobj.modbase!r},)\n"
            "called ZipFile.close\n"
            f"called ZipFile.__init__ with args ({filelist[5]!r},)\n"
            "called ZipFile.namelist\n"
            "called get_archive_root with arg ['name', 'list']\n"
            f"called ZipFile.extractall with args ({testobj.modbase!r},)\n"
            "called ZipFile.close\n"
            f"called ZipFile.__init__ with args ({filelist[6]!r},)\n"
            "called ZipFile.namelist\n"
            "called get_archive_root with arg ['name', 'list']\n"
            f"called ZipFile.extractall with args ({testobj.modbase!r},)\n"
            "called ZipFile.close\n")


def test_determine_unpack_directory(monkeypatch, capsys):
    """unittest for Activater.determine_unpack_directory
    """
    class MockZipFile:
        """testdouble object mimicking zipfile.ZipFile class
        """
        def __init__(self, *args, **kwargs):
            print('called zipfile.ZipFile with args', args, kwargs)
        def __enter__(self):
            """stub
            """
            print('called ZipFile.__enter__')
            return self
        def __exit__(self, *args):
            """stub
            """
            print('called ZipFile.__exit__')
            return True
        def namelist(self):
            """stub
            """
            print('called ZipFile.namelist')
            return []
    def mock_get(namelist):
        print(f'called Activater.get_archive_root with arg {namelist}')
        return []
    def mock_get_1(namelist):
        print(f'called Activater.get_archive_root with arg {namelist}')
        return ['name']
    def mock_get_2(namelist):
        print(f'called Activater.get_archive_root with arg {namelist}')
        return ['name', 'list']
    monkeypatch.setattr(testee.zipfile, 'ZipFile', MockZipFile)
    monkeypatch.setattr(testee.Activater, '__init__', mock_init)
    testobj = testee.Activater('')
    monkeypatch.setattr(testee, 'get_archive_root', mock_get)
    assert testobj.determine_unpack_directory('testfile.zip') == ''
    assert capsys.readouterr().out == (
            "called zipfile.ZipFile with args ('testfile.zip',) {}\n"
            "called ZipFile.__enter__\n"
            "called ZipFile.namelist\n"
            "called Activater.get_archive_root with arg []\n"
            "called ZipFile.__exit__\n")

    monkeypatch.setattr(testee, 'get_archive_root', mock_get_1)
    assert testobj.determine_unpack_directory('testfile.zip') == 'name'
    assert capsys.readouterr().out == (
            "called zipfile.ZipFile with args ('testfile.zip',) {}\n"
            "called ZipFile.__enter__\n"
            "called ZipFile.namelist\n"
            "called Activater.get_archive_root with arg []\n"
            "called ZipFile.__exit__\n")

    monkeypatch.setattr(testee, 'get_archive_root', mock_get_2)
    assert testobj.determine_unpack_directory('testfile.zip') == ''
    assert capsys.readouterr().out == (
            "called zipfile.ZipFile with args ('testfile.zip',) {}\n"
            "called ZipFile.__enter__\n"
            "called ZipFile.namelist\n"
            "called Activater.get_archive_root with arg []\n"
            "called ZipFile.__exit__\n")


class MockActivater:
    """testdouble object mimicking Activater class
    """
    def __init__(self, args):
        print('called Activater() with args', args)
        self.directories = []
        self.modnames = []
    def build_and_start_gui(self):
        """stub
        """
        print('called Activater.build_and_start_gui()')
    def select_activations(self):
        """stub
        """
        print('called Activater.select_activations()')
    def activate(self):
        """stub
        """
        print('called Activater.activate()')


def test_main(monkeypatch, capsys):
    """unittest for activate.main
    """
    monkeypatch.setattr(testee, 'Activater', MockActivater)
    monkeypatch.setattr(testee, 'CONFIG', 'filename')
    testee.main()
    assert capsys.readouterr().out == ("called Activater() with args filename\n"
                                       'called Activater.build_and_start_gui()\n')
