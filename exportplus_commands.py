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

"""Export commands with scaling support"""

import os
import sys
import tempfile
import FreeCAD
import FreeCADGui
import Part
from PySide import QtGui, QtCore


class QuickExportDialog(QtGui.QDialog):
    """Quick export dialog to choose format"""

    def __init__(self, parent=None):
        super(QuickExportDialog, self).__init__(parent)
        self.setWindowTitle("Quick Export with Scaling")
        self.setModal(True)

        layout = QtGui.QVBoxLayout()

        # Instructions
        label = QtGui.QLabel("Choose export format:")
        label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(label)

        # Format buttons with icons and shortcuts
        self.format_buttons = {}
        formats = [
            ("STEP", "S", "CAD interchange format"),
            ("STL", "T", "3D printing / mesh format"),
            ("OBJ", "O", "3D graphics format"),
            ("DXF", "D", "2D CAD format"),
            ("SVG", "V", "2D vector graphics"),
            ("PDF", "P", "Portable document format"),
        ]

        for format_name, shortcut, description in formats:
            btn = QtGui.QPushButton(f"{format_name} - {description}")
            btn.setToolTip(f"{description}\n\nKeyboard shortcut: {shortcut}")
            btn.setMinimumHeight(40)
            btn.setStyleSheet("text-align: left; padding: 8px; font-size: 11pt;")
            btn.clicked.connect(lambda checked=False, fmt=format_name: self.accept_format(fmt))
            self.format_buttons[format_name] = btn
            layout.addWidget(btn)

        # Cancel button
        layout.addSpacing(10)
        btn_cancel = QtGui.QPushButton("Cancel (Esc)")
        btn_cancel.clicked.connect(self.reject)
        layout.addWidget(btn_cancel)

        self.setLayout(layout)
        self.selected_format = None

        # Set size
        self.resize(450, 400)

    def accept_format(self, format_name):
        self.selected_format = format_name
        self.accept()

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        key = event.text().upper()
        format_map = {
            'S': 'STEP',
            'T': 'STL',
            'O': 'OBJ',
            'D': 'DXF',
            'V': 'SVG',
            'P': 'PDF',
        }

        if key in format_map:
            self.accept_format(format_map[key])
        else:
            super(QuickExportDialog, self).keyPressEvent(event)


def get_icon_path(format_name):
    """Get the path to the icon for a specific format"""
    icon_file = f"export-{format_name.lower()}.svg"

    # Try to find the icon in sys.path
    for path in sys.path:
        candidate = os.path.join(path, "ExportPlus", "Resources", "icons", icon_file)
        if os.path.exists(candidate):
            return candidate

    # Try alternate locations
    possible_paths = [
        os.path.join(FreeCAD.getUserAppDataDir(), "Mod", "ExportPlus", "Resources", "icons", icon_file),
        os.path.join(FreeCAD.getResourceDir(), "..", "Mod", "ExportPlus", "Resources", "icons", icon_file),
        os.path.join(FreeCAD.getResourceDir(), "Mod", "ExportPlus", "Resources", "icons", icon_file),
    ]

    for path in possible_paths:
        normalized = os.path.normpath(path)
        if os.path.exists(normalized):
            return normalized

    # Fallback to standard icon
    return "Std_Export"


def get_scaling_factor(format_name):
    """Get the scaling factor for a specific export format"""
    param_grp = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/ExportPlus")

    # Try format-specific setting first
    scale = param_grp.GetFloat(f"{format_name}ScalingFactor", 0.0)

    # If not set, use global setting
    if scale == 0.0:
        scale = param_grp.GetFloat("GlobalScalingFactor", 1.0)

    return scale


def scale_object(obj, scale_factor):
    """Create a scaled copy of an object"""
    if scale_factor == 1.0:
        return obj

    if hasattr(obj, "Shape") and hasattr(obj.Shape, "scale"):
        # Create a copy and scale it
        scaled_shape = obj.Shape.copy()
        scaled_shape.scale(scale_factor)
        return scaled_shape

    return obj


def export_with_scaling(file_path, objects, format_name, export_func):
    """
    Generic export function with scaling support

    Parameters:
    - file_path: Output file path
    - objects: List of objects to export
    - format_name: Format identifier (e.g., "STEP", "STL")
    - export_func: The actual export function to call
    """
    scale_factor = get_scaling_factor(format_name)

    FreeCAD.Console.PrintMessage(
        f"Exporting {format_name} with scaling factor: {scale_factor}\n"
    )

    if scale_factor == 1.0:
        # No scaling needed, export directly
        export_func(file_path, objects)
    else:
        # Create temporary scaled objects
        doc = FreeCAD.ActiveDocument
        temp_objs = []

        try:
            for obj in objects:
                if hasattr(obj, "Shape") and obj.Shape:
                    # Create a temporary object with scaled shape
                    temp_obj = doc.addObject("Part::Feature", "TempScaled")
                    # Make a copy and scale it - scale() returns a new shape
                    scaled_shape = obj.Shape.copy()
                    scaled_shape.scale(scale_factor)
                    temp_obj.Shape = scaled_shape
                    temp_objs.append(temp_obj)
                else:
                    temp_objs.append(obj)

            # Recompute to ensure shapes are valid
            doc.recompute()

            # Export the scaled objects
            export_func(file_path, temp_objs)

        finally:
            # Clean up temporary objects
            for obj in temp_objs:
                if hasattr(obj, "Name") and obj.Name.startswith("TempScaled"):
                    try:
                        doc.removeObject(obj.Name)
                    except:
                        pass  # Object might already be deleted


