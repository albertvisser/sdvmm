"""unittests for ./src/manager.py
"""
import types
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

    def select_activations(self, *args):
        "stub"
        print('called Manager.select_activations with args', args)

    def activate(self):
        "stub"
        print('called Manager.activate with args')

    def refresh_widget_data(self):
        "stub"
        print('called Manager.refresh_widget_data')


class MockConf:
    """testdouble for jsonconfig.JsonConf object
    object mimicking configparser.ConfigParser class
    """
    SCRNAM, NAME, DEPS, COMPS, VRS = 'SCRNAM', 'Name', 'Deps', 'Comps', 'Version'
    PNAME, FNAME, GDATE, MODS, NXSKEY = 'Pname', 'Fname', 'Gdate', 'Mods', '_NexusKey'
    OPTOUT, DIR, SEL, SCRPOS, SCRTXT = '_DoNotTouch', 'dirname', 'Sel', 'ScrPos', 'ScrTxt'

    # SCRNAM, SEL, SCRPOS, NXSKEY, SCRTXT, DIR, DEPS, COMPS, NAME, VRS = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    # OPTOUT = 10
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
    def list_all_saveitems(self):
        "stub"
        print('called Conf.list_all_mod_savetemitems')
        return ['qqq', 'rrr']
    def list_all_mod_dirs(self):
        "stub"
        print("called Conf.list_all_mod_dirs")
        return ['xxx', 'yyy']
    def list_components_for_dir(self, name):
        "stub"
        print(f"called Conf.list_components_for_dir with arg '{name}'")
        return ['xxx', 'yyy']
    def get_diritem_data(self, *args):
        "stub"
        print("called Conf.get_diritem_data with args", args)
        return f'{args[0]}_name'
    def get_component_data(self, *args):
        "stub"
        print("called Conf.get_component_data with args", args)
        if args[1] == self.NAME:
            return f'{args[0]}_compname'
        if args[1] == self.DEPS:
            return [f'{args[0]}_depname']
        if args[1] == self.VRS:
            return f'{args[0]}_version'
        return f'{args[0]}_name'
    def get_saveitem_attrs(self, value):
        "stub"
        print(f"called Conf.get_saveitem_attrs with arg {value}")
        return [], False
    def get_mods_for_saveitem(self, name):
        "stub"
        print(f"called Conf.get_mods_for_saveitem with arg {name}")
        return []
    def update_saveitem_data(self, *args):
        "stub"
        print('called Conf.update_saveitem_data with args', args)
    def set_componentdata_value(self, *args):
        "stub"
        print('called Conf.set_componenentdata_value with args', args)
    def remove_componentdata(self, name):
        "stub"
        print(f"called Conf.remove_component with arg '{name}'")
    def remove_diritem(self, name):
        "stub"
        print(f"called Conf.remove_diritem with arg '{name}'")


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
    def create_selectables_title(self, text):
        """stub
        """
        print('called gui.create_selectables_title with arg', text)
    def create_selectables_grid(self):
        """stub
        """
        print('called gui.create_selectables_grid')
    def create_dependencies_title(self, text):
        """stub
        """
        print('called gui.create_dependencies_title with arg', text)
    def create_dependencies_grid(self):
        """stub
        """
        print('called gui.create_dependencies_grid')
    def create_buttons(self, buttondict):
        """stub
        """
        print('called gui.create_buttons with arg', buttondict)
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
    def update_mods(self):
        "callback"
    def remove_mods(self):
        "callback"
    def confirm(self):
        "callback"
    def close(self):
        "callback"


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
            "Config was (re)built with the following messages:\n"
            "xxx\n"
            "yyy\n\n"
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
        monkeypatch.setattr(testee.dmlj, 'JsonConf', MockConf)
        monkeypatch.setattr(testee, 'CONFIG', '')
        testobj = testee.Manager()
        assert capsys.readouterr().out == "called JsonConf.__init__ with args ('',) {}\n"
        assert testobj.modnames == []
        assert testobj.modbase == testee.MODBASE
        assert testobj.downloads == testee.DOWNLOAD
        assert testobj.directories == set()
        assert testobj.screeninfo == {}
        monkeypatch.setattr(testee, 'CONFIG', 'configname')
        testobj = testee.Manager()
        assert capsys.readouterr().out == ("called JsonConf.__init__ with args ('configname',) {}\n"
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
        testobj.SEL_TITLE = 'xxxxx'
        testobj.DEP_TITLE = 'yyyyy'
        testobj.BUTTON_LIST = [{}, {}, {}, {}, {}, {}, {}]
        testobj.extract_screeninfo = mock_extract
        testobj.modnames = []
        testobj.build_and_start_gui()
        assert testobj.modnames == ['one', 'two', 'three']
        assert capsys.readouterr().out == (
                'called Manager.extract_screen_locations\n'
                f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
                # 'called gui.ShowMods.setup_screen()\n'
                "called gui.create_selectables_title with arg xxxxx\n"
                "called gui.create_selectables_grid\n"
                "called gui.create_dependencies_title with arg yyyyy\n"
                "called gui.create_dependencies_grid\n"
                f"called gui.create_buttons with arg [{{'callback': {testobj.manage_defaults}}},"
                f" {{'callback': {testobj.doit.update_mods}}},"
                f" {{'callback': {testobj.manage_deletions}}},"
                f" {{'callback': {testobj.manage_attributes}}},"
                f" {{'callback': {testobj.doit.confirm}}},"
                f" {{'callback': {testobj.manage_savefiles}}},"
                f" {{'callback': {testobj.doit.close}}}]\n"
                "called gui.ShowMods.refresh_widgets with args {'first_time': True}\n"
                'called gui.ShowMods.setup_actions()\n'
                'called gui.ShowMods.show_screen()\n')

    def test_extract_screeninfo(self, monkeypatch, capsys):
        """unittest for Manager.extract_screen_locations
        """
        def mock_list():
            print('called Conf.list_all_mod_dirs')
            return []
        def mock_list_2():
            print('called Conf.list_all_mod_dirs')
            return ['xxx', 'yyy']
        def mock_get(name, itemtype):
            print(f"called Conf.get_diritem_data with args ('{name}', '{itemtype}')")
            if itemtype == testobj.conf.COMPS:
                return ['']
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
            if itemtype == testobj.conf.OPTOUT:
                return 'optout'
            if itemtype == testobj.conf.COMPS:
                return ['comps']
            return 'sel'
        def mock_gett(name):
            print(f"called get_toplevel with arg '{name}'")
            return name
        def mock_getc(name, itemtype):
            print(f"called Conf.get_component_data with args ('{name}', '{itemtype}')")
            return ''
        def mock_getc_2(name, itemtype):
            print(f"called Conf.get_component_data with args ('{name}', '{itemtype}')")
            return name

        monkeypatch.setattr(testee, 'get_toplevel', mock_gett)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf.list_all_mod_dirs = mock_list
        testobj.conf.get_diritem_data = mock_get
        testobj.conf.get_component_data = mock_getc
        testobj.screeninfo = {'yyy': {'sel': 's', 'pos': 'p', 'key': 'k', 'txt': 't', 'opt': 'o'}}

        monkeypatch.setattr(testee, 'CONFIG', '')
        testobj.extract_screeninfo()
        assert capsys.readouterr().out == ""
        monkeypatch.setattr(testee, 'CONFIG', 'asdf')
        testobj.extract_screeninfo()
        assert testobj.screeninfo == {'yyy': {'sel': 's', 'pos': 'p', 'key': 'k', 'txt': 't',
                                              'opt': 'o'}}
        assert capsys.readouterr().out == "called Conf.list_all_mod_dirs\n"

        testobj.conf.list_all_mod_dirs = mock_list_2
        testobj.screeninfo = {}
        testobj.extract_screeninfo()
        assert testobj.screeninfo == {
                'xxx': {'dir': '', 'sel': False, 'pos': '', 'key': '', 'txt': '', 'opt': False},
                # 'yyy': {'dir': '', 'sel': 's', 'pos': 'p', 'key': 'k', 'txt': 't', 'opt': 'o'},
                'yyy': {'dir': '', 'sel': False, 'pos': '', 'key': '', 'txt': '', 'opt': False}}
        assert capsys.readouterr().out == (
                "called Conf.list_all_mod_dirs\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRNAM}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.COMPS}')\n"
                f"called Conf.get_component_data with args ('', '{testobj.conf.DIR}')\n"
                f"called get_toplevel with arg ''\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SEL}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.OPTOUT}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRPOS}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.NXSKEY}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRTXT}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRNAM}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.COMPS}')\n"
                f"called Conf.get_component_data with args ('', '{testobj.conf.DIR}')\n"
                f"called get_toplevel with arg ''\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SEL}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.OPTOUT}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRPOS}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.NXSKEY}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRTXT}')\n")

        testobj.conf.get_diritem_data = mock_get_2
        testobj.screeninfo = {}
        testobj.extract_screeninfo()
        assert testobj.screeninfo == {'scrxxx': {'dir': '', 'sel': 'sel', 'pos': 'scrpos',
                                                 'key': 'scrkey', 'txt': 'scrtxt', 'opt': 'optout'},
                                      'scryyy': {'dir': '', 'sel': 'sel', 'pos': 'scrpos',
                                                 'key': 'scrkey', 'txt': 'scrtxt', 'opt': 'optout'}}
        assert capsys.readouterr().out == (
                "called Conf.list_all_mod_dirs\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRNAM}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.COMPS}')\n"
                f"called Conf.get_component_data with args ('comps', '{testobj.conf.DIR}')\n"
                f"called get_toplevel with arg ''\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SEL}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.OPTOUT}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRPOS}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.NXSKEY}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRTXT}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRNAM}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.COMPS}')\n"
                f"called Conf.get_component_data with args ('comps', '{testobj.conf.DIR}')\n"
                f"called get_toplevel with arg ''\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SEL}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.OPTOUT}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRPOS}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.NXSKEY}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRTXT}')\n")

        testobj.conf.get_component_data = mock_getc_2
        testobj.extract_screeninfo()
        assert testobj.screeninfo == {
                'scryyy': {'dir': 'comps', 'sel': 'sel', 'pos': 'scrpos', 'key': 'scrkey',
                        'txt': 'scrtxt', 'opt': 'optout'},
                'scrxxx': {'dir': 'comps', 'sel': 'sel', 'pos': 'scrpos', 'key': 'scrkey',
                        'txt': 'scrtxt', 'opt': 'optout'}}
        assert capsys.readouterr().out == (
                "called Conf.list_all_mod_dirs\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRNAM}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.COMPS}')\n"
                f"called Conf.get_component_data with args ('comps', '{testobj.conf.DIR}')\n"
                f"called get_toplevel with arg 'comps'\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SEL}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.OPTOUT}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRPOS}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.NXSKEY}')\n"
                f"called Conf.get_diritem_data with args ('xxx', '{testobj.conf.SCRTXT}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRNAM}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.COMPS}')\n"
                f"called Conf.get_component_data with args ('comps', '{testobj.conf.DIR}')\n"
                f"called get_toplevel with arg 'comps'\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SEL}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.OPTOUT}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRPOS}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.NXSKEY}')\n"
                f"called Conf.get_diritem_data with args ('yyy', '{testobj.conf.SCRTXT}')\n")

    def test_order_widgets(self, monkeypatch, capsys):
        """unittest for ShowMods.order_widgets
        """
        def mock_remove(*args):
            print('called ShowMods.remove_widgets with args', args)
        def mock_add(*args):
            print('called ShowMods.add_items_to_grid with args', args)
            if args[0] == ['selectables']:
                return {('p', 'q'): 'rrr'}, {('s', 't'): 'uvw'}
            return {('x', 'y'): 'zzz'}, {('a', 'b'): 'ccc'}
        def mock_refresh(**kwargs):
            print('called Manager.refresh_widget_data with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = types.SimpleNamespace(remove_widgets=mock_remove)
        testobj.add_items_to_grid = mock_add
        testobj.refresh_widget_data = mock_refresh
        testobj.unplotted = []
        testobj.unplotted_widgets = {}
        testobj.unplotted_positions = {}
        testobj.not_selectable = []
        testobj.nonsel_widgets = {}
        testobj.nonsel_positions = {}
        testobj.screeninfo = {'abc': {'sel': True}, 'def': {'sel': False}}
        testobj.order_widgets(['selectables'], ['dependencies'], True)
        assert testobj.unplotted == ['abc']
        assert testobj.unplotted_widgets == {('s', 't'): 'uvw'}
        assert testobj.unplotted_positions == {('p', 'q'): 'rrr'}
        assert testobj.not_selectable == ['def']
        assert testobj.nonsel_widgets == {('a', 'b'): 'ccc'}
        assert testobj.nonsel_positions == {('x', 'y'): 'zzz'}
        assert capsys.readouterr().out == (
                "called ShowMods.add_items_to_grid with args (['selectables'], ['abc'])\n"
                "called ShowMods.add_items_to_grid with args (['dependencies'], ['def'])\n"
                "called Manager.refresh_widget_data with args {'texts_also': True}\n")
        testobj.order_widgets(['selectables'], ['dependencies'], False)
        assert testobj.unplotted == ['abc']
        assert testobj.unplotted_widgets == {('s', 't'): 'uvw'}
        assert testobj.unplotted_positions == {('p', 'q'): 'rrr'}
        assert testobj.not_selectable == ['def']
        assert testobj.nonsel_widgets == {('a', 'b'): 'ccc'}
        assert testobj.nonsel_positions == {('x', 'y'): 'zzz'}
        assert capsys.readouterr().out == (
                "called ShowMods.remove_widgets with args ('uvw', ['selectables'], 's', 't')\n"
                "called ShowMods.remove_widgets with args ('ccc', ['dependencies'], 'a', 'b')\n"
                "called ShowMods.add_items_to_grid with args (['selectables'], ['abc'])\n"
                "called ShowMods.add_items_to_grid with args (['dependencies'], ['def'])\n"
                "called Manager.refresh_widget_data with args {'texts_also': True}\n")

    def test_add_items_to_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.add_items_to_grid
        """
        def mock_add(*args):
            print("called ShowMods.add_checkbox")
            return 'hbox', 'btn', 'cbox'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = types.SimpleNamespace(add_checkbox=mock_add)
        testobj.maxcol = 3
        testobj.screeninfo = {'x': {'sel': True}, 'y': {'sel': True}, 'z': {'sel': False},
                              'q': {'sel': False}}
        assert testobj.add_items_to_grid('grid', []) == ({}, {})
        assert capsys.readouterr().out == ""
        assert testobj.add_items_to_grid('grid', ['x', 'y', 'z', 'q']) == (
                {(0, 0): ('q', {'sel': False, 'pos': '0x0'}),
                 (0, 1): ('x', {'sel': True, 'pos': '0x1'}),
                 (0, 2): ('y', {'sel': True, 'pos': '0x2'}),
                 (1, 0): ('z', {'sel': False, 'pos': '1x0'})},
                {(0, 0): ('hbox', 'btn', 'cbox'),
                 (0, 1): ('hbox', 'btn', 'cbox'),
                 (0, 2): ('hbox', 'btn', 'cbox'),
                 (1, 0): ('hbox', 'btn', 'cbox')})
        assert capsys.readouterr().out == ("called ShowMods.add_checkbox\n"
                                           "called ShowMods.add_checkbox\n"
                                           "called ShowMods.add_checkbox\n"
                                           "called ShowMods.add_checkbox\n")

    def test_refresh_widget_data(self, monkeypatch, capsys):
        """unittest for ShowMods.refresh_widgets
        """
        def mock_set1(*args):
            print("called Showmods.set_texts_for_grid with args", args)
        def mock_set2(*args):
            print("called Showmods.set_checks_for_grid with args", args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = types.SimpleNamespace()
        testobj.set_texts_for_grid = mock_set1
        testobj.set_checks_for_grid = mock_set2
        # testobj.plotted_widgets = {'x': '1', 'y': '2'}
        # testobj.plotted_positions = {'a': 1, 'b': 2}
        testobj.unplotted_widgets = {'x': '3', 'z': '4'}
        testobj.unplotted_positions = {'a': 3, 'c': 4}
        testobj.nonsel_widgets = {'q': 'r'}
        testobj.nonsel_positions = {'p': 's'}
        testobj.refresh_widget_data()
        assert capsys.readouterr().out == (
                "called Showmods.set_checks_for_grid with args"
                " ({'a': 3, 'c': 4}, {'x': '3', 'z': '4'})\n"
                "called Showmods.set_checks_for_grid with args ({'p': 's'}, {'q': 'r'})\n")
        testobj.refresh_widget_data(texts_also=True)
        assert capsys.readouterr().out == (
                "called Showmods.set_texts_for_grid with args"
                " ({'a': 3, 'c': 4}, {'x': '3', 'z': '4'})\n"
                "called Showmods.set_texts_for_grid with args ({'p': 's'}, {'q': 'r'})\n"
                "called Showmods.set_checks_for_grid with args"
                " ({'a': 3, 'c': 4}, {'x': '3', 'z': '4'})\n"
                "called Showmods.set_checks_for_grid with args ({'p': 's'}, {'q': 'r'})\n")

    def test_set_texts_for_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.set_texts_for_grid
        """
        def mock_set(*args):
            print('called ShowMods.set_label_text with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = types.SimpleNamespace(set_label_text=mock_set)
        widgets = {}
        positions = {}
        testobj.set_texts_for_grid(positions, widgets)
        assert capsys.readouterr().out == ""
        widgets = {(0, 1): ('', 'label1', ''), (1, 1): ('', 'label2', '')}
        positions = {(0, 1): ('aaa', {'txt': '', 'key': ''}),
                     (1, 1): ('bbb', {'txt': 'xxx', 'key': 'yyy'})}
        testobj.set_texts_for_grid(positions, widgets)
        assert capsys.readouterr().out == (
                "called ShowMods.set_label_text with args (('', 'label1', ''),"
                " 'aaa', '', '')\n"
                "called ShowMods.set_label_text with args (('', 'label2', ''),"
                " 'bbb', 'yyy', 'xxx')\n")

    def test_build_link_text(self, monkeypatch, capsys):
        """unittest for ShowMods.build_link_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_link_text('xxx', 'zz') == (
                '<a href=\"https://www.nexusmods.com/stardewvalley/mods/zz\">xxx</a>')

    def test_set_checks_for_grid(self, monkeypatch, capsys, tmp_path):
        """unittest for ShowMods.set_checks_for_grid
        """
        def mock_set(*args):
            print('called ShowMods.set_checkbox_state with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = types.SimpleNamespace(set_checkbox_state=mock_set)
        monkeypatch.setattr(testobj, 'modbase', tmp_path)
        (tmp_path / 'xxx').mkdir()
        testobj.enable_button = lambda x: 'dummy'
        widgets = {}
        positions = {}
        testobj.set_checks_for_grid(positions, widgets)
        assert capsys.readouterr().out == ""
        widgets = {(0, 1): ('', '', 'check1'), (1, 1): ('', '', 'check2'), (1, 2): ('', '', 'check3')}
        positions = {(0, 1): ('aaa', {'dir': 'qqq', 'sel': True}),
                     (1, 1): ('bbb', {'dir': 'xxx', 'sel': True}),
                     (1, 2): ('ccc', {'dir': 'rrr', 'sel': False})}
        testobj.set_checks_for_grid(positions, widgets)
        assert capsys.readouterr().out == (
                "called ShowMods.set_checkbox_state with args (('', '', 'check1'), False)\n"
                "called ShowMods.set_checkbox_state with args (('', '', 'check2'), True)\n"
                "called ShowMods.set_checkbox_state with args (('', '', 'check3'), False)\n")

    def test_process_activations(self, monkeypatch, capsys):
        """unittest for Manager.process_activations
        """
        def mock_get(arg):
            """stub
            """
            print('called ShowMods.get_labeltext_if_checked with arg', arg)
            return ''
        def mock_get_2(arg):
            """stub
            """
            print('called ShowMods.get_labeltext_if_checked with arg', arg)
            return 'labeltext'
        def mock_select(self, arg):
            """stub
            """
            print('called Manager.select_activations with arg', arg)
            self.directories = []
        def mock_select_2(self, names):
            """stub
            """
            print(f'called Manager.select_activations with arg {names}')
            self.directories = ['x']
        def mock_activate():
            """stub
            """
            print('called Manager.activate')
        def mock_refresh(**kwargs):
            """stub
            """
            print('called Manager.refresh_widget_data')
        monkeypatch.setattr(testee.Manager, 'select_activations', mock_select)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = types.SimpleNamespace(get_labeltext_if_checked=mock_get)
        testobj.activate = mock_activate
        testobj.refresh_widget_data = mock_refresh
        testobj.unplotted_widgets = {'x': ['widget', 'list']}
        testobj.process_activations()
        assert testobj.directories == []
        assert capsys.readouterr().out == (
                "called ShowMods.get_labeltext_if_checked with arg ['widget', 'list']\n"
                "called Manager.select_activations with arg []\n"
                "called Manager.refresh_widget_data\n")
        testobj.doit.get_labeltext_if_checked = mock_get_2
        testobj.process_activations()
        assert testobj.directories == []
        assert capsys.readouterr().out == (
                "called ShowMods.get_labeltext_if_checked with arg ['widget', 'list']\n"
                "called Manager.select_activations with arg ['labeltext']\n"
                "called Manager.refresh_widget_data\n")
        monkeypatch.setattr(testee.Manager, 'select_activations', mock_select_2)
        testobj.process_activations()
        assert testobj.directories == ['x']
        assert capsys.readouterr().out == (
                "called ShowMods.get_labeltext_if_checked with arg ['widget', 'list']\n"
                "called Manager.select_activations with arg ['labeltext']\n"
                "called Manager.activate\n"
                "called Manager.refresh_widget_data\n")

    def test_select_activations(self, monkeypatch, capsys):
        """unittest for Manager.select_activations
        """
        def mock_list(name):
            print(f'called Conf.list_components_for_dir with arg {name}')
            return []
        def mock_list_2(name):
            print(f'called Conf.list_components_for_dir with arg {name}')
            return [name]
        def mock_add(name):
            """stub
            """
            print(f'called Conf.add_dependencies with arg {name}')
        def mock_get(name, itemtype):
            print(f"called Conf.get_component_data with args ('{name}', '{itemtype}')")
            return name
        def mock_gett(name):
            print(f"called get_toplevel with arg '{name}'")
            return name
        monkeypatch.setattr(testee, 'get_toplevel', mock_gett)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_dependencies = mock_add
        testobj.conf.get_component_data = mock_get
        testobj.select_activations([])
        assert testobj.directories == set()
        assert capsys.readouterr().out == ""

        testobj.conf.list_components_for_dir = mock_list
        testobj.screeninfo = {'test': {'dir': 'xxx'}, 'other': {'dir': 'yyy'}}
        testobj.select_activations(['test', 'other'])
        assert testobj.directories == set()
        assert capsys.readouterr().out == ("called Conf.list_components_for_dir with arg xxx\n"
                                           "called Conf.list_components_for_dir with arg yyy\n")

        testobj.conf.list_components_for_dir = mock_list_2
        testobj.screeninfo = {'test': {'dir': 'xxx'}, 'other': {'dir': 'yyy'}}
        testobj.select_activations(['test', 'other'])
        assert testobj.directories == {'xxx', 'yyy'}
        assert capsys.readouterr().out == (
                "called Conf.list_components_for_dir with arg xxx\n"
                f"called Conf.get_component_data with args ('xxx', '{testobj.conf.DIR}')\n"
                "called get_toplevel with arg 'xxx'\n"
                "called Conf.add_dependencies with arg xxx\n"
                "called Conf.list_components_for_dir with arg yyy\n"
                f"called Conf.get_component_data with args ('yyy', '{testobj.conf.DIR}')\n"
                "called get_toplevel with arg 'yyy'\n"
                "called Conf.add_dependencies with arg yyy\n")

    def test_add_dependencies(self, monkeypatch, capsys):
        """unittest for Manager.add_dependencies
        """
        # def mock_list(name):
        #     "stub"
        #     print(f'called Conf.list_components_for_dir with arg {name}')
        #     if name == 'moddir':
        #         return ['w', 'x', 'y', 'x', 'z']
        #     return []
        # def mock_list_2(name):
        #     "stub"
        #     print(f'called Conf.list_comonents_for_dir with arg {name}')
        #     raise ValueError
        def mock_get(name, itemtype):
            print(f"called Conf.get_component_data with args('{name}', '{itemtype}')")
            if itemtype == testobj.conf.DIR:
                if name == 'r':
                    return f'{name}parent/{name}dir'
                return f'{name}dir'
            if itemtype == testobj.conf.DEPS:
                if name in ('w', 'x'):
                    return [f'{name}q']
                if name == 'comp.name':
                    return ['w', 'x']
                return []
            return ''
        def mock_gett(name):
            print(f"called get_toplevel with arg '{name}'")
            return name
        monkeypatch.setattr(testee, 'get_toplevel', mock_gett)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf.get_component_data = mock_get
        testobj.components_checked = []
        testobj.directories = set()
        testobj.add_dependencies('comp.name')
        assert testobj.directories == {'wdir', 'wqdir', 'xdir', 'xqdir'}
        assert capsys.readouterr().out == (
                f"called Conf.get_component_data with args('comp.name', '{testobj.conf.DEPS}')\n"
                f"called Conf.get_component_data with args('w', '{testobj.conf.DIR}')\n"
                "called get_toplevel with arg 'wdir'\n"
                f"called Conf.get_component_data with args('w', '{testobj.conf.DEPS}')\n"
                f"called Conf.get_component_data with args('wq', '{testobj.conf.DIR}')\n"
                "called get_toplevel with arg 'wqdir'\n"
                f"called Conf.get_component_data with args('wq', '{testobj.conf.DEPS}')\n"
                f"called Conf.get_component_data with args('x', '{testobj.conf.DIR}')\n"
                "called get_toplevel with arg 'xdir'\n"
                f"called Conf.get_component_data with args('x', '{testobj.conf.DEPS}')\n"
                f"called Conf.get_component_data with args('xq', '{testobj.conf.DIR}')\n"
                "called get_toplevel with arg 'xqdir'\n"
                f"called Conf.get_component_data with args('xq', '{testobj.conf.DEPS}')\n")

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
        assert capsys.readouterr().out == ("called os.rename with args (<DirEntry 'dirname4'>,"
                                           f" '{testobj.modbase}/.dirname4')\n"
                                           "called os.rename with args (<DirEntry '.dirname3'>,"
                                           f" '{testobj.modbase}/dirname3')\n")

    def test_manage_attributes(self, monkeypatch, capsys):
        """unittest for Manager.manage_attributes
        """
        def mock_show(*args):
            print('called show_dialog with args', args[0].__name__, args[1:])
            args[1].master.attr_changes = []
        def mock_show_2(*args):
            print('called show_dialog with args', args[0].__name__, args[1:])
            args[1].master.attr_changes = [('xxx', 'yyy'), ('zzz', '')]  # , ('', 'qqq')]i kan dit?
            args[1].master.screeninfo = {'xxx': {'dir': 'xxx-dir', 'txt': 'xxx-txt', 'sel': True,
                                                 'opt': False},
                                         'zzz': {'dir': 'zzz-dir', 'txt': 'zzz-txt', 'sel': False,
                                                 'opt': True}}
        def mock_set(*args):
            print('called Conf.set_diritem_value with args', args)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = MockShowMods(testobj)
        testobj.conf.set_diritem_value = mock_set
        assert capsys.readouterr().out == f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
        testobj.manage_attributes()
        assert capsys.readouterr().out == (
                f"called show_dialog with args AttributesDialog ({testobj.doit}, {testobj.conf})\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        testobj.manage_attributes()
        assert capsys.readouterr().out == (
                f"called show_dialog with args AttributesDialog ({testobj.doit}, {testobj.conf})\n"
                "called Conf.set_diritem_value with args ('xxx-dir', 'SCRNAM', 'xxx')\n"
                "called Conf.set_diritem_value with args ('xxx-dir', 'ScrTxt', 'xxx-txt')\n"
                "called Conf.set_diritem_value with args ('xxx-dir', 'Sel', True)\n"
                "called Conf.set_diritem_value with args ('xxx-dir', '_DoNotTouch', False)\n"
                "called Conf.set_diritem_value with args ('zzz-dir', 'ScrTxt', 'zzz-txt')\n"
                "called Conf.set_diritem_value with args ('zzz-dir', 'Sel', False)\n"
                "called Conf.set_diritem_value with args ('zzz-dir', '_DoNotTouch', True)\n"
                "called JsonConf.save\n")

    def test_get_mod_components(self, monkeypatch, capsys):
        """unittest for Manager.get_mod_components
        """
        def mock_list(self, name):
            "stub"
            print(f"called Conf.list_components_for_dir with arg '{name}'")
            return []
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_mod_components('aaa') == ("Components for aaa:\n"
                                                     "  xxx_compname   xxx_version\n"
                                                     "    (xxx)\n"
                                                     "  yyy_compname   yyy_version\n"
                                                     "    (yyy)")
        assert capsys.readouterr().out == (
                "called Conf.list_components_for_dir with arg 'aaa'\n"
                "called Conf.get_component_data with args ('xxx', 'Name')\n"
                "called Conf.get_component_data with args ('xxx', 'Version')\n"
                "called Conf.get_component_data with args ('yyy', 'Name')\n"
                "called Conf.get_component_data with args ('yyy', 'Version')\n")
        monkeypatch.setattr(MockConf, 'list_components_for_dir', mock_list)
        assert testobj.get_mod_components('aaa') == "Components for aaa:\n"
        assert capsys.readouterr().out == "called Conf.list_components_for_dir with arg 'aaa'\n"

    def test_get_mod_dependencies(self, monkeypatch, capsys):
        """unittest for Manager.get_mod_dependencies
        """
        def mock_list(self, name):
            "stub"
            print(f"called Conf.list_components_for_dir with arg '{name}'")
            return []
        def mock_get(self, *args):
            "stub"
            print("called Conf.get_component_data with args", args)
            if args[1] == self.DEPS:
                return [f'{args[0]}_compname']
            raise ValueError
        def mock_get_2(self, *args):
            "stub"
            print("called Conf.get_component_data with args", args)
            if args[1] == self.DEPS:
                return [f'{args[0]}_depname']
            if args[1] == self.NAME:
                return f'{args[0]}_compname'
            raise ValueError
        monkeypatch.setattr(MockConf, 'get_component_data', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_mod_dependencies('aaa') == ("Dependencies for aaa:\n"
                                                       " unknown component: xxx_compname\n"
                                                       " unknown component: yyy_compname")
        assert capsys.readouterr().out == (
                "called Conf.list_components_for_dir with arg 'aaa'\n"
                "called Conf.get_component_data with args ('xxx', 'Deps')\n"
                "called Conf.get_component_data with args ('yyy', 'Deps')\n"
                "called Conf.get_component_data with args ('xxx_compname', 'Name')\n"
                "called Conf.get_component_data with args ('yyy_compname', 'Name')\n")
        monkeypatch.setattr(MockConf, 'get_component_data', mock_get_2)
        assert testobj.get_mod_dependencies('aaa') == ("Dependencies for aaa:\n"
                                                       " xxx_depname_compname (xxx_depname)\n"
                                                       " yyy_depname_compname (yyy_depname)")
        assert capsys.readouterr().out == (
                "called Conf.list_components_for_dir with arg 'aaa'\n"
                "called Conf.get_component_data with args ('xxx', 'Deps')\n"
                "called Conf.get_component_data with args ('yyy', 'Deps')\n"
                "called Conf.get_component_data with args ('xxx_depname', 'Name')\n"
                "called Conf.get_component_data with args ('yyy_depname', 'Name')\n")
        monkeypatch.setattr(MockConf, 'list_components_for_dir', mock_list)
        assert testobj.get_mod_dependencies('aaa') == ("Dependencies for aaa:\n"
                                                       " None ")
        assert capsys.readouterr().out == "called Conf.list_components_for_dir with arg 'aaa'\n"

    def test_update_attributes(self, monkeypatch, capsys):
        """unittest for Manager.update_attributes
        """
        def mock_switch(*args):
            print('called Manager.switch_by_selectability with args', args)
            return False
        def mock_refresh(*args):
            print('called ShowMods.refresh_widgets with args', args)
        def mock_get(*args):
            print('called Manager.get_widget_list with args', args)
            return ['widget', 'label']
        def mock_build(*args):
            print('called ShowMods.set_label_text with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = types.SimpleNamespace(refresh_widgets=mock_refresh)
        # testobj.build_screen_text = mock_build
        testobj.doit.set_label_text = mock_build
        testobj.switch_by_selectability = mock_switch
        testobj.get_widget_list = mock_get
        testobj.screeninfo = {}
        testobj.attr_changes = []
        assert testobj.update_attributes(True, 'xxx', 'xxx', 'yyy', True) == (
                False, 'Tweemaal schermnaam wijzigen van een mod zonder de dialoog af te breken'
                ' en opnieuw te starten is helaas nog niet mogelijk')
        assert capsys.readouterr().out == ""
        testobj.screeninfo = {'xxx': {'sel': False, 'txt': '', 'opt': False, 'pos': '1x2'}}
        assert testobj.update_attributes(True, 'xxx', 'xxx', 'yyy', True) == (True, '')
        assert testobj.screeninfo == {'xxx': {'sel': True, 'txt': 'yyy', 'opt': True, 'pos': '1x2'}}
        assert testobj.attr_changes == [('xxx', '')]
        assert capsys.readouterr().out == (
                "called Manager.switch_by_selectability with args (True, 'xxx', 'xxx')\n"
                "called ShowMods.refresh_widgets with args ()\n")
        testobj.screeninfo = {'xxx': {'sel': False, 'txt': '', 'opt': False, 'pos': '1x2', 'key': 1}}
        testobj.attr_changes = []
        assert testobj.update_attributes(False, 'yyy', 'xxx', '', False) == (True, '')
        assert testobj.screeninfo == {'yyy': {'sel': False, 'txt': '', 'opt': False, 'pos': '1x2',
                                              'key': 1}}
        assert testobj.attr_changes == [('yyy', 'xxx')]
        assert capsys.readouterr().out == (
                "called Manager.get_widget_list with args (1, 2, False)\n"
                "called ShowMods.set_label_text with args (['widget', 'label'], 'yyy', 1, '')\n")
        testobj.screeninfo = {'xxx': {'sel': False, 'txt': '', 'opt': False, 'pos': '1x2', 'key': 1}}
        testobj.attr_changes = []
        assert testobj.update_attributes(False, 'xxx', 'xxx', '', False) == (True, '')
        assert testobj.screeninfo == {'xxx': {'sel': False, 'txt': '', 'opt': False, 'pos': '1x2',
                                              'key': 1}}
        assert testobj.attr_changes == [('xxx', '')]
        assert capsys.readouterr().out == ''

    def test_switch_by_selectability(self, monkeypatch, capsys):
        """unittest for Manager.switch_selectability
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.unplotted = []
        testobj.not_selectable = []
        with pytest.raises(ValueError):
            testobj.switch_by_selectability(True, 'xxx', 'xxx')
        # testobj.parent.unplotted = []
        testobj.not_selectable = ['xxx', 'yyy']
        testobj.switch_by_selectability(True, 'xxx', 'xxx')
        assert testobj.unplotted == ['xxx']
        assert testobj.not_selectable == ['yyy']
        testobj.unplotted = []
        testobj.not_selectable = ['xxx', 'yyy']
        testobj.switch_by_selectability(True, 'xxx', 'yyy')
        assert testobj.unplotted == ['xxx']
        assert testobj.not_selectable == ['xxx']
        testobj.unplotted = []
        testobj.not_selectable = []
        with pytest.raises(ValueError):
            testobj.switch_by_selectability(False, 'xxx', 'xxx')
        assert testobj.unplotted == []
        assert testobj.not_selectable == []
        testobj.unplotted = ['xxx', 'yyy']
        testobj.not_selectable = []
        testobj.switch_by_selectability(False, 'xxx', 'xxx')
        assert testobj.unplotted == ['yyy']
        assert testobj.not_selectable == ['xxx']
        testobj.unplotted = ['xxx', 'yyy']
        testobj.not_selectable = []
        testobj.switch_by_selectability(False, 'xxx', 'yyy')
        assert testobj.unplotted == ['xxx']
        assert testobj.not_selectable == ['xxx']

    def test_get_widget_list(self, monkeypatch, capsys):
        """unittest for Manager.get_widget_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.plotted_widgets = {(1, 2): ['x']}
        testobj.unplotted_widgets = {(1, 2): ['y']}
        testobj.nonsel_widgets = {(1, 2): ['z']}
        assert testobj.get_widget_list(1, 2, True) == ['x']
        testobj.plotted_widgets = {(1, 3): ['x']}
        testobj.unplotted_widgets = {(1, 2): ['y']}
        testobj.nonsel_widgets = {(1, 2): ['z']}
        assert testobj.get_widget_list(1, 2, True) == ['y']
        testobj.plotted_widgets = {(1, 2): ['x']}
        testobj.unplotted_widgets = {(1, 2): ['y']}
        testobj.nonsel_widgets = {(1, 2): ['z']}
        assert testobj.get_widget_list(1, 2, False) == ['z']

    def test_manage_savefiles(self, monkeypatch, capsys):
        """unittest for Manager.manage_savefiles
        """
        def mock_show(*args):
            print('called show_dialog with args', args[0].__name__, args[1:])
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = MockShowMods(testobj)
        assert capsys.readouterr().out == f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
        testobj.manage_savefiles()
        assert capsys.readouterr().out == (
                f"called show_dialog with args SaveGamesDialog ({testobj.doit}, {testobj.conf})\n")

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
                "called Conf.set_diritem_data with args ('x-dir', 'ScrPos', '5x5')\n"
                "called Conf.set_diritem_data with args ('y-dir', 'ScrPos', '1x1')\n"
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
        def mock_move(name):
            print('called move_zip_after_installing with arg', name)
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
        monkeypatch.setattr(testee, 'move_zip_after_installing', mock_move)
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
            f"called move_zip_after_installing with arg {tmp_path}/xxx\n"
            "called JsonConf.save\n"
            "called Manager.extract_screeninfo\n"
            "called gui.ShowMods.refresh_widgets with args {}\n")

        testobj.get_data_for_config = mock_get_2
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], False)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.add_mod_to_config with args ('root', (['done'], True))\n"
            f"called move_zip_after_installing with arg {tmp_path}/yyy\n"
            "called JsonConf.save\n"
            "called Manager.extract_screeninfo\n"
            "called gui.ShowMods.refresh_widgets with args {}\n")

        testobj.install_zipfile = mock_install_4
        testobj.get_data_for_config = mock_get
        testobj.update_mod_settings = mock_upd
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], False)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.update_mod_settings with args ('root', (['done'], False))\n"
            f"called move_zip_after_installing with arg {tmp_path}/yyy\n")

        testobj.update_mod_settings = mock_upd_2
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], False)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.update_mod_settings with args ('root', (['done'], False))\n"
            f"called move_zip_after_installing with arg {tmp_path}/yyy\n"
            "called JsonConf.save\n")

        testobj.get_data_for_config = mock_get_2
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], False)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.update_mod_settings with args ('root', (['done'], True))\n"
            f"called move_zip_after_installing with arg {tmp_path}/yyy\n"
            "called JsonConf.save\n")

        testobj.install_zipfile = mock_install_5
        testobj.get_data_for_config = mock_get
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], True)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.update_mod_settings with args ('root', (['done'], False))\n"
            f"called move_zip_after_installing with arg {tmp_path}/yyy\n"
            "called JsonConf.save\n")

        testobj.get_data_for_config = mock_get_2
        assert testobj.update_mods([str(tmp_path / 'yyy')]) == ['ok', 'done']
        assert capsys.readouterr().out == (
            f"called Manager.install_zipfile with arg '{tmp_path}/yyy'\n"
            f"called Manager.get_data_for_config with args (['yyy'], True)\n"
            f"called Manager.determine_moddir with args (['yyy'],)\n"
            f"called Manager.update_mod_settings with args ('root', (['done'], True))\n"
            f"called move_zip_after_installing with arg {tmp_path}/yyy\n"
            "called JsonConf.save\n")

    def test_install_zipfile(self, monkeypatch, capsys, tmp_path):
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
        def mock_rename(*args):
            print('called os.rename with args', args)
        def mock_move(name):
            print('called move_zip_after_installing with arg', name)
        monkeypatch.setattr(testee, 'move_zip_after_installing', mock_move)
        monkeypatch.setattr(testee.os, 'rename', mock_rename)
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
        zipfilepath = tmp_path / 'zipfile'
        assert testobj.install_zipfile(zipfilepath) == (
                [], None, None, [f'{zipfilepath}: zipfile appears to be empty'])
        assert capsys.readouterr().out == (
                f"called ZipFile.__init__ with args ({zipfilepath!r},)\n"
                "called ZipFile.__enter__\n"
                "called ZipFile.namelist\n"
                "called get_archive_roots with arg ['name', 'list']\n"
                "called check_if_active with arg set()\n"
                "called check_if_smapi with arg set()\n"
                "called ZipFile.__exit__\n")

        monkeypatch.setattr(testee, 'get_archive_roots', mock_get_3)
        assert testobj.install_zipfile(zipfilepath) == (
                [], None, None, ["SMAPI-install is waiting in a terminal window to be finished"
                                 " by executing './install on Linux.sh'"])
        assert capsys.readouterr().out == (
                f"called ZipFile.__init__ with args ({zipfilepath!r},)\n"
                "called ZipFile.__enter__\n"
                "called ZipFile.namelist\n"
                "called get_archive_roots with arg ['name', 'list']\n"
                "called check_if_active with arg {'root'}\n"
                "called check_if_smapi with arg {'root'}\n"
                "called ZipFile.__exit__\n"
                "called subprocess.run with args"
                f" (['unzip', {zipfilepath!r}, '-d', '/tmp'],) {{'check': True}}\n"
                "called subprocess.run with args (['gnome-terminal'],) {'cwd': '/tmp/root'}\n"
                f"called move_zip_after_installing with arg {zipfilepath}\n")

        monkeypatch.setattr(testee, 'get_archive_roots', mock_get_2)
        monkeypatch.setattr(testee, 'check_if_smapi', mock_check_smapi_2)
        assert testobj.install_zipfile(zipfilepath) == (
                {''}, False, False, [f'{zipfilepath} is successfully installed'])
        assert capsys.readouterr().out == (
                f"called ZipFile.__init__ with args ({zipfilepath!r},)\n"
                "called ZipFile.__enter__\n"
                "called ZipFile.namelist\n"
                "called get_archive_roots with arg ['name', 'list']\n"
                "called check_if_active with arg {''}\n"
                "called check_if_smapi with arg {''}\n"
                "called ZipFile.extractall with args ('modbase',)\n"
                "called ZipFile.__exit__\n"
                "called shutil.rmtree with args ('modbase/__MACOSX',)\n")

        monkeypatch.setattr(testee, 'get_archive_roots', mock_get_3)
        assert testobj.install_zipfile(zipfilepath) == (
                {'root'}, False, False, [f'{zipfilepath} is successfully installed'])
        assert capsys.readouterr().out == (
                f"called ZipFile.__init__ with args ({zipfilepath!r},)\n"
                "called ZipFile.__enter__\n"
                "called ZipFile.namelist\n"
                "called get_archive_roots with arg ['name', 'list']\n"
                "called check_if_active with arg {'root'}\n"
                "called check_if_smapi with arg {'root'}\n"
                "called ZipFile.extractall with args ('modbase',)\n"
                "called ZipFile.__exit__\n"
                "called shutil.rmtree with args ('modbase/__MACOSX',)\n")

        monkeypatch.setattr(testee.os.path, 'exists', lambda *x: False)
        assert testobj.install_zipfile(zipfilepath) == (
                {'root'}, False, False, [f'{zipfilepath} is successfully installed'])
        assert capsys.readouterr().out == (
                f"called ZipFile.__init__ with args ({zipfilepath!r},)\n"
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
        assert str(exc.value) == 'New mod "moddir" exists in configuration, should not be possible'
        assert capsys.readouterr().out == "called Conf.has_moddir with arg moddir\n"

        testobj.conf.has_moddir = mock_has_mod_2
        assert testobj.add_mod_to_config('moddir', {}) == [
                "  Screentext set to '(new mod)' ",
                '  Update ID set to xx ',
                '  Change the "Selectable" setting if you want to be able to activate the mod']
        assert capsys.readouterr().out == ("called Conf.has_moddir with arg moddir\n"
                                           "called Conf.add_diritem with arg moddir\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.COMPS}', [])\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.SCRNAM}', '(new mod)')\n"
                                           "called determine_update_id with arg set()\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.NXSKEY}', 'xx')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.SEL}', False)\n")

        assert testobj.add_mod_to_config('moddir', {'unzipdir': {}}) == [
                "  Screentext set to '(new mod)' ",
                '  Update ID set to xx ',
                '  Change the "Selectable" setting if you want to be able to activate the mod']
        assert capsys.readouterr().out == ("called Conf.has_moddir with arg moddir\n"
                                           "called Conf.add_diritem with arg moddir\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.COMPS}', [])\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.SCRNAM}', '(new mod)')\n"
                                           "called determine_update_id with arg set()\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.NXSKEY}', 'xx')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.SEL}', False)\n")

        assert testobj.add_mod_to_config('moddir', {'unzipdir': {'component': {}}}) == [
                "  Screentext set to '(new mod)' ",
                '  Update ID set to xx ',
                '  Change the "Selectable" setting if you want to be able to activate the mod']
        assert capsys.readouterr().out == ("called Conf.has_moddir with arg moddir\n"
                                           "called Conf.add_diritem with arg moddir\n"
                                           "called Conf.add_component with arg component\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.COMPS}', ['component'])\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.SCRNAM}', '(new mod)')\n"
                                           "called determine_update_id with arg set()\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.NXSKEY}', 'xx')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.SEL}', False)\n")

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
                                           f" ('component', '{testobj.conf.NAME}', 'abcdef')\n"
                                           "called Conf.add_component with arg comp2\n"
                                           "called Conf.set_component_value with args"
                                           f" ('comp2', '{testobj.conf.NAME}', 'pqrst')\n"
                                           "called Conf.add_component with arg comp3\n"
                                           "called Conf.set_component_value with args"
                                           f" ('comp3', '{testobj.conf.NAME}', 'abcdef')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.COMPS}',"
                                           " ['component', 'comp2', 'comp3'])\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.SCRNAM}', 'abcdef')\n"
                                           "called determine_update_id with arg set()\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.NXSKEY}', 'xx')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.SEL}', False)\n")

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
                                           f" ('component', '{testobj.conf.NAME}', 'abcdef')\n"
                                           "called Conf.set_component_value with args"
                                           f" ('component', '{testobj.conf.NXSKEY}', '123')\n"
                                           "called Conf.set_component_value with args"
                                           f" ('component', 'xxx', 'yyy')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.COMPS}', ['component'])\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.SCRNAM}', 'abcdef')\n"
                                           "called determine_update_id with arg {'123'}\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.NXSKEY}', 'xx')\n"
                                           "called Conf.set_diritem_value with args"
                                           f" ('moddir', '{testobj.conf.SEL}', False)\n")

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
            return {testobj.conf.NAME: 'xxx', testobj.conf.VRS: '1.0', 'aaa': 'bbb'}
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
                f"called Conf.get_diritem_data with args ('moddir', '{testobj.conf.COMPS}')\n")

        assert testobj.update_mod_settings('moddir', {'config': {}}) == ([], False)
        assert capsys.readouterr().out == (
                "called Conf.has_moddir with arg moddir\n"
                f"called Conf.get_diritem_data with args ('moddir', '{testobj.conf.COMPS}')\n")

        assert testobj.update_mod_settings('moddir', {'config': {'newcomp': {}}}) == (
                ["  List of components changed from [] to ['newcomp']"], True)
        assert capsys.readouterr().out == (
                "called Conf.has_moddir with arg moddir\n"
                f"called Conf.get_diritem_data with args ('moddir', '{testobj.conf.COMPS}')\n"
                f"called Conf.set_diritem_value with args ('moddir', '{testobj.conf.COMPS}',"
                " ['newcomp'])\n"
                "called Conf.get_component_data with arg newcomp\n"
                "called Conf.update_componentdata with args ('newcomp', {})\n")

        testobj.conf.get_diritem_data = mock_get_dir_2
        testobj.conf.get_component_data = mock_get_comp_2
        assert testobj.update_mod_settings('moddir', {'config': {'newcomp': {
            testobj.conf.NAME: 'xxx', testobj.conf.VRS: '2.0', 'ppp': 'qqq'}}}) == (
                    [f"  newcomp: {testobj.conf.VRS} changed from '1.0' to '2.0'",
                     "  newcomp: new key ppp added with value 'qqq'",
                     "  newcomp: key aaa with value 'bbb' removed"], True)
        assert capsys.readouterr().out == (
                "called Conf.has_moddir with arg moddir\n"
                f"called Conf.get_diritem_data with args ('moddir', '{testobj.conf.COMPS}')\n"
                "called Conf.get_component_data with arg newcomp\n"
                "called Conf.update_componentdata with args ('newcomp', {"
                f"'{testobj.conf.NAME}': 'xxx', '{testobj.conf.VRS}': '2.0', 'ppp': 'qqq'}})\n")

        assert testobj.update_mod_settings('moddir', {'config': {'newcomp': {
            testobj.conf.NAME: 'xxx', testobj.conf.VRS: '1.0', 'aaa': 'bbb'}}}) == ([], False)
        assert capsys.readouterr().out == (
                "called Conf.has_moddir with arg moddir\n"
                f"called Conf.get_diritem_data with args ('moddir', '{testobj.conf.COMPS}')\n"
                "called Conf.get_component_data with arg newcomp\n")

    def test_manage_defaults(self, monkeypatch, capsys):
        """unittest for Manager.manage_defaults
        """
        def mock_read(**kwargs):
            print('called dmlj.read_defaults with args', kwargs)
            return origdata
        def mock_read_2(**kwargs):
            print('called dmlj.read_defaults with args', kwargs)
            return newdata
        def mock_show(*args):
            print('called show_dialog with args', args[0].__name__, args[1:])
            args[1].parent.dialog_data = newdata
        def mock_show_2(*args):
            print('called show_dialog with args', args[0].__name__, args[1:])
            args[1].parent.dialog_data = origdata
        def mock_save(*args):
            print('called dmlj.save_defaults with args', args)
        origdata = ('orig', 'data', 'x', 'y', 'z')
        newdata = ('orig', 'data', 'x', 'max_col', 'z')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = MockShowMods(testobj)
        assert capsys.readouterr().out == f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
        testobj.maxcol = 'max_col'
        testobj.doit.parent = testobj
        monkeypatch.setattr(testee.dmlj, 'read_defaults', mock_read)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        monkeypatch.setattr(testee.dmlj, 'save_defaults', mock_save)
        testobj.manage_defaults()
        assert testobj.dialog_data == newdata
        assert capsys.readouterr().out == (
                "called dmlj.read_defaults with args {'bare': True}\n"
                f"called show_dialog with args SettingsDialog ({testobj.doit},)\n"
                f"called dmlj.save_defaults with args {newdata}\n")
        monkeypatch.setattr(testee.dmlj, 'read_defaults', mock_read_2)
        testobj.manage_defaults()
        assert capsys.readouterr().out == (
                "called dmlj.read_defaults with args {'bare': True}\n"
                f"called show_dialog with args SettingsDialog ({testobj.doit},)\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        testobj.manage_defaults()
        assert testobj.maxcol == 'y'
        assert capsys.readouterr().out == (
                "called dmlj.read_defaults with args {'bare': True}\n"
                f"called show_dialog with args SettingsDialog ({testobj.doit},)\n"
                f"called dmlj.save_defaults with args {origdata}\n")

    def test_manage_deletions(self, monkeypatch, capsys):
        """unittest for manager.manage_deletions
        """
        def mock_show(*args):
            print('called show_dialog with args', args[0].__name__, args[1:])
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = types.SimpleNamespace()
        testobj.conf = types.SimpleNamespace()
        testobj.manage_deletions()
        assert capsys.readouterr().out == (
                f"called show_dialog with args DeleteDialog ({testobj.doit}, {testobj.conf})\n")

    def test_remove_mod(self, monkeypatch, capsys):
        """unittest for manager.remove_mod
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit = MockShowMods(testobj)
        testobj.conf = MockConf()
        assert capsys.readouterr().out == (
                f"called gui.ShowMods.__init__() with arg '{testobj}'\n"
                "called JsonConf.__init__ with args () {}\n")
        testobj.screeninfo = {'moddir': {'dir': 'stuff'}}
        testobj.unplotted = ['moddir', 'stuff']
        testobj.not_selectable = ['stuff']
        testobj.remove_mod('moddir')
        assert testobj.screeninfo == {}
        assert testobj.unplotted == ['stuff']
        assert testobj.not_selectable == ['stuff']
        assert capsys.readouterr().out == (
                "called gui.ShowMods.refresh_widgets with args {'first_time': False}\n"
                "called Conf.list_components_for_dir with arg 'stuff'\n"
                "called Conf.remove_component with arg 'xxx'\n"
                "called Conf.remove_component with arg 'yyy'\n"
                "called Conf.remove_diritem with arg 'stuff'\n"
                "called JsonConf.save\n")
        testobj.screeninfo = {'moddir': {'dir': 'stuff'}}
        testobj.unplotted = ['stuff']
        testobj.not_selectable = ['moddir', 'stuff']
        testobj.remove_mod('moddir')
        assert testobj.screeninfo == {}
        assert testobj.unplotted == ['stuff']
        assert testobj.not_selectable == ['stuff']
        assert capsys.readouterr().out == (
                "called gui.ShowMods.refresh_widgets with args {'first_time': False}\n"
                "called Conf.list_components_for_dir with arg 'stuff'\n"
                "called Conf.remove_component with arg 'xxx'\n"
                "called Conf.remove_component with arg 'yyy'\n"
                "called Conf.remove_diritem with arg 'stuff'\n"
                "called JsonConf.save\n")


class MockSettingsGui:
    """teststub for gui.SettingsDialogGui object
    """
    def __init__(self, *args):
        print('called SettingsDialogGui.__init__ with args', args)
    def add_label(self, *args):
        "stub"
        print('called SettingsDialogGui.add_label with args', args)
    def add_line_entry(self, *args):
        "stub"
        print('called SettingsDialogGui.add_line_entry with args', args)
        return 'line_entry'
    def add_browse_button(self, *args):
        "stub"
        print('called SettingsDialogGui.add_browse_button with args', args)
        return 'browser'
    def add_spinbox(self, *args):
        "stub"
        print('called SettingsDialogGui.add_spinbox with args', args)
        return 'spinbox'
    def add_buttonbox(self, *args):
        "stub"
        print('called SettingsDialogGui.add_buttonbox with args', args)
    def set_focus(self, *args):
        "stub"
        print('called SettingsDialogGui.set_focus with args', args)
    def get_widget_text(self, *args):
        "stub"
        print('called SettingsDialogGui.get_widget_text with args', args)
        return ''
    def set_widget_text(self, *args):
        "stub"
        print('called SettingsDialogGui.set_widget_text with args', args)
    def select_directory(self, *args):
        "stub"
        print('called SettingsDialogGui.select_directory with args', args)
        return ''
    def reject(self):
        "stub"
        print('called SettingsDialogGui.reject')
    def confirm(self):
        "stub"
        print('called SettingsDialogGui.confirm')


class TestSettingsDialog:
    """unittests for qtgui.SettingsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SettingsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called SettingsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SettingsDialog, '__init__', mock_init)
        testobj = testee.SettingsDialog()
        testobj.doit = MockSettingsGui()
        assert capsys.readouterr().out == ('called SettingsDialog.__init__ with args ()\n'
                                           'called SettingsDialogGui.__init__ with args ()\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SettingsDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'SettingsDialogGui', MockSettingsGui)
        parent = MockManager()
        parent.master = types.SimpleNamespace(dialog_data=('xxx', 'yyy', 'zzz', 'qqq', 'rrr'))
        testobj = testee.SettingsDialog(parent)
        assert testobj.parent == parent
        assert testobj.modbase_text == 'line_entry'
        assert testobj.select_modbase_button == 'browser'
        assert testobj.config_text == 'line_entry'
        assert testobj.download_text == 'line_entry'
        assert testobj.select_download_button == 'browser'
        assert testobj.columns == 'spinbox'
        assert testobj.savepath_text == 'line_entry'
        assert testobj.select_savepath_button == 'browser'
        assert capsys.readouterr().out == expected_output['settings'].format(testobj=testobj)

    def test_select_modbase(self, monkeypatch, capsys):
        """unittest for SettingsDialog.select_modbase
        """
        def mock_get(*args):
            print('called SettingsDialogGui.get_widget_text with args', args)
            return 'widget-text'
        def mock_select(*args):
            print('called SettingsDialogGui.select_directory with args', args)
            return 'test'
        def mock_select_2(*args):
            print('called SettingsDialogGui.select_directory with args', args)
            return testee.os.path.expanduser('~/hello')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.modbase_text = 'modbase_text'
        testobj.select_modbase()
        assert capsys.readouterr().out == (
                "called SettingsDialogGui.get_widget_text with args ('modbase_text',)\n"
                "called SettingsDialogGui.select_directory with args"
                f" ('Where to install downloaded mods?', '{testee.os.path.expanduser("~")}')\n")
        testobj.doit.get_widget_text = mock_get
        testobj.doit.select_directory = mock_select
        testobj.select_modbase()
        assert capsys.readouterr().out == (
                "called SettingsDialogGui.get_widget_text with args ('modbase_text',)\n"
                "called SettingsDialogGui.select_directory with args"
                " ('Where to install downloaded mods?', 'widget-text')\n"
                "called SettingsDialogGui.set_widget_text with args ('modbase_text', 'test')\n")
        testobj.doit.select_directory = mock_select_2
        testobj.select_modbase()
        assert capsys.readouterr().out == (
                "called SettingsDialogGui.get_widget_text with args ('modbase_text',)\n"
                "called SettingsDialogGui.select_directory with args"
                " ('Where to install downloaded mods?', 'widget-text')\n"
                "called SettingsDialogGui.set_widget_text with args ('modbase_text', '~/hello')\n")

    def test_select_download_path(self, monkeypatch, capsys):
        """unittest for SettingsDialog.select_modbase
        """
        def mock_get(*args):
            print('called SettingsDialogGui.get_widget_text with args', args)
            return 'widget-text'
        def mock_select(*args):
            print('called SettingsDialogGui.select_directory with args', args)
            return 'test'
        def mock_select_2(*args):
            print('called SettingsDialogGui.select_directory with args', args)
            return testee.os.path.expanduser('~/hello')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.download_text = 'download_text'
        testobj.select_download_path()
        assert capsys.readouterr().out == (
                "called SettingsDialogGui.get_widget_text with args ('download_text',)\n"
                "called SettingsDialogGui.select_directory with args"
                f" ('Where to download mods to?', '{testee.os.path.expanduser("~")}')\n")
        testobj.doit.get_widget_text = mock_get
        testobj.doit.select_directory = mock_select
        testobj.select_download_path()
        assert capsys.readouterr().out == (
                "called SettingsDialogGui.get_widget_text with args ('download_text',)\n"
                "called SettingsDialogGui.select_directory with args"
                " ('Where to download mods to?', 'widget-text')\n"
                "called SettingsDialogGui.set_widget_text with args ('download_text', 'test')\n")
        testobj.doit.select_directory = mock_select_2
        testobj.select_download_path()
        assert capsys.readouterr().out == (
                "called SettingsDialogGui.get_widget_text with args ('download_text',)\n"
                "called SettingsDialogGui.select_directory with args"
                " ('Where to download mods to?', 'widget-text')\n"
                "called SettingsDialogGui.set_widget_text with args ('download_text', '~/hello')\n")

    def test_select_savepath(self, monkeypatch, capsys):
        """unittest for SettingsDialog.select_modbase
        """
        def mock_get(*args):
            print('called SettingsDialogGui.get_widget_text with args', args)
            return 'widget-text'
        def mock_select(*args):
            print('called SettingsDialogGui.select_directory with args', args)
            return 'test'
        def mock_select_2(*args):
            print('called SettingsDialogGui.select_directory with args', args)
            return testee.os.path.expanduser('~/hello')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.savepath_text = 'savepath_text'
        testobj.select_savepath()
        assert capsys.readouterr().out == (
                "called SettingsDialogGui.get_widget_text with args ('savepath_text',)\n"
                "called SettingsDialogGui.select_directory with args"
                f" ('Where are the saved games stored?', '{testee.os.path.expanduser("~")}')\n")
        testobj.doit.get_widget_text = mock_get
        testobj.doit.select_directory = mock_select
        testobj.select_savepath()
        assert capsys.readouterr().out == (
                "called SettingsDialogGui.get_widget_text with args ('savepath_text',)\n"
                "called SettingsDialogGui.select_directory with args"
                " ('Where are the saved games stored?', 'widget-text')\n"
                "called SettingsDialogGui.set_widget_text with args ('savepath_text', 'test')\n")
        testobj.doit.select_directory = mock_select_2
        testobj.select_savepath()
        assert capsys.readouterr().out == (
                "called SettingsDialogGui.get_widget_text with args ('savepath_text',)\n"
                "called SettingsDialogGui.select_directory with args"
                " ('Where are the saved games stored?', 'widget-text')\n"
                "called SettingsDialogGui.set_widget_text with args ('savepath_text', '~/hello')\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for SettingsDialog.update
        """
        def mock_get(*args):
            print('called SettingsDialogGui.get_widget_text with args', args)
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit.get_widget_text = mock_get
        testobj.parent = types.SimpleNamespace(master=types.SimpleNamespace())
        testobj.modbase_text = 'modbase_text'
        testobj.config_text = 'config_text'
        testobj.download_text = 'download_text'
        testobj.columns = '11'
        testobj.savepath_text = 'savepath_text'
        testobj.update()
        assert testobj.parent.master.dialog_data == ('modbase_text', 'config_text',
                                                     'download_text', 11, 'savepath_text')
        assert capsys.readouterr().out == (
                "called SettingsDialogGui.get_widget_text with args ('modbase_text',)\n"
                "called SettingsDialogGui.get_widget_text with args ('config_text',)\n"
                "called SettingsDialogGui.get_widget_text with args ('download_text',)\n"
                "called SettingsDialogGui.get_widget_text with args ('11',)\n"
                "called SettingsDialogGui.get_widget_text with args ('savepath_text',)\n"
                "called SettingsDialogGui.confirm\n")


class MockDeleteGui:
    """teststub for gui.DeleteDialogGui object
    """
    def __init__(self, *args):
        print('called DeleteDialogGui.__init__ with args', args)
    def add_label(self, *args):
        "stub"
        print('called DeleteDialogGui.add_label with args', args)
    def add_line_entry(self, *args):
        "stub"
        print('called DeleteDialogGui.add_line_entry with args', args)
        return 'line_entry'
    def add_browse_button(self, *args):
        "stub"
        print('called DeleteDialogGui.add_browse_button with args', args)
        return 'browser'
    def add_spinbox(self, *args):
        "stub"
        print('called DeleteDialogGui.add_spinbox with args', args)
        return 'spinbox'
    def add_combobox(self, *args, **kwargs):
        "stub"
        print('called DeleteDialogGui.add_combobox with args', args, kwargs)
        return 'combobox'
    def add_buttonbox(self, *args):
        "stub"
        print('called DeleteDialogGui.add_buttonbox with args', args)
        result = [f'button{i}' for i in range(len(args[0]))]
        return result
    def set_focus(self, *args):
        "stub"
        print('called DeleteDialogGui.set_focus with args', args)
    def enable_button(self, *args):
        "stub"
        print('called DeleteDialogGui.enable_button with args', args)
    def get_widget_text(self, *args):
        "stub"
        print('called DeleteDialogGui.get_widget_text with args', args)
        return ''
    def get_combobox_entry(self, *args):
        "stub"
        print('called DeleteDialogGui.get_combobox_entry with args', args)
        return ''
    def set_combobox_entry(self, *args):
        "stub"
        print('called DeleteDialogGui.set_combobox_entry with args', args)
    def select_directory(self, *args):
        "stub"
        print('called DeleteDialogGui.select_directory with args', args)
        return ''
    def accept(self):
        "stub"
        print('called DeleteDialogGui.accept')
    def reject(self):
        "stub"
        print('called DeleteDialogGui.reject')
    def confirm(self):
        "stub"
        print('called DeleteDialogGui.confirm')


class TestDeleteDialog:
    """unittests for qtgui.DeleteDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.DeleteDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called DeleteDialog.__init__ with args', args)
        monkeypatch.setattr(testee.DeleteDialog, '__init__', mock_init)
        testobj = testee.DeleteDialog()
        testobj.doit = MockDeleteGui()
        assert capsys.readouterr().out == ('called DeleteDialog.__init__ with args ()\n'
                                           'called DeleteDialogGui.__init__ with args ()\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for DeleteDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'DeleteDialogGui', MockDeleteGui)
        parent = MockManager()
        conf = MockConf()
        testobj = testee.DeleteDialog(parent, conf)
        assert testobj.parent == parent
        assert testobj.conf == conf
        assert testobj.modnames == {'xxx_name': 'xxx', 'yyy_name': 'yyy'}
        assert testobj.lbox == 'combobox'
        assert testobj.change_button == 'button0'
        assert capsys.readouterr().out == expected_output['delete'].format(testobj=testobj)

    def test_process(self, monkeypatch, capsys):
        """unittest for DeleteDialog.process
        """
        def mock_get(*args):
            print('called DeleteDialogGui.get_combobox_entry with args', args)
            return testee.DeleteDialog.seltext
        def mock_get_2(*args):
            print('called DeleteDialogGui.get_combobox_entry with args', args)
            return 'xxx'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.lbox = 'checkbox'
        testobj.change_button = 'change_button'
        testobj.doit.get_combobox_entry = mock_get
        testobj.process()
        assert testobj.choice == testee.DeleteDialog.seltext
        assert capsys.readouterr().out == (
                "called DeleteDialogGui.get_combobox_entry with args ('checkbox',)\n"
                "called DeleteDialogGui.enable_button with args ('change_button', False)\n")
        testobj.choice = 'xxxx'
        testobj.doit.get_combobox_entry = mock_get_2
        testobj.process()
        assert testobj.choice == 'xxx'
        assert capsys.readouterr().out == (
                "called DeleteDialogGui.get_combobox_entry with args ('checkbox',)\n"
                "called DeleteDialogGui.enable_button with args ('change_button', True)\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for DeleteDialog.update
        """
        def mock_remove(*args):
            print('called Manager.remove_mod with args')
        def mock_show(*args):
            print('called gui.show_message with args', args)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(remove_mod=mock_remove))
        testobj.lbox = 'combobox'
        testobj.choice = 'combochoice'
        testobj.change_button = 'change_button'
        testobj.update()
        assert capsys.readouterr().out == (
                "called Manager.remove_mod with args\n"
                f"called gui.show_message with args ({testobj.doit}, 'combochoice has been removed')\n"
                "called DeleteDialogGui.set_combobox_entry with args ('combobox', 0)\n"
                "called DeleteDialogGui.enable_button with args ('change_button', False)\n"
                "called DeleteDialogGui.confirm\n")


class MockAttributesGui:
    """teststub for gui.AttributesDialogGui object
    """
    def __init__(self, *args):
        print('called AttributesDialogGui.__init__ with args', args)
    def add_label(self, *args):
        "stub"
        print('called AttributesDialogGui.add_label with args', args)
    def add_line_entry(self, *args, **kwargs):
        "stub"
        print('called AttributesDialogGui.add_line_entry with args', args, kwargs)
        return 'line_entry'
    def add_browse_button(self, *args):
        "stub"
        print('called AttributesDialogGui.add_browse_button with args', args)
        return 'browser'
    def add_spinbox(self, *args):
        "stub"
        print('called AttributesDialogGui.add_spinbox with args', args)
        return 'spinbox'
    def add_combobox(self, *args, **kwargs):
        "stub"
        print('called AttributesDialogGui.add_combobox with args', args, kwargs)
        return 'combobox'
    def add_checkbox(self, *args, **kwargs):
        "stub"
        print('called AttributesDialogGui.add_checkbox with args', args, kwargs)
        return 'checkbox'
    def start_line_with_clear_button(self):
        "stub"
        print('called AttributesDialogGui.start_line_with_clear_button')
    def add_clear_button(self, *args, **kwargs):
        "stub"
        print('called AttributesDialogGui.add_clear_button with args', args, kwargs)
        return 'clear_button'
    def add_button(self, *args, **kwargs):
        "stub"
        print('called AttributesDialogGui.add_button with args', args, kwargs)
        return 'button'
    def add_buttonbox(self, *args):
        "stub"
        print('called AttributesDialogGui.add_buttonbox with args', args)
        result = [f'button{i}' for i in range(len(args[0]))]
        return result
    def set_focus(self, *args):
        "stub"
        print('called AttributesDialogGui.set_focus with args', args)
    def enable_button(self, *args):
        "stub"
        print('called AttributesDialogGui.enable_button with args', args)
    def get_field_text(self, *args):
        "stub"
        print('called AttributesDialogGui.get_field_text with args', args)
        return args[0]
    def get_combobox_value(self, *args):
        "stub"
        print('called AttributeDialogGui.get_combobox_value with args', args)
        return ''
    def set_combobox_entry(self, *args):
        "stub"
        print('called AttributeDialogGui.set_combobox_entry with args', args)
    def get_checkbox_value(self, *args):
        "stub"
        print('called AttributeDialogGui.get_checkbox_value with args', args)
        return args[0]  # eigenlijk True of False maar is hier niet belangrijk
    def clear_field(self, *args):
        "stub"
        print('called AttributeDialogGui.clear_field with args', args)
    def reset_all_fields(self, *args):
        "stub"
        print('called AttributeDialogGui.reset_all_fields with args', args)
    def activate_and_populate_fields(self, *args):
        "stub"
        print('called AttributeDialogGui.activate_and_populate_fields with args', args)
    def accept(self):
        "stub"
        print('called AttributeDialogGui.accept')
    def reject(self):
        "stub"
        print('called AttributeDialogGui.reject')
    def confirm(self):
        "stub"
        print('called AttributeDialogGui.confirm')


class TestAttributesDialog:
    """unittests for qtgui.AttributesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.AttributesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called AttributesDialog.__init__ with args', args)
        monkeypatch.setattr(testee.AttributesDialog, '__init__', mock_init)
        testobj = testee.AttributesDialog()
        testobj.doit = MockAttributesGui()
        assert capsys.readouterr().out == ('called AttributesDialog.__init__ with args ()\n'
                                           'called AttributesDialogGui.__init__ with args ()\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for AttributesDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'AttributesDialogGui', MockAttributesGui)
        parent = MockManager()
        conf = MockConf()
        testobj = testee.AttributesDialog(parent, conf)
        assert testobj.parent == parent
        assert testobj.conf == conf
        assert testobj.choice == ''
        assert testobj.modnames == {'xxx_name': 'xxx', 'yyy_name': 'yyy'}
        assert testobj.lbox == 'combobox'
        assert testobj.name == 'combobox'
        assert testobj.clear_name_button == 'clear_button'
        assert testobj.text == 'line_entry'
        assert testobj.clear_text_button == 'clear_button'
        assert testobj.activate_button == 'checkbox'
        assert testobj.exempt_button == 'checkbox'
        assert testobj.comps_button == 'button'
        assert testobj.deps_button == 'button'
        assert testobj.change_button == 'button0'
        assert testobj.add_dep_button == 'button1'
        assert capsys.readouterr().out == expected_output['attrs'].format(testobj=testobj)

    def test_enable_change(self, monkeypatch, capsys):
        """unittest for AttributesDialog.enable_change
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.change_button = 'change_button'
        testobj.add_dep_button = 'add_dep_button'
        testobj.enable_change()
        assert capsys.readouterr().out == (
                "called AttributesDialogGui.enable_button with args ('change_button', True)\n"
                "called AttributesDialogGui.enable_button with args ('add_dep_button', True)\n")

    def test_process(self, monkeypatch, capsys):
        """unittest for AttributesDialog.process
        """
        def mock_get(*args):
            print('called AttributesDialogGui.get_combobox_value with args', args)
            return testee.AttributesDialog.seltext
        def mock_get_2(*args):
            print('called AttributesDialogGui.get_combobox_value with args', args)
            return 'xxx'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        assert capsys.readouterr().out == "called JsonConf.__init__ with args () {}\n"
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(
                    screeninfo={'xxx': {'txt': 'Xxx', 'sel': True, 'opt': False}}))
        testobj.lbox = 'combobox'
        testobj.name = 'combobox'
        testobj.clear_name_button = 'clear_button'
        testobj.text = 'line_entry'
        testobj.clear_text_button = 'clear_button'
        testobj.activate_button = 'checkbox'
        testobj.exempt_button = 'checkbox'
        testobj.comps_button = 'button'
        testobj.deps_button = 'button'
        testobj.change_button = 'change_button'
        testobj.modnames = {'xxx': {'aaa'}}
        testobj.doit.get_combobox_value = mock_get
        testobj.process()
        assert testobj.choice == testee.AttributesDialog.seltext
        assert capsys.readouterr().out == (
                "called AttributesDialogGui.get_combobox_value with args ('combobox',)\n"
                "called AttributeDialogGui.reset_all_fields with args"
                " (['combobox', 'clear_button', 'line_entry', 'clear_button',"
                " 'checkbox', 'checkbox', 'button', 'button', 'change_button'],)\n")
        testobj.doit.get_combobox_value = mock_get_2
        testobj.process()
        assert testobj.choice == 'xxx'
        assert capsys.readouterr().out == (
                "called AttributesDialogGui.get_combobox_value with args ('combobox',)\n"
                "called Conf.list_components_for_dir with arg '{'aaa'}'\n"
                "called Conf.get_component_data with args ('xxx', 'Name')\n"
                "called Conf.get_component_data with args ('yyy', 'Name')\n"
                "called AttributeDialogGui.activate_and_populate_fields with args"
                " (['combobox', 'clear_button', 'line_entry', 'clear_button',"
                " 'checkbox', 'checkbox', 'button', 'button', 'change_button'],"
                " ['xxx', 'xxx_compname', 'yyy_compname'],"
                " {'txt': 'Xxx', 'sel': True, 'opt': False})\n")

    def test_clear_name_text(self, monkeypatch, capsys):
        """unittest for AttributesDialog.clear_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.name = 'screenname_field'
        testobj.clear_name_text()
        assert capsys.readouterr().out == (
            "called AttributeDialogGui.clear_field with args ('screenname_field',)\n")

    def test_clear_text_text(self, monkeypatch, capsys):
        """unittest for AttributesDialog.clear_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text = 'screentext_field'
        testobj.clear_text_text()
        assert capsys.readouterr().out == (
            "called AttributeDialogGui.clear_field with args ('screentext_field',)\n")

    def test_view_components(self, monkeypatch, capsys):
        """unittest for AttributesDialog.view_components
        """
        def mock_get(*args):
            print('called ShowMods.get_mod_components with args', args)
            return 'xxx'
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(get_mod_components=mock_get))
        # testobj.conf = MockConf()
        testobj.choice = 'xxx'
        testobj.modnames = {'xxx': {'aaa'}}
        testobj.view_components()
        assert capsys.readouterr().out == (
                "called ShowMods.get_mod_components with args ({'aaa'},)\n"
                f"called gui.show_message with args ({testobj.doit}, 'xxx')"
                " {'title': 'SDVMM mod info'}\n")

    def test_view_dependencies(self, monkeypatch, capsys):
        """unittest for AttributesDialog.view_dependencies
        """
        def mock_get(*args):
            print('called ShowMods.get_mod_dependencies with args', args)
            return 'xxx'
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(get_mod_dependencies=mock_get))
        # testobj.conf = MockConf()
        testobj.choice = 'xxx'
        testobj.modnames = {'xxx': {'aaa'}}
        testobj.view_dependencies()
        assert capsys.readouterr().out == (
                "called ShowMods.get_mod_dependencies with args ({'aaa'},)\n"
                f"called gui.show_message with args ({testobj.doit}, 'xxx')"
                " {'title': 'SDVMM mod info'}\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for AttributesDialog.update
        """
        def mock_update(*args):
            print("called ShowMods.update_attributes with args", args)
            return False, 'A message'
        def mock_update2(*args):
            print("called ShowMods.update_attributes with args", args)
            return True, ''
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                master=types.SimpleNamespace(update_attributes=mock_update))
        testobj.choice = 'xxx'
        testobj.name = 'name_button'
        testobj.text = 'text_button'
        testobj.clear_name_button = 'clear_name_button'
        testobj.clear_text_button = 'clear_text_button'
        testobj.activate_button = 'activate_button'
        testobj.exempt_button = 'exempt_button'
        testobj.change_button = 'change_button'
        testobj.update()
        assert capsys.readouterr().out == (
                "called AttributesDialogGui.enable_button with args ('clear_name_button', False)\n"
                "called AttributesDialogGui.enable_button with args ('clear_text_button', False)\n"
                "called AttributeDialogGui.get_checkbox_value with args ('activate_button',)\n"
                "called AttributesDialogGui.get_field_text with args ('text_button',)\n"
                "called AttributeDialogGui.get_combobox_value with args ('name_button',)\n"
                "called AttributeDialogGui.get_checkbox_value with args ('exempt_button',)\n"
                "called ShowMods.update_attributes with args"
                " ('activate_button', '', 'xxx', 'text_button', 'exempt_button')\n"
                f"called gui.show_message with args ({testobj.doit}, 'A message') {{}}\n")
        testobj.parent.master.update_attributes = mock_update2
        testobj.update()
        assert capsys.readouterr().out == (
                "called AttributesDialogGui.enable_button with args ('clear_name_button', False)\n"
                "called AttributesDialogGui.enable_button with args ('clear_text_button', False)\n"
                "called AttributeDialogGui.get_checkbox_value with args ('activate_button',)\n"
                "called AttributesDialogGui.get_field_text with args ('text_button',)\n"
                "called AttributeDialogGui.get_combobox_value with args ('name_button',)\n"
                "called AttributeDialogGui.get_checkbox_value with args ('exempt_button',)\n"
                "called ShowMods.update_attributes with args"
                " ('activate_button', '', 'xxx', 'text_button', 'exempt_button')\n"
                "called AttributesDialogGui.enable_button with args ('change_button', False)\n")

    def test_add_dep(self, monkeypatch, capsys):
        """unittest for AttributesDialog.add_dep
        """
        def mock_show(*args):
            print('called show_dialog with args', args[0].__name__, args[1:])
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        assert capsys.readouterr().out == "called JsonConf.__init__ with args () {}\n"
        testobj.add_dep()
        assert capsys.readouterr().out == (
                f"called show_dialog with args DependencyDialog ({testobj.doit}, {testobj.conf})\n")


class MockDependencyGui:
    """teststub for gui.DependencyDialogGui object
    """
    def __init__(self, *args):
        print('called DependencyDialogGui.__init__ with args', args)
    def add_label(self, *args):
        "stub"
        print('called DependencyDialogGui.add_label with args', args)
    def add_line_entry(self, *args):
        "stub"
        print('called DependencyDialogGui.add_line_entry with args', args)
        return 'line_entry'
    def add_browse_button(self, *args):
        "stub"
        print('called DependencyDialogGui.add_browse_button with args', args)
        return 'browser'
    def add_spinbox(self, *args):
        "stub"
        print('called DependencyDialogGui.add_spinbox with args', args)
        return 'spinbox'
    def add_combobox(self, *args, **kwargs):
        "stub"
        print('called DependencyDialogGui.add_combobox with args', args, kwargs)
        return 'combobox'
    def add_buttonbox(self, *args):
        "stub"
        print('called DependencyDialogGui.add_buttonbox with args', args)
    def set_focus(self, *args):
        "stub"
        print('called DependencyDialogGui.set_focus with args', args)
    def enable_button(self, *args):
        "stub"
        print('called DependencyDialogGui.enable_button with args', args)
    def get_widget_text(self, *args):
        "stub"
        print('called DependencyDialogGui.get_widget_text with args', args)
        return ''
    def get_combobox_value(self, *args):
        "stub"
        print('called DependencyDialogGui.get_combobox_value with args', args)
        return ''
    def set_combobox_entry(self, *args):
        "stub"
        print('called DependencyDialogGui.set_combobox_entry with args', args)
    def select_directory(self, *args):
        "stub"
        print('called DependencyDialogGui.select_directory with args', args)
        return ''
    def accept(self):
        "stub"
        print('called DependencyDialogGui.accept')
    def reject(self):
        "stub"
        print('called DependencyDialogGui.reject')
    def confirm(self):
        "stub"
        print('called DependencyDialogGui.confirm')


class TestDependencyDialog:
    """unittests for manager.SavegamesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SaveGamesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called DependencyDialog.__init__ with args', args)
        monkeypatch.setattr(testee.DependencyDialog, '__init__', mock_init)
        testobj = testee.DependencyDialog()
        testobj.doit = MockDependencyGui()
        assert capsys.readouterr().out == ('called DependencyDialog.__init__ with args ()\n'
                                           'called DependencyDialogGui.__init__ with args ()\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for DependencyDialog.__init__
        """
        def mock_list():
            print('called Conf.list_all_mod_dirs')
            return ['Xxx']
        def mock_listc(name):
            print(f"called Conf.list_components_for_dir with arg '{name}'")
            return ['yyy']
        monkeypatch.setattr(testee.gui, 'DependencyDialogGui', MockDependencyGui)
        parent = types.SimpleNamespace(
                maingui=types.SimpleNamespace(modnames={'xxx': 'Xxx'}, choice='xxx'))
        conf = MockConf()
        assert capsys.readouterr().out == "called JsonConf.__init__ with args () {}\n"
        testobj = testee.DependencyDialog(parent, conf)
        assert testobj.parent == parent
        assert testobj.conf == conf
        assert testobj.modnames == {'xxx_name': 'xxx', 'yyy_name': 'yyy'}
        assert capsys.readouterr().out == expected_output['deps'].format(testobj=testobj)

        conf.list_all_mod_dirs = mock_list
        conf.list_components_for_dir = mock_listc
        testobj = testee.DependencyDialog(parent, conf)
        assert testobj.parent == parent
        assert testobj.conf == conf
        assert testobj.modnames == {}
        assert capsys.readouterr().out == expected_output['deps2'].format(testobj=testobj)

    def test_accept(self, monkeypatch, capsys):
        """unittest for DependencyDialog.accept
        """
        def mock_get(*args):
            print('called DependencyDialogGui.get_combobox_value with args', args)
            return args[0]
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit.get_combobox_value = mock_get
        testobj.conf = MockConf()
        assert capsys.readouterr().out == "called JsonConf.__init__ with args () {}\n"
        testobj.modnames = {'depsel': 'qqq'}
        testobj.dependency_selector = 'depsel'
        testobj.component_selector = 'compsel'
        testobj.accept()
        assert capsys.readouterr().out == (
                "called DependencyDialogGui.get_combobox_value with args ('depsel',)\n"
                "called DependencyDialogGui.get_combobox_value with args ('compsel',)\n"
                "called Conf.list_components_for_dir with arg 'qqq'\n"
                "called Conf.get_component_data with args ('compsel', 'Deps')\n"
                "called Conf.set_componenentdata_value with args"
                f" ('compsel', 'Deps', ['compsel_depname', 'xxx'])\n"
                "called JsonConf.save\n"
                f"called gui.show_message with args ({testobj.doit}, 'Add Dependency',"
                " 'Wijziging is doorgevoerd\\nVergeet niet om na updaten van de mod"
                " te controleren of de dependency opnieuw moet worden toegevoegd') {}\n"
                "called DependencyDialogGui.confirm\n")


class MockSaveGamesGui:
    """teststub for gui.SaveGamesDialogGui object
    """
    def __init__(self, *args):
        print('called SaveGamesDialogGui.__init__ with args', args)
    def add_label(self, *args):
        "stub"
        print('called SaveGamesDialogGui.add_label with args', args)
    def add_line_entry(self, *args):
        "stub"
        print('called SaveGamesDialogGui.add_line_entry with args', args)
        return 'line_entry'
    def add_browse_button(self, *args):
        "stub"
        print('called SaveGamesDialogGui.add_browse_button with args', args)
        return 'browser'
    def add_spinbox(self, *args):
        "stub"
        print('called SaveGamesDialogGui.add_spinbox with args', args)
        return 'spinbox'
    def add_combobox(self, *args, **kwargs):
        "stub"
        print('called SaveGamesDialogGui.add_combobox with args', args, kwargs)
        return 'combobox'
    def add_buttonbox(self, *args):
        "stub"
        print('called SaveGamesDialogGui.add_buttonbox with args', args)
        result = [f'button{i}' for i in range(len(args[0]))]
        return result
    def start_modselect_block(self, *args):
        "stub"
        print('called SaveGamesDialogGui.start_modselect_block with args', args)
    def add_clear_button(self, *args, **kwargs):
        "stub"
        print('called AttributesDialogGui.add_clear_button with args', args, kwargs)
        return 'clear_button', 'container'
    def set_callbacks(self, *args):
        "stub"
        print('called SaveGamesDialogGui.set_callbacks with args', args)
    def set_focus(self, *args):
        "stub"
        print('called SaveGamesDialogGui.set_focus with args', args)
    def enable_change(self, *args):
        "stub"
        print('called SaveGamesDialogGui.enable_change with args', args)
    def enable_widget(self, *args):
        "stub"
        print('called SaveGamesDialogGui.enable_widget with args', args)
    def set_field_text(self, *args):
        "stub"
        print('called AttributesDialogGui.set_field_text with args', args)
    def get_field_text(self, *args):
        "stub"
        print('called AttributesDialogGui.get_field_text with args', args)
        return args[0]
    def get_widget_text(self, *args):
        "stub"
        print('called SaveGamesDialogGui.get_widget_text with args', args)
        return ''
    def get_combobox_value(self, *args):
        "stub"
        print('called SaveGamesDialogGui.get_combobox_value with args', args)
        return ''
    def set_combobox_value(self, *args):
        "stub"
        print('called SaveGamesDialogGui.set_combobox_value with args', args)
    def select_directory(self, *args):
        "stub"
        print('called SaveGamesDialogGui.select_directory with args', args)
        return ''
    def remove_modselector(self, *args):
        "stub"
        print('called SaveGamesDialogGui.remove_modselector with args', args)
    def accept(self):
        "stub"
        print('called SaveGamesDialogGui.accept')
    def reject(self):
        "stub"
        print('called SaveGamesDialogGui.reject')
    def confirm(self):
        "stub"
        print('called SaveGamesDialogGui.confirm')


class TestSaveGamesDialog:
    """unittests for qtgui.SaveGamesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SaveGamesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called SaveGamesDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SaveGamesDialog, '__init__', mock_init)
        testobj = testee.SaveGamesDialog()
        testobj.doit = MockSaveGamesGui()
        assert capsys.readouterr().out == ('called SaveGamesDialog.__init__ with args ()\n'
                                           'called SaveGamesDialogGui.__init__ with args ()\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SaveGamesDialog.__init__
        """
        def mock_add(self, *args):
            print('called SaveGamesDialog.add_modselector')
        parent = MockManager()
        conf = MockConf()
        assert capsys.readouterr().out == ("called Manager.__init__\n"
                                           "called JsonConf.__init__ with args () {}\n")
        monkeypatch.setattr(testee.gui, 'SaveGamesDialogGui', MockSaveGamesGui)
        monkeypatch.setattr(testee.SaveGamesDialog, 'add_modselector', mock_add)
        testobj = testee.SaveGamesDialog(parent, conf)
        assert testobj.parent == parent
        assert testobj.conf == conf
        assert testobj.savenames == ['qqq', 'rrr']
        assert testobj.modnames == {'xxx_name': 'xxx', 'yyy_name': 'yyy'}
        assert testobj.savegame_selector == 'combobox'
        assert testobj.oldsavename == ''
        assert testobj.pname == 'line_entry'
        assert testobj.fname == 'line_entry'
        assert testobj.gdate == 'line_entry'
        assert testobj.widgets == []
        assert testobj.update_button == 'button0'
        assert testobj.confirm_button == 'button1'
        assert capsys.readouterr().out == expected_output['saves'].format(testobj=testobj)

    def test_add_modselector(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.add_modselector
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.modnames = ['yyy', 'xxx']
        testobj.widgets = []
        testobj.add_modselector()
        assert testobj.widgets == [['clear_button', 'combobox', 'container']]
        assert capsys.readouterr().out == (
            "called SaveGamesDialogGui.add_combobox with args"
            " (['select a mod', 'xxx', 'yyy'], None) {'editable': True, 'enabled': True}\n"
            "called AttributesDialogGui.add_clear_button with args (True,) {}\n"
            "called SaveGamesDialogGui.set_callbacks with args (('combobox', 'clear_button'),"
            f" (functools.partial({testobj.process_mod}, 'combobox'),"
            f" functools.partial({testobj.remove_mod}, 'clear_button')))\n")
        testobj.widgets = []
        testobj.add_modselector(False)
        assert testobj.widgets == [['clear_button', 'combobox', 'container']]
        assert capsys.readouterr().out == (
            "called SaveGamesDialogGui.add_combobox with args"
            " (['select a mod', 'xxx', 'yyy'], None) {'editable': True, 'enabled': False}\n"
            "called AttributesDialogGui.add_clear_button with args (False,) {}\n"
            "called SaveGamesDialogGui.set_callbacks with args (('combobox', 'clear_button'),"
            f" (functools.partial({testobj.process_mod}, 'combobox'),"
            f" functools.partial({testobj.remove_mod}, 'clear_button')))\n")

    def test_process_mod(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.process_mod
        """
        def mock_add():
            print('called SaveGamesDialog.add_modselector')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_modselector = mock_add
        testobj.update_button = 'update_button'
        testobj.widgets = [('button0', 'lbox0'), ('button1', 'lbox1')]
        testobj.process_mod('lbox', 'select a mod')
        assert capsys.readouterr().out == ""
        testobj.process_mod('lbox0', 'item0')
        assert capsys.readouterr().out == (
                "called SaveGamesDialogGui.enable_widget with args ('button0', True)\n"
                "called SaveGamesDialogGui.enable_widget with args ('update_button', True)\n")
        testobj.process_mod('lbox1', 'item1')
        assert capsys.readouterr().out == (
                "called SaveGamesDialogGui.enable_widget with args ('button1', True)\n"
                "called SaveGamesDialogGui.enable_widget with args ('update_button', True)\n"
                "called SaveGamesDialog.add_modselector\n")

    def test_remove_mod(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.remove_mod
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.widgets = []
        testobj.remove_mod('btn')
        assert not testobj.widgets
        assert capsys.readouterr().out == ""
        testobj.widgets = [('button', 'checkbox')]
        testobj.remove_mod('btn')
        assert testobj.widgets == [('button', 'checkbox')]
        assert capsys.readouterr().out == ""
        testobj.widgets = [('btn', 'cbox')]
        testobj.remove_mod('btn')
        assert not testobj.widgets
        assert capsys.readouterr().out == (
                "called SaveGamesDialogGui.remove_modselector with args (('btn', 'cbox'),)\n")

    def test_confirm(self, monkeypatch, capsys, tmp_path):
        """unittest for SaveGamesDialog.confirm
        """
        def mock_get_value(*args):
            print('called SaveGamesDialogGui.get_combobox_value with args', args)
            return 'aaa'
        def mock_get_diritem_data(*args):
            print("called Conf.get_diritem_data with args", args)
            if args == ('xxx', '_DoNotTouch'):
                return False
            if args == ('yyy', '_DoNotTouch'):
                return True
            if args == ('zzz', '_DoNotTouch'):
                return True
        def mock_get_component_data(*args):
            print("called Conf.get_component_data with args", args)
            if args[0] == 'xxx':
                return 'aaa'
            if args[0] == 'yyy':
                return '.bbb'
        def mock_get_mods(name):
            print(f"called Conf.get_mods_for_saveitem with arg {name}")
            return ['qqq', 'rrr']
        def mock_select(self, names):
            print(f'called Manager.select_activations with arg {names}')
            self.directories = ['sss', 'ttt']
        def mock_list_dirs():
            print('called Conf.list_all_mod_dirs')
            return []
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        # monkeypatch.setattr(testee.os.path, 'exists', mock_exists)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(master=MockManager())
        testobj.conf = MockConf()
        assert capsys.readouterr().out == ('called Manager.__init__\n'
                                           'called JsonConf.__init__ with args () {}\n')
        testobj.savegame_selector = 'combobox'
        testobj.parent.master.modbase = tmp_path
        testobj.doit.get_combobox_value = mock_get_value

        testobj.conf.get_diritem_data = mock_get_diritem_data
        testobj.conf.get_component_data = mock_get_component_data
        testobj.conf.get_mods_for_saveitem = mock_get_mods
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called SaveGamesDialogGui.get_combobox_value with args ('combobox',)\n"
                "called Conf.get_mods_for_saveitem with arg aaa\n"
                "called Conf.list_all_mod_dirs\n"
                "called Conf.get_diritem_data with args ('xxx', '_DoNotTouch')\n"
                "called Conf.get_diritem_data with args ('yyy', '_DoNotTouch')\n"
                "called Manager.select_activations with args (['qqq', 'rrr'],)\n"
                "called Manager.refresh_widget_data\n"
                "called gui.show_message with args"
                f" ({testobj.doit}, 'wijzigingen zijn doorgevoerd') {{'title': 'Change Config'}}\n"
                "called SaveGamesDialogGui.accept\n")

        monkeypatch.setattr(MockManager, 'select_activations', mock_select)
        # monkeypatch.setattr(testee.os.path, 'exists', mock_exists_2)
        # testobj.conf.list_components_for_dir = mock_list_comps
        (tmp_path / 'yyy').touch()
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called SaveGamesDialogGui.get_combobox_value with args ('combobox',)\n"
                "called Conf.get_mods_for_saveitem with arg aaa\n"
                "called Conf.list_all_mod_dirs\n"
                "called Conf.get_diritem_data with args ('xxx', '_DoNotTouch')\n"
                "called Conf.get_diritem_data with args ('yyy', '_DoNotTouch')\n"
                "called Conf.get_diritem_data with args ('yyy', 'SCRNAM')\n"
                "called Manager.select_activations with arg ['qqq', 'rrr', 'yyy']\n"
                "called Manager.activate with args\n"
                "called Manager.refresh_widget_data\n"
                "called gui.show_message with args"
                f" ({testobj.doit}, 'wijzigingen zijn doorgevoerd') {{'title': 'Change Config'}}\n"
                "called SaveGamesDialogGui.accept\n")

    def test_update(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.update
        """
        def mock_get_value(*args):
            print('called SaveGamesDialogGui.get_combobox_value with args', args)
            return 'aaa'
        def mock_update(arg):
            print(f"called SaveGameDialog.update_conf with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.doit.get_combobox_value = mock_get_value
        testobj.update_conf = mock_update
        testobj.savegame_selector = 'combobox'
        testobj.update()
        assert capsys.readouterr().out == (
                "called SaveGamesDialogGui.get_combobox_value with args ('combobox',)\n"
                "called SaveGameDialog.update_conf with arg 'aaa'\n")

    def test_update_conf(self, monkeypatch, capsys):
        """unittest for SaveGamesDialog.update
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pname = 'pname'
        testobj.fname = 'fname'
        testobj.gdate = 'gdate'
        testobj.update_button = 'update_button'
        testobj.conf = MockConf()
        assert capsys.readouterr().out == "called JsonConf.__init__ with args () {}\n"
        testobj.widgets = []
        lbox = 'checkbox'
        testobj.old_pname = 'pname'
        testobj.old_fname = 'fname'
        testobj.old_gdate = 'gdate'
        testobj.oldmods = []
        testobj.update_conf('save_name')
        assert capsys.readouterr().out == (
                "called AttributesDialogGui.get_field_text with args ('pname',)\n"
                "called AttributesDialogGui.get_field_text with args ('fname',)\n"
                "called AttributesDialogGui.get_field_text with args ('gdate',)\n"
                # "called JsonConf.save\n"
                "called SaveGamesDialogGui.enable_widget with args ('update_button', False)\n")
        testobj.widgets = [lbox]
        testobj.oldmods = ['current text']
        testobj.update_conf('save_name')
        assert capsys.readouterr().out == (
                "called AttributesDialogGui.get_field_text with args ('pname',)\n"
                "called AttributesDialogGui.get_field_text with args ('fname',)\n"
                "called AttributesDialogGui.get_field_text with args ('gdate',)\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Mods', [])\n"
                "called JsonConf.save\n"
                "called SaveGamesDialogGui.enable_widget with args ('update_button', False)\n")

        testobj.old_pname = 'aaa'
        testobj.old_fname = 'bbb'
        testobj.old_gdate = 'ccc'
        testobj.oldmods = ['qqq']
        testobj.update_conf('save_name')
        assert capsys.readouterr().out == (
                "called AttributesDialogGui.get_field_text with args ('pname',)\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Pname', 'pname')\n"
                "called AttributesDialogGui.get_field_text with args ('fname',)\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Fname', 'fname')\n"
                "called AttributesDialogGui.get_field_text with args ('gdate',)\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Gdate', 'gdate')\n"
                "called Conf.update_saveitem_data with args ('save_name', 'Mods', [])\n"
                "called JsonConf.save\n"
                "called SaveGamesDialogGui.enable_widget with args ('update_button', False)\n")

    def test_get_savedata(self, monkeypatch, capsys):  # 907-932
        """unittest for SaveGamesDialog.get_savedata
        """
        def mock_update(name):
            print(f'called SaveGamesDialog with arg {name}')
        def mock_add(self):
            print('called SaveGamesDialog.add_modselector')
            self.widgets = [['button', 'combobox', 'container']]
        def mock_get(arg):
            print(f'called SaveGavesDialogGui.get_combobox_value with arg {arg}')
            return combobox_value
        def mock_get_attrs(value):
            "stub"
            print(f"called Conf.get_saveitem_attrs with arg {value}")
            return ('oldpname', 'oldfname', 'oldgdate'), True
        def mock_get_attrs_2(value):
            "stub"
            print(f"called Conf.get_saveitem_attrs with arg {value}")
            return ('oldpname', 'oldfname', 'oldgdate'), False
        def mock_get_mods(name):
            "stub"
            print(f"called Conf.get_mods_for_saveitem with arg {name}")
            return ['newmodname']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.conf = MockConf()
        assert capsys.readouterr().out == "called JsonConf.__init__ with args () {}\n"
        testobj.update_conf = mock_update
        monkeypatch.setattr(testee.SaveGamesDialog, 'add_modselector', mock_add)
        # testobj.vbox2 = mockqtw.MockVBoxLayout()
        testobj.savegame_selector = 'savegame_selector'
        testobj.oldsavename = ''
        testobj.pname = 'pname'
        testobj.fname = 'fname'
        testobj.gdate = 'gdate'
        testobj.update_button = 'update_button'
        testobj.confirm_button = 'confirm_button'
        testobj.widgets = []
        testobj.doit.get_combobox_value = mock_get

        combobox_value = 'select a saved game'
        testobj.get_savedata()
        assert capsys.readouterr().out == (
                "called SaveGavesDialogGui.get_combobox_value with arg savegame_selector\n"
                "called SaveGamesDialog.add_modselector\n")

        testobj.oldsavename = ''
        combobox_value = 'xxx'
        testobj.get_savedata()
        assert capsys.readouterr().out == (
                "called SaveGavesDialogGui.get_combobox_value with arg savegame_selector\n"
                "called SaveGamesDialogGui.remove_modselector with args"
                " (['button', 'combobox', 'container'],)\n"
                "called SaveGamesDialog.add_modselector\n"
                "called Conf.get_saveitem_attrs with arg xxx\n"
                "called SaveGamesDialogGui.enable_widget with args ('update_button', False)\n"
                "called SaveGamesDialogGui.enable_widget with args ('confirm_button', True)\n")
        testobj.oldsavename = 'yyy'
        testobj.get_savedata()
        assert capsys.readouterr().out == (
                "called SaveGavesDialogGui.get_combobox_value with arg savegame_selector\n"
                "called SaveGamesDialog with arg yyy\n"
                "called SaveGamesDialogGui.remove_modselector with args"
                " (['button', 'combobox', 'container'],)\n"
                "called SaveGamesDialog.add_modselector\n"
                "called Conf.get_saveitem_attrs with arg xxx\n"
                "called SaveGamesDialogGui.enable_widget with args ('update_button', False)\n"
                "called SaveGamesDialogGui.enable_widget with args ('confirm_button', True)\n")
        testobj.widgets = [['button', 'combobox', 'container']]
        testobj.conf.get_saveitem_attrs = mock_get_attrs
        testobj.conf.get_mods_for_saveitem = mock_get_mods
        testobj.get_savedata()
        assert capsys.readouterr().out == (
                "called SaveGavesDialogGui.get_combobox_value with arg savegame_selector\n"
                "called SaveGamesDialog with arg xxx\n"
                "called SaveGamesDialogGui.remove_modselector with args"
                " (['button', 'combobox', 'container'],)\n"
                "called SaveGamesDialog.add_modselector\n"
                "called Conf.get_saveitem_attrs with arg xxx\n"
                "called AttributesDialogGui.set_field_text with args ('pname', 'oldpname')\n"
                "called AttributesDialogGui.set_field_text with args ('fname', 'oldfname')\n"
                "called AttributesDialogGui.set_field_text with args ('gdate', 'oldgdate')\n"
                "called Conf.get_mods_for_saveitem with arg xxx\n"
                "called SaveGamesDialogGui.set_combobox_value with args ('combobox', 'newmodname')\n"
                "called SaveGamesDialogGui.enable_widget with args ('update_button', True)\n"
                "called SaveGamesDialogGui.enable_widget with args ('confirm_button', True)\n")
        # testobj.widgets = [['button', 'combobox', 'container']]
        testobj.conf.get_saveitem_attrs = mock_get_attrs_2
        testobj.conf.get_mods_for_saveitem = mock_get_mods
        testobj.get_savedata()
        assert capsys.readouterr().out == (
                "called SaveGavesDialogGui.get_combobox_value with arg savegame_selector\n"
                "called SaveGamesDialog with arg xxx\n"
                "called SaveGamesDialogGui.remove_modselector with args"
                " (['button', 'combobox', 'container'],)\n"
                "called SaveGamesDialog.add_modselector\n"
                "called Conf.get_saveitem_attrs with arg xxx\n"
                "called AttributesDialogGui.set_field_text with args ('pname', 'oldpname')\n"
                "called AttributesDialogGui.set_field_text with args ('fname', 'oldfname')\n"
                "called AttributesDialogGui.set_field_text with args ('gdate', 'oldgdate')\n"
                "called Conf.get_mods_for_saveitem with arg xxx\n"
                "called SaveGamesDialogGui.set_combobox_value with args ('combobox', 'newmodname')\n"
                "called SaveGamesDialogGui.enable_widget with args ('update_button', False)\n"
                "called SaveGamesDialogGui.enable_widget with args ('confirm_button', True)\n")


def test_get_toplevel():
    """unittest for Manager.get_toplevel
    """
    assert testee.get_toplevel('xxx') == 'xxx'
    assert testee.get_toplevel('xxx/yyy') == 'xxx'
    assert testee.get_toplevel('xxx/yyy/zzz') == 'xxx'


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


def test_move_zip_after_installing(monkeypatch, capsys):
    """unittest for Manager.move_zip_after_installing
    """
    def mock_rename(*args):
        print('called os.rename with args', args)
    monkeypatch.setattr(testee.os, 'rename', mock_rename)
    testee.move_zip_after_installing('xxx/yyy.zip')
    dirname = testee.os.path.abspath('xxx')
    assert capsys.readouterr().out == (
            f"called os.rename with args ('{dirname}/yyy.zip', '{dirname}/installed/yyy.zip')\n")


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
    def mock_load(*args):
        print('called json.load with args', args)
        return {'moddirs': {'a': 'c'}, 'components': ['q', 's'], 'savedgames': {'x': 'z'}}
    def mock_rebuild(arg):
        print(f'called dmlj.rebuild_all with arg {list(arg)}')
        return {'moddirs': {'a': 'b'}, 'components': ['q', 'r'], 'savedgames': {'x': 'y'}}, []
    def mock_rebuild_2(arg):
        print(f'called dmlj.rebuild_all with arg {list(arg)}')
        return ({'moddirs': {'a': 'b'}, 'components': ['q', 'r'], 'savedgames': {'x': 'y'}},
                ['xxx', 'yyy'])
    def mock_dump(*args):
        print('called json.dump with args', args)
    monkeypatch.setattr(testee, 'MODBASE', str(tmp_path))
    (tmp_path / 'xxx').touch()
    (tmp_path / 'yyy').touch()
    monkeypatch.setattr(testee, 'CONFIG', str(tmp_path / 'qqq'))
    monkeypatch.setattr(testee.json, 'dump', mock_dump)
    monkeypatch.setattr(testee.json, 'load', mock_load)
    monkeypatch.setattr(testee.dmlj, 'rebuild_all', mock_rebuild)
    assert testee.build_jsonconf() == []
    assert capsys.readouterr().out == (
            f"called dmlj.rebuild_all with arg [{tmp_path / 'yyy'!r}, {tmp_path / 'xxx'!r}]\n"
            "called json.dump with args ({'moddirs': {'a': 'b'}, 'components': ['q', 'r'],"
            " 'savedgames': {}},"
            f" <_io.TextIOWrapper name='{tmp_path / 'qqq'}' mode='w' encoding='UTF-8'>)\n")
    (tmp_path / 'qqq').touch()
    assert testee.build_jsonconf() == []
    assert capsys.readouterr().out == (
            f"called json.load with args (<_io.TextIOWrapper name='{tmp_path / 'qqq'}' mode='r'"
            " encoding='UTF-8'>,)\n"
            f"called dmlj.rebuild_all with arg [{tmp_path / 'qqq'!r}, {tmp_path / 'yyy'!r},"
            f" {tmp_path / 'xxx'!r}]\n"
            "called json.dump with args ({'moddirs': {'a': 'b'}, 'components': ['q', 'r'],"
            " 'savedgames': {'x': 'z'}},"
            f" <_io.TextIOWrapper name='{tmp_path / 'qqq'}' mode='w' encoding='UTF-8'>)\n")
    monkeypatch.setattr(testee.dmlj, 'rebuild_all', mock_rebuild_2)
    assert testee.build_jsonconf() == ['xxx', 'yyy']
    assert capsys.readouterr().out == (
            f"called json.load with args (<_io.TextIOWrapper name='{tmp_path / 'qqq'}' mode='r'"
            " encoding='UTF-8'>,)\n"
            f"called dmlj.rebuild_all with arg [{tmp_path / 'qqq~'!r}, {tmp_path / 'qqq'!r},"
            f" {tmp_path / 'yyy'!r}, {tmp_path / 'xxx'!r}]\n"
            "called json.dump with args ({'moddirs': {'a': 'b'}, 'components': ['q', 'r'],"
            " 'savedgames': {'x': 'z'}},"
            f" <_io.TextIOWrapper name='{tmp_path / 'qqq'}' mode='w' encoding='UTF-8'>)\n")


settings_output = """\
called Manager.__init__
called SettingsDialogGui.__init__ with args ({testobj}, {testobj.parent})
called SettingsDialogGui.add_label with args ('Base location for mods:',)
called SettingsDialogGui.add_line_entry with args ('xxx',)
called SettingsDialogGui.add_browse_button with args ({testobj.select_modbase},)
called SettingsDialogGui.add_label with args ('Configuration file name:',)
called SettingsDialogGui.add_line_entry with args ('yyy',)
called SettingsDialogGui.add_label with args ('Location for downloads:',)
called SettingsDialogGui.add_line_entry with args ('zzz',)
called SettingsDialogGui.add_browse_button with args ({testobj.select_download_path},)
called SettingsDialogGui.add_label with args ('Number of columns on screen:',)
called SettingsDialogGui.add_spinbox with args ('qqq',)
called SettingsDialogGui.add_label with args ('Location for save files:',)
called SettingsDialogGui.add_line_entry with args ('rrr',)
called SettingsDialogGui.add_browse_button with args ({testobj.select_savepath},)
called SettingsDialogGui.add_buttonbox with args ([('&Save', {testobj.update}), ('&Close', {testobj.doit.reject})],)
called SettingsDialogGui.set_focus with args ('line_entry',)
"""
delete_output = """\
called Manager.__init__
called JsonConf.__init__ with args () {{}}
called DeleteDialogGui.__init__ with args ({testobj}, {testobj.parent})
called Conf.list_all_mod_dirs
called Conf.get_diritem_data with args ('xxx', 'SCRNAM')
called Conf.get_diritem_data with args ('yyy', 'SCRNAM')
called DeleteDialogGui.add_combobox with args (['select a mod to remove from the config', 'xxx_name', 'yyy_name'], {testobj.process}) {{'editable': False}}
called DeleteDialogGui.add_buttonbox with args ([('&Remove', {testobj.update}, False), ('&Close', {testobj.doit.accept}, True)],)
called DeleteDialogGui.set_focus with args ('combobox',)
"""
attributes_output = """\
called Manager.__init__
called JsonConf.__init__ with args () {{}}
called AttributesDialogGui.__init__ with args ({testobj}, {testobj.parent})
called Conf.list_all_mod_dirs
called Conf.get_diritem_data with args ('xxx', 'SCRNAM')
called Conf.get_diritem_data with args ('yyy', 'SCRNAM')
called AttributesDialogGui.add_combobox with args (['select a mod to change the screen text etc.', 'xxx_name', 'yyy_name'], {testobj.process}) {{'editable': False}}
called AttributesDialogGui.add_label with args ('Screen Name:\\n(the suggestions in the box below are taken from\\nthe mod components',)
called AttributesDialogGui.start_line_with_clear_button
called AttributesDialogGui.add_combobox with args ([], {testobj.enable_change}) {{'editable': True, 'enabled': False}}
called AttributesDialogGui.add_clear_button with args ({testobj.clear_name_text},) {{}}
called AttributesDialogGui.add_label with args ('Screen Text:\\n(to add some information e.q. if the mod is broken)',)
called AttributesDialogGui.start_line_with_clear_button
called AttributesDialogGui.add_line_entry with args ('', {testobj.enable_change}) {{'enabled': False}}
called AttributesDialogGui.add_clear_button with args ({testobj.clear_text_text},) {{}}
called AttributesDialogGui.add_checkbox with args ('This mod can be activated by itself', {testobj.enable_change}) {{'enabled': False}}
called AttributesDialogGui.add_checkbox with args ('Do not touch when (de)activating for a save', {testobj.enable_change}) {{'enabled': False}}
called AttributesDialogGui.add_button with args ('View &Components', {testobj.view_components}) {{'enabled': False}}
called AttributesDialogGui.add_button with args ('View &Dependencies', {testobj.view_dependencies}) {{'enabled': False}}
called AttributesDialogGui.add_buttonbox with args ([('&Update', {testobj.update}, False), ('&Add dependency', {testobj.add_dep}, False), ('&Close', {testobj.doit.accept}, True)],)
called AttributesDialogGui.set_focus with args ('combobox',)
"""
dependency_output = """\
called DependencyDialogGui.__init__ with args ({testobj}, namespace(maingui=namespace(modnames={{'xxx': 'Xxx'}}, choice='xxx')))
called Conf.list_all_mod_dirs
called Conf.get_diritem_data with args ('xxx', 'SCRNAM')
called Conf.get_diritem_data with args ('yyy', 'SCRNAM')
called DependencyDialogGui.add_label with args ('Selecteer de toe te voegen dependency',)
called DependencyDialogGui.add_combobox with args (['select a mod', 'xxx_name', 'yyy_name'], None) {{'editable': False}}
called Conf.list_components_for_dir with arg 'Xxx'
called DependencyDialogGui.add_label with args ('Selecteer een component om de dependency aan toe te voegen',)
called DependencyDialogGui.add_combobox with args (['select a component', 'xxx', 'yyy'], None) {{'editable': False, 'enabled': True}}
called DependencyDialogGui.add_label with args ('Bij Add wordt de dependency direct aan de configuratie toegevoegd',)
called DependencyDialogGui.add_buttonbox with args ([('&Add dependency', {testobj.accept}), ('&Close', {testobj.doit.reject})],)
called DependencyDialogGui.set_focus with args ('combobox',)
"""
dependency_output_2 = """\
called DependencyDialogGui.__init__ with args ({testobj}, namespace(maingui=namespace(modnames={{'xxx': 'Xxx'}}, choice='xxx')))
called Conf.list_all_mod_dirs
called DependencyDialogGui.add_label with args ('Selecteer de toe te voegen dependency',)
called DependencyDialogGui.add_combobox with args (['select a mod'], None) {{'editable': False}}
called Conf.list_components_for_dir with arg 'Xxx'
called DependencyDialogGui.add_label with args ('De dependency wordt toegevoegd aan onderstaande component',)
called DependencyDialogGui.add_combobox with args (['yyy'], None) {{'editable': False, 'enabled': False}}
called DependencyDialogGui.add_label with args ('Bij Add wordt de dependency direct aan de configuratie toegevoegd',)
called DependencyDialogGui.add_buttonbox with args ([('&Add dependency', {testobj.accept}), ('&Close', {testobj.doit.reject})],)
called DependencyDialogGui.set_focus with args ('combobox',)
"""
savegames_output = """\
called SaveGamesDialogGui.__init__ with args ({testobj}, {testobj.parent})
called Conf.list_all_mod_savetemitems
called Conf.list_all_mod_dirs
called Conf.get_diritem_data with args ('xxx', 'SCRNAM')
called Conf.get_diritem_data with args ('yyy', 'SCRNAM')
called SaveGamesDialogGui.add_combobox with args (['select a saved game', 'qqq', 'rrr'], {testobj.get_savedata}) {{'editable': False}}
called SaveGamesDialogGui.add_label with args ('Player name:',)
called SaveGamesDialogGui.add_line_entry with args ('',)
called SaveGamesDialogGui.add_label with args ('Farm name:',)
called SaveGamesDialogGui.add_line_entry with args ('',)
called SaveGamesDialogGui.add_label with args ('In-game date:',)
called SaveGamesDialogGui.add_line_entry with args ('',)
called SaveGamesDialogGui.start_modselect_block with args ('Uses:',)
called SaveGamesDialog.add_modselector
called SaveGamesDialogGui.add_buttonbox with args ([('&Update config', {testobj.update}, False), ('&Activate Mods', {testobj.confirm}, False), ('&Close', {testobj.doit.accept}, True)],)
called SaveGamesDialogGui.set_focus with args ('combobox',)
"""

@pytest.fixture
def expected_output():
    "fixture giving output predictions"
    return {'settings': settings_output, 'delete': delete_output, 'attrs': attributes_output,
            'deps': dependency_output, 'deps2': dependency_output_2, 'saves': savegames_output}
