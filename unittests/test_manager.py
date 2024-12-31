"""unittests for ./manager.py
"""
import pathlib
import types
from src import manager as testee

def mock_init(self, *args):
    """stub for setting up manager.Manager class
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
    def set(self, *args):
        """stub
        """
        print("called ConfigParser.set with args", args)
    def add_section(self, *args):
        """stub
        """
        print("called ConfigParser.add_section with args", args)
        if args[0] == 'q':
            raise testee.configparser.DuplicateSectionError('q')
    def remove_option(self, *args):
        """stub
        """
        print("called ConfigParser.remove_option with args", args)
    def write(self, *args):
        """stub
        """
        print("called ConfigParser.write with args", args)


def test_get_archive_roots():
    """unittest for get_archive_root
    """
    assert testee.get_archive_roots([]) == set()
    assert testee.get_archive_roots(['path/to/file', 'path/to/other/file', 'root/dir']) == {'path',
                                                                                           'root'}
    assert testee.get_archive_roots(['path/to/file', '__MACOSX/dir', '__MACOSX/xxx']) == {'path'}


def test_init(monkeypatch, capsys):
    """unittest for Manager.init
    """
    monkeypatch.setattr(testee.configparser, 'ConfigParser', MockParser)
    testobj = testee.Manager('config')
    assert capsys.readouterr().out == (
            "called ConfigParser() with args () {'delimiters': (':',), 'allow_no_value': True}\n"
            "called ConfigParser.read with args ('config',)\n")
    assert isinstance(testobj.conf, testee.configparser.ConfigParser)
    # assert isinstance(testobj.conf.optionxform, str)
    assert testobj.conf.optionxform('AbcdEf') == str('AbcdEf')
    assert testobj.modnames == []
    assert testobj.modbase == testee.MODBASE
    assert testobj.downloads == testee.DOWNLOAD
    assert testobj.directories == set()
    assert testobj.screenpos == {}


def test_build_and_start_gui(monkeypatch, capsys):
    """unittest for Manager.build_and_start_gui
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
        print('called Manager.extract_screen_locations')
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    monkeypatch.setattr(testee.gui, 'ShowMods', MockShowMods)
    testobj = testee.Manager('')
    testobj.extract_screen_locations = mock_extract
    testobj.conf = {}
    testobj.modnames = []
    testobj.build_and_start_gui()
    assert testobj.modnames == ['one', 'two', 'three']
    assert capsys.readouterr().out == ('called Manager.extract_screen_locations\n'
                                       f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
                                       'called gui.ShowMods.setup_screen()\n'
                                       'called gui.ShowMods.setup_actions()\n'
                                       'called gui.ShowMods.show_screen()\n')


def test_extract_screen_locations(monkeypatch):
    """unittest for Manager.extract_screen_locations
    """
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
    testobj.screenpos = {}
    testobj.screentext = {}
    conf = (f'[test]\nthis\n{testee.SCRPOS}: x,y\n{testee.NXSKEY}: 123\n{testee.SCRTXT}: xxxx\n\n'
            f'[other]\nthey\nthem\n\n[Mod Directories]\ntest: x\nthis: y')
    testobj.conf = testee.configparser.ConfigParser(allow_no_value=True)
    testobj.conf.optionxform = str
    testobj.conf.read_string(conf)
    assert testobj.conf.sections() == ['test', 'other', 'Mod Directories']
    assert testobj.conf.options('test') == ['this', f'{testee.SCRPOS}', f'{testee.NXSKEY}',
                                            f'{testee.SCRTXT}']
    assert testobj.conf.options('other') == ['they', 'them']
    testobj.extract_screen_locations()
    assert testobj.conf.sections() == ['test', 'other', 'Mod Directories']
    assert testobj.conf.options('test') == ['this', '_ScreenPos', '_Nexus', '_ScreenText']
    assert testobj.conf.options('other') == ['they', 'them']
    assert testobj.screenpos == {'test': ['x,y', '123'], 'other': ['', '']}
    assert testobj.screentext == {'test': 'xxxx'}


