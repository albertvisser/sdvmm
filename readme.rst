Stardew Valley Mods Manager
===========================

For use with the user-written extensions (called "mods") for a game I very much like playing.

Based on the assumption that the files for all the mods exist in directories per mod which in turn all are collected in one "mod directory" and are active unless they are "hidden" (having a dot preceding the directory name).

It uses a configuration file containing all these directory names as well as the dependencies between the mods.

In the gui you can select which mods to activate, it shows which mods are already activated. When you activate an extension, mods they depend on should automatically also be activated.

In the config you define a mod by associating the mod's directory name to the mod's display name. 
Mods that need to be activatable must be named in a header (display name surrounded by [ and ]). 
Dependencies are defined by naming the dependent mod's display name under the header containing the name of the depending mod. 

Because names are important, there's an option to check the configuration for (non-)matching names (spelling and case).

There is also an option to directly edit the config file so you can add new mods to the collection.



How to set up
-------------

Modify the file `sdv_mods.config.example` to your needs and rename it removing the .example suffix. Either leave it in this directory or (what I did on my Linux system) move it to the mods installation directory and make a symlink to it here.


Dependencies of the project:
----------------------------
- Python
- PyQt(6)


Changes summary:
................

- Separated exiting the GUI from applying changes, so you can check and if necessary modify the results.
- Added a way to enter new mods and dependencies directly from the gui, without having to know the structure of the file.
- Added a (clunky) way to reorder the names on the screen.
- Added a way to install a mod from the downloads directory from this GUI.
