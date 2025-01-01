""" extract_updatekeys.py - read Nexus keys and descriptions from manifest files

1. loop over mod directories (skip the backups) and subdirectories
2. look for files named manifest.json and scan it for top level keys

Main interest: "UpdateKeys" (value is a list), specifically avalue that starts with "Nexus:"
also interesting: Author, Version, Description, Dependencies (list of dicts)
"""
import os
import pathlib
import shutil
import collections
import pprint
import json5
import json


def rebuild_all(startdirs):
    """loop over mod directories (skip the backups) and subdirectories
    """
    mods = {'moddirs': {}, 'components': {}}
    messages = []
    for modpath in startdirs:
        if modpath.name in ('.cjbcheats-warps-backup', 'ConsoleCommands', 'SaveBackup'):
            continue
        if modpath.is_dir() and not modpath.name.endswith('~'):
            # mods[modpath.name.removeprefix('.')] = build_entry_from_dir(modpath)
            data = build_entry_from_dir(modpath)
            if any(x in mods['components'] for x in data):
                messages.append(f'duplicate key(s) found in {modpath}')
                continue
            mods['moddirs'][modpath.name.lstrip('.')] = {'components': list(data)}
            mods['components'].update(data)
    return mods, messages


def build_entry_from_dir(modpath):
    "produce a config entry for an install  directory (top level and everyting under it)"
    mod_data = {}  # collections.defaultdict(list)
    for path in modpath.iterdir():
        data = read_dir(path)
        if data:
            root = modpath.name.removeprefix('.')
            # dirname = os.path.join(root, path.name) if path.is_dir() else root
            for item in data:
                mod_id = item.pop('UniqueID')
                item['dirname'] = str(item.pop('dirpath').relative_to(modpath.parent)).lstrip('.')
                mod_data[mod_id] = item
    return mod_data


def read_dir(path):
    "get data from mod (sub)directory"
    found_stuff = {}
    if path.name == 'manifest.json':
        found_stuff = read_keys(path)
        if found_stuff:
            found_stuff['dirpath'] = path.parent
            return [found_stuff]
    elif not path.is_dir():
        return
    result = []
    subdirs = []
    for subpath in path.iterdir():
        if subpath.name == 'manifest.json':
            found_stuff = read_keys(subpath)
            if found_stuff:
                # return found_stuff
                found_stuff['dirpath'] = path
                result.append(found_stuff)
        if subpath.is_dir():
            subdirs.append(subpath)
    for subpath in subdirs:
        for subsubpath in subpath.iterdir():
            if subsubpath.name == 'manifest.json':
                found_stuff = read_keys(subsubpath)
                if found_stuff:
                    # return found_stuff
                    found_stuff['dirpath'] = subpath
                    result.append(found_stuff)
            # we assume this is the deepest nesting level
    return result


def read_keys(path):
    """...and scan it for top level keys
    """
    result = {}
    with path.open('rb') as f:
        try:
            data = json5.load(f)
        except json5.decoder.JSONDecodeError as e:
            return f'{e} in {path}'
    if "UpdateKeys" in data:
        for value in data["UpdateKeys"]:
            items = value.split(':', 1)
            if len(items) == 2 and items[0].title() == "Nexus":
                result["_Nexus"] = items[1]
    for keyname in ["Name", "Author", "Description", "UniqueID", "Version", "MinimumApiVersion"]:
        if keyname in data:
            result[keyname] = data[keyname]
    if "Dependencies" in data:
        result["Deps"], error = read_dependencies(data["Dependencies"])
        if error:
            print(f"Geen 'IsRequired' key gevonden voor dep(s) in bestand {path}")
    return result


def read_dependencies(deplist):
    """process dependencies
    """
    result = []
    error = False
    for depdict in deplist:
        if 'IsRequired' not in depdict or depdict['IsRequired']:
            result.append(depdict["UniqueID"])
    return result, error