def test_select_activations(monkeypatch, capsys):
    """unittest for Manager.select_activations
    """
    def mock_add(self, *args):
        """stub
        """
        print('called self.add_activations with args', args)
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    monkeypatch.setattr(testee.Manager, 'add_activations', mock_add)
    testobj = testee.Manager('')
    conf = ('[test]\nthis\n\n[other]\nthey\nthem\n'
            f'{testee.SCRPOS}: x,y\n{testee.NXSKEY}: 5\n\n[third]\noink\n\n'
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
    """unittest for Manager.add_activations
    """
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
    testobj.conf = {'test': {'this': '', 'that': ''},
                    'this': {'those': '', testee.SCRPOS: 'x,y', testee.NXSKEY: '5'},
                    'Mod Directories': {'this': 'that, another', 'those': 'thoze'}}
    testobj.directories.add('that')
    assert testobj.directories == {'that'}
    testobj.add_activations('test', 'this')
    assert testobj.directories == {'that', 'another', 'thoze'}


def test_activate(monkeypatch, capsys):
    """unittest for Manager.activate
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
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
    testobj.conf['Mod Directories'] = {'SMAPI': ['test']}
    testobj.directories |= {'yes', 'off'}
    assert testobj.directories == {'yes', 'off'}
    testobj.activate()
    assert capsys.readouterr().out == ("called os.rename() with args (PosixPath('modbase/on'),"
                                       " 'modbase/.on')\n"
                                       "called os.rename() with args (PosixPath('modbase/.off'),"
                                       " 'modbase/off')\n")


def test_edit_config(monkeypatch, capsys):
    """unittest for Manager.edit_config
    """
    def mock_run(*args):
        print('called subprocess.run with args', args)
    monkeypatch.setattr(testee.subprocess, 'run', mock_run)
    monkeypatch.setattr(testee, 'CONFIG', 'mock_config')
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
    testobj.edit_config()
    assert capsys.readouterr().out == ("called subprocess.run with args (['gnome-terminal',"
                                       " '--geometry=102x54+1072+0', '--', 'vim', 'mock_config'],)\n")


def test_reload_config(monkeypatch, capsys):
    """unittest for Manager.reload_config
    """
    def mock_read(config):
        print(f"called config.read with arg {config}")
    def mock_refresh():
        print("called AcivateGui.refresh_widgets")
    def mock_extract():
        print("called Manager.extract_screen_locations")
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
    testobj.config = {'config': 'parameters'}
    testobj.conf = types.SimpleNamespace(read=mock_read)
    testobj.doit = types.SimpleNamespace(refresh_widgets=mock_refresh)
    testobj.extract_screen_locations = mock_extract
    testobj.reload_config()
    assert capsys.readouterr().out == ("called config.read with arg {'config': 'parameters'}\n"
                                       "called Manager.extract_screen_locations\n"
                                       "called AcivateGui.refresh_widgets\n")


def test_check_config(monkeypatch):
    """unittest for Manager.check_config
    """
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
    conf_ok = ('[test]\nthis\nthese\n\n[this]\nthose\n_xxx: yyy\n\n'
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
    """unittest for Manager.add_to_config
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
        args[1].dialog_data = {'mods': [('x', 'y')], 'deps': {'a': 'b', 'c': ''},
                               'set_active': ['q', 'r']}
        return True
    def mock_copyfile(*args):
        print('called shutil.copyfile with args', args)
    conffile = tmp_path / 'sdvmm' / 'config'
    conffile.parent.mkdir()
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copyfile)
    # monkeypatch.setattr(testee.gui, 'NewModDialog', MockDialog)
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
    testobj.conf = MockParser()
    assert capsys.readouterr().out == "called ConfigParser() with args () {}\n"
    testobj.conf['Mod Directories'] = 'mods'
    showmods = MockShow()
    testobj.doit = showmods
    testobj.config = str(conffile)
    testobj.add_to_config()
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args (<class 'src.gui.NewModDialog'>,"
            f" {showmods}, 'mods') {{'first_time': True}}\n")
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
    testobj = testee.Manager('')
    testobj.conf = MockParser()
    assert capsys.readouterr().out == "called ConfigParser() with args () {}\n"
    testobj.conf['Mod Directories'] = 'mods'
    testobj.doit = showmods
    testobj.config = str(conffile)
    testobj.add_to_config()
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" (<class 'src.gui.NewModDialog'>, {showmods}, 'mods') {{'first_time': True}}\n"
            "called ConfigParser.set with args ('Mod Directories', 'x', 'y')\n"
            "called ConfigParser.add_section with args ('a',)\n"
            "called ConfigParser.set with args ('a', 'b', '')\n"
            "called ConfigParser.add_section with args ('q',)\n"
            "called ConfigParser.add_section with args ('r',)\n"
            "called ShowMods.add_entries_for_name with arg 'r'\n"
            f"called shutil.copyfile with args ('{conffile}', '{conffile}~')\n"
            f"called ConfigParser.write with args (<_io.TextIOWrapper name='{conffile}'"
            " mode='w' encoding='UTF-8'>,)\n"
            "called ShowMods.refresh_widgets\n")


