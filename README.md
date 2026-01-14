# ExportPlus Workbench

Enhanced export functionality for FreeCAD with built-in unit scaling.

## Overview

ExportPlus is a FreeCAD workbench that provides all the standard export capabilities with an added feature: **automatic unit scaling**. This allows you to export your models directly in the units you need (e.g., inches instead of millimeters) without manually scaling your models first.

## Features

- **All Standard Export Formats** supported:
  - STEP (.step, .stp)
  - STL (.stl)
  - OBJ (.obj)
  - DXF (.dxf)
  - SVG (.svg)
  - PDF (.pdf)

- **Global Scaling Factor**: Set one scaling factor that applies to all exports
- **Per-Format Scaling**: Override the global setting for specific formats
- **Quick Presets**: One-click buttons for common unit conversions:
  - Millimeters (1.0) - FreeCAD default
  - Inches (0.0393701) - Convert mm to inches
  - Centimeters (0.1) - Convert mm to cm
  - Meters (0.001) - Convert mm to meters

## Installation

### Option 1: Build with FreeCAD

This workbench is included in the FreeCAD source tree under `src/Mod/ExportPlus/`.

To enable it during build:
```bash
cmake -DBUILD_EXPORTPLUS=ON ..
make
```

### Option 2: Manual Installation

1. Copy the `ExportPlus` folder to your FreeCAD Mod directory:
   - **Windows**: `%APPDATA%\FreeCAD\Mod\`
   - **Linux**: `~/.FreeCAD/Mod/`
   - **macOS**: `~/Library/Application Support/FreeCAD/Mod/`

2. Restart FreeCAD

3. The "Export Plus" workbench should appear in the workbench selector

## Usage

### Basic Export with Scaling

1. **Select objects** you want to export in the 3D view
2. **Switch to Export Plus workbench** from the workbench dropdown
3. **Click the appropriate export button** (STEP, STL, OBJ, etc.)
4. **Choose a file location** and save
5. The file will be exported with the scaling factor applied

### Configuring Scaling Factors

1. Go to **Edit → Preferences**
2. Navigate to **Import-Export → Export Plus Settings**
3. Set your desired scaling factors:
   - **Global scaling factor**: Applies to all formats by default
   - **Format-specific factors**: Override global setting for individual formats (set to 0 to use global)

### Common Unit Conversions

| From | To | Scaling Factor |
|------|-----|---------------|
| mm | inches | 0.0393701 (1/25.4) |
| mm | cm | 0.1 |
| mm | meters | 0.001 |
| mm | feet | 0.00328084 |
| inches | mm | 25.4 |
| cm | mm | 10.0 |
| meters | mm | 1000.0 |

### Example: Exporting to Inches

**Scenario**: You have a model in FreeCAD (which uses mm internally) and need to export it as a STEP file in inches for a machinist.

**Method 1 - Use Global Setting:**
1. Open Preferences → Import-Export → Export Plus Settings
2. Set "Global scaling factor" to `0.0393701` (or click the "Inches" preset button)
3. Use Export Plus → Export STEP
4. Your file is now in inches!

**Method 2 - Use Format-Specific Setting:**
1. Open Preferences → Import-Export → Export Plus Settings
2. Under "STEP Format", set scaling factor to `0.0393701`
3. This only affects STEP exports, other formats use the global setting

## Technical Details

### How It Works

1. **Selection**: Export commands work on currently selected objects
2. **Temporary Scaling**: The workbench creates temporary scaled copies of your geometry
3. **Standard Export**: Uses FreeCAD's built-in export functions with the scaled geometry
4. **Cleanup**: Temporary objects are automatically removed after export
5. **Original Unchanged**: Your original model is never modified

### Scaling Method

The workbench uses the `Shape.scale()` method to scale geometry uniformly in all three axes. This ensures:
- Dimensional accuracy
- Preserved proportions
- No loss of detail
- Compatible output for all formats

### Preferences Storage

All settings are stored in FreeCAD's parameter system under:
```
User parameter:BaseApp/Preferences/Mod/ExportPlus/
```

Parameters:
- `GlobalScalingFactor` (float, default: 1.0)
- `STEPScalingFactor` (float, default: 0.0)
- `STLScalingFactor` (float, default: 0.0)
- `OBJScalingFactor` (float, default: 0.0)
- `DXFScalingFactor` (float, default: 0.0)
- `SVGScalingFactor` (float, default: 0.0)

## Supported Export Formats

### STEP (ISO 10303)
- Extensions: `.step`, `.stp`
- Uses: Import.export()
- Best for: Parametric CAD interchange

### STL (Stereolithography)
- Extension: `.stl`
- Uses: Mesh.export()
- Best for: 3D printing, mesh-based applications

### OBJ (Wavefront)
- Extension: `.obj`
- Uses: Mesh.export()
- Best for: 3D graphics, visualization

### DXF (Drawing Exchange Format)
- Extension: `.dxf`
- Uses: importDXF.export()
- Best for: 2D CAD, laser cutting, CNC

### SVG (Scalable Vector Graphics)
- Extension: `.svg`
- Uses: importSVG.export()
- Best for: 2D vector graphics, web graphics

### PDF (Portable Document Format)
- Extension: `.pdf`
- Uses: TechDraw pages
- Best for: Documentation, drawings
- **Note**: Requires existing TechDraw pages

## Troubleshooting

### "No objects selected for export"
- Make sure you have selected one or more objects in the 3D view before clicking export

### Export appears at wrong scale
- Check your scaling factor in Preferences
- Verify which unit system the target application expects
- Remember: FreeCAD uses millimeters internally

### PDF export not working
- PDF export requires TechDraw pages to be created first
- Use the TechDraw workbench to create drawing views
- Then use standard File → Export for PDF

### Workbench doesn't appear
- Verify the ExportPlus folder is in the correct Mod directory
- Restart FreeCAD completely
- Check the FreeCAD console (View → Panels → Report view) for error messages

## Limitations

- **Object Types**: Only objects with valid `Shape` attributes can be scaled and exported
- **Assemblies**: Complex assemblies may need to be exported as separate parts
- **Metadata**: Some format-specific metadata is not preserved (colors, materials, etc.)
- **Performance**: Very large models may take time to scale and export

## Development

### File Structure
```
ExportPlus/
├── Init.py                          # Module initialization
├── InitGui.py                       # Workbench definition and GUI setup
├── exportplus_commands.py           # Export command implementations
├── README.md                        # This file
└── Resources/
    ├── icons/
    │   └── ExportPlus.svg          # Workbench icon
    └── ui/
        └── preferences-exportplus.ui # Preferences page
