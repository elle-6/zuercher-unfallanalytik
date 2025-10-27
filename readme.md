Zürcher Unfallanalytik - Erweitertes Dashboard

📋 Projektbeschreibung

Ein interaktives Web-Dashboard zur Visualisierung und Analyse von Unfalldaten im Kanton Zürich. Die Anwendung ermöglicht die Darstellung von Unfällen auf einer Karte, Filterung nach verschiedenen Kriterien und die Generierung von Statistiken und Diagrammen speziell für den Kanton Zürich.

🗂️ Datenvorbereitung

Vorverarbeitung der Daten

Das Projekt verwendet zwei Python-Skripte zur Datenaufbereitung:

1. Datenbereinigung (clean_data.py)

python
# Bereinigt die Rohdaten und reduziert die Dateigröße
python clean_data.py
Funktionen:

Entfernt unnötige Felder
Behält essentielle Unfallinformationen bei
Verarbeitet Koordinaten (Location oder LV95)
Reduziert Dateigröße um ~70%
2. Straßennamen-Hinzufügung (add_streetnames.py)

python
# Fügt Straßennamen mittels Geocoding hinzu
python add_streetnames.py
Funktionen:

Transformiert WGS84-Koordinaten zu LV95
Matcht Unfälle mit dem Schweizer Straßennetz (SWISSTLM3D)
Fügt Straßennamen innerhalb von 50m Distanz hinzu
Verwendet Spatial Index für Performance
Datenfluss:

text
strassenverkehrsunfallorte.json
         ↓
clean_data.py
         ↓
strassenverkehrsunfallorte_cleaned.json  
         ↓
add_streetnames.py
         ↓
unfaelle_mit_strassen.json  ← Finale Datei für das Dashboard
🚀 Schnellstart

1. Datenvorbereitung

bash
# 1. Daten bereinigen
python clean_data.py

# 2. Straßennamen hinzufügen  
python add_streetnames.py
2. Dashboard starten

bash
# Über lokalen Webserver
python -m http.server 8000
# Oder direkt im Browser: index.html öffnen
3. Daten laden

Im Dashboard auf "Daten importieren" klicken
Datei unfaelle_mit_strassen.json auswählen
Daten werden automatisch verarbeitet und visualisiert
📁 Projektstruktur

text
zuerich-accident-analytics/
├── index.html                          # Haupt-Dashboard
├── unfaelle_mit_strassen.json          # Finale Unfalldaten (generiert)
├── clean_data.py                       # Datenbereinigung-Skript
├── add_streetnames.py                  # Straßennamen-Skript
├── SWISSTLM3D_2025.gpkg               # Schweizer Straßennetz (extern)
└── README.md
🔧 Technische Details

Datenformat (Finale JSON)

json
{
  "accidentuid": "12345",
  "cantoncode": "ZH",
  "municipalitycode": "261",
  "gem_name": "Zürich", 
  "accidentyear": 2023,
  "accidentmonth_de": "Januar",
  "accidentweekday_de": "Montag", 
  "accidenthour": 8,
  "accidenttype_de": "Zusammenstoss",
  "accidentseveritycategory_de": "Schwerverletzten",
  "roadtype_de": "Hauptstrasse",
  "location": {
    "lon": 8.539182,
    "lat": 47.378177
  },
  "strassenname": "Bahnhofstrasse",
  "strassen_distanz": 12.5
}
Koordinatensysteme

Input: WGS84 (GPS) oder LV95 (Schweizer Landeskoordinaten)
Processing: LV95 für Straßen-Matching
Output: WGS84 für Kartenvisualisierung
Abhängigkeiten

bash
# Für Datenvorbereitung
pip install geopandas pandas pyproj shapely
🎯 Dashboard-Funktionen

Visualisierung

🗺️ Interaktive Karte mit Unfall-Hotspots
🔥 Heatmap für Unfallschwerpunkte
📍 Clustering bei vielen Markern
🛣️ Zürcher Straßennetz (optional)
Filterung

Gemeinde (nur Kanton Zürich)
Straße (dank Straßennamen-Matching)
Zeit (Jahr, Monat, Wochentag, Stunde)
Unfalltyp und -schwere
Analyse

📊 Interaktive Diagramme mit Klick-Filterung
📈 Trendanalyse über Jahre
🔍 Top-Gemeinden und Straßen
💾 CSV-Export der gefilterten Daten
⚠️ Wichtige Hinweise

Datenqualität

Nur Unfälle mit gültigen Koordinaten werden angezeigt
Straßennamen werden nur bei Match innerhalb 50m zugewiesen
LV95-Koordinaten werden automatisch zu WGS84 konvertiert
Performance

Spatial Index beschleunigt Straßen-Matching
Bereinigte Daten reduzieren Ladezeit im Browser
Cluster-Modus verbessert Performance bei vielen Markern
Bekannte Einschränkungen

Straßennamen-Matching erfordert SWISSTLM3D-Datenbank
Nicht alle Unfälle haben exakte Straßenzuordnungen
Dashboard funktioniert nur mit korrekt vorbereiteten JSON-Daten
🐛 Problembehebung

Häufige Fehler:

"Keine Daten gefunden": JSON-Datei nicht korrekt vorbereitet
"Koordinaten fehlen": Unfall ohne location/LV95-Koordinaten
"Straßennamen nicht verfügbar": SWISSTLM3D nicht gefunden
Lösungen:

Datenvorbereitungsskripte in korrekter Reihenfolge ausführen
SWISSTLM3D.gpkg muss im Projektverzeichnis liegen
Browser-Konsole für detaillierte Fehlermeldungen prüfen
📄 Lizenz

MIT License - Siehe LICENSE Datei für Details.