def test_add_remark(monkeypatch, capsys, tmp_path):
    """unittest for Manager.add_remark
    """
    class MockShow:
        "stub for testee.ShowMods"
        def __init__(self, master):
            self.master = master
        def refresh_widgets(self):
            print("called ShowMods.refresh_widgets")
    def mock_show(*args):
        print("called gui.show_dialog with args", args)
        args[1].master.screentext = {}
    def mock_show_2(*args):
        print("called gui.show_dialog with args", args)
        args[1].master.screentext = {'xxx': 'aaaaaaa', 'zzz': 'zzzzzzz', 'qqq': 'qqqqqqq'}
    def mock_copyfile(*args):
        print('called shutil.copyfile with args', args)
    conffile = tmp_path / 'sdvmm' / 'config'
    conffile.parent.mkdir()
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copyfile)
    # monkeypatch.setattr(testee.gui, 'NewModDialog', MockDialog)
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
    testobj.conf = MockParser()
    assert capsys.readouterr().out == "called ConfigParser() with args () {}\n"
    testobj.conf['Mod Directories'] = 'mods'
    showmods = MockShow(testobj)
    testobj.doit = showmods
    testobj.config = str(conffile)

    testobj.screentext = {}
    testobj.add_remark()
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" (<class 'src.gui.RemarksDialog'>, {testobj.doit}, 'mods')\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
    testobj.screentext = {'xxx': 'xxxxxxx', 'yyy': 'yyyyyyy', 'qqq': 'qqqqqqq'}
    testobj.add_remark()
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" (<class 'src.gui.RemarksDialog'>, {testobj.doit}, 'mods')\n"
            "called ConfigParser.set with args ('xxx', '_ScreenText', 'aaaaaaa')\n"
            "called ConfigParser.set with args ('zzz', '_ScreenText', 'zzzzzzz')\n"
            "called ConfigParser.remove_option with args ('yyy', '_ScreenText')\n"
            f"called shutil.copyfile with args ('{conffile}', '{conffile}~')\n"
            f"called ConfigParser.write with args (<_io.TextIOWrapper name='{conffile}'"
            " mode='w' encoding='UTF-8'>,)\n"
            "called ShowMods.refresh_widgets\n")