```

### Adding New Export Formats

To add a new export format:

1. Create a new command class in `exportplus_commands.py`:
```python
class ExportPlusNEWFORMAT:
    def GetResources(self):
        return {
            'Pixmap': 'Std_Export',
            'MenuText': 'Export NEWFORMAT (with scaling)',
            'ToolTip': 'Export to NEWFORMAT with unit scaling'
        }

    def Activated(self):
        # ... implementation ...

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None
```

2. Register the command:
```python
FreeCADGui.addCommand('ExportPlus_NEWFORMAT', ExportPlusNEWFORMAT())
```

3. Add to command list in `InitGui.py`

4. Add scaling options to `preferences-exportplus.ui`

## Contributing

Contributions are welcome! Please:
1. Test your changes thoroughly
2. Follow the existing code style
3. Update documentation
4. Submit pull requests to the main FreeCAD repository

## License

LGPL-2.1-or-later (same as FreeCAD)

## Credits

Created as an enhancement to FreeCAD's export capabilities.

Built upon FreeCAD's existing export modules:
- Import (STEP)
- Mesh (STL, OBJ)
- importDXF
- importSVG

## Support

For issues and questions:
- FreeCAD Forum: https://forum.freecad.org/
- Bug Reports: https://github.com/FreeCAD/FreeCAD/issues

## Changelog

### Version 1.0.0 (2026-01-13)
- Initial release
- Support for STEP, STL, OBJ, DXF, SVG formats
- Global and per-format scaling factors
- Quick preset buttons for common conversions
- Preferences UI integration
