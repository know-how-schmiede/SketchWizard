# Version History

## 0.7.4 (2026-03-12)

- Updated i18n translations for `es`, `fr`, `it`, and `pl` to cover all current face/projection/deactivation dialog options and related messages.
- Updated localized command descriptions to include sketch-or-face export behavior.

## 0.7.3 (2026-03-12)

- Added checkbox option `Skizze deaktivieren` to the command dialog.
- If enabled, an automatically created export sketch (from selected face) is deactivated in the Fusion Browser after successful export.

## 0.7.2 (2026-03-12)

- Added a new dialog dropdown to select projection mode: `Angegebene Objekte` or `Koerper`.
- The selected projection mode is now used as projection filter during automatic sketch creation from a selected face.

## 0.7.1 (2026-03-12)

- Changed export file naming scheme to `NameKonstruktion_NameSkizze` for DXF/SVG/PDF exports.
- Construction name is derived from the active Fusion document name (fallback: root component name / `construction`).

## 0.7.0 (2026-03-12)

- Added optional planar face selection as export source in addition to direct sketch selection.
- When a face is selected, SketchWizard now creates a new sketch automatically (`Export1`, `Export2`, ...) on that face and projects the face contour.
- Enforced mutual exclusivity in the dialog: selecting a sketch clears face selection, selecting a face clears sketch selection.

## 0.6.1 (2026-03-11)

- Added full i18n translation sets for `de`, `en`, `es`, `fr`, `it`, and `pl`.
- Implemented automatic language selection based on Fusion 360 user language preferences with system-locale fallback.

## 0.6.0 (2026-03-11)

- Switched plugin UI language to English (menu, dialog labels, messages, and logs).
- Added a simple translation structure (`LANGUAGE` + `TRANSLATIONS` + `tr(...)`) as a base for future localization.

## 0.5.5 (2026-03-11)

- Logo-Auswahl auf `Logo_SketchWizard_200.png` festgelegt (PNG wird vor anderen Dateien verwendet).

## 0.5.4 (2026-03-11)

- Dialog-Crash bei Logo-Ladung behoben (`RuntimeError: invalid argument imageFile`).
- Logo-Einbindung jetzt robust: versucht mehrere Kandidaten (JPG/PNG/Fallback) und faengt ungueltige Bildpfade ab.

## 0.5.3 (2026-03-11)

- Logo-Pfad fuer den Dialog priorisiert jetzt explizit `C:/Users/.../AppData/Roaming/Autodesk/Autodesk Fusion 360/API/AddIns/SketchWizard/images/Logo_SketchWizard_200.jpg`.
- Logo-Pfad wird fuer Fusion normalisiert (`/` statt `\`) und der verwendete Pfad im Log ausgegeben.

## 0.5.2 (2026-03-11)

- Logo-Pfadauflosung korrigiert: bevorzugt jetzt die AddIn-Installation unter `.../AddIns/SketchWizard/images/Logo_SketchWizard_200.jpg`.

## 0.5.1 (2026-03-11)

- Name im Menue/Dialog auf `SketchWizard <Versionsnummer>` korrigiert.
- Info-Zeile (`Hello WOrld`) aus dem Dialog entfernt.
- Logo `images/Logo_SketchWizard_200.jpg` als Dialog-Bild eingebunden (mit Fallback auf PNG/Resource).

## 0.5.0 (2026-03-11)

- Exportformat `PDF` als dritte Option im Dialog hinzugefuegt.
- PDF-Export als Vektor-Ausgabe aus Sketch-Kurven implementiert.
- Export-Validierung auf `DXF`, `SVG` und `PDF` erweitert.

## 0.4.2 (2026-03-11)

- Skizzenaufloesung von Token auf direkte Objekt-Referenzen umgestellt.
- Fehler `Es wurde keine gueltige Skizze ausgewaehlt.` bei vorhandener Auswahl behoben.

## 0.4.1 (2026-03-11)

- Validierung fuer den `OK`-Button korrigiert (Skizze/Pfad/Format werden direkt ueber Dialogwerte geprueft).
- Fallback fuer Skizzenaufloesung beim Export ergaenzt.

## 0.4.0 (2026-03-11)

- Dialog um Ausgabepfad-Auswahl per Button erweitert.
- Ausgabepfad wird persistent in einer Settings-Datei gespeichert.
- Exportformat-Auswahl (DXF oder SVG) in den Dialog integriert.
- Ausgewaehlte Skizze kann mit ihrem Namen als Dateiname exportiert werden.
- DXF-Export ueber Fusion-API implementiert.
- SVG-Export ueber Sketch-Kurven (Strokes) implementiert.

## 0.3.1 (2026-03-11)

- Dialog um ein Auswahlfeld fuer Skizzen erweitert.
- Auswahlfeld listet alle Skizzen der aktiven Konstruktion auf.
- Wenn keine Skizzen vorhanden sind, zeigt das Auswahlfeld eine passende Meldung.

## 0.3.0 (2026-03-11)

- Menueposition geaendert auf `Konstruktion > Volumenkoerper > Erstellen`.
- Menueeintrag auf `SketchWizzard <Versionsnummer>` umgestellt.
- Zentrale Versionsverwaltung ueber `SketchWizard/version.py` eingefuehrt.
- Legacy-UI-Eintraege aus frueheren Positionen (`Zusatzmodule`/Dienstprogramme) werden beim Start bereinigt.
- Dialog beim Aufruf zeigt weiterhin `Hello WOrld`.
