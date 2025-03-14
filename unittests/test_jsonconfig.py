"""unittests for ./src/jsonconfig.py
"""
import pytest
from src import jsonconfig as testee


def test_read_defaults(monkeypatch, tmp_path):
    "unittest for jsonconfig.read_defaults"
    monkeypatch.setattr(testee, 'DEFAULTS', str(tmp_path / 'defaults.json'))
    assert testee.read_defaults() == ('', '', '', '')
    (tmp_path / 'defaults.json').write_text('{"modbase": "xxx", "config": "yyy",'
                                            '"download": "zzz",' '"savepath": "qqq"}')
    assert testee.read_defaults() == ('xxx', 'xxx/yyy', 'zzz', testee.pathlib.Path('qqq'))
    (tmp_path / 'defaults.json').write_text('{"modbase": "~/xxx", "config": "yyy",'
                                            '"download": "~/zzz",' '"savepath": "~/qqq"}')
    assert testee.read_defaults() == (testee.os.path.expanduser('~/xxx'),
                                      testee.os.path.expanduser('~/xxx/yyy'),
                                      testee.os.path.expanduser('~/zzz'),
                                      testee.pathlib.Path('~/qqq').expanduser())
    assert testee.read_defaults(bare=True) == ('~/xxx', 'yyy', '~/zzz', '~/qqq')


def test_save_defaults(monkeypatch, tmp_path):
    "unittest for jsonconfig.write_defaults"
    defaultloc = tmp_path / 'defaults.json'
    backuploc = tmp_path / 'defaults.json~'
    monkeypatch.setattr(testee, 'DEFAULTS', str(defaultloc))
    assert not defaultloc.exists()
    testee.save_defaults('xxx', 'yyy', 'zzz', 'qqq')
    assert defaultloc.exists()
    assert defaultloc.read_text() == ('{"modbase": "xxx", "config": "yyy",'
                                      ' "download": "zzz", "savepath": "qqq"}')
    assert not backuploc.exists()
    testee.save_defaults('aaa', 'bbb', 'ccc', 'ddd')
    assert defaultloc.read_text() == ('{"modbase": "aaa", "config": "bbb", '
                                      '"download": "ccc", "savepath": "ddd"}')
    assert backuploc.exists()


def test_rebuild_all(monkeypatch, capsys):
    """unittest for jsonconfig.rebuild_all
    """
    def mock_build(path):
        print(f"called build_entry_from_dir with arg {path}")
        return {'x': {'y': 'yyy', 'z': 'zzz'}, 'a': {'b': 'bbb', 'c': 'ccc'}}
    def mock_build_2(path):
        print(f"called build_entry_from_dir with arg {path}")
        return {'x': {'y': 'yyy', 'z': 'zzz'}}
    def mock_isdir(path):
        print(f"called path.isdir with arg {path}")
        return False
    def mock_isdir_2(path):
        print(f"called path.isdir with arg {path}")
        return True
    monkeypatch.setattr(testee, 'build_entry_from_dir', mock_build)
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir)
    assert testee.rebuild_all([]) == ({'moddirs': {}, 'components': {}}, [])
    assert capsys.readouterr().out == ("")
    startdirs = [testee.pathlib.Path('.cjbcheats-warps-backup'),
                 testee.pathlib.Path('ConsoleCommands'),
                 testee.pathlib.Path('SaveBackup')]
    assert testee.rebuild_all(startdirs) == ({'moddirs': {}, 'components': {}}, [])
    assert capsys.readouterr().out == ""

    startdirs = [testee.pathlib.Path('dirname')]
    assert testee.rebuild_all(startdirs) == ({'moddirs': {}, 'components': {}}, [])
    assert capsys.readouterr().out == "called path.isdir with arg dirname\n"

    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir_2)
    startdirs = [testee.pathlib.Path('dirname~')]
    assert testee.rebuild_all(startdirs) == ({'moddirs': {}, 'components': {}}, [])
    assert capsys.readouterr().out == "called path.isdir with arg dirname~\n"

    startdirs = [testee.pathlib.Path('dirname')]
    assert testee.rebuild_all(startdirs) == ({'moddirs': {'dirname': {'components': ['x', 'a']}},
                                              'components': {'a': {'b': 'bbb', 'c': 'ccc'},
                                                             'x': {'y': 'yyy', 'z': 'zzz'}}}, [])
    assert capsys.readouterr().out == ("called path.isdir with arg dirname\n"
                                       "called build_entry_from_dir with arg dirname\n")

    monkeypatch.setattr(testee, 'build_entry_from_dir', mock_build_2)
    startdirs = [testee.pathlib.Path('dirname'), testee.pathlib.Path('dirname2')]
    # dit kan wel: dubbele componenten in meer uitpakdirectories
    assert testee.rebuild_all(startdirs) == ({'moddirs': {'dirname': {'components': ['x']}},
                                              'components': {'x': {'y': 'yyy', 'z': 'zzz'}}},
                                             ['duplicate component(s) found in dirname2'])
    assert capsys.readouterr().out == ("called path.isdir with arg dirname\n"
                                       "called build_entry_from_dir with arg dirname\n"
                                       "called path.isdir with arg dirname2\n"
                                       "called build_entry_from_dir with arg dirname2\n")


