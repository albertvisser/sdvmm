"""unittests for ./src/manager.py
"""
import pytest
from src import manager as testee


class MockManager:
    """testdouble object mimicking Manager class
    """
    def __init__(self):
        print('called Manager.__init__')
        self.directories = []
        self.modnames = []

    def build_and_start_gui(self):
        """stub
        """
        print('called Manager.build_and_start_gui()')


class MockConf:
    """testdouble object mimicking configparser.ConfigParser class
    """
    SCRNAM, SEL, SCRPOS, NXSKEY, SCRTXT, DIR, DEPS, COMPS, NAME, VER = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    def __init__(self, *args, **kwargs):
        print('called JsonConf.__init__ with args', args, kwargs)
    def load(self):
        """stub
        """
        print('called JsonConf.load')
    def save(self):
        """stub
        """
        print("called JsonConf.save")


class MockShowMods:
    """stub voor gui.ShowMods object
    """
    def __init__(self, master):
        print(f"called gui.ShowMods.__init__() with arg '{master}'")
        self.master = master
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
    def refresh_widgets(self, **kwargs):
        """stub
        """
        print('called gui.ShowMods.refresh_widgets with args', kwargs)


def test_main(monkeypatch, capsys, tmp_path):
    """unittest for manager.main
    """
    def mock_build():
        print('called build_jsonconf')
        return []
    def mock_build_2():
        print('called build_jsonconf')
        return ['xxx', 'yyy']
    def mock_run(*args):
        print('called subprocess.run with args', args)
    monkeypatch.setattr(testee, 'CONFIG', tmp_path / 'testconf')
    monkeypatch.setattr(testee, 'Manager', MockManager)
    monkeypatch.setattr(testee, 'build_jsonconf', mock_build)
    monkeypatch.setattr(testee.subprocess, 'run', mock_run)
    testee.main()
    assert capsys.readouterr().out == ("called build_jsonconf\n"
                                       "called Manager.__init__\n"
                                       "called Manager.build_and_start_gui()\n")
    monkeypatch.setattr(testee, 'build_jsonconf', mock_build_2)
    testee.main()
    assert capsys.readouterr().out == (
            "called build_jsonconf\n"
            "called subprocess.run with args (['zenity', '--info',"
            " '--text=\"Config was (re)built with the following messages:\\n\\nxxx\\nyyy\"'],)\n"
            "called Manager.__init__\n"
            "called Manager.build_and_start_gui()\n")
    testee.CONFIG.touch()
    testee.main()
    assert capsys.readouterr().out == ("called Manager.__init__\n"
                                       "called Manager.build_and_start_gui()\n")


