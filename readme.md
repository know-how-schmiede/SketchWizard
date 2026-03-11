# SketchWizard

**SketchWizard** is a Fusion 360 Add-In that allows you to export any sketch as a clean vector file for use in other software such as CAM tools, laser cutters, plotters, and graphic design applications.

![Logo SketchWizard](/images/Logo_SketchWizard_200.png)


The add-in provides a simple workflow: select a sketch from your design and export it directly as a vector file (e.g. SVG or DXF) with a **1:1 scale**.

Perfect for workflows involving:

- CNC machining
- Laser cutting
- Plotters
- CAM software (e.g. EstlCAM)
- Graphic software (Inkscape, Illustrator)
- Documentation and templates

---

# Features

✔ Export Fusion sketches directly to **SVG**  
✔ Planned support for **DXF export**  
✔ **1:1 scale export** (1 mm in Fusion = 1 mm in the exported file)  
✔ Select any sketch in the design  
✔ Custom output path  
✔ Clean vector output optimized for CAM workflows  

---

# Typical Workflow

1. Create a sketch in Fusion 360
2. Draw geometry or project body edges into the sketch
3. Finish the sketch
4. Launch **SketchWizard**
5. Select the sketch you want to export
6. Choose the output path
7. Export the file

The resulting file can be directly used in other applications.

---

# Supported Geometry

SketchWizard currently supports:

- Lines
- Arcs
- Circles
- Polylines

Future versions may include:

- Splines
- Layers
- Color based laser operations
- Multi-format export

---

# Planned Export Formats

| Format | Use Case |
|------|------|
| SVG | Laser cutting, graphic tools |
| DXF | CAM software, CNC |
| HPGL | Plotters |
| PDF | Documentation |
| G-Code | Direct machining |

---

# Installation

1. Download or clone the repository

git clone https://github.com/know-how-schmiede/SketchWizard.git

2. Copy the folder into your Fusion 360 **AddIns directory**

Typical location:

Windows
%appdata%\Autodesk\Autodesk Fusion 360\API\AddIns


3. Restart Fusion 360

4. Open:

UTILITIES → Add-Ins → Scripts and Add-Ins


5. Run **SketchWizard**

---

# Example Use Cases

### Laser Cutting
Export a sketch to SVG and import it into:

- LightBurn
- Inkscape
- LaserGRBL

### CNC / CAM

Export DXF and open it in:

- EstlCAM
- SheetCAM
- FreeCAD

### Plotter / Vinyl Cutting

Export SVG for:

- Cricut
- Silhouette
- Vinyl plotters

---

# Project Goals

SketchWizard aims to simplify the workflow between **Fusion 360 and fabrication tools** by providing a fast and clean export of sketch geometry.

The goal is to create a lightweight tool that removes unnecessary steps between CAD and manufacturing.

---

# Roadmap

Planned improvements:

- DXF exporter
- spline support
- multi-sketch export
- layer support
- laser color mapping
- UI improvements
- export presets

---

# Contributing

Contributions, bug reports and feature requests are welcome.

If you have ideas for improvements or additional export formats, feel free to open an issue.

---

# License

MIT License

---

# Author

**René Triebenstein**

Know-How-Schmiede  
YouTube | Maker Projects | Fusion 360 Tutorials

GitHub:  
https://github.com/know-how-schmiede

---

# Related Projects

- **InsertWizard** – Fusion 360 heat-set insert generator  
- **NeoFab** – Maker fabrication management system  
- **PrintFleet** – 3D printer fleet monitoring

---

# Support the Project

If you like this tool, consider supporting the project by:

⭐ starring the repository  
📢 sharing it with other makers  
🛠 contributing improvements