def test_build_entry_from_dir(monkeypatch, capsys):
    """unittest for jsonconfig.build_entry_from_dir
    """
    def mock_iter(path):
        print(f'called path.iterdir with arg {path}')
        return []
    def mock_iter_2(path):
        print(f'called path.iterdir with arg {path}')
        return [testee.pathlib.Path('xxx/yyy')]  # , pathlib.Path('aaa/bbb')]
    def mock_read(path):
        print(f'called read_dir with arg {path}')
        return []
    def mock_read_2(path):
        print(f'called read_dir with arg {path}')
        return [{'dirpath': testee.pathlib.Path('xxx/yyy/zz'), 'UniqueID': ''},
                {'dirpath': testee.pathlib.Path('xxx/qqq'), 'UniqueID': 'aaa.bbb', 'argl': 'bargl'}]
    monkeypatch.setattr(testee.pathlib.Path, 'iterdir', mock_iter)
    monkeypatch.setattr(testee, 'read_dir', mock_read)
    modpath = testee.pathlib.Path('xxx/yyy')
    assert testee.build_entry_from_dir(modpath) == {}
    assert capsys.readouterr().out == "called path.iterdir with arg xxx/yyy\n"
    monkeypatch.setattr(testee.pathlib.Path, 'iterdir', mock_iter_2)
    assert testee.build_entry_from_dir(modpath) == {}
    assert capsys.readouterr().out == ("called path.iterdir with arg xxx/yyy\n"
                                       "called read_dir with arg xxx/yyy\n")
    monkeypatch.setattr(testee, 'read_dir', mock_read_2)
    assert testee.build_entry_from_dir(modpath) == {'': {'dirname': 'yyy/zz'},
                                                    'aaa.bbb': {'argl': 'bargl', 'dirname': 'qqq'}}
    assert capsys.readouterr().out == ("called path.iterdir with arg xxx/yyy\n"
                                       "called read_dir with arg xxx/yyy\n")


