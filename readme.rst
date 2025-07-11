Stardew Valley Mods Manager
===========================

For use with the user-written extensions (called "mods") for a game I very much like playing.

Based on the given that the files for all the mods exist in directories per mod which in turn all are collected in one "mod directory" and are active unless they are "hidden" (having a dot preceding the directory name).

It uses a configuration file containing all these directory names as well as the dependencies between the mods.

In the gui you can select which mods to activate, it shows which mods are already activated. When you activate a mod, mods they in turn depend on should automatically also be activated.

The configuration is primarily built while installing the mods; they contain metadata about their structure which is read and converted for use. Installing is basically unzipping a downloaded mod file into the directory from where they are used. Reinstalling a(n updated) mod can also update the config if necessary.

More stuff is defined in the configuration, most importantly it holds a list of all your save files and the mods they use, which may come in handy when you want to replay on an earlier save file, as you have the opportunity to activate all the mods it uses in one go.


How to set up
-------------

Create a shortcut to ``start.py`` in a directory on your system path. Adapt the shebang line if needed. 
Edit ``toolkit.py`` to point to the type of gui you want to use (PyQt is the default, but you can switch to Tkinter if you don't want to install it). 
Use the "Set Defaults" option to define some locations the program needs and download and install some mods to start populating the configuration.


Dependencies of the project:
----------------------------
- Python
- PyQt or TkInter


Changes summary:
................

This used to be a very simple app, but it escalated quickly.

- Originally you had to enter the mod names, locations and dependencies manually, this is all done automatically now. You can still add a dependency manually if the mod author forgot to include it in the manifest.
- Added a way to install a mod directly from this GUI. This started the move from maintaining the config manually to managing it automatically. 
- I abandoned trying to create the possibilty to reorder the displayed names in favor of a distinction between mods you can activate by themselves and ones that you can't. So I had to build a means to indicate that, among other "mod attributes".
- I added a way to register your save files with the mods they use, as well as a way to indicate a mod is to be "always on".
