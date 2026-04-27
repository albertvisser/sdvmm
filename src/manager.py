"""Stardew Valley Expansion manager
Oorspronkelijk idee: selecteer uit een lijst met mogelijkheden welke je actief wilt hebben
"""
import os
import json
import pathlib
import contextlib
import shutil
import zipfile
import tempfile
import subprocess
import functools
from src import gui
import src.jsonconfig as dmlj
MODBASE, CONFIG, DOWNLOAD = dmlj.read_defaults()[:3]


def main(rebuild=False):
    "main line"
    if rebuild or (CONFIG and not os.path.exists(CONFIG)):
        messages = build_jsonconf()
        if messages:
            print('Config was (re)built with the following messages:')
            for line in messages:
                print(line)
            print()
    DoIt = Manager()
    DoIt.build_and_start_gui()


class Manager:
    "Processing class (the one that contains the application logic (except the GUI stuff)"
    SEL_TITLE = ('Dit overzicht toont de namen van mods die je kunt activeren'
                 ' (inclusief die al geactiveerd zijn).\n'
                 'In de achterliggende configuratie is geregeld welke mods'
                 ' hiervoor eventueel nog meer aangezet moeten worden\n'
                 'De blauw gekleurde items zijn hyperlinks; ze leiden naar de pagina'
                 ' waarvandaan ik ze van gedownload heb (doorgaans op Nexus)')
    DEP_TITLE = ('Hieronder volgen afhankelijkheden; deze zijn niet'
                 ' apart te activeren maar je kunt wel zien of ze actief zijn')
    BUTTON_LIST = [{"name": "dflt", "text": 'Set &Defaults',
                    "tooltip": "define key locations for the application"},
                   {"name": "inst", "text": '&Install / update', "tooltip": 'Selecteer uit een lijst'
                    ' met recent gedownloade mods één of meer om te installeren'},
                   {"name": "rmv", "text": '&Remove',
                    "tooltip": "Selecteer mods om van het scherm te verwijderen"},
                   {"name": "attr", "text": '&Mod attributes', "tooltip": "Set/Change selectability,"
                    " View components and dependencies of a mod etc."},
                   {"name": "actv", "text": '&Activate changes',
                    "tooltip": "Make the game work with the indicated selection of mods"},
                   {"name": "sel", "text": '&Select Savefile',
                    "tooltip": "Activate mods associated with a selected save file"},
                   {"name": "close", "text": '&Close', "tooltip": "Sluit de applicatie af"}]

    def __init__(self):
        self.conf = dmlj.JsonConf(CONFIG)
        if CONFIG:
            self.conf.load()
        self.modnames = []
        self.modbase = MODBASE
        self.downloads = DOWNLOAD
        self.maxcol = dmlj.read_defaults()[3] or 3
        self.directories = set()
        self.screeninfo = {}
        self.revlookup = {}
        self.complookup = {}
        self.unplotted = []
        self.not_selectable = []
        self.plotted_widgets = {}
        self.plotted_positions = {}
        self.unplotted_widgets = {}
        self.unplotted_positions = {}
        self.nonsel_widgets = {}
        self.nonsel_positions = {}

    def build_and_start_gui(self):
        """build screen: make the user select from a list which expansions they want to have active
        """
        # self.initializing = True
        self.extract_screeninfo()
        self.doit = gui.ShowMods(self)
        # self.doit.setup_screen()
        self.BUTTON_LIST[0]["callback"] = self.manage_defaults
        self.BUTTON_LIST[1]["callback"] = self.doit.update_mods
        self.BUTTON_LIST[2]["callback"] = self.manage_deletions
        self.BUTTON_LIST[3]["callback"] = self.manage_attributes
        self.BUTTON_LIST[4]["callback"] = self.doit.confirm
        self.BUTTON_LIST[5]["callback"] = self.manage_savefiles
        self.BUTTON_LIST[6]["callback"] = self.doit.close
        self.doit.create_selectables_title(self.SEL_TITLE)
        self.doit.create_selectables_grid()
        self.doit.create_dependencies_title(self.DEP_TITLE)
        self.doit.create_dependencies_grid()
        self.doit.create_buttons(self.BUTTON_LIST)
        self.doit.refresh_widgets(first_time=True)
        self.doit.setup_actions()
        # self.initializing = False
        self.doit.show_screen()

    def extract_screeninfo(self):
        """map the config info for a mod to its screen name

        read the 'position' key from the config entries that will be presented and remove them
        temporarily from the config
        allows for the key not being present due to the screen never being reorganized
        """
        # dit is waar ik de modname bij in wilthouden zodat ik ondanks schermmnaam wijzigen
        # toch bij de correcte mod kan uitkomen (issue #1106)
        # breakpoint()
        if not CONFIG:
            return
        for dirname in self.conf.list_all_mod_dirs():
            self.screeninfo[dirname] = {
                'nam': self.conf.get_diritem_data(dirname, self.conf.SCRNAM) or dirname,
                'sel': self.conf.get_diritem_data(dirname, self.conf.SEL) or False,
                'opt': self.conf.get_diritem_data(dirname, self.conf.OPTOUT) or False,
                'key': self.conf.get_diritem_data(dirname, self.conf.NXSKEY) or '',
                'txt': self.conf.get_diritem_data(dirname, self.conf.SCRTXT) or ''}
            self.revlookup[self.screeninfo[dirname]['nam']] = dirname
            # bedacht voor dependents cross reference, maar misschien breder bruikbaar?
            for component in self.conf.get_diritem_data(dirname, self.conf.COMPS):
                self.complookup[component] = dirname

    def order_widgets(self, selectable_container, dependencies_container, first_time=True):
        """reshuffle the lists and dicts containing the widget info:
        """
        if first_time:
            # rownum, colnum = 0, 0
            for text, data in self.screeninfo.items():
                # if data['pos']:
                #     rownum, colnum = [int(y) for y in data['pos'].split('x', 1)]
                #     self.plotted_widgets[(rownum, colnum)] = self.add_checkbox(data['sel'])
                #     self.plotted_positions[(rownum, colnum)] = text, data
                #     selectable_container.addLayout(self.plotted_widgets[(rownum, colnum)][0],
                #                                    rownum, colnum)
                #     self.lastrow, self.lastcol = max((self.lastrow, self.lastcol), (rownum, colnum))
                # elif data['sel']:
                # if data['sel']:
                if data.get('sel', ''):
                    self.unplotted.append(text)
                else:
                    self.not_selectable.append(text)
        else:  # if reorder_widgets:
            for coords, widgetlist in self.unplotted_widgets.items():
                self.doit.remove_widgets(widgetlist, selectable_container, coords[0], coords[1])
            for coords, widgetlist in self.nonsel_widgets.items():
                self.doit.remove_widgets(widgetlist, dependencies_container, coords[0], coords[1])
        self.unplotted_positions, self.unplotted_widgets = self.add_items_to_grid(
            selectable_container, self.unplotted)
        self.nonsel_positions, self.nonsel_widgets = self.add_items_to_grid(
            dependencies_container, self.not_selectable)
        self.refresh_widget_data(texts_also=True)

    def add_items_to_grid(self, grid, items):
        """create the screen widgets and and remember their positions
        """
        rownum, colnum = 0, -1
        widgets = {}
        positions = {}
        for text in sorted(items, key=lambda x: self.screeninfo[x]['nam']):
            colnum += 1
            if colnum == self.maxcol:
                rownum += 1
                colnum = 0
            widgets[(rownum, colnum)] = self.doit.add_checkbox(grid, rownum, colnum,
                                                               self.screeninfo[text]['sel'])
            positions[(rownum, colnum)] = text, self.screeninfo[text]
            self.screeninfo[text]['pos'] = f'{rownum}x{colnum}'
        return positions, widgets

    def refresh_widget_data(self, texts_also=False):
        """actually set the extra texts and checks
        """
        # sel_positions = self.plotted_positions | self.unplotted_positions
        # sel_widgets = self.plotted_widgets | self.unplotted_widgets
        if texts_also:
            # self.doit.set_texts_for_grid(sel_positions, sel_widgets)
            self.set_texts_for_grid(self.unplotted_positions, self.unplotted_widgets)
            self.set_texts_for_grid(self.nonsel_positions, self.nonsel_widgets)
        # self.doit.set_checks_for_grid(sel_positions, sel_widgets)
        self.set_checks_for_grid(self.unplotted_positions, self.unplotted_widgets)
        self.set_checks_for_grid(self.nonsel_positions, self.nonsel_widgets)

    def set_texts_for_grid(self, positions, widgets):
        """add texts to the widgets
        """
        for pos, info in positions.items():
            data = info[1]
            self.doit.set_label_text(widgets[pos], data['nam'], data['key'], data['txt'])

    def build_link_text(self, name, updateid):
        """use updateid and name to create text for a clickable link

        (kept here in case we find out how to use this in the tk version as well)
        """
        return f'<a href="https://www.nexusmods.com/stardewvalley/mods/{updateid}">{name}</a>'

    def set_checks_for_grid(self, positions, widgets):
        "determine what value to set the checkboxes to"
        for pos, info in positions.items():
            # data = info[1]
            # loc = os.path.join(self.modbase, data['dir'])
            loc = os.path.join(self.modbase, info[0])
            self.doit.set_checkbox_state(widgets[pos], os.path.exists(loc))

    def process_activations(self):
        """process changes in mods to activate
        """
        modnames = self.get_activated_activatable_mods()
        # modnames = []
        # for widgetlist in self.unplotted_widgets.values():
        #     name = self.doit.get_labeltext_if_checked(widgetlist)
        #     if name:
        #         modnames.append(name)
        self.select_activations(modnames)
        if self.directories:   # alleen leeg als er niks aangevinkt is
            self.activate()
        self.refresh_widget_data()

    def get_activated_activatable_mods(self):
        """return a list of mods that can be selected and have been selected
        (mods that cannot be selected directly are not of interest here)
        """
        modnames = []
        for widgetlist in self.unplotted_widgets.values():
            name = self.doit.get_labeltext_if_checked(widgetlist)
            if name:
                modnames.append(name)
        return modnames

    def select_activations(self, modnames):
        "expand the selection to a list of directories"
        # determine which directories should be activated
        # breakpoint()
        self.directories = set()
        for name in modnames:
            # moddir = self.screeninfo[item]['dir']
            moddir = self.revlookup[name]
            for entry in self.conf.list_components_for_dir(moddir):
                compdir = get_toplevel(self.conf.get_component_data(entry, self.conf.DIR))
                self.directories.add(compdir)
                self.add_dependencies(entry)

    def add_dependencies(self, entry):
        "expand an item with a list of subitems"
        deps = self.conf.get_component_data(entry, self.conf.DEPS)
        for dep in deps:
            depdir = get_toplevel(self.conf.get_component_data(dep, self.conf.DIR))
            self.directories.add(depdir)
            self.add_dependencies(dep)

    def activate(self):
        "activate by making directories hidden or not"
        for entry in os.scandir(self.modbase):
            # leave my files alone!
            if entry.is_file():
                continue
            # if smapi, do not deactivate
            if entry.name in ('ConsoleCommands', 'SaveBackup'):
                # skip SMAPI componenten
                continue
            # if in list and deactivated, re-activate
            if entry.name.startswith('.'):
                if entry.name[1:] in self.directories:
                    os.rename(entry, os.path.join(self.modbase, entry.name[1:]))
            # if not in list and activated, deactivate
            elif entry.name not in self.directories:
                os.rename(entry, os.path.join(self.modbase, '.' + entry.name))

    def manage_attributes(self):
        """handle dialog for showing / changing screen name, selectability and extra text

        also the possibility to view components and dependencies
        """
        self.attr_changes = {}  # list of changed mods
        gui.show_dialog(AttributesDialog, self.doit, self.conf)
        # screeninfo is updated in the dialog, here we update the configuration
        # attr_changes is also changed in the dialog (through calling update_attributes)
        changes = False
        for dirname, oldname in self.attr_changes.items():
            newname = self.screeninfo[dirname]['nam']
            self.conf.set_diritem_value(dirname, self.conf.SCRNAM, newname)
            self.conf.set_diritem_value(dirname, self.conf.SCRTXT, self.screeninfo[dirname]['txt'])
            self.conf.set_diritem_value(dirname, self.conf.SEL, self.screeninfo[dirname]['sel'])
            self.conf.set_diritem_value(dirname, self.conf.OPTOUT, self.screeninfo[dirname]['opt'])
            # also update reverse lookup
            self.revlookup[newname] = self.revlookup.pop(oldname)
            changes = True
        if changes:
            self.conf.save()

    def get_mod_components(self, modname):
        "build a message containing a list of mod components"
        # verplaatst naar aanroepende methode omdat die nu in deze module zit

    def get_mod_dependencies(self, modname):
        "build a imessage containing a list of mod dependencies"
        # verplaatst naar aanroepende methode omdat die nu in deze module zit

    def update_attributes(self, selectable, name, oldname, text, is_exempt):
        "do the updating (called from the dialog each time a mod is modified)"
        # we kunnen er van uitgaan dat de screeninfo values altijd alle waarden bevatten
        # zie methode extract_screeninfo
        # 1106: we gaan hier zorgen dat de key van screeninfo niet meer aangepast hoeft te worden
        # nieuwe variant
        # breakpoint()
        dirname = self.revlookup[oldname]
        self.attr_changes[dirname] = oldname
        oldselect = self.screeninfo[dirname]['sel']
        # oldtext = self.screeninfo[dirname]['txt']
        self.screeninfo[dirname]['sel'] = selectable
        self.screeninfo[dirname]['nam'] = name
        self.screeninfo[dirname]['txt'] = text
        self.screeninfo[dirname]['opt'] = is_exempt
        rownum, colnum = [int(y) for y in self.screeninfo[dirname]['pos'].split('x', 1)]
        if selectable != oldselect:
            # self.switch_by_selectability(selectable, dirname)
            if selectable:
                self.not_selectable.remove(dirname)
                self.unplotted.append(dirname)
            else:
                self.unplotted.remove(dirname)
                self.not_selectable.append(dirname)
            self.doit.refresh_widgets()  # not first_time
        else:  # if text != oldtext or name != oldname: moet ook bij naam terugzetten
            # alleen schermtekst wijzigen
            # widgetlist = self.get_widget_list(rownum, colnum, oldselect)
            widgetlist = self.unplotted_widgets if selectable else self.nonsel_widgets
            self.doit.set_label_text(widgetlist[(rownum, colnum)], name,
                                     self.screeninfo[dirname]['key'], text)

    def switch_by_selectability(self, selectable, name):
        "move screeninfo keys to from unplotted to not_selectable or vice versa"
        # versimpeld en daarom teruggestopt in de aanroeper

    def get_widget_list(self, rownum, colnum, selectable):
        "retrieve list of windows depending on screen location and selectability"
        # versimpeld en daarom teruggestopt in de aanroeper

    def manage_savefiles(self):
        "handle dialog for selecting a savefile to perform actions on"
        # changes = False
        gui.show_dialog(SaveGamesDialog, self.doit, self.conf)
        # if changes:
        #     self.conf.save()

    def update_mods(self, names):
        "installeer de aangegeven mod files"
        save_needed = got_new_mod = False
        report = []
        for zipfilename in names:
            roots, mod_existed, mod_was_active, messages = self.install_zipfile(zipfilename)
            report.extend(messages)
            if not roots or roots == ['']:  # just (a) file(s), e.g. ConfigEditor.html
                continue
            configdata = self.get_data_for_config(roots, mod_was_active)
            moddir = self.determine_moddir(roots)
            if mod_existed:
                messages, conf_changed = self.update_mod_settings(moddir, configdata)
                save_needed = save_needed or conf_changed
            else:
                messages = self.add_mod_to_config(moddir, configdata)
                save_needed = got_new_mod = True
            report.extend(messages)
            move_zip_after_installing(zipfilename)
        if save_needed:
            self.conf.save()
        if got_new_mod:
            self.screeninfo = {}
            self.extract_screeninfo()
            self.doit.refresh_widgets()  # not first_time=True)
        return report

    def install_zipfile(self, zipfilename):
        "unzip and update config if necessary"
        # roots = []
        with zipfile.ZipFile(zipfilename) as archive:
            names = archive.namelist()
            roots = get_archive_roots(names)
            mod_existed, mod_was_active = check_if_active(roots)
            smapi_install = check_if_smapi(roots)
            if not smapi_install:
                archive.extractall(self.modbase)
        if not roots:
            return [], None, None, [f'{zipfilename}: zipfile appears to be empty']
        if smapi_install:
            termprog = dmlj.read_defaults()[-2]
            if not termprog:
                termprog = 'gnome-terminal'
            installdir = os.path.join('/tmp', roots.pop())
            subprocess.run(['unzip', zipfilename, '-d', '/tmp'], check=True)
            subprocess.run([termprog], cwd=installdir)  # , capture_output=True)
            move_zip_after_installing(zipfilename)
            return [], None, None, ["SMAPI-install is waiting in a terminal window to be finished"
                                    " by executing './install on Linux.sh'"]
        if os.path.exists(os.path.join(self.modbase, '__MACOSX')):  # remove junk
            shutil.rmtree(os.path.join(self.modbase, '__MACOSX'))
        result = [f'{zipfilename} is successfully installed']
        return roots, mod_existed, mod_was_active, result

    def determine_moddir(self, roots):
        "Ask for mod entry point if necessary"
        if len(roots) > 1:
            root = ''
            while not root:
                root = self.doit.select_value('Select one of the directories as the'
                                              ' "mod base"', roots, False, True)
        else:
            root = roots[0]
        return root

    def get_data_for_config(self, roots, mod_was_active):
        """inspect mod directory/ies for items to be included in configuration

        while looping over them, deactivate when necessary
        """
        configdata = {}
        for rootitem in roots:
            importpath = pathlib.Path(self.modbase) / rootitem
            configdata[rootitem] = dmlj.build_entry_from_dir(importpath)
            if not mod_was_active:
                os.rename(os.path.join(self.modbase, f'{rootitem}'),
                          os.path.join(self.modbase, f'.{rootitem}'))
        return configdata

    def add_mod_to_config(self, moddir, configdata):
        "add info about mod to configuration"
        # {{<uitpakdir>: {<component>: {<key>: <value>, ...}, ...}, ...}}
        if self.conf.has_moddir(moddir):
            raise ValueError(f'New mod "{moddir}" exists in configuration, should not be possible')
        messages = []
        names = set()
        keys = set()
        self.conf.add_diritem(moddir)
        complist = []
        for data in configdata.values():
            for component, compdict in data.items():
                complist.append(component)
                self.conf.add_componentdata(component)
                for key, value in compdict.items():
                    if key == self.conf.NAME:
                        names.add(value)
                    elif key == self.conf.NXSKEY:
                        keys.add(value.strip().replace('?', '').split('@')[0])
                    self.conf.set_componentdata_value(component, key, value)
        self.conf.set_diritem_value(moddir, self.conf.COMPS, complist)
        # bepaal (voorlopige) schermtekst
        screentext = sorted(names)[0] if names else '(new mod)'
        self.conf.set_diritem_value(moddir, self.conf.SCRNAM, screentext)
        select = ', multiple possibilities found' if names else ''
        messages.append(f"  Screentext set to '{screentext}' {select}")
        # bepaal updateid en check voor multiple
        oldid, more_ids = determine_update_id(keys)
        select = f', multiple values found: {more_ids} ' if more_ids else ''
        self.conf.set_diritem_value(moddir, self.conf.NXSKEY, oldid)
        messages.append(f"  Update ID set to {oldid} {select}")
        messages.append('  Change the "Selectable" setting if you want to be able to activate'
                        ' the mod')
        self.conf.set_diritem_value(moddir, self.conf.SEL, False)
        return messages

    def update_mod_settings(self, moddir, configdata):
        "update info about mod if necessary"
        if not self.conf.has_moddir(moddir):
            raise ValueError('Installed mod is not in configuration, should not be possible')
        messages, conf_changed = [], False
        olddata = self.conf.get_diritem_data(moddir, self.conf.COMPS)
        newdata = []
        for data in configdata.values():
            for component in data:
                newdata.append(component)
        if newdata != olddata:
            messages.append(f"  List of components changed from {olddata} to {newdata}")
            self.conf.set_diritem_value(moddir, self.conf.COMPS, newdata)
            conf_changed = True
        for data in configdata.values():
            for component, compdict in data.items():
                oldcomp = self.conf.get_component_data(component)
                for key, value in compdict.items():
                    if key not in oldcomp:
                        messages.append(f"  {component}: new key {key} added"
                                        f" with value '{value}'")
                        self.conf_changed = True
                    elif value != oldcomp[key]:
                        messages.append(f"  {component}: {key} changed from '{oldcomp[key]}'"
                                        f" to '{value}'")
                        conf_changed = True
                for key, value in oldcomp.items():
                    if key not in compdict:
                        messages.append(f"  {component}: key {key} with value '{value}' removed")
                        conf_changed = True
                if conf_changed:
                    self.conf.update_componentdata(component, compdict)
        return messages, conf_changed

    def manage_defaults(self):
        """handle dialog for settings several application defaults
        """
        origdata = dmlj.read_defaults(bare=True)
        self.dialog_data = list(origdata)
        self.dialog_data[3] = self.maxcol
        gui.show_dialog(SettingsDialog, self.doit)
        if self.dialog_data != origdata:
            dmlj.save_defaults(*self.dialog_data)
            self.maxcol = self.dialog_data[3]

    def manage_deletions(self):
        "call up a dialog to select mods to remove"
        gui.show_dialog(DeleteDialog, self.doit, self.conf)

    def remove_mod(self, modname):
        "remove a mod from the config"
        # remove from screen attributes dict
        moddir = self.revlookup[modname]
        self.screeninfo.pop(moddir)
        with contextlib.suppress(ValueError):
            self.unplotted.remove(moddir)
        with contextlib.suppress(ValueError):
            self.not_selectable.remove(moddir)
        # refresh names on screen
        self.doit.refresh_widgets(first_time=False)
        # remove from config
        components = self.conf.list_components_for_dir(moddir)
        for comp in components:
            self.conf.remove_componentdata(comp)
        self.conf.remove_diritem(moddir)
        self.conf.save()


