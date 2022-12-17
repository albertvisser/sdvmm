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
import activate_gui as gui
CONFIG = 'sdv_mods.config'
MODBASE = os.path.expanduser('~/.steam/steam/steamapps/common/Stardew Valley/Mods')


def main():
    "main line"
    DoIt = Activate(CONFIG)
    DoIt.select_expansions()  # result of selection process
    # print('gekozen expansions:', expansions_to_activate)
    DoIt.select_activations()
    # print('bijbehorende directories', DoIt.directories)
    if DoIt.directories:
        DoIt.activate()


class Activate:
    "Processing class (the one that contains the application logic (except the GUI stuff)"
    def __init__(self, config):
        self.conf = configparser.ConfigParser(allow_no_value=True)
        self.conf.optionxform = str
        self.conf.read(config)
        self.modnames = []
        self.directories = set()

    def select_expansions(self):
        "make the user select from a list which expansions the want to have active"
        # expansions = list(self.conf['Expansions'])   # list of expansions to activate or not
        doit = gui.ShowMods(self)
        doit.show_screen()

    def select_activations(self):
        "expand the selection to a list of directories"
        # determine which directories should be activated
        # conf['item'] is een lijst van modules bij een expansie
        for item in self.modnames:
            print(item, self.conf[item], self.conf.options(item))
            for entry in self.conf[item]:
                print(entry)
                self.add_activations(item, entry)

    def add_activations(self, section_name, entry):
        "expand an item with a list of subitems"
        # conf['item'] is een lijst van modules bij een expansie
        # conf['item']['entry'] is een string van één of meer directories bij een module
        # directories = self.conf[item][entry].split(', ')
        directories = self.conf['Mod Directories'][entry].split(', ')
        self.directories |= set(directories)
        for dirname in directories:
            if dirname in self.conf:
                for item in self.conf[dirname]:
                    self.add_activations(dirname, item)

    def activate(self):
        "activate by making directories hidden or not"
        for entry in os.scandir(MODBASE):
            # if smapi, do not deactivate
            if entry.name in self.conf['Mod Directories']['SMAPI']:
                continue
            # if in list and deactivated, re-activate
            if entry.name.startswith('.'):
                if entry.name[1:] in self.directories:
                    os.rename(entry, os.path.join(MODBASE, entry.name[1:]))
            # if not in list and activated, deactivate
            else:
                if entry.name not in self.directories:
                    os.rename(entry, os.path.join(MODBASE, '.' + entry.name))