""" extract_updatekeys.py - read Nexus keys and descriptions from manifest files

1. loop over mod directories (skip the backups) and subdirectories
2. look for files named manifest.json and scan it for top level keys

Main interest: "UpdateKeys" (value is a list), specifically avalue that starts with "Nexus:"
also interesting: Author, Version, Description, Dependencies (list of dicts)
"""
import pathlib
import shutil
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
                messages.append(f'duplicate component(s) found in {modpath}')
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
            # root = modpath.name.removeprefix('.')
            # dirname = os.path.join(root, path.name) if path.is_dir() else root
            for item in data:
                mod_id = item.pop('UniqueID')
                item['dirname'] = str(item.pop('dirpath').relative_to(modpath.parent)).lstrip('.')
                mod_data[mod_id] = item
    return mod_data


def read_dir(path):
    "get data from mod (sub)directory"
    if path.name == 'manifest.json':
        result = read_manifest(path)
        if result:
            return [result]
    if not path.is_dir():
        return []
    result = []
    subdirs = []
    for subpath in path.iterdir():
        if subpath.name == 'manifest.json':
            info = read_manifest(subpath)
            if info:
                result.append(info)
        if subpath.is_dir():
            subdirs.append(subpath)
    for subpath in subdirs:
        for subsubpath in subpath.iterdir():
            if subsubpath.name == 'manifest.json':
                info = read_manifest(subsubpath)
                if info:
                    result.append(info)
            # we assume this is the deepest nesting level
    return result


def read_manifest(path):
    """...and scan it for top level keys
    """
    result = {}
    with path.open('rb') as f:
        data = json5.load(f)
    if "UpdateKeys" in data:
        for value in data["UpdateKeys"]:
            items = value.split(':', 1)
            if len(items) == 2 and items[0].title() == "Nexus":
                result["_Nexus"] = items[1]
    for keyname in ["Name", "Author", "Description", "UniqueID", "Version", "MinimumApiVersion"]:
        if keyname in data:
            result[keyname] = data[keyname]
    for keyname in ("Dependencies", "dependencies"):
        if keyname in data:
            result["Deps"], error = read_dependencies(data[keyname])
            if error:
                print(f"Geen 'IsRequired' key gevonden voor dep(s) in bestand {path}")
    if result:
        result['dirpath'] = path.parent
    return result


def read_dependencies(deplist):
    """process dependencies
    """
    result = []
    error = False
    for depdict in deplist:
        # if 'IsRequired' not in depdict:       Deze key wordt vaker vergeten dan dat hij
        #     error = True                      netjes op True gezet wordt dus maar geen controle
        if 'IsRequired' not in depdict or depdict['IsRequired']:
            result.append(depdict["UniqueID"])
    return result, error


class JsonConf:
    "configuration to be stored externally in JSON format"
    MODS = 'moddirs'
    knownmodkeys = ['components', '_ScreenPos', '_ScreenName', '_ScreenText', '_Nexus',
                    '_Selectable']
    COMPS, SCRPOS, SCRNAM, SCRTXT, NXSKEY, SEL = knownmodkeys
    knownkeys = ['Name', 'Author', 'Description', 'Version', 'MinimumApiVersion', 'Deps', 'dirname',
                 NXSKEY]
    NAME, AUTH, DESC, VRS, APIVRS, DEPS, DIR = knownkeys[:7]

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
        shutil.copyfile(self.filename, str(backup_path))
        with self.filepath.open('w') as f:
            json.dump(self._data, f)

    def list_all_mod_dirs(self):
        "return a list of all known mod directories"
        return list(self._data[self.MODS])

    def list_all_components(self):
        "return a list of all known mod components"
        return list(self._data[self.COMPS])

    def has_moddir(self, dirname):
        "return whether or not the given directory is in the config"
        return dirname in self._data[self.MODS]

    def has_component(self, dirname):
        "return whether or not the given component is in the config"
        return dirname in self._data[self.COMPS]

    def list_components_for_dir(self, dirname):
        "return a list of components in the given mod directory"
        if dirname not in self._data[self.MODS]:
            raise ValueError(f'mod directory {dirname} not found in config')
        return self._data[self.MODS][dirname][self.COMPS]

    def get_diritem_data(self, dirname, key=None):
        "return the value for a given key for the given mod directory"
        if dirname not in self._data[self.MODS]:
            raise ValueError(f'mod directory {dirname} not found in config')
        if key is None:
            return self._data[self.MODS][dirname]
        if key not in self.knownmodkeys:
            raise ValueError(f"Unknown key '{key}' for directory {dirname}")
        if key == '_Nexus':
            return self._data[self.MODS][dirname].get(key, 0)
        if key == '_Selectable':
            return self._data[self.MODS][dirname].get(key, False)
        return self._data[self.MODS][dirname].get(key, '')

    def get_component_data(self, component, key=None):
        "return the value for a given key for the given component"
        if component not in self._data[self.COMPS]:
            raise ValueError(f'component {component} not found in config')
        if key is None:
            return self._data[self.COMPS][component]
        if key not in self.knownkeys:
            raise ValueError(f"Unknown key '{key}' for component {component}")
        return self._data[self.COMPS][component].get(key, '')

    def add_diritem(self, dirname):
        "add a new (empty) mod directory to the config"
        if not self.has_moddir(dirname):
            self._data[self.MODS][dirname] = {}

    def update_diritem(self, dirname, value):
        "set all values for the keys for the given mod directory at once"
        if self.has_moddir(dirname):
            self._data[self.MODS][dirname] = value

    def set_diritem_value(self, dirname, key, value):
        "set the value for a given key for the given mod directory"
        if self.has_moddir(dirname):
            if key not in self.knownmodkeys:
                raise ValueError(f"Unknown key '{key}' for directory {dirname}")
            self._data[self.MODS][dirname][key] = value

    def add_componentdata(self, component):
        "add a new (empty) component to the config"
        if not self.has_component(component):
            self._data[self.COMPS][component] = {}

    def update_componentdata(self, component, value):
        "set all values for the keys for the given component at once"
        if self.has_component(component):
            self._data[self.COMPS][component] = value

    def set_componentdata_value(self, component, key, value):
        "set the value for a given key for the given component"
        if self.has_component(component):
            if key not in self.knownkeys:
                raise ValueError(f"Unknown key '{key}' for component {component}")
            self._data[self.COMPS][component][key] = value

    def determine_nexuskey_for_mod(self, dirname):
        "copy nexuskey in config from component to moddir"
        nexusid = ''
        # extravalues = []
        for item in self.list_components_for_dir(dirname):
            value = self.get_component_data(item, self.NXSKEY).strip().replace('?', '').split('@')[0]
            if value and value != '-1':
                value = int(value)
                if value != nexusid:
                    if not nexusid:
                        nexusid = value
                    # else:
                    #     extravalues.append(value)
        if nexusid:
            self.set_diritem_value(dirname, self.NXSKEY, int(nexusid))
        # if extravalues:
        #     self.set_diritem_value(dirname, self.MULTI, extravalues)

    def mergecomponents(self, title, dirnames):
        "old_to_new: fix situation for multiple components in multiple unpack directories"
        dirnames = dirnames.split(',')
        newdirname = dirnames[0]
        componentlist = self.get_diritem_data(dirnames[0], self.COMPS)
        for name in dirnames[1:]:
            data = self._data[self.MODS].pop(name.strip())
            componentlist.extend(data[self.COMPS])
        self.set_diritem_value(dirnames[0], self.COMPS, componentlist)