class SettingsDialog:
    """Dialog for changing some application defaults
    """
    def __init__(self, parent):
        self.parent = parent
        # breakpoint()
        # data = self.parent.master.dialog_data
        self.doit = gui.SettingsDialogGui(self, parent)
        self.doit.add_label('Base location for mods:')
        self.modbase_text = self.doit.add_line_entry(self.parent.master.dialog_data[0])
        self.select_modbase_button = self.doit.add_browse_button(self.select_modbase)
        self.doit.add_label('Configuration file name:')
        self.config_text = self.doit.add_line_entry(self.parent.master.dialog_data[1])
        self.doit.add_label('Location for downloads:')
        self.download_text = self.doit.add_line_entry(self.parent.master.dialog_data[2])
        self.select_download_button = self.doit.add_browse_button(self.select_download_path)
        self.doit.add_label('Number of columns on screen:')
        self.columns = self.doit.add_spinbox(self.parent.master.dialog_data[3])
        self.doit.add_label('Terminal program to use:')
        self.termprog_text = self.doit.add_line_entry(self.parent.master.dialog_data[4])
        self.doit.add_label('Location for save files:')
        self.savepath_text = self.doit.add_line_entry(self.parent.master.dialog_data[5])
        self.select_savepath_button = self.doit.add_browse_button(self.select_savepath)
        self.doit.add_buttonbox([('&Save', self.update), ('&Close', self.doit.reject)])
        self.doit.set_focus(self.modbase_text)

    def select_modbase(self):
        "define mod location"
        oldmodbase = self.doit.get_widget_text(self.modbase_text) or '~'
        filename = self.doit.select_directory("Where to install downloaded mods?",
                                              os.path.expanduser(oldmodbase))
        if filename:
            self.doit.set_widget_text(self.modbase_text,
                                      filename.replace(os.path.expanduser('~'), '~'))

    def select_download_path(self):
        "define download location"
        olddownload = self.doit.get_widget_text(self.download_text) or '~'
        filename = self.doit.select_directory("Where to download mods to?",
                                              os.path.expanduser(olddownload))
        if filename:
            self.doit.set_widget_text(self.download_text,
                                      filename.replace(os.path.expanduser('~'), '~'))

    def select_savepath(self):
        "define savefile location"
        oldsavepath = self.doit.get_widget_text(self.savepath_text) or '~'
        filename = self.doit.select_directory("Where are the saved games stored?",
                                              os.path.expanduser(oldsavepath))
        if filename:
            self.doit.set_widget_text(self.savepath_text,
                                      filename.replace(os.path.expanduser('~'), '~'))

    def update(self):
        "update settings and exit"
        termprog = self.doit.get_widget_text(self.termprog_text)
        if not termprog:
            gui.show_message(self.doit,
                             "If you leave this empty you may encounter problems installing SMAPI")
        self.parent.master.dialog_data = (self.doit.get_widget_text(self.modbase_text),
                                          self.doit.get_widget_text(self.config_text),
                                          self.doit.get_widget_text(self.download_text),
                                          int(self.doit.get_widget_text(self.columns)),
                                          termprog,
                                          self.doit.get_widget_text(self.savepath_text))
        self.doit.confirm()


