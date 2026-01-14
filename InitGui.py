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

"""ExportPlus Workbench - Enhanced export with scaling options"""

import os
import sys
import FreeCAD
import FreeCADGui


class ExportPlusWorkbench(Workbench):
    """ExportPlus Workbench - Enhanced export functionality"""

    @staticmethod
    def get_module_path():
        """Get the path to the ExportPlus module directory"""
        # Try to find the module path from sys.modules or sys.path
        for path in sys.path:
            candidate = os.path.join(path, "ExportPlus")
            if os.path.exists(candidate) and os.path.isdir(candidate):
                return candidate

        # Fallback: check common locations
        possible_paths = [
            os.path.join(FreeCAD.getUserAppDataDir(), "Mod", "ExportPlus"),
            os.path.join(FreeCAD.getResourceDir(), "..", "Mod", "ExportPlus"),
            os.path.join(FreeCAD.getResourceDir(), "Mod", "ExportPlus"),
        ]

        for path in possible_paths:
            normalized = os.path.normpath(path)
            if os.path.exists(normalized):
                return normalized

        # Last resort - return empty string
        return ""

    def __init__(self):
        def QT_TRANSLATE_NOOP(context, text):
            return text

        # Get the path to this module
        mod_path = self.get_module_path()

        self.__class__.MenuText = QT_TRANSLATE_NOOP("ExportPlus", "Export Plus")
        self.__class__.ToolTip = QT_TRANSLATE_NOOP(
            "ExportPlus",
            "Enhanced export functionality with unit scaling"
        )

        icon_path = os.path.join(mod_path, "Resources", "icons", "ExportPlus.svg")
        if os.path.exists(icon_path):
            self.__class__.Icon = icon_path
        else:
            # Fallback to standard export icon
            self.__class__.Icon = "Std_Export"

    def Initialize(self):
        """Initialize the workbench"""
        import exportplus_commands

        # Create export commands
        self.export_commands = [
            "ExportPlus_Quick",  # Quick export with format chooser (Ctrl+E)
            "Separator",
            "ExportPlus_STEP",
            "ExportPlus_STL",
            "ExportPlus_OBJ",
            "ExportPlus_SVG",
            "ExportPlus_DXF",
            "ExportPlus_PDF",
        ]

        # Option 1: Add to File menu (integrates with standard FreeCAD workflow)
        # This adds our export commands to the File → Export submenu
        try:
            self.appendMenu(["&File", "Export with Scaling"], self.export_commands)
        except:
            # Fallback: create our own menu
            self.appendMenu("Export Plus", self.export_commands)

        # Option 2: Also create a toolbar for quick access
        self.appendToolbar("Export Plus", self.export_commands)

        # Load preferences page with custom class that connects buttons
        try:
            import ExportPlusPreferencePage
            FreeCADGui.addPreferencePage("ExportPlusPreferencePage.ExportPlusPreferencePage", "Import-Export")
            FreeCAD.Console.PrintLog("ExportPlus: Preferences page registered\n")
        except Exception as e:
            # Fallback to plain UI file if custom class fails
            FreeCAD.Console.PrintWarning(f"ExportPlus: Could not load custom preference page: {e}\n")
            mod_path = self.get_module_path()
            prefs_ui = os.path.join(mod_path, "Resources", "ui", "preferences-exportplus.ui")
            if os.path.exists(prefs_ui):
                FreeCADGui.addPreferencePage(prefs_ui, "Import-Export")

        FreeCAD.Console.PrintLog("ExportPlus Workbench initialized\n")

    def Activated(self):
        """Code to execute when workbench is activated"""
        # Try to connect preference buttons when workbench is activated
        # (user might open preferences while this workbench is active)
        try:
            import exportplus_preferences
            exportplus_preferences.connectPreferenceButtons()
        except:
            pass

    def Deactivated(self):
        """Code to execute when workbench is deactivated"""
        pass

    def ContextMenu(self, recipient):
        """Add commands to context menu"""
        self.appendContextMenu("Export Plus", self.export_commands)

    def GetClassName(self):
        """Return the C++ class name"""
        return "Gui::PythonWorkbench"


# Register the workbench
FreeCADGui.addWorkbench(ExportPlusWorkbench())

# Register global shortcuts and menu integration
# This makes ExportPlus commands available in all workbenches
def init_global_integration():
    """Initialize global commands when GUI is ready"""
    try:
        FreeCAD.Console.PrintLog("ExportPlus: Initializing global integration...\n")
        import exportplus_init_global
        exportplus_init_global.add_to_file_menu()
    except Exception as e:
        import traceback
        FreeCAD.Console.PrintWarning(f"ExportPlus: Could not register global integration: {e}\n")
        FreeCAD.Console.PrintWarning(f"Traceback: {traceback.format_exc()}\n")

# Schedule initialization after FreeCAD GUI is fully loaded
from PySide import QtCore
QtCore.QTimer.singleShot(2000, init_global_integration)
FreeCAD.Console.PrintLog("ExportPlus: Scheduled global integration\n")
