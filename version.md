# Version History

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