class DeleteDialog:
    """Dialog for viewing and optionally changing a mod's properties
    """
    seltext = 'select a mod to remove from the config'

    def __init__(self, parent, conf):
        self.parent = parent
        self.conf = conf
        self.doit = gui.DeleteDialogGui(self, parent)
        self.choice = ''
        self.modnames = {}
        for x in conf.list_all_mod_dirs():
            name = conf.get_diritem_data(x, conf.SCRNAM) or x
            self.modnames[name] = x
        self.lbox = self.doit.add_combobox([self.seltext] + sorted(self.modnames), self.process,
                                           editable=False)
        self.change_button = self.doit.add_buttonbox([('&Remove', self.update, False),
                                                     ('&Close', self.doit.accept, True)])[0]
        self.doit.set_focus(self.lbox)

    def process(self, *args):
        "determine the selected mod"
        self.choice = self.doit.get_combobox_entry(self.lbox)
        self.doit.enable_button(self.change_button, self.choice != self.seltext)

    def update(self):
        "start the removal"
        self.parent.master.remove_mod(self.choice)
        gui.show_message(self.doit, f'{self.choice} has been removed')
        self.doit.set_combobox_entry(self.lbox, 0)
        self.doit.enable_button(self.change_button, False)
        self.doit.confirm()