class TestManager:
    """unittest for manager.Manager
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for manager.Manager object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Manager.__init__ with args', args)
        monkeypatch.setattr(testee.Manager, '__init__', mock_init)
        testobj = testee.Manager()
        testobj.conf = MockConf()
        assert capsys.readouterr().out == ('called Manager.__init__ with args ()\n'
                                           'called JsonConf.__init__ with args () {}\n')
        testobj.modnames = []
        testobj.modbase = 'modbase'
        testobj.directories = set()
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Manager.__init__
        """
        monkeypatch.setattr(testee, 'CONFIG', 'configname`')
        monkeypatch.setattr(testee.dmlj, 'JsonConf', MockConf)
        testobj = testee.Manager()
        assert capsys.readouterr().out == ("called JsonConf.__init__ with args ('configname`',) {}\n"
                                           "called JsonConf.load\n")
        assert testobj.modnames == []
        assert testobj.modbase == testee.MODBASE
        assert testobj.downloads == testee.DOWNLOAD
        assert testobj.directories == set()
        assert testobj.screeninfo == {}

    def test_build_and_start_gui(self, monkeypatch, capsys):
        """unittest for Manager.build_and_start_gui
        """
        def mock_extract():
            print('called Manager.extract_screen_locations')
        monkeypatch.setattr(testee.gui, 'ShowMods', MockShowMods)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.extract_screeninfo = mock_extract
        testobj.modnames = []
        testobj.build_and_start_gui()
        assert testobj.modnames == ['one', 'two', 'three']
        assert capsys.readouterr().out == ('called Manager.extract_screen_locations\n'
                                           f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
                                           'called gui.ShowMods.setup_screen()\n'
                                           'called gui.ShowMods.setup_actions()\n'
                                           'called gui.ShowMods.show_screen()\n')

    def test_extract_screeninfo(self, monkeypatch, capsys):
        """unittest for Manager.extract_screen_locations
        """
        def mock_list():
            print('called Conf.list_all_mod_dirs')
            return ['xxx', 'yyy']
        def mock_list_2():
            print('called Conf.list_all_mod_dirs')
            return ['xxx']
        def mock_get(name, itemtype):
            print(f"called Conf.get_diritem_data with args ('{name}', '{itemtype}')")
            return ''
        def mock_get_2(name, itemtype):
            print(f"called Conf.get_diritem_data with args ('{name}', '{itemtype}')")
            if itemtype == testobj.conf.SCRNAM:
                return f"scr{name}"
            if itemtype == testobj.conf.SCRPOS:
                return 'scrpos'
            if itemtype == testobj.conf.NXSKEY:
                return 'scrkey'
            if itemtype == testobj.conf.SCRTXT:
                return 'scrtxt'
            return 'sel'

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf.list_all_mod_dirs = mock_list
        testobj.conf.get_diritem_data = mock_get
        testobj.screeninfo = {'yyy': {'sel': 's', 'pos': 'p', 'key': 'k', 'txt': 't'}}

        testobj.extract_screeninfo()
        assert testobj.screeninfo == {
                'yyy': {'dir': 'yyy', 'sel': 's', 'pos': 'p', 'key': 'k', 'txt': 't'},
                'xxx': {'dir': 'xxx', 'sel': False, 'pos': '', 'key': '', 'txt': ''}}
        assert capsys.readouterr().out == (
                "called Conf.list_all_mod_dirs\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRNAM}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SEL}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRPOS}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.NXSKEY}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRTXT}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRNAM}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SEL}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRPOS}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.NXSKEY}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRTXT}')\n")

        testobj.conf.list_all_mod_dirs = mock_list_2
        testobj.conf.get_diritem_data = mock_get_2
        testobj.screeninfo = {}
        testobj.extract_screeninfo()
        assert testobj.screeninfo == {'scrxxx': {'dir': 'xxx', 'sel': 'sel', 'pos': 'scrpos',
                                                 'key': 'scrkey', 'txt': 'scrtxt'}}
        assert capsys.readouterr().out == ("called Conf.list_all_mod_dirs\n"
                                           "called Conf.get_diritem_data with args ('xxx', '0')\n"
                                           "called Conf.get_diritem_data with args ('xxx', '1')\n"
                                           "called Conf.get_diritem_data with args ('xxx', '2')\n"
                                           "called Conf.get_diritem_data with args ('xxx', '3')\n"
                                           "called Conf.get_diritem_data with args ('xxx', '4')\n")

    def test_select_activations(self, monkeypatch, capsys):
        """unittest for Manager.select_activations
        """
        def mock_add(name):
            """stub
            """
            print(f'called self.add_dependencies with arg {name}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_dependencies = mock_add
        testobj.select_activations([])
        assert testobj.directories == set()
        assert capsys.readouterr().out == ""

        testobj.screeninfo = {'test': {'dir': 'xxx'}, 'other': {'dir': 'yyy'}}
        testobj.select_activations(['test', 'other'])
        assert testobj.directories == {'xxx', 'yyy'}
        assert capsys.readouterr().out == ("called self.add_dependencies with arg xxx\n"
                                           "called self.add_dependencies with arg yyy\n")

    def test_add_dependencies(self, monkeypatch, capsys):
        """unittest for Manager.add_dependencies
        """
        def mock_list(name):
            "stub"
            print(f'called Conf.list_comonents_for_dir with arg {name}')
            if name == 'moddir':
                return ['x', 'y', 'z']
            return []
        def mock_get(name, itemtype):
            print(f"called Conf.get_component_data with args('{name}', '{itemtype}')")
            if itemtype == testobj.conf.DIR:
                return f'{name}dir'
            if itemtype == testobj.conf.DEPS:
                if name in ('x', 'y'):
                    return ['z']
                return []
            return ''
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf.list_components_for_dir = mock_list
        testobj.conf.get_component_data = mock_get
        testobj.get_component_data = mock_get
        testobj.directories = set()
        testobj.add_dependencies('moddir')
        assert testobj.directories == {'zdir'}
        assert capsys.readouterr().out == (
                "called Conf.list_comonents_for_dir with arg moddir\n"
                f"called Conf.get_component_data with args('x', '{testobj.conf.DEPS}')\n"
                f"called Conf.get_component_data with args('z', '{testobj.conf.DIR}')\n"
                "called Conf.list_comonents_for_dir with arg zdir\n"
                f"called Conf.get_component_data with args('y', '{testobj.conf.DEPS}')\n"
                f"called Conf.get_component_data with args('z', '{testobj.conf.DIR}')\n"
                "called Conf.list_comonents_for_dir with arg zdir\n"
                f"called Conf.get_component_data with args('z', '{testobj.conf.DEPS}')\n")

    def test_activate(self, monkeypatch, capsys, tmp_path):
        """unittest for Manager.activate
        """
        def mock_rename(*args):
            print('called os.rename with args', args)
        monkeypatch.setattr(testee.os, 'rename', mock_rename)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.modbase = tmp_path / 'modbase'
        testobj.modbase.mkdir()
        (testobj.modbase / 'somefile').touch()
        (testobj.modbase / 'ConsoleCommands').mkdir()
        (testobj.modbase / 'SaveBackup').mkdir()
        (testobj.modbase / '.dirname1').mkdir()
        (testobj.modbase / 'dirname2').mkdir()
        (testobj.modbase / '.dirname3').mkdir()
        (testobj.modbase / 'dirname4').mkdir()
        testobj.directories = ['dirname2', 'dirname3']
        testobj.activate()
        assert capsys.readouterr().out == ("called os.rename with args (<DirEntry '.dirname3'>,"
                                           f" '{testobj.modbase}/dirname3')\n"
                                           "called os.rename with args (<DirEntry 'dirname4'>,"
                                           f" '{testobj.modbase}/.dirname4')\n")

    def test_manage_attributes(self, monkeypatch, capsys):
        """unittest for Manager.manage_attributes
        """
        def mock_show(*args):
            print('called show_dialog with args', args)
            args[1].master.attr_changes = []
        def mock_show_2(*args):
            print('called show_dialog with args', args)
            args[1].master.attr_changes = [('xxx', 'yyy'), ('zzz', '')]  # , ('', 'qqq')]i kan dit?
            args[1].master.screeninfo = {'xxx': {'dir': 'xxx-dir', 'txt': 'xxx-txt', 'sel': True},
                                         'zzz': {'dir': 'zzz-dir', 'txt': 'zzz-txt', 'sel': False}}
        def mock_set(*args):
            print('called Conf.set_diritem_value with args', args)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = MockShowMods(testobj)
        testobj.conf.set_diritem_value = mock_set
        assert capsys.readouterr().out == f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
        testobj.manage_attributes()
        assert capsys.readouterr().out == (
                "called show_dialog with args (<class 'src.gui.AttributesDialog'>,"
                f" {testobj.doit}, {testobj.conf})\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        testobj.manage_attributes()
        assert capsys.readouterr().out == (
                "called show_dialog with args (<class 'src.gui.AttributesDialog'>,"
                f" {testobj.doit}, {testobj.conf})\n"
                "called Conf.set_diritem_value with args ('xxx-dir', 0, 'xxx')\n"
                "called Conf.set_diritem_value with args ('xxx-dir', 4, 'xxx-txt')\n"
                "called Conf.set_diritem_value with args ('xxx-dir', 1, True)\n"
                "called Conf.set_diritem_value with args ('zzz-dir', 4, 'zzz-txt')\n"
                "called Conf.set_diritem_value with args ('zzz-dir', 1, False)\n"
                "called JsonConf.save\n")

    def test_update_config_from_screenpos(self, monkeypatch, capsys):
        """unittest for Manager.update_config_from_screenpos
        """
        def mock_set(*args):
            print('called Conf.set_diritem_data with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf.set_diritem_data = mock_set
        testobj.screeninfo = {}
        testobj.update_config_from_screenpos()
        assert capsys.readouterr().out == "called JsonConf.save\n"
        testobj.screeninfo = {'xxx': {'pos': '5x5', 'dir': 'x-dir'},
                              'yyy': {'pos': '1x1', 'dir': 'y-dir'}}
        testobj.update_config_from_screenpos()
        assert capsys.readouterr().out == (
                "called Conf.set_diritem_data with args ('x-dir', 2, '5x5')\n"
                "called Conf.set_diritem_data with args ('y-dir', 2, '1x1')\n"
                "called JsonConf.save\n")

    def test_update_mods(self, monkeypatch, capsys, tmp_path):
        """unittest for Manager.update_mods
        """
        def mock_install(name):
            print(f"called Manager.install_zipfile with arg '{name}'")
            return [], False, False, ['no roots']
        def mock_install_2(name):
            print(f"called Manager.install_zipfile with arg '{name}'")
            return [''], False, False, ['not a mod']
        def mock_install_3(name):
            print(f"called Manager.install_zipfile with arg '{name}'")
            self.conf_changed = True
            return ['yyy'], False, False, ['ok']
        def mock_install_4(name):
            print(f"called Manager.install_zipfile with arg '{name}'")
            self.conf_changed = True
            return ['yyy'], True, False, ['ok']
        def mock_install_5(name):
            print(f"called Manager.install_zipfile with arg '{name}'")
            self.conf_changed = True
            return ['yyy'], True, True, ['ok']
        def mock_rename(*args):
            print('called os.rename with args', args)
        def mock_extract():
            print('called Manager.extract_screeninfo')
        def mock_get(*args):
            print('called Manager.get_data_for_config with args', args)
            return ['done'], False
        def mock_get_2(*args):
            print('called Manager.get_data_for_config with args', args)
            return ['done'], True
        def mock_det(*args):
            print('called Manager.determine_moddir with args', args)
            return 'root'
        def mock_upd(*args):
            print('called Manager.update_mod_settings with args', args)
            return (['done'], False)
        def mock_upd_2(*args):
            print('called Manager.update_mod_settings with args', args)
            return (['done'], True)
        def mock_add(*args):
            print('called Manager.add_mod_to_config with args', args)
            return ['done']
        # monkeypatch.setattr(testee, 'check_if_active', mock_check)
        monkeypatch.setattr(testee.os, 'rename', mock_rename)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.extract_screeninfo = mock_extract
        testobj.install_zipfile = mock_install
        testobj.get_data_for_config = mock_get
        testobj.determine_moddir = mock_det
        testobj.update_mod_settings = mock_upd
        testobj.add_mod_to_config = mock_add
        testobj.doit = MockShowMods(testobj)
        assert capsys.readouterr().out == f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
        assert testobj.update_mods([]) == []
        assert capsys.readouterr().out == ""

        assert testobj.update_mods([str(tmp_path / 'xxx')]) == ['no roots']
        assert capsys.readouterr().out == (
                f"called Manager.install_zipfile with arg '{tmp_path}/xxx'\n")
        testobj.install_zipfile = mock_install_2
        assert testobj.update_mods([str(tmp_path / 'xxx')]) == ['not a mod']
        assert capsys.readouterr().out == (
                f"called Manager.install_zipfile with arg '{tmp_path}/xxx'\n")

        testobj.install_zipfile = mock_install_3
        assert testobj.update_mods([str(tmp_path / 'xxx')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/xxx'\n"
            f"called Manager.get_data_for_config with args (['yyy'], False)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.add_mod_to_config with args ('root', (['done'], False))\n"
            f"called os.rename with args ('{tmp_path}/xxx', '{tmp_path}/installed/xxx')\n"
            "called JsonConf.save\n"
            "called Manager.extract_screeninfo\n"
            "called gui.ShowMods.refresh_widgets with args {'first_time': True}\n")

        testobj.get_data_for_config = mock_get_2
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], False)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.add_mod_to_config with args ('root', (['done'], True))\n"
            f"called os.rename with args ('{tmp_path}/yyy', '{tmp_path}/installed/yyy')\n"
            "called JsonConf.save\n"
            "called Manager.extract_screeninfo\n"
            "called gui.ShowMods.refresh_widgets with args {'first_time': True}\n")

        testobj.install_zipfile = mock_install_4
        testobj.get_data_for_config = mock_get
        testobj.update_mod_settings = mock_upd
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], False)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.update_mod_settings with args ('root', (['done'], False))\n"
            f"called os.rename with args ('{tmp_path}/yyy', '{tmp_path}/installed/yyy')\n")

        testobj.update_mod_settings = mock_upd_2
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], False)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.update_mod_settings with args ('root', (['done'], False))\n"
            f"called os.rename with args ('{tmp_path}/yyy', '{tmp_path}/installed/yyy')\n"
            "called JsonConf.save\n")

        testobj.get_data_for_config = mock_get_2
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], False)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.update_mod_settings with args ('root', (['done'], True))\n"
            f"called os.rename with args ('{tmp_path}/yyy', '{tmp_path}/installed/yyy')\n"
            "called JsonConf.save\n")

        testobj.install_zipfile = mock_install_5
        testobj.get_data_for_config = mock_get
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], True)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.update_mod_settings with args ('root', (['done'], False))\n"
            f"called os.rename with args ('{tmp_path}/yyy', '{tmp_path}/installed/yyy')\n"
            "called JsonConf.save\n")

        testobj.get_data_for_config = mock_get_2
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], True)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.update_mod_settings with args ('root', (['done'], True))\n"
            f"called os.rename with args ('{tmp_path}/yyy', '{tmp_path}/installed/yyy')\n"
            "called JsonConf.save\n")

    def test_install_zipfile(self, monkeypatch, capsys):  # , tmp_path):
        """unittest for Manager.install_zipfile
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
            def __enter__(self):
                print('called ZipFile.__enter__')
                return self
            def __exit__(self, *args):
                print('called ZipFile.__exit__')
                return True
        def mock_get(arg):
            print(f'called get_archive_roots with arg {arg}')
            return set()
        def mock_get_2(arg):
            print(f'called get_archive_roots with arg {arg}')
            return {''}
        def mock_get_3(arg):
            print(f'called get_archive_roots with arg {arg}')
            return {'root'}
        def mock_check(arg):
            print(f'called check_if_active with arg {arg}')
            return False, False
        # def mock_check_2(arg):
        #     print(f'called check_if_active with arg {arg}')
        #     return True, False
        # def mock_check_3(arg):
        #     print(f'called check_if_active with arg {arg}')
        #     return True, True
        def mock_check_smapi(arg):
            print(f'called check_if_smapi with arg {arg}')
            return True
        def mock_check_smapi_2(arg):
            print(f'called check_if_smapi with arg {arg}')
            return False
        def mock_run(*args, **kwargs):
            print('called subprocess.run with args', args, kwargs)
        def mock_rm(*args):
            print('called shutil.rmtree with args', args)
        def mock_get_data(*args):
            print('called Manager.get_data_for_config with args', args)
        def mock_add(*args):
            print('called Manager.add_mod_to_config with args', args)
            return ['xxx']
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.subprocess, 'run', mock_run)
        monkeypatch.setattr(testee.zipfile, 'ZipFile', MockZipFile)
        monkeypatch.setattr(testee, 'get_archive_roots', mock_get)
        monkeypatch.setattr(testee, 'check_if_active', mock_check)
        monkeypatch.setattr(testee, 'check_if_smapi', mock_check_smapi)
        monkeypatch.setattr(testee.os.path, 'exists', lambda *x: True)
        monkeypatch.setattr(testee.shutil, 'rmtree', mock_rm)
        testobj.get_data_for_config = mock_get_data
        testobj.add_mod_to_config = mock_add
        assert testobj.install_zipfile(testee.pathlib.Path('zipfile')) == (
                [], None, None, ['zipfile: zipfile appears to be empty'])
        assert capsys.readouterr().out == (
                "called ZipFile.__init__ with args (PosixPath('zipfile'),)\n"
                "called ZipFile.__enter__\n"
                "called ZipFile.namelist\n"
                "called get_archive_roots with arg ['name', 'list']\n"
                "called check_if_active with arg set()\n"
                "called check_if_smapi with arg set()\n"
                "called ZipFile.__exit__\n")

        monkeypatch.setattr(testee, 'get_archive_roots', mock_get_2)
        assert testobj.install_zipfile(testee.pathlib.Path('zipfile')) == (
                [], None, None, ["SMAPI-install is waiting in a terminal window to be finished"
                                 " by executing './install on Linux.sh'"])
        assert capsys.readouterr().out == (
                "called ZipFile.__init__ with args (PosixPath('zipfile'),)\n"
                "called ZipFile.__enter__\n"
                "called ZipFile.namelist\n"
                "called get_archive_roots with arg ['name', 'list']\n"
                "called check_if_active with arg {''}\n"
                "called check_if_smapi with arg {''}\n"
                "called ZipFile.__exit__\n"
                "called subprocess.run with args"
                " (['unzip', PosixPath('zipfile'), '-d', '/tmp'],) {'check': True}\n"
                "called subprocess.run with args (['gnome-terminal'],) {'cwd': '/tmp/'}\n")

        monkeypatch.setattr(testee, 'get_archive_roots', mock_get_3)
        monkeypatch.setattr(testee, 'check_if_smapi', mock_check_smapi_2)
        assert testobj.install_zipfile(testee.pathlib.Path('zipfile')) == (
                {'root'}, False, False, ['zipfile is successfully installed'])
        assert capsys.readouterr().out == (
                "called ZipFile.__init__ with args (PosixPath('zipfile'),)\n"
                "called ZipFile.__enter__\n"
                "called ZipFile.namelist\n"
                "called get_archive_roots with arg ['name', 'list']\n"
                "called check_if_active with arg {'root'}\n"
                "called check_if_smapi with arg {'root'}\n"
                "called ZipFile.extractall with args ('modbase',)\n"
                "called ZipFile.__exit__\n"
                "called shutil.rmtree with args ('modbase/__MACOSX',)\n")

        monkeypatch.setattr(testee.os.path, 'exists', lambda *x: False)
        assert testobj.install_zipfile(testee.pathlib.Path('zipfile')) == (
                {'root'}, False, False, ['zipfile is successfully installed'])
        assert capsys.readouterr().out == (
                "called ZipFile.__init__ with args (PosixPath('zipfile'),)\n"
                "called ZipFile.__enter__\n"
                "called ZipFile.namelist\n"
                "called get_archive_roots with arg ['name', 'list']\n"
                "called check_if_active with arg {'root'}\n"
                "called check_if_smapi with arg {'root'}\n"
                "called ZipFile.extractall with args ('modbase',)\n"
                "called ZipFile.__exit__\n")

    def test_determine_moddir(self, monkeypatch, capsys):
        """unittest for Manager.determine_moddir
        """
        def mock_select(*args):
            nonlocal counter
            print('called ShowMods.select_value with args', args)
            counter += 1
            if counter == 1:
                return ''
            return 'qqq'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = MockShowMods(testobj)
        testobj.doit.select_value = mock_select
        counter = 0
        assert capsys.readouterr().out == f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
        assert testobj.determine_moddir(['xxx']) == 'xxx'
        assert capsys.readouterr().out == ''
        assert testobj.determine_moddir(['xxx', 'yyy']) == 'qqq'
        assert capsys.readouterr().out == ("called ShowMods.select_value with args"
                                           " ('Select one of the directories as the \"mod base\"',"
                                           " ['xxx', 'yyy'], False, True)\n"
                                           "called ShowMods.select_value with args"
                                           " ('Select one of the directories as the \"mod base\"',"
                                           " ['xxx', 'yyy'], False, True)\n")

    def test_get_data_for_config(self, monkeypatch, capsys, tmp_path):
        """unittest for Manager.get_data_for_config
        """
        def mock_build(arg):
            print(f'called JsonConf.build_entry_from_dir with arg {arg}')
            return ['stuff']
        def mock_rename(*args):
            print('called os.rename with args', args)
        monkeypatch.setattr(testee.dmlj, 'build_entry_from_dir', mock_build)
        monkeypatch.setattr(testee.os, 'rename', mock_rename)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.modbase = str(tmp_path)
        assert testobj.get_data_for_config(['x', 'y'], True) == {'x': ['stuff'], 'y': ['stuff']}
        assert capsys.readouterr().out == (
                f"called JsonConf.build_entry_from_dir with arg {tmp_path}/x\n"
                f"called JsonConf.build_entry_from_dir with arg {tmp_path}/y\n")
        assert testobj.get_data_for_config(['x', 'y'], False) == {'x': ['stuff'], 'y': ['stuff']}
        assert capsys.readouterr().out == (
                f"called JsonConf.build_entry_from_dir with arg {tmp_path}/x\n"
                f"called os.rename with args ('{tmp_path}/x', '{tmp_path}/.x')\n"
                f"called JsonConf.build_entry_from_dir with arg {tmp_path}/y\n"
                f"called os.rename with args ('{tmp_path}/y', '{tmp_path}/.y')\n")

    def test_add_mod_to_config(self, monkeypatch, capsys):
        """unittest for Manager.add_mod_to_config
        """
        def mock_has_mod(arg):
            print(f'called Conf.has_moddir with arg {arg}')
            return True
        def mock_has_mod_2(arg):
            print(f'called Conf.has_moddir with arg {arg}')
            return False
        def mock_add_dir(arg):
            print(f'called Conf.add_diritem with arg {arg}')
        def mock_set_dir(*args):
            print('called Conf.set_diritem_value with args', args)
        def mock_add_comp(arg):
            print(f'called Conf.add_component with arg {arg}')
        def mock_set_comp(*args):
            print('called Conf.set_component_value with args', args)
        def mock_determine(arg):
            print(f'called determine_update_id with arg {arg}')
            return 'xx', []
        def mock_determine_2(arg):
            print(f'called determine_update_id with arg {arg}')
            return 'xx', ['more', 'ids']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf.has_moddir = mock_has_mod
        testobj.conf.add_diritem = mock_add_dir
        testobj.conf.set_diritem_value = mock_set_dir
        testobj.conf.add_componentdata = mock_add_comp
        testobj.conf.set_componentdata_value = mock_set_comp
        monkeypatch.setattr(testee, 'determine_update_id', mock_determine)
        with pytest.raises(ValueError) as exc:
            testobj.add_mod_to_config('moddir', {'config': 'data'})
        assert str(exc.value) == '"New" mod exists in configuration, should not be possible'
        assert capsys.readouterr().out == "called Conf.has_moddir with arg moddir\n"

        testobj.conf.has_moddir = mock_has_mod_2
        assert testobj.add_mod_to_config('moddir', {}) == [
                "  Screentext set to '(new mod)' ",
                '  Update ID set to xx ',
                '  Change the "Selectable" setting if you want to be able to activate the mod']
        assert capsys.readouterr().out == ("called Conf.has_moddir with arg moddir\n"
                                           "called Conf.add_diritem with arg moddir\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.COMPS}, [])\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.SCRNAM}, '(new mod)')\n"
                                           "called determine_update_id with arg set()\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.NXSKEY}, 'xx')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.SEL}, False)\n")

        assert testobj.add_mod_to_config('moddir', {'unzipdir': {}}) == [
                "  Screentext set to '(new mod)' ",
                '  Update ID set to xx ',
                '  Change the "Selectable" setting if you want to be able to activate the mod']
        assert capsys.readouterr().out == ("called Conf.has_moddir with arg moddir\n"
                                           "called Conf.add_diritem with arg moddir\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.COMPS}, [])\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.SCRNAM}, '(new mod)')\n"
                                           "called determine_update_id with arg set()\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.NXSKEY}, 'xx')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.SEL}, False)\n")

        assert testobj.add_mod_to_config('moddir', {'unzipdir': {'component': {}}}) == [
                "  Screentext set to '(new mod)' ",
                '  Update ID set to xx ',
                '  Change the "Selectable" setting if you want to be able to activate the mod']
        assert capsys.readouterr().out == ("called Conf.has_moddir with arg moddir\n"
                                           "called Conf.add_diritem with arg moddir\n"
                                           "called Conf.add_component with arg component\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.COMPS}, ['component'])\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.SCRNAM}, '(new mod)')\n"
                                           "called determine_update_id with arg set()\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.NXSKEY}, 'xx')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.SEL}, False)\n")

        result = testobj.add_mod_to_config('moddir',
                                           {'unzipdir': {'component': {testobj.conf.NAME: 'abcdef'},
                                                         'comp2': {testobj.conf.NAME: 'pqrst'},
                                                         'comp3': {testobj.conf.NAME: 'abcdef'}}})
        assert result == [
                "  Screentext set to 'abcdef' , multiple possibilities found",
                '  Update ID set to xx ',
                '  Change the "Selectable" setting if you want to be able to activate the mod']
        assert capsys.readouterr().out == ("called Conf.has_moddir with arg moddir\n"
                                           "called Conf.add_diritem with arg moddir\n"
                                           "called Conf.add_component with arg component\n"
                                           "called Conf.set_component_value with args"
                                           f" ('component', {testobj.conf.NAME}, 'abcdef')\n"
                                           "called Conf.add_component with arg comp2\n"
                                           "called Conf.set_component_value with args"
                                           f" ('comp2', {testobj.conf.NAME}, 'pqrst')\n"
                                           "called Conf.add_component with arg comp3\n"
                                           "called Conf.set_component_value with args"
                                           f" ('comp3', {testobj.conf.NAME}, 'abcdef')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.COMPS},"
                                           " ['component', 'comp2', 'comp3'])\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.SCRNAM}, 'abcdef')\n"
                                           "called determine_update_id with arg set()\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.NXSKEY}, 'xx')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.SEL}, False)\n")

        monkeypatch.setattr(testee, 'determine_update_id', mock_determine_2)
        result = testobj.add_mod_to_config('moddir',
                                           {'unzipdir': {'component': {testobj.conf.NAME: 'abcdef',
                                                                       testobj.conf.NXSKEY: '123',
                                                                       'xxx': 'yyy'}}})
        assert result == [
                "  Screentext set to 'abcdef' , multiple possibilities found",
                "  Update ID set to xx , multiple values found: ['more', 'ids'] ",
                '  Change the "Selectable" setting if you want to be able to activate the mod']
        assert capsys.readouterr().out == ("called Conf.has_moddir with arg moddir\n"
                                           "called Conf.add_diritem with arg moddir\n"
                                           "called Conf.add_component with arg component\n"
                                           "called Conf.set_component_value with args"
                                           f" ('component', {testobj.conf.NAME}, 'abcdef')\n"
                                           "called Conf.set_component_value with args"
                                           f" ('component', {testobj.conf.NXSKEY}, '123')\n"
                                           "called Conf.set_component_value with args"
                                           f" ('component', 'xxx', 'yyy')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.COMPS}, ['component'])\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.SCRNAM}, 'abcdef')\n"
                                           "called determine_update_id with arg {'123'}\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.NXSKEY}, 'xx')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', {testobj.conf.SEL}, False)\n")

    def test_update_mod_settings(self, monkeypatch, capsys):
        """unittest for Manager.update_mod_settings
        """
        def mock_has_mod(arg):
            print(f'called Conf.has_moddir with arg {arg}')
            return False
        def mock_has_mod_2(arg):
            print(f'called Conf.has_moddir with arg {arg}')
            return True
        def mock_get_dir(*args):
            print('called Conf.get_diritem_data with args', args)
            return []
        def mock_get_dir_2(*args):
            print('called Conf.get_diritem_data with args', args)
            return ['newcomp']
        def mock_set(*args):
            print('called Conf.set_diritem_value with args', args)
        def mock_get_comp(arg):
            print(f'called Conf.get_component_data with arg {arg}')
            return {}
        def mock_get_comp_2(arg):
            print(f'called Conf.get_component_data with arg {arg}')
            return {testobj.conf.NAME: 'xxx', testobj.conf.VER: '1.0', 'aaa': 'bbb'}
        def mock_update(*args):
            print('called Conf.update_componentdata with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf.has_moddir = mock_has_mod
        testobj.conf.get_diritem_data = mock_get_dir
        testobj.conf.set_diritem_value = mock_set
        testobj.conf.get_component_data = mock_get_comp
        testobj.conf.update_componentdata = mock_update

        with pytest.raises(ValueError) as exc:
            testobj.update_mod_settings('moddir', {'config': 'data'})
        assert str(exc.value) == 'Installed mod is not in configuration, should not be possible'
        assert capsys.readouterr().out == "called Conf.has_moddir with arg moddir\n"

        testobj.conf.has_moddir = mock_has_mod_2
        assert testobj.update_mod_settings('moddir', {}) == ([], False)
        assert capsys.readouterr().out == (
                "called Conf.has_moddir with arg moddir\n"
                f"called Conf.get_diritem_data with args ('moddir', {testobj.conf.COMPS})\n")

        assert testobj.update_mod_settings('moddir', {'config': {}}) == ([], False)
        assert capsys.readouterr().out == (
                "called Conf.has_moddir with arg moddir\n"
                f"called Conf.get_diritem_data with args ('moddir', {testobj.conf.COMPS})\n")

        assert testobj.update_mod_settings('moddir', {'config': {'newcomp': {}}}) == (
                ["  List of components changed from [] to ['newcomp']"], True)
        assert capsys.readouterr().out == (
                "called Conf.has_moddir with arg moddir\n"
                f"called Conf.get_diritem_data with args ('moddir', {testobj.conf.COMPS})\n"
                f"called Conf.set_diritem_value with args ('moddir', {testobj.conf.COMPS},"
                " ['newcomp'])\n"
                "called Conf.get_component_data with arg newcomp\n"
                "called Conf.update_componentdata with args ('newcomp', {})\n")

        testobj.conf.get_diritem_data = mock_get_dir_2
        testobj.conf.get_component_data = mock_get_comp_2
        assert testobj.update_mod_settings('moddir', {'config': {'newcomp': {
            testobj.conf.NAME: 'xxx', testobj.conf.VER: '2.0', 'ppp': 'qqq'}}}) == (
                    [f"  newcomp: {testobj.conf.VER} changed from '1.0' to '2.0'",
                     "  newcomp: new key ppp added with value 'qqq'",
                     "  newcomp: key aaa with value 'bbb' removed"], True)
        assert capsys.readouterr().out == (
                "called Conf.has_moddir with arg moddir\n"
                f"called Conf.get_diritem_data with args ('moddir', {testobj.conf.COMPS})\n"
                "called Conf.get_component_data with arg newcomp\n"
                "called Conf.update_componentdata with args ('newcomp', {"
                f"{testobj.conf.NAME}: 'xxx', {testobj.conf.VER}: '2.0', 'ppp': 'qqq'}})\n")

        assert testobj.update_mod_settings('moddir', {'config': {'newcomp': {
            testobj.conf.NAME: 'xxx', testobj.conf.VER: '1.0', 'aaa': 'bbb'}}}) == ([], False)
        assert capsys.readouterr().out == (
                "called Conf.has_moddir with arg moddir\n"
                f"called Conf.get_diritem_data with args ('moddir', {testobj.conf.COMPS})\n"
                "called Conf.get_component_data with arg newcomp\n")


def test_get_archive_roots():
    """unittest for Manager.get_archive_roots
    """
    assert testee.get_archive_roots([]) == []
    assert testee.get_archive_roots(['path/to/file', 'path/to/other/file', 'root/dir']) == ['path',
                                                                                           'root']
    assert testee.get_archive_roots(['path/to/file', '__MACOSX/dir', '__MACOSX/xxx']) == ['path']


def test_check_if_smapi():
    """unittest for Manager.check_if_smapi
    """
    assert not testee.check_if_smapi(['xxx', 'yyy'])
    assert testee.check_if_smapi(['SMAPI-root', 'yyy'])
    assert testee.check_if_smapi(['xxx', 'SMAPI-root'])


def test_check_if_active(monkeypatch, capsys, tmp_path):
    """unittest for Manager.check_if_active
    """
    def mock_rm(*args):
        print('called shutil.rmtree with args', args)
    def mock_rename(*args):
        print('called os.rename with args', args)
    monkeypatch.setattr(testee, 'MODBASE', tmp_path)
    monkeypatch.setattr(testee.shutil, 'rmtree', mock_rm)
    monkeypatch.setattr(testee.os, 'rename', mock_rename)
    assert testee.check_if_active([]) == (False, False)
    assert testee.check_if_active(['root']) == (False, False)
    (tmp_path / 'root').touch()
    assert testee.check_if_active(['root']) == (True, True)
    assert capsys.readouterr().out == (
            f"called os.rename with args ('{tmp_path}/root', '{tmp_path}/.root~')\n")
    (tmp_path / '.root~').touch()
    assert testee.check_if_active(['root']) == (True, True)
    assert capsys.readouterr().out == (
            f"called shutil.rmtree with args ('{tmp_path}/.root~',)\n"
            f"called os.rename with args ('{tmp_path}/root', '{tmp_path}/.root~')\n")
    (tmp_path / 'root').unlink()
    (tmp_path / '.root').touch()
    assert testee.check_if_active(['root']) == (True, False)
    assert capsys.readouterr().out == (
            f"called shutil.rmtree with args ('{tmp_path}/.root~',)\n"
            f"called os.rename with args ('{tmp_path}/.root', '{tmp_path}/.root~')\n")


def test_determine_update_id():
    """unittest for Manager.test_determine_update_id
    """
    assert testee.determine_update_id([]) == (0, [])
    assert testee.determine_update_id(['', '']) == (0, [])
    assert testee.determine_update_id(['0', '0']) == (0, [])
    assert testee.determine_update_id(['0', '1']) == (1, [])
    assert testee.determine_update_id(['1', '0']) == (1, [])
    assert testee.determine_update_id(['1', '1']) == (1, [])
    assert testee.determine_update_id(['1', '2', '1']) == (1, [2])


def test_build_jsonconf(monkeypatch, capsys, tmp_path):
    """unittest for manager.build_jsonconf
    """
    def mock_rebuild(arg):
        print(f'called dmlj.rebuild_all with arg {list(arg)}')
        return 'data', []
    def mock_rebuild_2(arg):
        print(f'called dmlj.rebuild_all with arg {list(arg)}')
        return 'data', ['xxx', 'yyy']
    def mock_dump(*args):
        print('called json.dump with args', args)
    monkeypatch.setattr(testee, 'MODBASE', str(tmp_path))
    (tmp_path / 'xxx').touch()
    (tmp_path / 'yyy').touch()
    monkeypatch.setattr(testee, 'CONFIG', 'qqq')
    monkeypatch.setattr(testee.json, 'dump', mock_dump)
    monkeypatch.setattr(testee.dmlj, 'rebuild_all', mock_rebuild)
    assert testee.build_jsonconf() == []
    assert capsys.readouterr().out == (
            f"called dmlj.rebuild_all with arg [{tmp_path / 'xxx'!r}, {tmp_path / 'yyy'!r}]\n"
            "called json.dump with args ('data',"
            " <_io.TextIOWrapper name='qqq' mode='w' encoding='UTF-8'>)\n")
    monkeypatch.setattr(testee.dmlj, 'rebuild_all', mock_rebuild_2)
    assert testee.build_jsonconf() == ['xxx', 'yyy']
    assert capsys.readouterr().out == (
            f"called dmlj.rebuild_all with arg [{tmp_path / 'xxx'!r}, {tmp_path / 'yyy'!r}]\n"
            "called json.dump with args ('data',"
            " <_io.TextIOWrapper name='qqq' mode='w' encoding='UTF-8'>)\n")
