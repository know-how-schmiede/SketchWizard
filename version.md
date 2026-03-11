# Version History

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