def test_read_dir(monkeypatch, capsys, tmp_path):
    """unittest for jsonconfig.read_dir
    """
    def mock_read(path):
        print(f'called read_manifest with arg {path}')
        return {}
    def mock_read_2(path):
        print(f'called read_manifest with arg {path}')
        return {'x': 'y'}
    def mock_isdir(path):
        print(f"called path.is_dir with arg {path}")
        return old_is_dir(path)
    def mock_iter(path):
        print(f"called path.iterdir with arg {path}")
        return old_iterdir(path)
    monkeypatch.setattr(testee, 'read_manifest', mock_read)
    old_is_dir = testee.pathlib.Path.is_dir
    old_iterdir = testee.pathlib.Path.iterdir
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir)
    monkeypatch.setattr(testee.pathlib.Path, 'iterdir', mock_iter)
    path = tmp_path / 'manifest.json'
    path.touch()
    assert testee.read_dir(tmp_path) == []
    assert capsys.readouterr().out == (f"called path.is_dir with arg {tmp_path}\n"
                                       f"called path.iterdir with arg {tmp_path}\n"
                                       f"called read_manifest with arg {tmp_path}/manifest.json\n"
                                       f"called path.is_dir with arg {tmp_path}/manifest.json\n")
    monkeypatch.setattr(testee, 'read_manifest', mock_read_2)
    assert testee.read_dir(tmp_path) == [{'x': 'y'}]
    assert capsys.readouterr().out == (f"called path.is_dir with arg {tmp_path}\n"
                                       f"called path.iterdir with arg {tmp_path}\n"
                                       f"called read_manifest with arg {tmp_path}/manifest.json\n"
                                       f"called path.is_dir with arg {tmp_path}/manifest.json\n")
    path.unlink()
    path = tmp_path / 'xxx'
    path.touch()
    assert testee.read_dir(tmp_path) == []
    assert capsys.readouterr().out == (f"called path.is_dir with arg {tmp_path}\n"
                                       f"called path.iterdir with arg {tmp_path}\n"
                                       f"called path.is_dir with arg {tmp_path}/xxx\n")
    path.unlink()
    path = tmp_path / 'xxx'
    path.mkdir()
    assert testee.read_dir(tmp_path) == []
    assert capsys.readouterr().out == (f"called path.is_dir with arg {tmp_path}\n"
                                       f"called path.iterdir with arg {tmp_path}\n"
                                       f"called path.is_dir with arg {tmp_path}/xxx\n"
                                       f"called path.iterdir with arg {tmp_path}/xxx\n")
    monkeypatch.setattr(testee, 'read_manifest', mock_read)
    subpath = tmp_path / 'xxx' / 'manifest.json'
    subpath.touch()
    assert testee.read_dir(tmp_path) == []
    assert capsys.readouterr().out == (
            f"called path.is_dir with arg {tmp_path}\n"
            f"called path.iterdir with arg {tmp_path}\n"
            f"called path.is_dir with arg {tmp_path}/xxx\n"
            f"called path.iterdir with arg {tmp_path}/xxx\n"
            f"called read_manifest with arg {tmp_path}/xxx/manifest.json\n")
    monkeypatch.setattr(testee, 'read_manifest', mock_read_2)
    subpath = tmp_path / 'xxx' / 'qqq'
    subpath.touch()
    subpath = tmp_path / 'xxx' / 'yyy'
    subpath.mkdir()
    assert testee.read_dir(tmp_path) == [{'x': 'y'}]
    assert capsys.readouterr().out == (
            f"called path.is_dir with arg {tmp_path}\n"
            f"called path.iterdir with arg {tmp_path}\n"
            f"called path.is_dir with arg {tmp_path}/xxx\n"
            f"called path.iterdir with arg {tmp_path}/xxx\n"
            f"called read_manifest with arg {tmp_path}/xxx/manifest.json\n")
    monkeypatch.setattr(testee, 'read_manifest', mock_read)
    path = testee.pathlib.Path('manifest.json')
    assert testee.read_dir(path) == []
    assert capsys.readouterr().out == ("called read_manifest with arg manifest.json\n"
                                       "called path.is_dir with arg manifest.json\n")
    monkeypatch.setattr(testee, 'read_manifest', mock_read_2)
    assert testee.read_dir(path) == [{'x': 'y'}]
    assert capsys.readouterr().out == "called read_manifest with arg manifest.json\n"


def test_read_manifest(monkeypatch, capsys, tmp_path):
    """unittest for jsonconfig.read_manifest
    """
    def mock_load(*args):
        print('called json.load with args', args)
        return {}
    def mock_load_2(*args):
        print('called json.load with args', args)
        return {'Name': 'My Mod', 'Author': 'Me', 'Version': '1.0', 'Description': 'A Mod',
                'EntryDll': 'not used', 'UniqueID': 'Me.Mymod', 'MinimumApiVersion': '4.0.0',
                'deps': ['x'], 'UpdateKeys': ['xxx']}
    def mock_load_3(*args):
        print('called json.load with args', args)
        return {'dependencies': [], 'ContentPackFor': {}, 'UpdateKeys': ['Other:1234']}
    def mock_load_4(*args):
        print('called json.load with args', args)
        return {'Dependencies': ['x'], 'UpdateKeys': ['Nexus:99']}
    def mock_load_5(*args):
        print('called json.load with args', args)
        return {'ContentPackFor': {'UniqueID': 'y'}, 'UpdateKeys': ['Nexus:99']}
    def mock_load_6(*args):
        print('called json.load with args', args)
        return {'Dependencies': ['x', 'y'], 'ContentPackFor': {'UniqueID': 'y'},
                'UpdateKeys': ['Nexus:99']}
    def mock_load_7(*args):
        print('called json.load with args', args)
        return {'Dependencies': ['x', 'y'], 'ContentPackFor': {'UniqueID': 'z', 'required': True},
                'UpdateKeys': ['Nexus:99']}
    def mock_read(arg):
        print(f"called read_dependencies with arg {arg}")
        # return ['qqq']
        return arg  # ['qqq']
    path = tmp_path / 'testfile'
    path.touch()
    monkeypatch.setattr(testee.json5, 'load', mock_load)
    monkeypatch.setattr(testee, 'read_dependencies', mock_read)
    assert testee.read_manifest(path) == {}
    assert capsys.readouterr().out == (
            f"called json.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n")
    monkeypatch.setattr(testee.json5, 'load', mock_load_2)
    assert testee.read_manifest(path) == {'Author': 'Me', 'Description': 'A Mod',
                                          'MinimumApiVersion': '4.0.0', 'Name': 'My Mod',
                                          'UniqueID': 'Me.Mymod', 'Version': '1.0',
                                          'dirpath': path.parent}
    assert capsys.readouterr().out == (
            f"called json.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n")
    monkeypatch.setattr(testee.json5, 'load', mock_load_3)
    assert testee.read_manifest(path) == {'Deps': [], 'dirpath': path.parent}
    assert capsys.readouterr().out == (
            f"called json.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n"
            "called read_dependencies with arg []\n")
    # 92, 104-107, 129-140
    monkeypatch.setattr(testee.json5, 'load', mock_load_4)
    assert testee.read_manifest(path) == {'_Nexus': '99', 'Deps': ['x'], 'dirpath': path.parent}
    assert capsys.readouterr().out == (
            f"called json.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n"
            "called read_dependencies with arg ['x']\n")
    # 104-107, 129-140
    monkeypatch.setattr(testee.json5, 'load', mock_load_5)
    result = testee.read_manifest(path)
    assert result == {'_Nexus': '99', 'Deps': ['y'], 'dirpath': path.parent}
    assert capsys.readouterr().out == (
            f"called json.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n")
    # 104->103, 106->103, 129-140
    monkeypatch.setattr(testee.json5, 'load', mock_load_6)
    assert testee.read_manifest(path) == {'_Nexus': '99', 'Deps': ['x', 'y'], 'dirpath': path.parent}
    assert capsys.readouterr().out == (
            f"called json.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n"
            "called read_dependencies with arg ['x', 'y']\n")
    # 106-103, 129-140  -> 104-103
    monkeypatch.setattr(testee.json5, 'load', mock_load_7)
    # breakpoint()
    assert testee.read_manifest(path) == {'_Nexus': '99', 'Deps': ['x', 'y', 'z'],
                                          'dirpath': path.parent}
    assert capsys.readouterr().out == (
            f"called json.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n"
            "called read_dependencies with arg ['x', 'y']\n")