class AttributesDialog:
    """Dialog for viewing and optionally changing a mod's properties
    """
    seltext = 'select a mod to change the screen text etc.'

    def __init__(self, parent, conf):
        self.parent = parent
        self.conf = conf
        self.doit = gui.AttributesDialogGui(self, parent)
        self.choice = ''
        self.modnames = {}
        for x in conf.list_all_mod_dirs():
            name = conf.get_diritem_data(x, conf.SCRNAM) or x
            self.modnames[name] = x

        self.lbox = self.doit.add_combobox([self.seltext] + sorted(self.modnames), self.process,
                                           editable=False)
        self.doit.add_label('Screen Name:\n'
                            '(the suggestions in the box below are taken from\n'
                            'the mod components')
        # self.name, self.clear_name_button = self.doit.add_with_clear_button(
        #         self.doit.add_combobox([], self.enable_change, editable=True, enabled=False),
        #         self.clear_name_text)
        self.doit.start_line_with_clear_button()
        self.name = self.doit.add_combobox([], self.enable_change, editable=True, enabled=False)
        self.clear_name_button = self.doit.add_clear_button(self.clear_name_text)
        self.doit.add_label('Screen Text:\n'
                            '(to add some information e.q. if the mod is broken)')
        # self.text, self.clear_text_button = self.doit.add_with_clear_button(
        #         self.doit.add_line_entry('', self.enable_change, enabled=False),
        #         self.clear_text_text)
        self.doit.start_line_with_clear_button()
        self.text = self.doit.add_line_entry('', self.enable_change, enabled=False)
        self.clear_text_button = self.doit.add_clear_button(self.clear_text_text)
        self.activate_button = self.doit.add_checkbox('This mod can be activated by itself',
                                                      self.enable_change, enabled=False)
        self.exempt_button = self.doit.add_checkbox('Do not touch when (de)activating for a save',
                                                    self.enable_change, enabled=False)
        self.backup_button = self.doit.add_button('&Backup Mod Config', self.backup_settings,
                                                  pos=1, enabled=False)
        self.restore_button = self.doit.add_button('&Restore', self.restore_settings,
                                                   pos=2, enabled=False)
        self.compare_button = self.doit.add_menubutton(
            'Co&mpare', ['previous <-> current', 'backup <-> current', 'view current'],
            [self.compare_settings, self.compare_to_backup, self.view_current], pos=3,
            enabled=False)
        self.comps_button = self.doit.add_button('&View Components', self.view_components,
                                                 enabled=False)
        self.deps_button = self.doit.add_button('View &Dependencies', self.view_dependencies,
                                                enabled=False)
        self.depts_button = self.doit.add_button('View De&pendents', self.view_dependents,
                                                 enabled=False)
        self.change_button, self.add_dep_button = self.doit.add_buttonbox([
            ('&Update', self.update, False), ('&Add dependency', self.add_dep, False),
            ('&Close', self.doit.accept, True)])[:-1]
        self.doit.set_focus(self.lbox)

    def enable_change(self):
        "enable change button"
        self.doit.enable_button(self.change_button, True)
        self.doit.enable_button(self.add_dep_button, True)

    def process(self, *args):
        "get description if any"
        # self.select_button.setDisabled(True)
        self.choice = self.doit.get_combobox_value(self.lbox)
        field_list = [self.name, self.clear_name_button, self.text, self.clear_text_button,
                      self.activate_button, self.exempt_button, self.comps_button,
                      self.deps_button, self.depts_button, self.change_button, self.backup_button,
                      self.restore_button, self.compare_button]
        if self.choice == self.seltext:
            self.doit.reset_all_fields(field_list)
            return
        dirname = self.parent.master.revlookup[self.choice]
        items = set()
        for x in self.conf.list_components_for_dir(self.modnames[self.choice]):
            items.add(self.conf.get_component_data(x, self.conf.NAME))
        self.doit.activate_and_populate_fields(field_list, [self.choice] + sorted(list(items)),
                                               self.parent.master.screeninfo[dirname])

    def clear_name_text(self):
        "visually delete screen text"
        self.doit.clear_field(self.name)

    def clear_text_text(self):
        "visually delete additional text if any"
        self.doit.clear_field(self.text)

    def backup_settings(self):
        "store current mod settings - if present - for safekeeping"
        modname = self.modnames[self.choice]
        names, locs = self.conf.find_modsett(modname, 'new')
        if not locs:
            message = 'Geen mod settings gevonden'
        else:
            self.conf.backup_modsett(modname, locs)
            self.conf.save()
            message = 'Mod settings van huidige versie veilig gesteld:'
            message += '\n' + '\n'.join(names)
        gui.show_message(self.doit, message, title='SDVMM mod info')

    def restore_settings(self):
        "retrieve mod settings from older version"
        modname = self.modnames[self.choice]
        # zoek opgeslagen versie
        saveloc = self.conf.find_modsett_backup(modname)
        names, locs = self.conf.find_modsett(modname, 'old')
        # indien gevonden:
        if not saveloc and not locs:
            message = 'Geen mod settings gevonden in vorige versie of in backup'
        else:
            message = ''
            self.doit.dialog_data = {'found': [saveloc, locs]}  # alleen indicaties nodig denk ik
            gui.show_dialog(RestoreDialog, self.doit)
            choices = self.doit.dialog_data.get('choices', '')
            if choices:
                restore_from_backup, restore_from_previous, backup_previous = choices
            else:
                restore_from_backup = restore_from_previous = backup_previous = False
            messagelist = []
            if restore_from_backup:
                self.conf.restore_modsett(modname, frombackup=True)
                messagelist.append('teruggezet van backup')
            elif restore_from_previous:
                self.conf.restore_modsett(locs, fromprevious=True)
                messagelist.append('teruggezet van vorige versie')
            if backup_previous:
                self.conf.backup_modsett(modname, locs)
                self.conf.save()
                messagelist.append('vorige versie veiliggesteld\n' + '\n'.join(names))
            if messagelist:
                message = 'Mod settings '
                if len(messagelist) > 1:
                    message += ', '.join(messagelist[:-1]) + ' en '
                message += messagelist[-1]
        if message:
            gui.show_message(self.doit, message, title='SDVMM mod info')

    def compare_settings(self):
        "compare current mod settings with older version"
        modname = self.modnames[self.choice]
        newlocs = self.conf.find_modsett(modname, 'new')[1]
        oldlocs = self.conf.find_modsett(modname, 'old')[1]
        if newlocs and oldlocs:
            if len(newlocs) == len(oldlocs):
                for ix, loc in enumerate(newlocs):
                    subprocess.run(['meld', loc, oldlocs[ix]])
                message = 'Done.'
            else:
                message = 'Verschillende aantallen mod settings bestanden gevonden'
        elif newlocs and not oldlocs:
            message = 'Alleen mod settings van huidige versie gevonden'
        elif oldlocs and not newlocs:
            message = 'Alleen mod settings van vorige versie gevonden'
        else:
            message = 'Geen mod settings gevonden in vorige en huidige versie'
        gui.show_message(self.doit, message, title='SDVMM mod info')

    def compare_to_backup(self):
        "compare current mod settings with backupped version"
        modname = self.modnames[self.choice]
        newlocs = self.conf.find_modsett(modname, 'new')[1]
        if not self.conf.find_modsett_backup(modname):
            message = 'Geen backup van mod settings gevonden'
        else:
            backups = self.conf._data[self.conf.BAK][modname]
            tmpfile = tempfile.mkstemp()[1]
            for ix, loc in enumerate(newlocs):
                data = backups[loc]
                with open(tmpfile, 'w') as f:
                    json.dump(data, f, indent=2)
                subprocess.run(['meld', loc, tmpfile])
            os.unlink(tmpfile)
            message = 'Done.' if newlocs else 'Geen mod settings gevonden'
        gui.show_message(self.doit, message, title='SDVMM mod info')

    def view_current(self):
        "view config files for current version"
        modname = self.modnames[self.choice]
        newlocs = self.conf.find_modsett(modname, 'new')[1]
        message = 'Geen mod settings gevonden'
        for ix, loc in enumerate(newlocs):
            # subprocess.run(['gnome-terminal', '--', 'vim', loc])  # opent in de achtergrond
            # subprocess.run(['scite', loc])
            message = pathlib.Path(loc).read_text()
            if ix < len(newlocs) - 1:
                gui.show_message(self.doit, message, title='SDVMM mod info')
        gui.show_message(self.doit, message, title='SDVMM mod info')

    def view_components(self):
        "list components for mod"
        complist = []
        modname = self.modnames[self.choice]
        for comp in self.conf.list_components_for_dir(modname):
            text = (f'  {self.conf.get_component_data(comp, self.conf.NAME)} '
                    f'  {self.conf.get_component_data(comp, self.conf.VRS)}\n'
                    f'    ({comp})')
            complist.append(text)
        # message = self.parent.master.get_mod_components(self.modnames[self.choice])
        message = f'Components for {modname}:\n' + '\n'.join(complist)
        gui.show_message(self.doit, message, title='SDVMM mod info')

    def view_dependencies(self):
        "list dependencies for mod"
        deplist = set()
        modname = self.modnames[self.choice]
        for comp in self.conf.list_components_for_dir(modname):
            for dep in self.conf.get_component_data(comp, self.conf.DEPS):
                deplist.add(dep)
        depnames = []
        for dep in sorted(deplist):
            try:
                depname = self.conf.get_component_data(dep, self.conf.NAME)
            except ValueError:
                depname = 'unknown component:'
                depnames.append((depname, dep))
            else:
                depnames.append((depname, f'({dep})'))
        if not depnames:
            depnames = [('None', '')]
        # message = self.parent.master.get_mod_dependencies(self.modnames[self.choice])
        message = f'Dependencies for {modname}:\n' + "\n".join(f' {x} {y}'
                                                               for (x, y) in sorted(depnames))
        gui.show_message(self.doit, message, title='SDVMM mod info')

    def view_dependents(self):
        "list mods that depend on this mod"
        # zoek de dirnaam bij de schermnaam
        modname = self.modnames[self.choice]
        # zoek de componenten bij de dirnaam en zet deze in een lijst
        complist = self.conf.list_components_for_dir(modname)
        # voor alle componenten in de configuratie:
        userlist = set()
        for component in self.conf.list_all_components():
            if component.startswith('YourName'):  # uitzondering voor voorbeeldmods
                continue
            # als componentnaam in de bovengenoemde lijst dan overslaan
            if component in complist:
                continue
            deplist = self.conf.get_component_data(component, self.conf.DEPS)
            # voor alle componenten in de lijst:
            for comp in complist:
                # als componentnaam niet voorkomt in 'Deps' dan overslaan
                if comp in deplist:
                    # voeg de 'dirname' key aan een set (om te ontdubbelen)
                    userlist.add(self.parent.master.complookup[component])
        # herleiden naar schermnamen
        userlist_screennames = []
        for item in userlist:
            userlist_screennames.append(self.conf.get_diritem_data(item, self.conf.SCRNAM))
        if userlist_screennames:
            message = '\n'.join([f'Mods depending on {self.choice}:\n'] + userlist_screennames)
        else:
            message = f'Mods depending on {self.choice}:\n\nNone'
        gui.show_message(self.doit, message, title='SDVMM mod info')

    def update(self):
        "update screentext in dictionary"
        # self.text.setReadOnly(True)
        self.doit.enable_button(self.clear_name_button, False)
        self.doit.enable_button(self.clear_text_button, False)
        selectable = self.doit.get_checkbox_value(self.activate_button)
        text = self.doit.get_field_text(self.text)
        name = self.doit.get_combobox_value(self.name)
        is_exempt = self.doit.get_checkbox_value(self.exempt_button)
        self.parent.master.update_attributes(selectable, name, self.choice, text, is_exempt)
        self.doit.enable_button(self.change_button, False)

    def add_dep(self):
        """add dependency manually
        """
        gui.show_dialog(DependencyDialog, self.doit, self.conf)
        # add new dependency immediately


