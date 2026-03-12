# SketchWizard

**SketchWizard** ist ein Fusion-360-Add-in zum Export von Skizzen und planaren Flaechen in fertigungsfaehige Dateien.
Es ist fuer eine schnelle Uebergabe von CAD an CAM-, Laser-, Plotter- und Dokumentations-Workflows ausgelegt.

![Logo SketchWizard](/images/Logo_SketchWizard_200.png)

## Video-Demo

[![Video auf YouTube ansehen](https://img.youtube.com/vi/yTXmVZhCibU/hqdefault.jpg)](https://youtu.be/yTXmVZhCibU)

## Aktueller Funktionsumfang

- Exportquelle kann sein:
  - eine vorhandene Skizze oder
  - eine ausgewaehlte planare Koerperflaeche (erstellt automatisch eine Export-Skizze)
- Exportformate:
  - `DXF`
  - `SVG`
  - `PDF`
  - `HPGL`
  - `G-Code` (`.gcode`)
- Projektionsmodus fuer flaechenbasierte Exporte:
  - `Specified Objects`
  - `Bodies`
- Optionale Funktion `Deactivate Sketch` nach erfolgreichem Export einer automatisch erzeugten Flaechen-Skizze
- Dialog-Sicherheitslogik:
  - Auswahl einer Skizze entfernt die Flaechenauswahl
  - Auswahl einer Flaeche entfernt die Skizzenauswahl
- Persistenter Ausgabepfad (wird zwischen Sitzungen gespeichert)
- Automatisches Dateinamensschema:
  - `<ConstructionName>_<SketchName>.<ext>`
- UI-Uebersetzungen:
  - `de`, `en`, `es`, `fr`, `it`, `pl`

![SketchWizard Dialog](/images/SketschWizard_Dialog_2.jpg)

## Typischer Workflow

1. Starte SketchWizard in Fusion 360.
2. Waehle entweder eine Skizze oder eine planare Flaeche.
3. Wenn eine Flaeche gewaehlt ist, waehle den Projektionsmodus.
4. Waehle das Exportformat (`DXF`, `SVG`, `PDF`, `HPGL` oder `G-Code`).
5. Waehle den Ausgabeordner.
6. Aktiviere optional `Deactivate Sketch` (fuer automatisch erzeugte Flaechen-Skizzen).
7. Fuehre den Export aus.

## Unterstuetzte Exportformate

| Format | Erweiterung | Typische Verwendung |
| --- | --- | --- |
| DXF | `.dxf` | CAM/CNC-Pipelines |
| SVG | `.svg` | Laserschneiden, Vektor-Tools |
| PDF | `.pdf` | Dokumentation und Druck-Workflows |
| HPGL | `.hpgl` | Plotter und Legacy-Pen-Systeme |
| G-Code | `.gcode` | CNC-Toolpath-Handoff (2D-Konturausgabe) |

## Installation

1. Repository klonen:

```bash
git clone https://github.com/know-how-schmiede/SketchWizard.git
```

2. Ordner in dein Fusion-360-`AddIns`-Verzeichnis kopieren.

Typischer Windows-Pfad:

```text
%appdata%\Autodesk\Autodesk Fusion 360\API\AddIns
```

3. Fusion 360 neu starten.
4. `UTILITIES -> Add-Ins -> Scripts and Add-Ins` oeffnen.
5. **SketchWizard** starten.

## Projektstatus

- Aktuelle Version: `0.7.6`
- Detaillierte Aenderungen: siehe `version.md`

## Roadmap

Geplante Verbesserungen:

- Multi-Skizzen-Export
- Layer-Unterstuetzung
- Export-Presets
- Zusaetzliche CAM-spezifische Steuerungen fuer den G-Code-Export

## Mitwirken

Beitraege, Bug-Reports und Feature-Requests sind willkommen.
Bitte erstelle ein Issue oder einen Pull Request.

## Lizenz

MIT License

## Autor

**Rene Triebenstein**  
Know-How-Schmiede

GitHub: https://github.com/know-how-schmiede