def test_update_config_from_screenpos(monkeypatch, tmp_path):
    """unittest for Manager.update_config_from_screenpos
    """
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
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
    """unittest for Manager.update_mods
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
            nonlocal extractall_counter
            print('called ZipFile.extractall with args', args)
            extractall_counter += 1
            (tmp_path / 'mods' / self._name).touch()
            if extractall_counter == 1:
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
    def mock_get_2(arg):
        print(f'called get_archive_root with arg {arg}')
        return {''}
    def mock_get_3(arg):
        print(f'called get_archive_root with arg {arg}')
        return {'SMAPI-root-1'}
    def mock_run(*args, **kwargs):
        print('called subprocess.run with args', args, kwargs)
    monkeypatch.setattr(testee.subprocess, 'run', mock_run)
    monkeypatch.setattr(testee.zipfile, 'ZipFile', MockZipFile)
    (tmp_path / 'mods').mkdir()
    (tmp_path / 'dl').mkdir()
    (tmp_path / 'dl' / 'installed').mkdir()
    (tmp_path / 'dl' / 'root-1').touch()
    (tmp_path / 'mods' / 'root-1').touch()
    (tmp_path / 'dl' / 'two').touch()
    (tmp_path / 'mods' / 'two').touch()
    (tmp_path / 'dl' / 'roots').touch()
    (tmp_path / 'mods' / 'roots').touch()
    (tmp_path / 'dl' / 'root-2').touch()
    (tmp_path / 'dl' / 'root-3').touch()
    (tmp_path / 'mods' / '.root-3').touch()
    (tmp_path / 'dl' / 'root-4').touch()
    (tmp_path / 'dl' / 'root-5').touch()
    (tmp_path / 'dl' / 'root-6').touch()
    (tmp_path / 'mods' / 'root-6').touch()
    (tmp_path / 'mods' / '.root-6~').mkdir()
    (tmp_path / 'dl' / 'root-7').touch()
    (tmp_path / 'mods' / '.root-7').touch()
    (tmp_path / 'mods' / '.root-7~').mkdir()
    monkeypatch.setattr(testee, 'get_archive_roots', mock_get)
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
    testobj.modbase = str(tmp_path / 'mods')
    assert testobj.update_mods([]) == []
    assert capsys.readouterr().out == ''
    filelist = [tmp_path / 'dl' / 'root-1', tmp_path / 'dl' / 'root-2', tmp_path / 'dl' / 'root-3',
                tmp_path / 'dl' / 'root-4', tmp_path / 'dl' / 'root-5', tmp_path / 'dl' / 'root-6',
                tmp_path / 'dl' / 'root-7']
    extractall_counter = 0
    assert testobj.update_mods(filelist) == [
            f"{tmp_path}/dl/root-1 is successfully installed",
            f"{tmp_path}/dl/root-2 is successfully installed",
            f"{tmp_path}/dl/root-3 is successfully installed",
            f"{tmp_path}/dl/root-4: zipfile appears to be empty",
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
            f"called ZipFile.extractall with args ({testobj.modbase!r},)\n"
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

    monkeypatch.setattr(testee, 'get_archive_roots', mock_get_2)
    (tmp_path / 'dl' / 'root-1').touch()
    filelist = [tmp_path / 'dl' / 'root-1']
    assert testobj.update_mods(filelist) == [
            f"{tmp_path}/dl/root-1 is successfully installed"]
    assert capsys.readouterr().out == (
            f"called ZipFile.__init__ with args ({filelist[0]!r},)\n"
            "called ZipFile.namelist\n"
            "called get_archive_root with arg ['name', 'list']\n"
            f"called ZipFile.extractall with args ({testobj.modbase!r},)\n"
            "called ZipFile.close\n")

    monkeypatch.setattr(testee, 'get_archive_roots', mock_get_3)
    fpath = tmp_path / 'dl' / 'SMAPI-root-1'
    fpath.touch()
    filelist = [fpath]
    assert testobj.update_mods(filelist) == [
            "SMAPI-install is waiting in a terminal window to be finished"
            " by executing './install on Linux.sh'"]
    assert capsys.readouterr().out == (
            f"called ZipFile.__init__ with args ({filelist[0]!r},)\n"
            "called ZipFile.namelist\n"
            "called get_archive_root with arg ['name', 'list']\n"
            "called ZipFile.close\n"
            f"called subprocess.run with args (['unzip', {fpath!r}, '-d', '/tmp'],)"
            " {'check': True}\n"
            f"called subprocess.run with args (['gnome-terminal'],)"
            " {'cwd': '/tmp/SMAPI-root-1'}\n")


def test_determine_unpack_directory(monkeypatch, capsys):
    """unittest for Manager.determine_unpack_directory
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
        print(f'called Manager.get_archive_roots with arg {namelist}')
        return []
    def mock_get_1(namelist):
        print(f'called Manager.get_archive_roots with arg {namelist}')
        return ['name']
    def mock_get_2(namelist):
        print(f'called Manager.get_archive_roots with arg {namelist}')
        return ['name', 'list']
    monkeypatch.setattr(testee.zipfile, 'ZipFile', MockZipFile)
    monkeypatch.setattr(testee.Manager, '__init__', mock_init)
    testobj = testee.Manager('')
    monkeypatch.setattr(testee, 'get_archive_roots', mock_get)
    assert testobj.determine_unpack_directory('testfile.zip') == ''
    assert capsys.readouterr().out == (
            "called zipfile.ZipFile with args ('testfile.zip',) {}\n"
            "called ZipFile.__enter__\n"
            "called ZipFile.namelist\n"
            "called Manager.get_archive_roots with arg []\n"
            "called ZipFile.__exit__\n")

    monkeypatch.setattr(testee, 'get_archive_roots', mock_get_1)
    assert testobj.determine_unpack_directory('testfile.zip') == 'name'
    assert capsys.readouterr().out == (
            "called zipfile.ZipFile with args ('testfile.zip',) {}\n"
            "called ZipFile.__enter__\n"
            "called ZipFile.namelist\n"
            "called Manager.get_archive_roots with arg []\n"
            "called ZipFile.__exit__\n")

    monkeypatch.setattr(testee, 'get_archive_roots', mock_get_2)
    assert testobj.determine_unpack_directory('testfile.zip') == 'name, list'
    assert capsys.readouterr().out == (
            "called zipfile.ZipFile with args ('testfile.zip',) {}\n"
            "called ZipFile.__enter__\n"
            "called ZipFile.namelist\n"
            "called Manager.get_archive_roots with arg []\n"
            "called ZipFile.__exit__\n")


class MockManager:
    """testdouble object mimicking Manager class
    """
    def __init__(self, args):
        print('called Manager() with args', args)
        self.directories = []
        self.modnames = []
    def build_and_start_gui(self):
        """stub
        """
        print('called Manager.build_and_start_gui()')
    def select_activations(self):
        """stub
        """
        print('called Manager.select_activations()')
    def activate(self):
        """stub
        """
        print('called Manager.activate()')


def test_main(monkeypatch, capsys):
    """unittest for manager.main
    """
    monkeypatch.setattr(testee, 'Manager', MockManager)
    monkeypatch.setattr(testee, 'CONFIG', 'filename')
    testee.main()
    assert capsys.readouterr().out == ("called Manager() with args filename\n"
                                       'called Manager.build_and_start_gui()\n')