def test_read_dependencies():
    """unittest for jsonconfig.read_dependencies
    """
    deplist = [{'UniqueID': 'xxx'}, {'UniqueID': 'yyy', "IsRequired": False},
               {'UniqueID': 'zzz', "IsRequired": True}]
    assert testee.read_dependencies(deplist) == ['xxx', 'zzz']


def test_merge_old_info():
    """unittest for jsonconfig.merge_old_info
    """
    assert testee.merge_old_info({}, {'x': 'y'}) == {}
    assert testee.merge_old_info({'a': {'x': 'y'}}, {'b': {'x': 'z'}}) == {'a': {'x': 'y'}}
    assert testee.merge_old_info({
        'a': {}}, {'a': {'_ScreenName': 'y', '_Selectable': 'x', '_Nexus': 'q', '_ScreenPos': 'r',
                         '_ScreenText': 's'}}) == {'a': {'_ScreenName': 'y', '_Selectable': 'x',
                                                         '_Nexus': 'q', '_ScreenPos': 'r',
                                                         '_ScreenText': 's'}}
    assert testee.merge_old_info({
        'a': {'_ScreenName': '', '_Selectable': '', '_Nexus': '', '_ScreenPos': '',
              '_ScreenText': ''}}, {'a': {
                  '_ScreenName': 'y', '_Selectable': 'x', '_Nexus': 'q', '_ScreenPos': 'r',
                  '_ScreenText': 's'}}) == {'a': {'_ScreenName': 'y', '_Selectable': 'x',
                                                  '_Nexus': 'q', '_ScreenPos': 'r',
                                                  '_ScreenText': 's'}}
    assert testee.merge_old_info({
        'a': {'_ScreenName': 'y', '_Selectable': 'x', '_Nexus': 'q', '_ScreenPos': 'r',
              '_ScreenText': 's'}}, {'a': {
                  '_ScreenName': 'y', '_Selectable': 'x', '_Nexus': 'q', '_ScreenPos': 'r',
                  '_ScreenText': 's'}}) == {'a': {'_ScreenName': 'y', '_Selectable': 'x',
                                                  '_Nexus': 'q', '_ScreenPos': 'r',
                                                  '_ScreenText': 's'}}
    assert testee.merge_old_info({'a': {'x': 'y'}}, {'a': {'x': 'z'}}) == {'a': {'x': 'y'}}


