"""import symbols for the right gui toolkit
"""
from .toolkit import toolkit
if toolkit == 'qt':
    from .qtgui import ShowMods, show_dialog, SettingsDialog, AttributesDialog, SaveGamesDialog
elif toolkit == 'tk':
    from .tkgui import ShowMods, show_dialog, SettingsDialog, AttributesDialog, SaveGamesDialog
