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
import zipfile
import subprocess
import activate_gui as gui
MODBASE = os.path.expanduser('~/.steam/steam/steamapps/common/Stardew Valley/Mods')
CONFIG = os.path.join(MODBASE, 'sdv_mods.config')
DOWNLOAD = os.path.expanduser('~/Downloads/Stardew Valley Mods')
SCRPOS = '_ScreenPos'
NXSKEY = '_Nexus'


def main():
    "main line"
    DoIt = Activater(CONFIG)
    DoIt.build_and_start_gui()


class Activater:
    "Processing class (the one that contains the application logic (except the GUI stuff)"
    def __init__(self, config):
        self.config = config
        self.conf = configparser.ConfigParser(delimiters=(':',), allow_no_value=True)
        self.conf.optionxform = str
        self.conf.read(self.config)
        self.modnames = []
        self.modbase = MODBASE
        self.downloads = DOWNLOAD
        self.directories = set()
        self.screenpos = {}

    def build_and_start_gui(self):
        """build screen: make the user select from a list which expansions they want to have active
        """
        self.extract_screen_locations()
        self.doit = gui.ShowMods(self)
        self.doit.setup_screen()
        self.doit.setup_actions()
        self.doit.show_screen()

    def extract_screen_locations(self):
        """read the 'position' key from the config entries that will be presented and remove them
        temporarily from the config
        allows for the key not being present due to the screen never being reorganized
        """
        for item in self.conf.sections():
            if item == 'Mod Directories':
                continue
            self.screenpos[item] = ['', '']  # screenpos is eigenlijk geen goede naam meer
            if self.conf.has_option(item, SCRPOS):
                self.screenpos[item][0] = self.conf[item][SCRPOS]
                # self.conf.remove_option(item, SCRPOS)
            if self.conf.has_option(item, NXSKEY):
                self.screenpos[item][1] = self.conf[item][NXSKEY]

    def select_activations(self):
        "expand the selection to a list of directories"
        # determine which directories should be activated
        # conf['item'] is een lijst van modules bij een expansie
        self.directories.clear()
        for item in self.modnames:
            self.directories |= set(self.conf['Mod Directories'][item].split(', '))
            for entry in self.conf[item]:
                if entry not in (SCRPOS, NXSKEY):
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
                    if item not in (SCRPOS, NXSKEY):
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

    def reload_config(self):
        "reload config after editing"
        self.conf.read(self.config)
        self.extract_screen_locations()
        self.doit.refresh_widgets()

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
                if name2 not in modnames and name2 != "_ScreenPos":
                    errors.append(f'Unknown mod name `{name2}` for expansion/mod `{name}`')
        return errors or ['No errors']

    def add_to_config(self):
        "add a new mod (with dependencies if any) to the configuration"
        ok = gui.show_dialog(gui.NewModDialog, self.doit, self.conf['Mod Directories'],
                             first_time=True)
        if ok:
            new_entries = self.doit.dialog_data
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
                    self.doit.add_entries_for_name(name)
            shutil.copyfile(self.config, self.config + '~')
            with open(self.config, 'w') as cfg:
                self.conf.write(cfg)
            self.doit.refresh_widgets()

    def update_config_from_screenpos(self):
        """rewrite and reread config after reorganizing screen
        """
        # oldconf = self.conf
        for item in self.conf.sections():
            if item == 'Mod Directories':
                continue
            scrpos = self.screenpos[item]
            if scrpos:
                self.conf[item][SCRPOS] = scrpos
        shutil.copyfile(self.config, self.config + '~')
        with open(self.config, 'w') as cfg:
            self.conf.write(cfg)
        # reset conf to version without screen positions, to continue operation
        # self.conf = oldconf

    def update_mods(self, names):
        "installeer de aangegeven mod files"
        report = []
        for zipfilename in names:
            archive = zipfile.ZipFile(zipfilename)
            names = archive.namelist()
            roots = get_archive_roots(names)
            # if len(root) != 1:
            if not roots:
            #     report.append(f'{zipfilename}: zipfile should contain only one base directory')
                report.append(f'{zipfilename}: zipfile appears to be empty')
                archive.close()
                continue
            #     # dit is geen probleem als ik de downloads directories gewoon in de config opneem
            #     # als een comma separated list (vgl. SMAPI en BusLocations)
            #     # de activeer routines snappen dit al
            #     # nu het vervolg van deze methode nog
            # root = root.pop()
            for rootitem in roots:
                if os.path.exists(os.path.join(self.modbase, rootitem)):
                    mod_was_active = True
                    if os.path.exists(os.path.join(self.modbase, f'.{rootitem}~')):
                        shutil.rmtree(os.path.join(self.modbase, f'.{rootitem}~'))
                    os.rename(os.path.join(self.modbase, f'{rootitem}'),
                              os.path.join(self.modbase, f'.{rootitem}~'))
                elif os.path.exists(os.path.join(self.modbase, f'.{rootitem}')):
                    mod_was_active = False
                    if os.path.exists(os.path.join(self.modbase, f'.{rootitem}~')):
                        shutil.rmtree(os.path.join(self.modbase, f'.{rootitem}~'))
                    os.rename(os.path.join(self.modbase, f'.{rootitem}'),
                              os.path.join(self.modbase, f'.{rootitem}~'))
                else:
                    mod_was_active = False  # strictly speaking: should be "not applicable"
            archive.extractall(self.modbase)
            if os.path.exists(os.path.join(self.modbase, '__MACOSX')):
                shutil.rmtree(os.path.join(self.modbase, '__MACOSX'))
            for rootitem in roots:
                if not mod_was_active:
                    os.rename(os.path.join(self.modbase, f'{rootitem}'),
                              os.path.join(self.modbase, f'.{rootitem}'))
            zipfilepath = os.path.abspath(zipfilename)
            os.rename(zipfilepath, os.path.join(os.path.dirname(zipfilepath), 'installed',
                                                os.path.basename(zipfilepath)))
            archive.close()
            report.append(f'{zipfilename} is successfully installed')
        return report

    def determine_unpack_directory(self, zipfilename):
        """read the unpack directory to transfer to linedit fields
        """
        # dit is waarschijnlijk de handigste plek om ook de andere gegevens (nexus key, mod naam
        # volgens manifest) op te halen en door te geven
        with zipfile.ZipFile(zipfilename) as archive:
            roots = get_archive_roots(archive.namelist())
        return '' if not roots else ', '.join(list(roots))


def get_archive_roots(namelist):
    "determine base directories for a list of filenames"
    roots = set()
    for name in namelist:
        parent = os.path.dirname(name)
        while parent:
            test = os.path.dirname(parent)
            if not test:
                break
            parent = test
        if parent == '__MACOSX':
            continue
        roots.add(parent)
    print(roots)
    return roots
