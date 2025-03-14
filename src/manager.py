"""Stardew Valley Expansion manager
Oorspronkelijk idee: selecteer uit een lijst met mogelijkheden welke je actief wilt hebben
"""
import os
import json
import pathlib
import shutil
import zipfile
import subprocess
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
    def __init__(self):
        self.conf = dmlj.JsonConf(CONFIG)
        if CONFIG:
            self.conf.load()
        self.modnames = []
        self.modbase = MODBASE
        self.downloads = DOWNLOAD
        self.directories = set()
        self.screeninfo = {}

    def build_and_start_gui(self):
        """build screen: make the user select from a list which expansions they want to have active
        """
        self.extract_screeninfo()
        self.doit = gui.ShowMods(self)
        self.doit.setup_screen()
        self.doit.setup_actions()
        self.doit.show_screen()

    def extract_screeninfo(self):
        """read the 'position' key from the config entries that will be presented and remove them
        temporarily from the config
        allows for the key not being present due to the screen never being reorganized
        """
        if not CONFIG:
            return
        for dirname in self.conf.list_all_mod_dirs():
            item = self.conf.get_diritem_data(dirname, self.conf.SCRNAM) or dirname
            oldinfo = self.screeninfo[item] if item in self.screeninfo else {'sel': False, 'pos': '',
                                                                             'key': '', 'txt': '',
                                                                             'opt': False}
            realdirname = get_toplevel(self.conf.get_component_data(
                self.conf.get_diritem_data(dirname, self.conf.COMPS)[0], self.conf.DIR))
            self.screeninfo[item] = {
                'dir': realdirname,
                'sel': self.conf.get_diritem_data(dirname, self.conf.SEL) or oldinfo['sel'],
                'opt': self.conf.get_diritem_data(dirname, self.conf.OPTOUT) or oldinfo['opt'],
                'pos': self.conf.get_diritem_data(dirname, self.conf.SCRPOS) or oldinfo['pos'],
                'key': self.conf.get_diritem_data(dirname, self.conf.NXSKEY) or oldinfo['key'],
                'txt': self.conf.get_diritem_data(dirname, self.conf.SCRTXT) or oldinfo['txt']}

    def select_activations(self, modnames):
        "expand the selection to a list of directories"
        # determine which directories should be activated
        self.directories = set()
        for item in modnames:
            moddir = self.screeninfo[item]['dir']
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
        self.attr_changes = []  # list of changed mods
        gui.show_dialog(gui.AttributesDialog, self.doit, self.conf)
        # screeninfo is updated in the dialog, here we update the configuration
        changes = False
        for newname, oldname in self.attr_changes:
            dirname = self.screeninfo[newname]['dir']
            if oldname:
                self.conf.set_diritem_value(dirname, self.conf.SCRNAM, newname)
            self.conf.set_diritem_value(dirname, self.conf.SCRTXT, self.screeninfo[newname]['txt'])
            self.conf.set_diritem_value(dirname, self.conf.SEL, self.screeninfo[newname]['sel'])
            self.conf.set_diritem_value(dirname, self.conf.OPTOUT, self.screeninfo[newname]['opt'])
            changes = True
        if changes:
            self.conf.save()

    def manage_savefiles(self):
        "handle dialog for selecting a savefile to perform actions on"
        # changes = False
        gui.show_dialog(gui.SaveGamesDialog, self.doit, self.conf)
        # if changes:
        #     self.conf.save()

    def update_config_from_screenpos(self):
        """rewrite and reread config after reorganizing screen
        """
        for item in self.screeninfo.values():
            self.conf.set_diritem_data(item['dir'], self.conf.SCRPOS, item['pos'])
        self.conf.save()

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
            zipfilepath = os.path.abspath(zipfilename)
            os.rename(zipfilepath, os.path.join(os.path.dirname(zipfilepath), 'installed',
                                                os.path.basename(zipfilepath)))
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
            installdir = os.path.join('/tmp', roots.pop())
            subprocess.run(['unzip', zipfilename, '-d', '/tmp'], check=True)
            subprocess.run(['gnome-terminal'], cwd=installdir)  # , capture_output=True)
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
        origdata = self.dialog_data = dmlj.read_defaults(bare=True)
        gui.show_dialog(gui.SettingsDialog, self.doit)
        if self.dialog_data != origdata:
            dmlj.save_defaults(*self.dialog_data)


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