def test_get_savenames(monkeypatch, tmp_path):
    "unittest for jsonconfig.get_savenames"
    monkeypatch.setattr(testee, 'read_defaults', lambda: ('', '', '', tmp_path))
    assert testee.get_savenames() == []
    (tmp_path / 'a-file').touch()
    (tmp_path / 'a-link').symlink_to(tmp_path / 'a-file')
    (tmp_path / 'a-directory').mkdir()
    (tmp_path / 'another-link').symlink_to(tmp_path / 'a-directory')
    (tmp_path / 'a-directory.backup').mkdir()
    assert testee.get_savenames() == ['a-directory']


def test_get_save_attrs(monkeypatch, tmp_path):
    "unittest for jsonconfig.get_save_attrs"
    monkeypatch.setattr(testee, 'read_defaults', lambda: ('', '', '', tmp_path))
    (tmp_path / 'xxxx').mkdir()
    assert testee.get_save_attrs('xxxx') == {}
    (tmp_path / 'xxxx' / 'yyyy').touch()
    assert testee.get_save_attrs('xxxx') == {}
    (tmp_path / 'xxxx' / 'xxxx').write_text('<SaveGame><player/><day>1</day></SaveGame>')
    assert testee.get_save_attrs('xxxx') == {'player/name': None, 'player/farmName': None,
                                             'dayOfMonth': None, 'currentSeason': None, 'year': None}
    (tmp_path / 'xxxx' / 'xxxx').write_text('<SaveGame><player><name>PName</name>'
                                            '<farmName>FName</farmName></player>'
                                            '<dayOfMonth>1</dayOfMonth>'
                                            '<currentSeason>2</currentSeason>'
                                            '<year>3</year></SaveGame>')
    assert testee.get_save_attrs('xxxx') == {'player/name': 'PName', 'player/farmName': 'FName',
                                             'dayOfMonth': '1', 'currentSeason': '2', 'year': '3'}


