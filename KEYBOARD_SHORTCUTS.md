# ExportPlus Keyboard Shortcuts

## Built-in Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| **Ctrl+E** | Export STEP | Export to STEP format with scaling |
| **Ctrl+Shift+S** | Export STL | Export to STL format with scaling |
| **Ctrl+Shift+D** | Export DXF | Export to DXF format with scaling |

## How to Customize Shortcuts

If you want to change or add more shortcuts:

1. **Open Tools → Customize**
2. **Go to Keyboard tab**
3. **Select "ExportPlus" from Category dropdown**
4. **Click on a command** (e.g., "ExportPlus_OBJ")
5. **Press your desired key combination** in the "Press shortcut key" field
6. **Click "Assign"**
7. **Click "OK"**

### Recommended Custom Shortcuts

Here are some suggestions for formats that don't have default shortcuts:

| Format | Suggested Shortcut | How to Set |
|--------|-------------------|------------|
| OBJ | Ctrl+Shift+O | Tools → Customize → Keyboard → ExportPlus_OBJ |
| SVG | Ctrl+Shift+V | Tools → Customize → Keyboard → ExportPlus_SVG |
| PDF | Ctrl+Shift+P | Tools → Customize → Keyboard → ExportPlus_PDF |

## Overriding Default Ctrl+E

FreeCAD's default Ctrl+E is used for "Export" (standard export dialog).

Our ExportPlus STEP command now uses **Ctrl+E** and will override the default when the ExportPlus workbench is active.

### Behavior:

- **When ExportPlus workbench is active**: Ctrl+E = Export STEP with scaling
- **When other workbench is active**: Ctrl+E = Standard export (if not using global mode)

### To make Ctrl+E always use ExportPlus:

1. **Enable Global Mode** (see USAGE.md)
2. Or **manually reassign** in Tools → Customize → Keyboard

## Quick Export Workflow

For fastest workflow:

1. **Model your part** (FreeCAD uses mm internally)
2. **Set scaling once** in preferences (e.g., inches = 0.0393701)
3. **Select objects** to export
4. **Press Ctrl+E** (STEP), Ctrl+Shift+S (STL), or Ctrl+Shift+D (DXF)
5. **Choose filename** and save

Done! File exported with scaling applied automatically.

## Tips

- **Ctrl+E is the fastest** - memorize this for quick STEP exports
- **Set scaling in preferences** before exporting (doesn't change between exports)
- **Check console** for confirmation: "Exporting STEP with scaling factor: X.XXX"
- **Use toolbar buttons** if you forget shortcuts (they show the format name)

## Modifier Key Reference

| Modifier | Windows/Linux | macOS |
|----------|---------------|-------|
| Ctrl | Ctrl | Cmd (⌘) |
| Shift | Shift | Shift |
| Alt | Alt | Option (⌥) |

## Conflict Resolution

If a shortcut is already in use:

1. FreeCAD will warn you
2. Choose to **replace** the old assignment or **cancel**
3. Or use a different key combination

Common conflicts:
- **Ctrl+E**: Standard Export (safe to override with ExportPlus)
- **Ctrl+S**: Save (don't override!)
- **Ctrl+Shift+S**: Usually available

## See Also

- [USAGE.md](USAGE.md) - Full usage guide
- [README.md](README.md) - Complete documentation
- Tools → Customize → Keyboard - FreeCAD's shortcut customization
