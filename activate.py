"""Stardew Valley Expansion manager
Het idee: selecteer uit een lijst met mogelijkheden welke je actief wilt hebben

Realisatie: aan de hand van een configuratiebestand waarin per expansie de requirements staan
dat zijn namen die verwijzen naar entries in een lijst met Mod directories

werkwijze:
    1. verzamel alle mods die aan moeten staan in een lijst:
        a. alles in de config entry
        b. voor elke die een eigen config entry heeft ook alles
        c. ontdubbelen voor het geval dat
    2. alle mods uitzetten behalve degene die in het lijstje verzameld zijn
"""
import os
import configparser
import shutil
import subprocess
import activate_gui as gui
MODBASE = os.path.expanduser('~/.steam/steam/steamapps/common/Stardew Valley/Mods')
CONFIG = os.path.join(MODBASE, 'sdv_mods.config')


def main():
    "main line"
    DoIt = Activate(CONFIG)
    DoIt.build_and_start_gui()


class Activate:
    "Processing class (the one that contains the application logic (except the GUI stuff)"
    def __init__(self, config):
        self.config = config
        self.conf = configparser.ConfigParser(delimiters=(':',), allow_no_value=True)
        self.conf.optionxform = str
        self.conf.read(self.config)
        self.modnames = []
        self.modbase = MODBASE
        self.directories = set()

    def build_and_start_gui(self):
        """build screen: make the user select from a list which expansions they want to have active
        """
        self.doit = gui.ShowMods(self)
        self.doit.setup_screen()
        self.doit.setup_actions()
        self.doit.show_screen()

    def select_activations(self):
        "expand the selection to a list of directories"
        # determine which directories should be activated
        # conf['item'] is een lijst van modules bij een expansie
        self.directories.clear()
        for item in self.modnames:
            self.directories |= set(self.conf['Mod Directories'][item].split(', '))
            for entry in self.conf[item]:
                self.add_activations(item, entry)

    def add_activations(self, section_name, entry):
        "expand an item with a list of subitems"
        # conf['item'] is een lijst van modules bij een expansie
        # conf['item']['entry'] is een string van één of meer directories bij een module
        directories = []
        for dirname in self.conf[section_name]:
            directories.extend(self.conf['Mod Directories'][entry].split(', '))
        self.directories |= set(directories)
        for dirname in self.conf[section_name]:
            if dirname in self.conf:
                for item in self.conf[dirname]:
                    self.add_activations(dirname, item)

    def activate(self):
        "activate by making directories hidden or not"
        for entry in os.scandir(self.modbase):
            # leave my files alone!
            if entry.is_file():
                continue
            # if smapi, do not deactivate
            if entry.name in self.conf['Mod Directories']['SMAPI']:
                continue
            # if in list and deactivated, re-activate
            if entry.name.startswith('.'):
                if entry.name[1:] in self.directories:
                    os.rename(entry, os.path.join(self.modbase, entry.name[1:]))
            # if not in list and activated, deactivate
            elif entry.name not in self.directories:
                os.rename(entry, os.path.join(self.modbase, '.' + entry.name))

    def edit_config(self):
        "open config file for editing"
        # subprocess.run(['scite', CONFIG])
        subprocess.run(['gnome-terminal', '--geometry=102x54+1072+0', '--', 'vim', CONFIG])

    def check_config(self):
        "check names in config files for spelling errors etc."
        modnames = self.conf.options('Mod Directories')
        errors = []
        for name in self.conf.sections():
            if name == 'Mod Directories':
                continue
            if name not in modnames:
                errors.append(f'Unknown expansion / mod name: `{name}`')
            for name2 in self.conf.options(name):
                if name2 not in modnames:
                    errors.append(f'Unknown mod name `{name2}` for expansion/mod `{name}`')
        return errors or ['No errors']

    def add_to_config(self):
        "add a new mod (with dependencies if any) to the configuration"
        ok, new_entries = gui.show_dialog(gui.NewModDialog, self.doit, self.conf['Mod Directories'],
                                          first_time=True)
        if ok:
            # print(new_entries)
            for name, other in new_entries['mods']:
                self.conf.set('Mod Directories', name, other)
            for name, other in new_entries['deps'].items():
                if other:
                    self.conf.add_section(name)
                    for item in other:
                        self.conf.set(name, item, '')
            for name in new_entries['set_active']:
                try:
                    self.conf.add_section(name)
                except configparser.DuplicateSectionError:
                    pass
                else:
                    self.doit.add_checkbox(name)
            shutil.copyfile(self.config, self.config + '~')
            with open(self.config, 'w') as cfg:
                self.conf.write(cfg)
            self.doit.refresh_widgets()
