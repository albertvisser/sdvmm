"""unittests for ./src/jsonconfig.py
"""
import pytest
from src import jsonconfig as testee


def test_rebuild_all(monkeypatch, capsys):
    """unittest for jsonconfig.rebuild_all
    """
    def mock_build(path):
        print(f"called build_entry_from_dir with arg {path}")
        return {'x': {'y': 'yyy', 'z': 'zzz'}, 'x': {'b': 'bbb', 'c': 'ccc'}}
    def mock_build_2(path):
        print(f"called build_entry_from_dir with arg {path}")
        return {'x': {'y': 'yyy', 'z': 'zzz'}}
    def mock_build_3(path):
        print(f"called build_entry_from_dir with arg {path}")
        return {'x': {'y': 'yyy', 'z': 'zzz'}, 'a': {'b': 'bbb', 'c': 'ccc'}}
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
    # dit kan eigenlijk niet: dubbele componenten in één uitpakdirectory
    assert testee.rebuild_all(startdirs) == ({'moddirs': {'dirname': {'components': ['x']}},
                                              'components': {'x': {'b': 'bbb', 'c': 'ccc'}}}, [])
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

    monkeypatch.setattr(testee, 'build_entry_from_dir', mock_build_3)
    startdirs = [testee.pathlib.Path('dirname')]
    assert testee.rebuild_all(startdirs) == ({'moddirs': {'dirname': {'components': ['x', 'a']}},
                                              'components': {'a': {'b': 'bbb', 'c': 'ccc'},
                                                             'x': {'y': 'yyy', 'z': 'zzz'}}}, [])
    assert capsys.readouterr().out == ("called path.isdir with arg dirname\n"
                                       "called build_entry_from_dir with arg dirname\n")


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
    # {
    #     "Name": "Hover Labels",
    #     "Author": "Achtuur",
    #     "Version": "2.1.1",
    #     "Description": "Adds labels to things when you hover over them",
    #     "UniqueID": "Achtuur.HoverLabels",
    #     "EntryDll": "HoverLabels.dll",
    #     "MinimumApiVersion": "4.0.0",
    #     "dependencies": [
    #         {
    #             "UniqueID": "Achtuur.AchtuurCore",
    #             "MinimumVersion": "1.3.0"
    #         }
    #     ],
    #     "UpdateKeys": [ "Nexus:17501" ]
    # }
    def mock_load(*args):
        print('called json5.load with args', args)
        return {}
    def mock_load_2(*args):
        print('called json5.load with args', args)
        return {'Name': 'My Mod', 'Author': 'Me', 'Version': '1.0', 'Description': 'A Mod',
                'EntryDll': 'not used', 'UniqueID': 'Me.Mymod', 'MinimumApiVersion': '4.0.0',
                'deps': ['x'], 'UpdateKeys': ['xxx']}
    def mock_load_3(*args):
        print('called json5.load with args', args)
        return {'dependencies': [], 'UpdateKeys': ['Other:1234']}
    def mock_load_4(*args):
        print('called json5.load with args', args)
        return {'Dependencies': ['x'], 'UpdateKeys': ['Nexus:99']}
    def mock_read(arg):
        print(f"called read_dependencies with arg {arg}")
        return ['qqq'], True
    def mock_read_2(arg):
        print(f"called read_dependencies with arg {arg}")
        return ['aaa', 'bbb'], False
    path = tmp_path / 'testfile'
    path.touch()
    monkeypatch.setattr(testee.json5, 'load', mock_load)
    monkeypatch.setattr(testee, 'read_dependencies', mock_read)
    assert testee.read_manifest(path) == {}
    assert capsys.readouterr().out == (
            f"called json5.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n")
    monkeypatch.setattr(testee.json5, 'load', mock_load_2)
    assert testee.read_manifest(path) == {'Author': 'Me', 'Description': 'A Mod',
                                          'MinimumApiVersion': '4.0.0', 'Name': 'My Mod',
                                          'UniqueID': 'Me.Mymod', 'Version': '1.0',
                                          'dirpath': path.parent}
    assert capsys.readouterr().out == (
            f"called json5.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n")
    monkeypatch.setattr(testee.json5, 'load', mock_load_3)
    monkeypatch.setattr(testee, 'read_dependencies', mock_read_2)
    assert testee.read_manifest(path) == {'Deps': ['aaa', 'bbb'], 'dirpath': path.parent}
    assert capsys.readouterr().out == (
            f"called json5.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n"
            "called read_dependencies with arg []\n")
    monkeypatch.setattr(testee.json5, 'load', mock_load_4)
    monkeypatch.setattr(testee, 'read_dependencies', mock_read)
    assert testee.read_manifest(path) == {'_Nexus': '99', 'Deps': ['qqq'],
                                          'dirpath': path.parent}
    assert capsys.readouterr().out == (
            f"called json5.load with args (<_io.BufferedReader name='{tmp_path}/testfile'>,)\n"
            "called read_dependencies with arg ['x']\n"
            f"Geen 'IsRequired' key gevonden voor dep(s) in bestand {tmp_path}/testfile\n")


def test_read_dependencies():
    """unittest for jsonconfig.read_dependencies
    """
    #     "dependencies": [
    #         {
    #             "UniqueID": "Achtuur.AchtuurCore",
    #             "MinimumVersion": "1.3.0"
    #         }
    #     ],
    deplist = [{'UniqueID': 'xxx'}, {'UniqueID': 'yyy', "IsRequired": False},
               {'UniqueID': 'zzz', "IsRequired": True}]
    assert testee.read_dependencies(deplist) == (['xxx', 'zzz'], False)


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
        assert testobj.list_all_components() ==  ['xxx', 'yyy']

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
        # 211-223
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
                # "called JsonConf.set_diritem.value with args ('dirname', '_Nexus2', [100])\n")

    def test_mergecomponents(self, monkeypatch, capsys):
        """unittest for JsonConf.mergecomponents
        """
        def mock_get(*args):
            print('called JsonConf.get_diritem.data with args', args)
            return ['xxx', 'yyy']
        def mock_set(*args):
            print('called JsonConf.set_diritem.value with args', args)
        testobj = self.setup_testobj('', monkeypatch, capsys)
        testobj.get_diritem_data = mock_get
        testobj.set_diritem_value = mock_set
        testobj.mergecomponents('title', 'dirname')
        assert capsys.readouterr().out == (
                "called JsonConf.get_diritem.data with args ('dirname', 'components')\n"
                "called JsonConf.set_diritem.value with args"
                " ('dirname', 'components', ['xxx', 'yyy'])\n")
        testobj._data = {'moddirs': {'dirname2': {'components': ['aaa', 'bbb']}}}
        testobj.mergecomponents('title', 'dirname1, dirname2')
        assert testobj._data == {'moddirs': {}}
        assert capsys.readouterr().out == (
                "called JsonConf.get_diritem.data with args ('dirname1', 'components')\n"
                "called JsonConf.set_diritem.value with args"
                " ('dirname1', 'components', ['xxx', 'yyy', 'aaa', 'bbb'])\n")
