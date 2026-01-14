# SPDX-License-Identifier: LGPL-2.1-or-later
# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2026 ExportPlus Workbench                               *
# *                                                                         *
# *   This file is part of FreeCAD.                                         *
# *                                                                         *
# *   FreeCAD is free software: you can redistribute it and/or modify it    *
# *   under the terms of the GNU Lesser General Public License as           *
# *   published by the Free Software Foundation, either version 2.1 of the  *
# *   License, or (at your option) any later version.                       *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful, but        *
# *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
# *   Lesser General Public License for more details.                       *
# *                                                                         *
# *   You should have received a copy of the GNU Lesser General Public      *
# *   License along with FreeCAD. If not, see                               *
# *   <https://www.gnu.org/licenses/>.                                      *
# *                                                                         *
# ***************************************************************************

"""
Global initialization for ExportPlus - makes export commands available everywhere

To enable global integration, add this to Init.py:
    import exportplus_init_global
    exportplus_init_global.register_global_commands()
"""

import FreeCAD
import FreeCADGui


def register_global_commands():
    """
    Register ExportPlus commands globally so they're available in all workbenches
    """
    try:
        import exportplus_commands

        # Commands are already registered by exportplus_commands module
        # Now we add them to the File menu of ALL workbenches

        # This will be called when FreeCAD starts
        FreeCAD.Console.PrintLog("ExportPlus: Registering global export commands\n")

        # We can't modify other workbenches directly, but we can add items
        # to the main window menus
        # This would require C++ integration or waiting for FreeCAD to fully load

    except Exception as e:
        FreeCAD.Console.PrintWarning(f"ExportPlus: Could not register global commands: {e}\n")


def add_to_file_menu():
    """
    Add ExportPlus commands to the File menu
    This should be called after FreeCAD GUI is fully loaded
    """
    try:
        from PySide import QtGui

        # Find the main window
        main_window = FreeCADGui.getMainWindow()
        if not main_window:
            return

        # Find the File menu
        menu_bar = main_window.menuBar()
        file_menu = None

        for action in menu_bar.actions():
            if action.text().replace("&", "") == "File":
                file_menu = action.menu()
                break

        if not file_menu:
            FreeCAD.Console.PrintWarning("ExportPlus: Could not find File menu\n")
            return

        # Add a separator and our export submenu
        file_menu.addSeparator()

        export_menu = file_menu.addMenu("Export with Scaling")
        export_menu.setToolTip("Export with automatic unit scaling")

        # Add our export commands
        commands = [
            ("ExportPlus_STEP", "STEP"),
            ("ExportPlus_STL", "STL"),
            ("ExportPlus_OBJ", "OBJ"),
            ("ExportPlus_SVG", "SVG"),
            ("ExportPlus_DXF", "DXF"),
            ("ExportPlus_PDF", "PDF"),
        ]

        for cmd_name, label in commands:
            action = export_menu.addAction(label)
            action.setToolTip(f"Export to {label} with scaling")
            action.triggered.connect(lambda checked, cmd=cmd_name: FreeCADGui.runCommand(cmd))

        FreeCAD.Console.PrintLog("ExportPlus: Added to File menu\n")

    except Exception as e:
        FreeCAD.Console.PrintWarning(f"ExportPlus: Could not add to File menu: {e}\n")