class JsonConf:
    "configuration to be stored externally in JSON format"
    knownmodkeys = ['components', '_ScreenPos', '_ScreenName', '_ScreenText', '_Nexus', '_Nexus2',
                    '_Selectable']
    knownkeys = ['Name', 'Author','Description', 'Version', 'MinimumApiVersion', 'Deps', 'Dirname',
                 '_Nexus']

    def __init__(self, filename):
        self.filename = filename
        self.filepath = pathlib.Path(filename)
        self._data = {}

    def load(self):
        "read configuration from json file"
        with self.filepath.open() as f:
            self._data = json.load(f)

    def save(self):
        "save configuration to json file"
        backup_path = pathlib.Path(self.filename + '~')
        shutil.copyfile(self.filepath, backup_path)
        with self.filepath.open('w') as f:
            json.dump(self._data, f)

    def list_all_mod_dirs(self):
        "return a list of all known mod directories"
        return list(self._data['moddirs'])

    def list_all_components(self):
        "return a list of all known mod components"
        return list(self._data['components'])

    def has_moddir(self, dirname):
        "return whether or not the given directory is in the config"
        return dirname in self._data['moddirs']

    def has_component(self, dirname):
        "return whether or not the given component is in the config"
        return dirname in self._data['components']

    def list_components_for_dir(self, dirname):
        "return a list of components in the given mod directory"
        if dirname not in self._data['moddirs']:
            raise ValueError('mod directory not found in config')
        return self._data['moddirs'][dirname]['components']

    def get_diritem_data(self, dirname, key=None):
        "return the value for a given key for the given mod directory"
        if dirname not in self._data['moddirs']:
            raise ValueError('mod directory not found in config')
        if key is None:
            return self._data['moddirs'][dirname]
        if key not in self.knownmodkeys:
            raise ValueError(f"Unknown key '{key}'")
        if key == '_Nexus':
            return self._data['moddirs'][dirname].get(key, 0)
        if key == '_Selectable':
            return self._data['moddirs'][dirname].get(key, False)
        return self._data['moddirs'][dirname].get(key, '')

    def get_component_data(self, component, key):
        "return the value for a given key for the given component"
        if component not in self._data['components']:
            raise ValueError('component not found')
        if key is None:
            return self._data['components'][component]
        if key not in self.knownkeys:
            raise ValueError(f"Unknown key '{key}'")
        return self._data['components'][component].get(key, '')

    def update_diritem(self, dirname, value):
        "set all values for the keys for the given mod directory at once"
        if self.has_moddir(dirname):
            self._data['moddirs'][dirname] = value

    def set_diritem_value(self, dirname, key, value):
        "set the value for a given key for the given mod directory"
        if self.has_moddir(dirname):
            self._data['moddirs'][dirname][key] = value

    def update_componentdata(self, component, value):
        "set all values for the keys for the given component at once"
        if self.has_component(component):
            self._data['components'][component] = value

    def set_componentdata_value(self, component, key, value):
        "set the value for a given key for the given component"
        if self.has_component(component):
            self._data['components'][component][key] = value

    def determine_nexuskey_for_mod(self, dirname):
        "copy nexuskey in config from component to moddir"
        nexusid = ''
        extravalues = []
        for item in self.list_components_for_dir(dirname):
            value = self.get_component_data(item, '_Nexus').strip().replace('?', '').split('@')[0]
            if value and value != nexusid:
                if not nexusid:
                    nexusid = value
                else:
                    extravalues.append(value)
        if nexusid:
            self.set_diritem_value(dirname, '_Nexus', int(nexusid))
        if extravalues:
            self.set_diritem_value(dirname, '_Nexus2', extravalues)

    def mergecomponents(self, title, dirnames):
        "old_to_new: fix situation for multiple components in multiple unpack directories"
        dirnames = dirnames.split(',')
        newdirname = dirnames[0]
        componentlist = self.get_diritem_data(dirnames[0], 'components')
        for name in dirnames[1:]:
            data = self._data['moddirs'].pop(name.strip())
            componentlist.extend(data['components'])
        self.set_diritem_value(dirnames[0], 'components', componentlist)


if __name__ == "__main__":
    root = pathlib.Path("~/.steam/steam/steamapps/common/Stardew Valley/Mods").expanduser()
    data, messages = rebuild_all(root.iterdir())
    for m in messages:
        print(m)
    with open('new_config.json', 'w') as f:
       json.dump(data, f)
    # with open('new_config', 'w') as f:
    #    pprint.pprint(data, stream=f)

data = {
        "Alvadea's Farm Maps": [
             {'_Nexus': '13187',
              'Name': 'Alvadeas Mining Map',
              'Author': 'Alvadea',
              'Description': 'A new mining map with custom sprites',
              'UniqueID': 'alvadea.minemap',
              'Deps': []},
             {'_Nexus': '15926',
              'Name': 'Alvadeas Combat Map',
              'Author': 'Alvadea',
              'Description': 'A new combat map with custom sprites and a swamp',
              'UniqueID': 'alvadea.combatmap',
              'Deps': []}],
        'ContentPatcher': [
            {'_Nexus': '1915',
             'Name': 'Content Patcher',
             'Author': 'Pathoschild',
             'Description': 'Loads content packs which edit game data, images, and maps without changing the game files.',
             'UniqueID': 'Pathoschild.ContentPatcher'}],
        'Cape Stardew 1.6': [
            'Expecting property name enclosed in double quotes: line 10 column 5 (char 257) in /tmp/SDVMods/.Cape Stardew 1.6/OrbOfTheTides/(CP)OrbOfTheTides/manifest.json',
            'Expecting property name enclosed in double quotes: line 13 column 4 (char 344) in /tmp/SDVMods/.Cape Stardew 1.6/OrbOfTheTides/OrbOfTheTidesMod/manifest.json',
            'Expecting property name enclosed in double quotes: line 10 column 5 (char 279) in /tmp/SDVMods/.Cape Stardew 1.6/Cape Stardew/manifest.json',
            {'Name': 'BL for Cape Stardew',
             'Author': 'DreamyGloom',
             'Description': 'Bus Locations Compatibility for Cape Stardew',
             'UniqueID': 'dreamy.CapeBus'},
            'Expecting property name enclosed in double quotes: line 2 column 5 (char 7) in /tmp/SDVMods/.Cape Stardew 1.6/(FTM) Cape Stardew/manifest.json',
            'Expecting property name enclosed in double quotes: line 9 column 3 (char 235) in /tmp/SDVMods/.Cape Stardew 1.6/[CP]Annetta/manifest.json']}