class RestoreDialog:
    """toon een dialoog die aangeeft welke van de twee gevonden is/zijn en vraagt
    welke er teruggezet moet worden
    vraag ook of de evt. vorige versie gebackupt moet worden indien gevonden
    """
    def __init__(self, parent):
        self.parent = parent
        self.doit = gui.RestoreDialogGui(self, parent)
        # backup_found, oldlocs = self.parent.master.dialog_data['found']
        backup_found, oldlocs = self.parent.dialog_data['found']
        self.from_backup = self.doit.add_checkbox('&1. Restore from backup', backup_found)
        self.from_previous = self.doit.add_checkbox('&2. Restore from previous version',
                                                    bool(oldlocs))
        self.backup_previous = self.doit.add_checkbox("&Backup previous version's settings",
                                                      bool(oldlocs) and not backup_found)
        self.doit.add_buttonbox([('&Ok', self.accept), ('&Cancel', self.doit.reject)])
        self.doit.set_focus(self.from_backup)

    def accept(self):
        "communicate choices to parent"
        from_backup = self.doit.get_checkbox_value(self.from_backup)
        from_previous = self.doit.get_checkbox_value(self.from_previous)
        backup_previous = self.doit.get_checkbox_value(self.backup_previous)
        self.parent.dialog_data['choices'] = [from_backup, from_previous, backup_previous]
        self.doit.accept()


