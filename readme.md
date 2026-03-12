# SketchWizard

**SketchWizard** is a Fusion 360 add-in for exporting sketches and planar faces into fabrication-ready files.
It is built for fast handoff from CAD to CAM, laser, plotter, and documentation workflows.

![Logo SketchWizard](/images/Logo_SketchWizard_200.png)

## Video Demo

[![Watch the video on YouTube](https://img.youtube.com/vi/yTXmVZhCibU/hqdefault.jpg)](https://youtu.be/yTXmVZhCibU)


## Current Feature Set

- Export source can be:
  - an existing sketch, or
  - a selected planar body face (auto-creates an export sketch)
- Export formats:
  - `DXF`
  - `SVG`
  - `PDF`
  - `HPGL`
  - `G-Code` (`.gcode`)
- Projection mode for face-based exports:
  - `Specified Objects`
  - `Bodies`
- Optional `Deactivate Sketch` after successful export of an auto-created face sketch
- Dialog safety logic:
  - selecting a sketch clears face selection
  - selecting a face clears sketch selection
- Persistent output path (stored between runs)
- Automatic filename scheme:
  - `<ConstructionName>_<SketchName>.<ext>`
- UI translations:
  - `de`, `en`, `es`, `fr`, `it`, `pl`

![SketchWizard Dialog](/images/SketschWizard_Dialog_2.jpg)

## Typical Workflow

1. Start SketchWizard from Fusion 360.
2. Select either a sketch or a planar face.
3. If a face is selected, choose the projection mode.
4. Choose export format (`DXF`, `SVG`, `PDF`, `HPGL`, or `G-Code`).
5. Select output folder.
6. Optionally enable `Deactivate Sketch` (for auto-created face sketches).
7. Run export.

## Supported Export Formats

| Format | Extension | Typical Use |
| --- | --- | --- |
| DXF | `.dxf` | CAM/CNC pipelines |
| SVG | `.svg` | Laser cutting, vector tools |
| PDF | `.pdf` | Documentation and print workflows |
| HPGL | `.hpgl` | Plotters and legacy pen systems |
| G-Code | `.gcode` | CNC toolpath handoff (2D contour output) |

## Installation

1. Clone the repository:

```bash
git clone https://github.com/know-how-schmiede/SketchWizard.git
```

2. Copy the folder to your Fusion 360 `AddIns` directory.

Typical Windows path:

```text
%appdata%\Autodesk\Autodesk Fusion 360\API\AddIns
```

3. Restart Fusion 360.
4. Open `UTILITIES -> Add-Ins -> Scripts and Add-Ins`.
5. Run **SketchWizard**.

## Project Status

- Current version: `0.7.6`
- Detailed changes: see `version.md`

## Roadmap

Planned improvements include:

- multi-sketch export
- layer support
- export presets
- additional CAM-specific controls for G-Code output

## Contributing

Contributions, bug reports, and feature requests are welcome.
Please open an issue or submit a pull request.

## License

MIT License

## Author

**Rene Triebenstein**  
Know-How-Schmiede

GitHub: https://github.com/know-how-schmiede