class TestJsonConf:
    """unittest for jsonconfig.JsonConf
    """
    def setup_testobj(self, filename, monkeypatch, capsys):
        """stub for jsonconfig.JsonConf object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called JsonConf.__init__ with args', args)
        monkeypatch.setattr(testee.JsonConf, '__init__', mock_init)
        testobj = testee.JsonConf(filename)
        assert capsys.readouterr().out == f'called JsonConf.__init__ with args ({filename!r},)\n'
        return testobj

    def test_init(self):
        """unittest for JsonConf.__init__
        """
        testobj = testee.JsonConf('filename')
        assert testobj.filename == 'filename'
        assert testobj.filepath == testee.pathlib.Path('filename')
        assert testobj._data == {}

    def test_load(self, monkeypatch, capsys, tmp_path):
        """unittest for JsonConf.load
        """
        def mock_load(*args):
            print('called json.load with args', args)
            return {'some': 'data'}
        def mock_open(*args):
            print('called path.open with args', args)
            return old_open(*args)
        monkeypatch.setattr(testee.json, 'load', mock_load)
        old_open = testee.pathlib.Path.open
        monkeypatch.setattr(testee.pathlib.Path, 'open', mock_open)
        filename = tmp_path / 'testfile'
        filename.touch()
        testobj = self.setup_testobj(filename, monkeypatch, capsys)
        testobj.filepath = filename
        testobj.load()
        assert testobj._data == {'some': 'data'}
        assert capsys.readouterr().out == (
                f"called path.open with args ({filename!r},)\n"
                f"called json.load with args (<_io.TextIOWrapper name='{filename}' mode='r'"
                " encoding='UTF-8'>,)\n")

    def test_save(self, monkeypatch, capsys, tmp_path):
        """unittest for JsonConf.save
        """
        def mock_dump(*args):
            print('called json.dump with args', args)
            return {'some': 'data'}
        def mock_open(*args):
            print('called path.open with args', args)
            return old_open(*args)
        def mock_copy(*args):
            print('called shutil.copyfile with args', args)
        monkeypatch.setattr(testee.json, 'dump', mock_dump)
        old_open = testee.pathlib.Path.open
        monkeypatch.setattr(testee.pathlib.Path, 'open', mock_open)
        filename = tmp_path / 'testfile'
        filename.touch()
        monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
        testobj = self.setup_testobj(filename, monkeypatch, capsys)
        testobj.filename = str(filename)
        testobj.filepath = filename
        testobj._data = {'some': 'data'}
        testobj.save()
        assert capsys.readouterr().out == (
                f"called shutil.copyfile with args ('{filename}', '{filename}~')\n"
                f"called path.open with args ({filename!r}, 'w')\n"
                "called json.dump with args ({'some': 'data'},"
                f" <_io.TextIOWrapper name='{filename}' mode='w' encoding='UTF-8'>)\n")

    def test_list_all_mod_dirs(self, monkeypatch, capsys):
        """unittest for JsonConf.list_all_mod_dirs
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'moddirs': {'xxx': {}, 'yyy': {}}}
        assert testobj.list_all_mod_dirs() == ['xxx', 'yyy']

    def test_list_all_components(self, monkeypatch, capsys):
        """unittest for JsonConf.list_all_components
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'components': {'xxx': {}, 'yyy': {}}}
        assert testobj.list_all_components() == ['xxx', 'yyy']

    def test_list_all_savenames(self, monkeypatch, capsys):
        """unittest for JsonConf.list_all_savenames
        """
        def mock_get():
            print('called get_savenames')
            return ['xxx']
        monkeypatch.setattr(testee, 'get_savenames', mock_get)
        testobj = self.setup_testobj('', monkeypatch, capsys)
        assert testobj.list_all_saveitems() == ['xxx']
        assert capsys.readouterr().out == "called get_savenames\n"

    def test_has_moddir(self, monkeypatch, capsys):
        """unittest for JsonConf.has_moddir
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'moddirs': {'xxx': {}, 'yyy': {}}}
        assert testobj.has_moddir('xxx')
        assert not testobj.has_moddir('zzz')

    def test_has_component(self, monkeypatch, capsys):
        """unittest for JsonConf.has_component
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'components': {'xxx': {}, 'yyy': {}}}
        assert testobj.has_component('xxx')
        assert not testobj.has_component('zzz')

    def test_list_components_for_dir(self, monkeypatch, capsys):
        """unittest for JsonConf.list_components_for_dir
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'moddirs': {'xxx': {'components': ['yyy', 'zzz']}}}
        assert testobj.list_components_for_dir('xxx') == ['yyy', 'zzz']
        with pytest.raises(ValueError) as exc:
            testobj.list_components_for_dir('qqq')
        assert str(exc.value) == 'mod directory qqq not found in config'

    def test_get_diritem_data(self, monkeypatch, capsys):
        """unittest for JsonConf.get_diritem_data
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj.knownmodkeys = ['aaa', 'q']
        testobj._data = {'moddirs': {'xxx': {'aaa': 'bbb', 'q': 'rrr'}, 'yyy': {'aaa': 'ccc'}}}
        with pytest.raises(ValueError) as exc:
            testobj.get_diritem_data('qqq')
        assert str(exc.value) == 'mod directory qqq not found in config'
        assert testobj.get_diritem_data('xxx') == {'aaa': 'bbb', 'q': 'rrr'}
        with pytest.raises(ValueError) as exc:
            assert testobj.get_diritem_data('xxx', 'qqq') == 'bbb'
        assert str(exc.value) == "Unknown key 'qqq' for directory xxx"
        assert testobj.get_diritem_data('xxx', 'aaa') == 'bbb'
        testobj.knownmodkeys = ['_Nexus', '_Selectable']
        assert testobj.get_diritem_data('xxx', '_Nexus') == 0
        assert not testobj.get_diritem_data('xxx', '_Selectable')
        testobj._data = {'moddirs': {'xxx': {'_Nexus': 1234, '_Selectable': True}}}
        assert testobj.get_diritem_data('xxx', '_Nexus') == 1234
        assert testobj.get_diritem_data('xxx', '_Selectable')

    def test_get_component_data(self, monkeypatch, capsys):
        """unittest for JsonConf.get_component_data
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj.knownkeys = ['qqq', 'r', 's']
        testobj._data = {'components': {'xxx': {'qqq': '...', 'r': 'rrr'}, 'yyy': {}}}
        with pytest.raises(ValueError) as exc:
            testobj.get_component_data('zzz')
        assert str(exc.value) == 'component zzz not found in config'
        assert testobj.get_component_data('xxx') == {'qqq': '...', 'r': 'rrr'}
        with pytest.raises(ValueError) as exc:
            assert testobj.get_component_data('xxx', 'ppp')
        assert str(exc.value) == "Unknown key 'ppp' for component xxx"
        assert testobj.get_component_data('xxx', 'qqq') == '...'
        assert testobj.get_component_data('xxx', 's') == ''

    def test_get_saveitem_attrs(self, monkeypatch, capsys):
        """unittest for JsonConf.get_saveitem_attrs
        """
        def mock_get(savename):
            print(f"called get_saveitem_attrs with arg '{savename}'")
            return {'player/name': 'xxx', 'player/farmName': 'yyy', 'dayOfMonth': '01',
                    'currentSeason': '02', 'year': '03'}
        monkeypatch.setattr(testee, 'get_save_attrs', mock_get)
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {}
        assert testobj.get_saveitem_attrs('xxx') == ('xxx', 'yyy Farm', '01 02 year 03')
        assert testobj._data == {'savedgames': {'xxx': {'player': 'xxx', 'farmName': 'yyy Farm',
                                                        'ingameDate': '01 02 year 03'}}}
        assert capsys.readouterr().out == "called get_saveitem_attrs with arg 'xxx'\n"
        testobj._data = {testobj.SAVES: {'yyy': 'zzz'}}
        assert testobj.get_saveitem_attrs('xxx') == ('xxx', 'yyy Farm', '01 02 year 03')
        assert testobj._data == {'savedgames': {'yyy': 'zzz',
                                                'xxx': {'player': 'xxx', 'farmName': 'yyy Farm',
                                                        'ingameDate': '01 02 year 03'}}}
        assert capsys.readouterr().out == "called get_saveitem_attrs with arg 'xxx'\n"
        testobj._data = {testobj.SAVES: {'xxx': {testobj.PNAME: 'qqq', testobj.FNAME: 'rrr',
                                                 testobj.GDATE: 'ss tt year uu'}}}
        assert testobj.get_saveitem_attrs('xxx') == ('qqq', 'rrr', 'ss tt year uu')
        assert testobj._data == {'savedgames': {'xxx': {'player': 'qqq', 'farmName': 'rrr',
                                                        'ingameDate': 'ss tt year uu'}}}
        assert capsys.readouterr().out == ""

    def test_get_mods_for_saveitem(self, monkeypatch, capsys):
        """unittest for JsonConf.get_mods_for_saveitem
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {}
        assert testobj.get_mods_for_saveitem('xxx') == []
        testobj._data = {testobj.SAVES: {'xxx': {testobj.MODS: ['qqq']}}}
        assert testobj.get_mods_for_saveitem('xxx') == ['qqq']

    def test_update_saveitem_data(self, monkeypatch, capsys):
        """unittest for JsonConf.update_saveitem_data
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        with pytest.raises(ValueError) as e:
            testobj.update_saveitem_data('xxxx', 'unknown', 'new value')
        assert str(e.value) == "Unknown key 'unknown' for savedata xxxx"
        testobj._data = {}
        testobj.update_saveitem_data('xxxx', testobj.PNAME, 'yyyy')
        assert testobj._data == {'savedgames': {'xxxx': {'player': 'yyyy'}}}
        testobj.update_saveitem_data('xxxx', testobj.FNAME, 'zzzz')
        assert testobj._data == {'savedgames': {'xxxx': {'player': 'yyyy', 'farmName': 'zzzz'}}}
        testobj.update_saveitem_data('xxxx', testobj.GDATE, 'qqqq')
        assert testobj._data == {'savedgames': {'xxxx': {'player': 'yyyy', 'farmName': 'zzzz',
                                                         'ingameDate': 'qqqq'}}}
        testobj.update_saveitem_data('xxxx', testobj.MODS, 'rrrr')
        assert testobj._data == {'savedgames': {'xxxx': {'player': 'yyyy', 'farmName': 'zzzz',
                                                         'ingameDate': 'qqqq', 'moddirs': 'rrrr'}}}

    def test_add_diritem(self, monkeypatch, capsys):
        """unittest for JsonConf.add_diritem
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'moddirs': {'xxx': {}, 'yyy': {}}}
        testobj.add_diritem('xxx')
        assert testobj._data['moddirs'] == {'xxx': {}, 'yyy': {}}
        testobj.add_diritem('zzz')
        assert testobj._data['moddirs'] == {'xxx': {}, 'yyy': {}, 'zzz': {}}

    def test_update_diritem(self, monkeypatch, capsys):
        """unittest for JsonConf.update_diritem
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'moddirs': {'xxx': {}, 'yyy': {}}}
        testobj.update_diritem('zzz', 'value')
        assert testobj._data['moddirs'] == {'xxx': {}, 'yyy': {}}
        testobj.update_diritem('xxx', 'value')
        assert testobj._data['moddirs']['xxx'] == 'value'

    def test_set_diritem_value(self, monkeypatch, capsys):
        """unittest for JsonConf.set_diritem_value
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'moddirs': {'xxx': {}, 'yyy': {'ppp': 'qqq'}}}
        testobj.knownmodkeys = ['aaa', 'ppp']
        testobj.set_diritem_value('zzz', 'key', 'value')
        assert testobj._data['moddirs'] == {'xxx': {}, 'yyy': {'ppp': 'qqq'}}
        with pytest.raises(ValueError) as exc:
            testobj.set_diritem_value('xxx', 'qqq', 'value')
        assert str(exc.value) == "Unknown key 'qqq' for directory xxx"
        testobj.set_diritem_value('xxx', 'ppp', 'value')
        assert testobj._data['moddirs']['xxx'] == {'ppp': 'value'}
        testobj.set_diritem_value('yyy', 'ppp', 'value')
        assert testobj._data['moddirs']['yyy'] == {'ppp': 'value'}

    def test_add_componentdata(self, monkeypatch, capsys):
        """unittest for JsonConf.add_componentdata
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'components': {'xxx': {}, 'yyy': {}}}
        testobj.add_componentdata('xxx')
        assert testobj._data['components'] == {'xxx': {}, 'yyy': {}}
        testobj.add_componentdata('zzz')
        assert testobj._data['components'] == {'xxx': {}, 'yyy': {}, 'zzz': {}}

    def test_update_componentdata(self, monkeypatch, capsys):
        """unittest for JsonConf.update_componentdata
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'components': {'xxx': {}, 'yyy': {}}}
        testobj.update_componentdata('zzz', 'value')
        assert testobj._data['components'] == {'xxx': {}, 'yyy': {}}
        testobj.update_componentdata('xxx', 'value')
        assert testobj._data['components']['xxx'] == 'value'

    def test_set_componentdata_value(self, monkeypatch, capsys):
        """unittest for JsonConf.set_componentdata_value
        """
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj._data = {'components': {'xxx': {}, 'yyy': {'ppp': 'qqq'}}}
        testobj.knownkeys = ['aaa', 'ppp']
        testobj.set_componentdata_value('zzz', 'key', 'value')
        assert testobj._data == {'components': {'xxx': {}, 'yyy': {'ppp': 'qqq'}}}
        with pytest.raises(ValueError) as exc:
            testobj.set_componentdata_value('xxx', 'qqq', 'value')
        assert str(exc.value) == "Unknown key 'qqq' for component xxx"
        testobj.set_componentdata_value('xxx', 'ppp', 'value')
        assert testobj._data['components']['xxx'] == {'ppp': 'value'}
        testobj.set_componentdata_value('yyy', 'ppp', 'value')
        assert testobj._data['components']['yyy'] == {'ppp': 'value'}

    def test_determine_nexuskey_for_mod(self, monkeypatch, capsys):
        """unittest for JsonConf.determine_nexuskey_for_mod
        """
        def mock_list(name):
            print(f'called JsonConf.list_components_for_dir with arg {name}')
            return []
        def mock_list_2(name):
            print(f'called JsonConf.list_components_for_dir with arg {name}')
            return ["hasid1234", "hasid1234@XX", "hasid", "hasid-1", "hasid???"]
        def mock_list_3(name):
            print(f'called JsonConf.list_components_for_dir with arg {name}')
            return ['hasid99', 'hasid100']
        def mock_get(*args):
            print('called JsonConf.get_component_data with args', args)
            return ''
        def mock_get_2(*args):
            print('called JsonConf.get_component_data with args', args)
            return args[0].removeprefix('hasid')
        def mock_set(*args):
            print('called JsonConf.set_diritem.value with args', args)
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj.list_components_for_dir = mock_list
        testobj.get_component_data = mock_get
        testobj.set_diritem_value = mock_set
        testobj.determine_nexuskey_for_mod('dirname')
        assert capsys.readouterr().out == (
                "called JsonConf.list_components_for_dir with arg dirname\n")
        testobj.list_components_for_dir = mock_list_2
        testobj.get_component_data = mock_get_2
        testobj.determine_nexuskey_for_mod('dirname')
        assert capsys.readouterr().out == (
                "called JsonConf.list_components_for_dir with arg dirname\n"
                "called JsonConf.get_component_data with args ('hasid1234', '_Nexus')\n"
                "called JsonConf.get_component_data with args ('hasid1234@XX', '_Nexus')\n"
                "called JsonConf.get_component_data with args ('hasid', '_Nexus')\n"
                "called JsonConf.get_component_data with args ('hasid-1', '_Nexus')\n"
                "called JsonConf.get_component_data with args ('hasid???', '_Nexus')\n"
                "called JsonConf.set_diritem.value with args ('dirname', '_Nexus', 1234)\n")
        testobj.list_components_for_dir = mock_list_3
        testobj.determine_nexuskey_for_mod('dirname')
        assert capsys.readouterr().out == (
                "called JsonConf.list_components_for_dir with arg dirname\n"
                "called JsonConf.get_component_data with args ('hasid99', '_Nexus')\n"
                "called JsonConf.get_component_data with args ('hasid100', '_Nexus')\n"
                "called JsonConf.set_diritem.value with args ('dirname', '_Nexus', 99)\n")