class DependencyDialog:
    """Dialog for manually defining a new dependency
    """
    def __init__(self, parent, conf):
        self.parent = parent
        self.conf = conf
        self.doit = gui.DependencyDialogGui(self, parent)
        current_mod = self.parent.master.modnames[self.parent.master.choice]
        self.modnames = {}
        for x in conf.list_all_mod_dirs():
            if x != current_mod:
                self.modnames[conf.get_diritem_data(x, conf.SCRNAM)] = x
        self.doit.add_label("Selecteer de toe te voegen dependency")
        self.dependency_selector = self.doit.add_combobox(['select a mod'] + sorted(self.modnames),
                                                          None, editable=False)
        components = self.conf.list_components_for_dir(current_mod)
        if len(components) == 1:
            self.doit.add_label('De dependency wordt toegevoegd aan onderstaande component')
            self.component_selector = self.doit.add_combobox(components, None, editable=False,
                                                             enabled=False)
        else:
            self.doit.add_label('Selecteer een component om de dependency aan toe te voegen')
            self.component_selector = self.doit.add_combobox(['select a component'] + components,
                                                             None, editable=False, enabled=True)
        self.doit.add_label("Bij Add wordt de dependency direct aan de configuratie toegevoegd")
        self.doit.add_buttonbox([('&Add dependency', self.accept), ('&Close', self.doit.reject)])
        self.doit.set_focus(self.dependency_selector)

    def accept(self):
        "add dependncy to configuration"
        selected_dependency = self.doit.get_combobox_value(self.dependency_selector)
        selected_component = self.doit.get_combobox_value(self.component_selector)
        dependency_to_add = self.conf.list_components_for_dir(self.modnames[selected_dependency])[0]
        deps = self.conf.get_component_data(selected_component, self.conf.DEPS)
        deps.append(dependency_to_add)
        self.conf.set_componentdata_value(selected_component, self.conf.DEPS, deps)
        self.conf.save()
        gui.show_message(self.doit, 'Add Dependency', 'Wijziging is doorgevoerd\n'
                         'Vergeet niet om na updaten van de mod te controleren of'
                         ' de dependency opnieuw moet worden toegevoegd')
        self.doit.confirm()


