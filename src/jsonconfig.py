""" extract_updatekeys.py - read Nexus keys and descriptions from manifest files

1. loop over mod directories (skip the backups) and subdirectories
2. look for files named manifest.json and scan it for top level keys

Main interest: "UpdateKeys" (value is a list), specifically avalue that starts with "Nexus:"
also interesting: Author, Version, Description, Dependencies (list of dicts)
"""
import os.path
import pathlib
import shutil
import json
import json5    # needed because not all manifest files conform to standard (no comments etc)?
try:
    from lxml import etree as et
except ImportError:
    import xml.etree.ElementTree as et
DEFAULTS = os.path.join(os.path.dirname(__file__), 'defaults.json')


def read_defaults(bare=False):
    "read default locations from file"
    data = {}
    if os.path.exists(DEFAULTS):
        with open(DEFAULTS) as f:
            data = json.load(f)
    modbase = data.get('modbase', '')
    config = data.get('config', '')
    download = data.get('download', '')
    savepath = data.get('savepath', '')
    if not bare:
        modbase = os.path.expanduser(modbase)
        if config:
            config = os.path.join(modbase, config)
        download = os.path.expanduser(download)
        if savepath:
            savepath = pathlib.Path(savepath).expanduser()
    return modbase, config, download, savepath


def save_defaults(modbase, config, download, savepath):
    "write new/changed default values"
    data = {'modbase': modbase, 'config': config, 'download': download, 'savepath': savepath}
    if os.path.exists(DEFAULTS):
        shutil.copyfile(DEFAULTS, DEFAULTS + '~')
    with open(DEFAULTS, 'w') as f:
        json.dump(data, f)


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
    DEPS = "Deps"
    result = {}
    # print(path)
    with path.open('rb') as f:
        data = json5.load(f)
        # data = json.load(f)
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
            result[DEPS] = read_dependencies(data[keyname])
    if 'ContentPackFor' in data:
        # if DEPS not in result:
        #     result[DEPS] = []
        deps = result.setdefault(DEPS, [])
        for key, value in data['ContentPackFor'].items():
            if key == 'UniqueID':
                dep = value
                if dep not in deps:
                    result[DEPS].append(dep)
    if result:
        result['dirpath'] = path.parent
    return result


def read_dependencies(deplist):
    """process dependencies
    """
    result = []
    for depdict in deplist:
        if 'IsRequired' not in depdict or depdict['IsRequired']:
            result.append(depdict["UniqueID"])
    return result


def merge_old_info(newdata, olddata):
    """salvage information like screen texts, position, selectability from the earlier config
    """
    # breakpoint()
    for key, value in newdata.items():
        if key not in olddata:
            # komt bv voor bij GingerIslandStart waar de CP component op hetzelfde niveau zit
            # je zou dit moeten melden zodat je het later kunt corrigeren maar daar heb ik nog niks
            # voor
            # bij Swim Mod zie ik hetzelfde; daar heeft het zich vanzelf opgelost LIJKT HET:
            # de drie uitpakdirectories zijn samengevoegd onder "componenten" MAAR de modddirs key
            # heeft de waarde "true" in plaats van een directory naam
            continue
        oldvalue = olddata[key]
        for name in ('_ScreenName', '_Selectable', '_Nexus', '_ScreenPos', '_ScreenText'):
            if name in value:
                if value[name] != oldvalue[name]:
                    value[name] = oldvalue[name]
            elif name in oldvalue:
                value[name] = oldvalue[name]
        # for name in ('_ScreenPos', '_ScreenText'):
        #     if name in value:
        #         value[name] = oldvalue[name]
        #     elif name in oldvalue:
        #         value[name] = oldvalue[name]
        # newdata[key] = value
    return newdata


def get_savenames():
    "get a list of the names of valid save file directories"
    result = []
    for item in read_defaults()[-1].iterdir():
        if item.is_file() or item.is_symlink() or item.name.endswith('backup'):
            continue
        result.append(item.name)
    return result


def get_save_attrs(savename):
    "return the values of specific elements in the savefile"
    result = {}
    for item in (read_defaults()[-1] / savename).iterdir():
        if item.name == savename:
            savedata = et.ElementTree(file=str(item))
            root = savedata.getroot()
            for key in ('player/name', 'player/farmName', 'dayOfMonth', 'currentSeason', 'year'):
                el = root.find(f'./{key}')
                result[key] = el.text if el is not None else None
            break
    return result


class JsonConf:
    "configuration to be stored externally in JSON format"
    MODS = 'moddirs'
    knownmodkeys = ['components', '_ScreenPos', '_ScreenName', '_ScreenText', '_Nexus',
                    '_Selectable', '_DoNotTouch']
    COMPS, SCRPOS, SCRNAM, SCRTXT, NXSKEY, SEL, OPTOUT = knownmodkeys
    knownkeys = ['Name', 'Author', 'Description', 'Version', 'MinimumApiVersion', 'Deps', 'dirname',
                 NXSKEY]
    NAME, AUTH, DESC, VRS, APIVRS, DEPS, DIR = knownkeys[:7]
    SAVES = 'savedgames'
    knownsavekeys = ['player', 'farmName', 'ingameDate', MODS]
    PNAME, FNAME, GDATE = knownsavekeys[:-1]

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

    def list_all_saveitems(self):
        "return a list of Stardew Valley save files (or rather, directories)"
        return get_savenames()

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
        if key == self.NXSKEY:
            return self._data[self.MODS][dirname].get(key, 0)
        if key in (self.SEL, self.OPTOUT):
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

    def get_saveitem_attrs(self, savename):
        """return certain save game attributes from the config or, if they're not in the config yet,
        get them from the save file and save them into the config
        """
        if self.SAVES not in self._data:
            self._data[self.SAVES] = {}
        if savename not in self._data[self.SAVES]:
            attrs = get_save_attrs(savename)
            self._data[self.SAVES][savename] = {}
            self._data[self.SAVES][savename][self.PNAME] = attrs['player/name']
            self._data[self.SAVES][savename][self.FNAME] = f"{attrs['player/farmName']} Farm"
            ingame_date = f"{attrs['dayOfMonth']} {attrs['currentSeason']} year {attrs['year']}"
            self._data[self.SAVES][savename][self.GDATE] = ingame_date
        return (self._data[self.SAVES][savename][self.PNAME],
                self._data[self.SAVES][savename][self.FNAME],
                self._data[self.SAVES][savename][self.GDATE])

    def get_mods_for_saveitem(self, savename):
        """return the names of the mods that are associated with this save
        """
        if self.SAVES not in self._data:
            self._data[self.SAVES] = {}
        if savename not in self._data[self.SAVES]:
            return []
        modnames = self._data[self.SAVES][savename].get(self.MODS, [])
        # for name in modnames:
        return modnames

    def update_saveitem_data(self, savename, key, value):
        "set the value for a given key for the given savefile"
        if key not in self.knownsavekeys:
            raise ValueError(f"Unknown key '{key}' for savedata {savename}")
        if self.SAVES not in self._data:
            self._data[self.SAVES] = {}
        if savename not in self._data[self.SAVES]:
            self._data[self.SAVES][savename] = {}
        self._data[self.SAVES][savename][key] = value

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
        for item in self.list_components_for_dir(dirname):
            value = self.get_component_data(item, self.NXSKEY).strip().replace('?', '').split('@')[0]
            if value and value != '-1':
                value = int(value)
                if value != nexusid:
                    if not nexusid:
                        nexusid = value
        if nexusid:
            self.set_diritem_value(dirname, self.NXSKEY, int(nexusid))
