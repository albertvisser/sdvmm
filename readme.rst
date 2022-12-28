Stardew Valley Mods Manager
===========================

Based on the assumption that the files for all the mods exist in directories per mod which in turn all are collected in one "mod directory" and are active unless they are "hidden" (having a dot preceding the directory name).

It uses a configuration file containing all these directory names as well as the dependencies between the mods.

In the gui you can select which mods to activate, it shows which mods are already activated. When you activate an extesion, mods they depend on should automatically also be activated.

Because names are important, there's also an option to check the configuration for (non-)matching names (spelling and case).

Dependencies of the project:
----------------------------
- Python
- PyQt6
