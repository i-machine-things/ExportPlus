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

"""ExportPlus Workbench - Enhanced export functionality with scaling options"""

import FreeCAD

FreeCAD.Console.PrintLog("Loading ExportPlus module...\n")

# Optional: Register commands globally (available in all workbenches)
# Uncomment the lines below to add "Export with Scaling" to the File menu
# This makes the functionality available without switching to the ExportPlus workbench

# try:
#     import exportplus_init_global
#     # This will be called when FreeCAD GUI is ready
#     from PySide import QtCore
#     QtCore.QTimer.singleShot(2000, exportplus_init_global.add_to_file_menu)
# except Exception as e:
#     FreeCAD.Console.PrintWarning(f"ExportPlus: Could not register global integration: {e}\n")
