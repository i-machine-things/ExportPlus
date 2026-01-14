# ExportPlus Keyboard Shortcuts

## Global Shortcuts (Work in All Workbenches)

ExportPlus registers global keyboard shortcuts that work in **any workbench**, not just when ExportPlus is active:

| Shortcut | Action | Description |
|----------|--------|-------------|
| **Ctrl+Shift+E** | Quick Export | Opens format selection dialog with scaling |
| **Ctrl+Shift+S** | Export STL | Export to STL format with scaling |
| **Ctrl+Shift+D** | Export DXF | Export to DXF format with scaling |

These shortcuts are automatically registered when FreeCAD starts and are available globally.

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

## Quick Export Dialog (Ctrl+Shift+E)

The **Quick Export** feature provides a convenient dialog to choose your export format:

1. **Select objects** in the 3D view
2. **Press Ctrl+Shift+E** (works in any workbench)
3. **Choose format** from the dialog (STEP, STL, OBJ, DXF, SVG, or PDF)
4. Use **keyboard shortcuts in the dialog**:
   - **S** = STEP
   - **T** = STL
   - **O** = OBJ
   - **D** = DXF
   - **V** = SVG
   - **P** = PDF
   - **Esc** = Cancel
5. **Choose filename** and save

This is the fastest way to export with scaling!

## Quick Export Workflow

For fastest workflow:

1. **Model your part** (FreeCAD uses mm internally)
2. **Set scaling once** in preferences (e.g., inches = 0.0393701)
3. **Select objects** to export
4. **Press Ctrl+Shift+E** for Quick Export dialog
5. **Press a format key** (S/T/O/D/V/P) or click a button
6. **Choose filename** and save

Done! File exported with scaling applied automatically.

### Direct Format Shortcuts

For even faster workflow, use direct format shortcuts:
- **Ctrl+Shift+S** → STL (3D printing)
- **Ctrl+Shift+D** → DXF (2D CAD/laser cutting)

## Tips

- **Ctrl+Shift+E is the fastest** - opens Quick Export dialog with all formats
- **Use in-dialog shortcuts** - press S, T, O, D, V, or P to select format instantly
- **Global shortcuts work everywhere** - no need to switch to ExportPlus workbench
- **Set scaling in preferences** before exporting (doesn't change between exports)
- **Check console** for confirmation: "Exporting [FORMAT] with scaling factor: X.XXX"
- **Use File menu** if you forget shortcuts: File → Export with Scaling
- **Access from context menu** - right-click selected objects (when in ExportPlus workbench)

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
- **Ctrl+Shift+E**: Usually available (used by ExportPlus Quick Export)
- **Ctrl+Shift+S**: May conflict with some workbenches (used by ExportPlus STL)
- **Ctrl+Shift+D**: May conflict with some workbenches (used by ExportPlus DXF)
- **Ctrl+S**: Save (don't override!)

## See Also

- [USAGE.md](USAGE.md) - Full usage guide
- [README.md](README.md) - Complete documentation
- Tools → Customize → Keyboard - FreeCAD's shortcut customization
