"""import symbols for the right gui toolkit
"""
from .toolkit import toolkit
if toolkit == 'qt':
    from .qtgui import (ShowMods, show_message, show_dialog, SettingsDialogGui, DeleteDialogGui,
                        AttributesDialogGui, DependencyDialogGui, SaveGamesDialogGui,
                        RestoreDialogGui)
elif toolkit == 'tk':
    from .tkgui import (ShowMods, show_message, show_dialog, SettingsDialogGui, DeleteDialogGui,
                        AttributesDialogGui, DependencyDialogGui, SaveGamesDialogGui,
                        RestoreDialogGui)