class SaveGamesDialog:
    """Dialog for defining and viewing which mods are used for a (to be selected) savefile
    and optionally activating them
    """
    def __init__(self, parent, conf):
        self.parent = parent
        self.conf = conf
        self.doit = gui.SaveGamesDialogGui(self, parent)
        self.savenames = conf.list_all_saveitems()
        self.modnames = {}
        for x in conf.list_all_mod_dirs():
            self.modnames[conf.get_diritem_data(x, conf.SCRNAM)] = x
        self.savegame_selector = self.doit.add_combobox(
            ['select a saved game'] + sorted(self.savenames), self.get_savedata, editable=False)
        self.oldsavename = ''
        self.doit.add_label('Player name:')
        self.pname = self.doit.add_line_entry('')
        self.doit.add_label('Farm name:')
        self.fname = self.doit.add_line_entry('')
        self.doit.add_label('In-game date:')
        self.gdate = self.doit.add_line_entry('')
        self.widgets = []
        self.doit.start_modselect_block('Uses:')
        self.add_modselector(False)
        self.update_button, self.confirm_button = self.doit.add_buttonbox([
            ('&Update config', self.update, False), ('&Activate Mods', self.confirm, False),
            ('&Close', self.doit.accept, True)])[:-1]
        self.doit.set_focus(self.savegame_selector)

    def add_modselector(self, enabled=True):
        "add a selector to make an association between a mod and the save file"
        # lbox, button, container = self.doit.add_with_clear_button(
        #         self.doit.add_combobox(['select a mod'] + sorted(self.modnames), None,
        #                               editable=True, enabled=False), bool(name))
        # print('in add_modselector')
        lbox = self.doit.add_combobox(['select a mod'] + sorted(self.modnames), None,
                                      editable=True, enabled=enabled)
        button, container = self.doit.add_clear_button(enabled)
        self.doit.set_callbacks((lbox, button), (functools.partial(self.process_mod, lbox),
                                                 functools.partial(self.remove_mod, button)))
        self.widgets.append([button, lbox, container])
        # print(f'  added {lbox=}, {button=} to {container=}')
        # print(f'  {len(self.widgets)=}', flush=True)

    def process_mod(self, lbox, newvalue):
        """add or change an association between a mod and the save file

        creates a new selector if changing the last one from empty to non-empty
        """
        # print(f'in process_mod, {lbox=}, {newvalue=}', flush=True)
        if newvalue == 'select a mod':
            return
        for item in self.widgets:
            if item[1] == lbox:
                self.doit.enable_widget(item[0], True)
        self.doit.enable_widget(self.update_button, True)
        if lbox == self.widgets[-1][1]:  # and len(self.widgets) > len(self.prevmods):
            self.add_modselector()

    def remove_mod(self, btn):
        "delete an association between a mod and the save file"
        # print(f'in remove_mod, {btn=}', flush=True)
        for item in self.widgets:
            if item[0] == btn:
                self.doit.remove_modselector(item)
                self.widgets.remove(item)
        self.doit.enable_widget(self.update_button, True)

    def confirm(self):
        "activate the mods belonging to this save file"
        activated = self.parent.master.get_activated_activatable_mods()
        selected = self.doit.get_combobox_value(self.savegame_selector)
        modnames = self.conf.get_mods_for_saveitem(selected)[:]
        # uitzetten gebeurt in activate(), hier moeten de mods die ongemoeid gelaten moeten worden
        # en aanstaan, toegevoegd worden aan de selectie
        for dirname in self.conf.list_all_mod_dirs():
            # if (self.conf.get_diritem_data(dirname, self.conf.OPTOUT)
            #         and os.path.exists(os.path.join(self.parent.master.modbase, dirname))):
            #     modnames.append(dirname)
            if self.conf.get_diritem_data(dirname, self.conf.OPTOUT):
                # modnames.append(self.conf.get_diritem_data(dirname, self.conf.SCRNAM))
                # alleen de mods die al aan staan
                modname = self.conf.get_diritem_data(dirname, self.conf.SCRNAM)
                if modname in activated:
                    modnames.append(modname)
        self.parent.master.select_activations(modnames)
        if self.parent.master.directories:   # alleen leeg als er niks geselecteerd is
            self.parent.master.activate()
        self.parent.master.refresh_widget_data()
        gui.show_message(self.doit, 'wijzigingen zijn doorgevoerd', title='Change Config')
        self.doit.accept()

    def update(self):
        "callback for update button"
        self.update_conf(self.doit.get_combobox_value(self.savegame_selector))

    def update_conf(self, savename):
        "save the mod associations in the config"
        # print(f'in update_conf, {savename=}')
        changes = False
        new_pname = self.doit.get_field_text(self.pname)
        if new_pname != self.old_pname:
            self.conf.update_saveitem_data(savename, self.conf.PNAME, new_pname)
            changes = True
        new_fname = self.doit.get_field_text(self.fname)
        if new_fname != self.old_fname:
            self.conf.update_saveitem_data(savename, self.conf.FNAME, new_fname)
            changes = True
        new_gdate = self.doit.get_field_text(self.gdate)
        if new_gdate != self.old_gdate:
            self.conf.update_saveitem_data(savename, self.conf.GDATE, new_gdate)
            changes = True
        # dit lijkt nu niet meer goed te gaan want er komen steeds meer dubbele entries:
        newmods = [self.doit.get_combobox_value(item[1]) for item in self.widgets[:-1]]
        # print(f'  {newmods=}')
        # print(f'  {self.widgets=}', flush=True)
        if newmods != self.oldmods:
            self.conf.update_saveitem_data(savename, self.conf.MODS, newmods)
            changes = True
        if changes:
            # print('  there were changes')
            self.conf.save()
        self.doit.enable_widget(self.update_button, False)

    def get_savedata(self, *args):
        "find and show existing configuration data for this save file"
        newvalue = self.doit.get_combobox_value(self.savegame_selector)
        # print(f'in get_savedata, {newvalue=}')
        if self.oldsavename:
            self.update_conf(self.oldsavename)
        for item in reversed(self.widgets):
            # print(f'  removing modselector {item=}')
            self.doit.remove_modselector(item)
            self.widgets.remove(item)
        self.add_modselector()
        if newvalue == 'select a saved game':
            self.oldsavename = ''
            return
        self.oldsavename = newvalue
        self.oldmods = []
        save_attrs, new_in_conf = self.conf.get_saveitem_attrs(newvalue)
        if save_attrs:
            self.old_pname, self.old_fname, self.old_gdate = save_attrs
            self.doit.set_field_text(self.pname, self.old_pname)
            self.doit.set_field_text(self.fname, self.old_fname)
            self.doit.set_field_text(self.gdate, self.old_gdate)
            self.oldmods = self.conf.get_mods_for_saveitem(newvalue)
        for modname in self.oldmods:
            # name = self.conf.get_diritem_data(modname, self.conf.SCRNAM)
            # self.doit.set_combobox_value(self.widgets[-1][1], name)
            self.doit.set_combobox_value(self.widgets[-1][1], modname)
        self.doit.enable_widget(self.update_button, new_in_conf)
        self.doit.enable_widget(self.confirm_button, True)


