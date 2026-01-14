# SPDX-License-Identifier: LGPL-2.1-or-later
# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2026 ExportPlus Workbench                               *
# *                                                                         *
# *   This file is part of the ExportPlus FreeCAD Workbench.                *
# *                                                                         *
# *   ExportPlus is free software: you can redistribute it and/or modify    *
# *   it under the terms of the GNU Lesser General Public License as        *
# *   published by the Free Software Foundation, either version 2.1 of the  *
# *   License, or (at your option) any later version.                       *
# *                                                                         *
# *   ExportPlus is distributed in the hope that it will be useful, but     *
# *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
# *   Lesser General Public License for more details.                       *
# *                                                                         *
# *   You should have received a copy of the GNU Lesser General Public      *
# *   License along with ExportPlus. If not, see                               *
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

# Global list to keep shortcuts alive (prevent garbage collection)
_global_shortcuts = []


def register_global_commands():
    """
    Register ExportPlus commands globally so they're available in all workbenches
    """
    try:
        FreeCAD.Console.PrintLog("ExportPlus: Importing exportplus_commands module...\n")

        # Import commands module - this will register all commands globally
        import exportplus_commands

        FreeCAD.Console.PrintLog("ExportPlus: Global export commands registered\n")

        # Verify commands are registered
        try:
            test_cmd = FreeCADGui.Command.get("ExportPlus_Quick")
            if test_cmd:
                FreeCAD.Console.PrintLog("ExportPlus: Command registration verified\n")
            else:
                FreeCAD.Console.PrintWarning("ExportPlus: Commands may not be properly registered\n")
        except:
            FreeCAD.Console.PrintWarning("ExportPlus: Could not verify command registration\n")

    except Exception as e:
        import traceback
        FreeCAD.Console.PrintWarning(f"ExportPlus: Could not register global commands: {e}\n")
        FreeCAD.Console.PrintWarning(f"Traceback: {traceback.format_exc()}\n")


def add_to_file_menu():
    """
    Add ExportPlus commands to the File menu
    This should be called after FreeCAD GUI is fully loaded
    """
    try:
        from PySide import QtGui, QtCore

        FreeCAD.Console.PrintLog("ExportPlus: Starting global menu integration...\n")

        # Register commands first
        register_global_commands()

        # Find the main window
        main_window = FreeCADGui.getMainWindow()
        if not main_window:
            FreeCAD.Console.PrintWarning("ExportPlus: Main window not available\n")
            return

        # Create global keyboard shortcuts that work in all workbenches
        # This is the key - we need to add shortcuts directly to the main window
        global _global_shortcuts

        shortcuts = [
            ("Ctrl+Shift+E", "ExportPlus_Quick"),
            ("Ctrl+Shift+S", "ExportPlus_STL"),
            ("Ctrl+Shift+D", "ExportPlus_DXF"),
        ]

        for key_seq, cmd_name in shortcuts:
            try:
                shortcut = QtGui.QShortcut(QtGui.QKeySequence(key_seq), main_window)
                shortcut.setContext(QtCore.Qt.ApplicationShortcut)  # Works globally
                shortcut.activated.connect(lambda cmd=cmd_name: FreeCADGui.runCommand(cmd))
                _global_shortcuts.append(shortcut)  # Keep reference to prevent garbage collection
                FreeCAD.Console.PrintLog(f"ExportPlus: Registered global shortcut {key_seq} -> {cmd_name}\n")
            except Exception as e:
                FreeCAD.Console.PrintWarning(f"ExportPlus: Failed to register shortcut {key_seq}: {e}\n")

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

        # Add Quick Export command first
        quick_action = export_menu.addAction("Quick Export... (Ctrl+Shift+E)")
        quick_action.setToolTip("Quick export - choose format (Ctrl+Shift+E)")
        quick_action.triggered.connect(lambda checked=False: FreeCADGui.runCommand("ExportPlus_Quick"))

        export_menu.addSeparator()

        # Add our export commands
        commands = [
            ("ExportPlus_STEP", "STEP"),
            ("ExportPlus_STL", "STL (Ctrl+Shift+S)"),
            ("ExportPlus_OBJ", "OBJ"),
            ("ExportPlus_SVG", "SVG"),
            ("ExportPlus_DXF", "DXF (Ctrl+Shift+D)"),
            ("ExportPlus_PDF", "PDF"),
        ]

        for cmd_name, label in commands:
            action = export_menu.addAction(label)
            action.setToolTip(f"Export to {label} with scaling")
            action.triggered.connect(lambda checked=False, cmd=cmd_name: FreeCADGui.runCommand(cmd))

        FreeCAD.Console.PrintLog("ExportPlus: Added to File menu\n")

    except Exception as e:
        import traceback
        FreeCAD.Console.PrintWarning(f"ExportPlus: Could not add to File menu: {e}\n")
        FreeCAD.Console.PrintWarning(f"Traceback: {traceback.format_exc()}\n")
