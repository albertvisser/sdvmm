"""unittests for ./src/tkgui.py
"""
import types
import pytest
from src import tkgui as testee


def _test_show_dialog(monkeypatch, capsys):
    """unittest for tkgui.show_dialog
    """
    assert testee.show_dialog(cls, parent, *args, **kwargs) == "expected_result"
    assert capsys.readouterr().out == ("")


class TestShowMods:
    """unittest for tkgui.ShowMods
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for tkgui.ShowMods object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ShowMods.__init__ with args', args)
        monkeypatch.setattr(testee.ShowMods, '__init__', mock_init)
        testobj = testee.ShowMods()
        assert capsys.readouterr().out == 'called ShowMods.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ShowMods.__init__
        """
        testobj = testee.ShowMods(master)
        assert capsys.readouterr().out == ("")

    def _test_setup_screen(self, monkeypatch, capsys):
        """unittest for ShowMods.setup_screen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_screen() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setup_actions(self, monkeypatch, capsys):
        """unittest for ShowMods.setup_actions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_actions() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_refresh_widgets(self, monkeypatch, capsys):
        """unittest for ShowMods.refresh_widgets
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.refresh_widgets(first_time=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_items_to_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.add_items_to_grid
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_items_to_grid(root, items) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_checkbox(self, monkeypatch, capsys):
        """unittest for ShowMods.add_checkbox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_checkbox(root, colnum, rownum, selectable) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_refresh_widget_data(self, monkeypatch, capsys):
        """unittest for ShowMods.refresh_widget_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.refresh_widget_data(texts_also=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_texts_for_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.set_texts_for_grid
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_texts_for_grid(positions, widgets) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_build_screen_text(self, monkeypatch, capsys):
        """unittest for ShowMods.build_screen_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_screen_text(widgets, name, text, updateid) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_checks_for_grid(self, monkeypatch, capsys):
        """unittest for ShowMods.set_checks_for_grid
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_checks_for_grid(positions, widgets) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_screen(self, monkeypatch, capsys):
        """unittest for ShowMods.show_screen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_screen() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_stop(self, monkeypatch, capsys):
        """unittest for ShowMods.stop
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.stop(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_button(self, monkeypatch, capsys):
        """unittest for ShowMods.enable_button
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_button() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_update(self, monkeypatch, capsys):
        """unittest for ShowMods.update
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.update() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_manage_attributes(self, monkeypatch, capsys):
        """unittest for ShowMods.manage_attributes
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.manage_attributes() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_confirm(self, monkeypatch, capsys):
        """unittest for ShowMods.confirm
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.confirm() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_manage_savefiles(self, monkeypatch, capsys):
        """unittest for ShowMods.manage_savefiles
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.manage_savefiles() == "expected_result"
        assert capsys.readouterr().out == ("")


class _TestAttributesDialog:
    """unittest for tkgui.AttributesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for tkgui.AttributesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called AttributesDialog.__init__ with args', args)
        monkeypatch.setattr(testee.AttributesDialog, '__init__', mock_init)
        testobj = testee.AttributesDialog()
        assert capsys.readouterr().out == 'called AttributesDialog.__init__ with args ()\n'
        return testobj


class _TestSaveGamesDialog:
    """unittest for tkgui.SaveGamesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for tkgui.SaveGamesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SaveGamesDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SaveGamesDialog, '__init__', mock_init)
        testobj = testee.SaveGamesDialog()
        assert capsys.readouterr().out == 'called SaveGamesDialog.__init__ with args ()\n'
        return testobj