def get_toplevel(dirname):
    """extract name of directory to rename from config entry
    """
    return dirname.split('/')[0] if '/' in dirname else dirname


def get_archive_roots(namelist):
    "determine base directories for a list of filenames"
    roots = set()
    for name in namelist:
        parent = os.path.dirname(name)
        while True:
            test = os.path.dirname(parent)
            if not test:
                break
            parent = test
        if parent == '__MACOSX':
            continue
        roots.add(parent)
    return sorted(roots)


def check_if_smapi(roots):
    "determine if mod is SMAPI"
    for rootitem in roots:
        if rootitem.startswith('SMAPI'):
            return True
    return False


def move_zip_after_installing(zipfilename):
    """make sure zipfile can't be installed again (from here) by accident"""
    zipfilepath = os.path.abspath(zipfilename)
    os.rename(zipfilepath, os.path.join(os.path.dirname(zipfilepath), 'installed',
                                        os.path.basename(zipfilepath)))


def check_if_active(roots):
    "determine state of mod before installing"
    mod_existed = mod_was_active = False
    for rootitem in roots:
        if os.path.exists(os.path.join(MODBASE, rootitem)):
            oldmodname = rootitem
        elif os.path.exists(os.path.join(MODBASE, f'.{rootitem}')):
            oldmodname = f'.{rootitem}'
        else:
            oldmodname = ''
        if oldmodname:
            mod_existed = True
            if os.path.exists(os.path.join(MODBASE, f'.{rootitem}~')):
                shutil.rmtree(os.path.join(MODBASE, f'.{rootitem}~'))
            os.rename(os.path.join(MODBASE, oldmodname),
                      os.path.join(MODBASE, f'.{rootitem}~'))
            mod_was_active = not oldmodname.startswith('.')
        else:
            mod_existed = False
            mod_was_active = False  # strictly speaking: should be "not applicable"
    return mod_existed, mod_was_active


def determine_update_id(keys):
    "loop over keys to get the one we need and to check if there are more"
    oldid, more_ids = 0, []
    for value in keys:
        if value:
            value = int(value)
            if value and value > 0 and value != oldid:
                if not oldid:
                    oldid = value
                else:
                    more_ids.append(value)
    return oldid, more_ids


def build_jsonconf():
    """build new configuration from current state of mod directory
    """
    if os.path.exists(CONFIG):
        with open(CONFIG) as f:
            olddata = json.load(f)
    else:
        olddata = {'moddirs': {}, 'savedgames': {}}
    data, messages = dmlj.rebuild_all(pathlib.Path(MODBASE).iterdir())
    # breakpoint()
    data['moddirs'] = dmlj.merge_old_info(data['moddirs'], olddata['moddirs'])
    data['savedgames'] = olddata['savedgames']
    if os.path.exists(CONFIG):
        shutil.copyfile(CONFIG, CONFIG + '~')
    with open(CONFIG, 'w') as f:
        json.dump(data, f)
    return messages