class ExportPlusSTEP:
    """Export to STEP format with scaling"""

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('STEP'),
            'MenuText': 'STEP',
            'ToolTip': 'Export to STEP format with optional unit scaling\n\nCurrent scaling: check Edit → Preferences → Import-Export → Export Plus Settings'
        }

    def Activated(self):
        # Get file path from user
        file_path = QtGui.QFileDialog.getSaveFileName(
            QtGui.QApplication.activeWindow(),
            "Export STEP",
            "",
            "STEP files (*.step *.stp);;All files (*.*)"
        )[0]

        if not file_path:
            return

        # Get selected objects
        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            FreeCAD.Console.PrintError("No objects selected for export\n")
            return

        # Export with scaling
        def export_step(path, objs):
            import Import
            Import.export(objs, path)

        export_with_scaling(file_path, selection, "STEP", export_step)

        FreeCAD.Console.PrintMessage(f"Exported to {file_path}\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class ExportPlusSTL:
    """Export to STL format with scaling"""

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('STL'),
            'MenuText': 'STL',
            'Accel': 'Ctrl+Shift+S',
            'ToolTip': 'Export to STL format with optional unit scaling (Ctrl+Shift+S)'
        }

    def Activated(self):
        file_path = QtGui.QFileDialog.getSaveFileName(
            QtGui.QApplication.activeWindow(),
            "Export STL",
            "",
            "STL files (*.stl);;All files (*.*)"
        )[0]

        if not file_path:
            return

        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            FreeCAD.Console.PrintError("No objects selected for export\n")
            return

        def export_stl(path, objs):
            import Mesh
            # Merge all shapes and export
            shapes = [obj.Shape for obj in objs if hasattr(obj, 'Shape')]
            if shapes:
                compound = Part.makeCompound(shapes)
                Mesh.export([compound], path)

        export_with_scaling(file_path, selection, "STL", export_stl)

        FreeCAD.Console.PrintMessage(f"Exported to {file_path}\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class ExportPlusOBJ:
    """Export to OBJ format with scaling"""

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('OBJ'),
            'MenuText': 'OBJ',
            'ToolTip': 'Export to OBJ format with optional unit scaling'
        }

    def Activated(self):
        file_path = QtGui.QFileDialog.getSaveFileName(
            QtGui.QApplication.activeWindow(),
            "Export OBJ",
            "",
            "OBJ files (*.obj);;All files (*.*)"
        )[0]

        if not file_path:
            return

        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            FreeCAD.Console.PrintError("No objects selected for export\n")
            return

        def export_obj(path, objs):
            import Mesh
            shapes = [obj.Shape for obj in objs if hasattr(obj, 'Shape')]
            if shapes:
                compound = Part.makeCompound(shapes)
                Mesh.export([compound], path)

        export_with_scaling(file_path, selection, "OBJ", export_obj)

        FreeCAD.Console.PrintMessage(f"Exported to {file_path}\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class ExportPlusSVG:
    """Export to SVG format with scaling"""

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('SVG'),
            'MenuText': 'SVG',
            'ToolTip': 'Export to SVG format with optional unit scaling'
        }

    def Activated(self):
        file_path = QtGui.QFileDialog.getSaveFileName(
            QtGui.QApplication.activeWindow(),
            "Export SVG",
            "",
            "SVG files (*.svg);;All files (*.*)"
        )[0]

        if not file_path:
            return

        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            FreeCAD.Console.PrintError("No objects selected for export\n")
            return

        def export_svg(path, objs):
            import importSVG
            importSVG.export(objs, path)

        export_with_scaling(file_path, selection, "SVG", export_svg)

        FreeCAD.Console.PrintMessage(f"Exported to {file_path}\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class ExportPlusDXF:
    """Export to DXF format with scaling"""

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('DXF'),
            'MenuText': 'DXF',
            'Accel': 'Ctrl+Shift+D',
            'ToolTip': 'Export to DXF format with optional unit scaling (Ctrl+Shift+D)'
        }

    def Activated(self):
        file_path = QtGui.QFileDialog.getSaveFileName(
            QtGui.QApplication.activeWindow(),
            "Export DXF",
            "",
            "DXF files (*.dxf);;All files (*.*)"
        )[0]

        if not file_path:
            return

        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            FreeCAD.Console.PrintError("No objects selected for export\n")
            return

        def export_dxf(path, objs):
            import importDXF
            importDXF.export(objs, path)

        export_with_scaling(file_path, selection, "DXF", export_dxf)

        FreeCAD.Console.PrintMessage(f"Exported to {file_path}\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class ExportPlusPDF:
    """Export to PDF format with scaling"""

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('PDF'),
            'MenuText': 'PDF',
            'ToolTip': 'Export to PDF format with optional unit scaling'
        }

    def Activated(self):
        file_path = QtGui.QFileDialog.getSaveFileName(
            QtGui.QApplication.activeWindow(),
            "Export PDF",
            "",
            "PDF files (*.pdf);;All files (*.*)"
        )[0]

        if not file_path:
            return

        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            FreeCAD.Console.PrintError("No objects selected for export\n")
            return

        def export_pdf(path, objs):
            # PDF export typically requires TechDraw pages
            FreeCAD.Console.PrintWarning(
                "PDF export requires TechDraw pages. "
                "Use TechDraw workbench to create drawings first.\n"
            )

        export_with_scaling(file_path, selection, "PDF", export_pdf)

        FreeCAD.Console.PrintMessage(f"Exported to {file_path}\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


class ExportPlusQuick:
    """Quick export - choose format from dialog"""

    def GetResources(self):
        return {
            'Pixmap': 'Std_Export',
            'MenuText': 'Quick Export...',
            'Accel': 'Ctrl+Shift+E',
            'ToolTip': 'Quick export - choose format (Ctrl+Shift+E)\n\nShows dialog to select export format with scaling'
        }

    def Activated(self):
        # Check for selection
        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            FreeCAD.Console.PrintError("No objects selected for export\n")
            QtGui.QMessageBox.warning(
                QtGui.QApplication.activeWindow(),
                "No Selection",
                "Please select objects to export"
            )
            return

        # Show format selection dialog
        dialog = QuickExportDialog(QtGui.QApplication.activeWindow())
        if dialog.exec_() != QtGui.QDialog.Accepted or not dialog.selected_format:
            return

        format_name = dialog.selected_format

        # Map format to file extension and filter
        format_info = {
            'STEP': ('.step', 'STEP files (*.step *.stp);;All files (*.*)'),
            'STL': ('.stl', 'STL files (*.stl);;All files (*.*)'),
            'OBJ': ('.obj', 'OBJ files (*.obj);;All files (*.*)'),
            'DXF': ('.dxf', 'DXF files (*.dxf);;All files (*.*)'),
            'SVG': ('.svg', 'SVG files (*.svg);;All files (*.*)'),
            'PDF': ('.pdf', 'PDF files (*.pdf);;All files (*.*)'),
        }

        ext, file_filter = format_info.get(format_name, ('.step', 'All files (*.*)'))

        # Get file path from user
        file_path = QtGui.QFileDialog.getSaveFileName(
            QtGui.QApplication.activeWindow(),
            f"Export {format_name}",
            "",
            file_filter
        )[0]

        if not file_path:
            return

        # Define export functions
        def export_step(path, objs):
            import Import
            Import.export(objs, path)

        def export_stl(path, objs):
            import Mesh
            shapes = [obj.Shape for obj in objs if hasattr(obj, 'Shape')]
            if shapes:
                compound = Part.makeCompound(shapes)
                Mesh.export([compound], path)

        def export_obj(path, objs):
            import Mesh
            shapes = [obj.Shape for obj in objs if hasattr(obj, 'Shape')]
            if shapes:
                compound = Part.makeCompound(shapes)
                Mesh.export([compound], path)

        def export_dxf(path, objs):
            import importDXF
            importDXF.export(objs, path)

        def export_svg(path, objs):
            import importSVG
            importSVG.export(objs, path)

        def export_pdf(path, objs):
            FreeCAD.Console.PrintWarning(
                "PDF export requires TechDraw pages. "
                "Use TechDraw workbench to create drawings first.\n"
            )

        # Map format to export function
        export_functions = {
            'STEP': export_step,
            'STL': export_stl,
            'OBJ': export_obj,
            'DXF': export_dxf,
            'SVG': export_svg,
            'PDF': export_pdf,
        }

        export_func = export_functions.get(format_name)
        if export_func:
            export_with_scaling(file_path, selection, format_name, export_func)
            FreeCAD.Console.PrintMessage(f"Exported to {file_path}\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


# Register all commands
FreeCADGui.addCommand('ExportPlus_Quick', ExportPlusQuick())
FreeCADGui.addCommand('ExportPlus_STEP', ExportPlusSTEP())
FreeCADGui.addCommand('ExportPlus_STL', ExportPlusSTL())
FreeCADGui.addCommand('ExportPlus_OBJ', ExportPlusOBJ())
FreeCADGui.addCommand('ExportPlus_SVG', ExportPlusSVG())
FreeCADGui.addCommand('ExportPlus_DXF', ExportPlusDXF())
FreeCADGui.addCommand('ExportPlus_PDF', ExportPlusPDF())
