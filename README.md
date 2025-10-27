# Zürcher Unfallanalytik - Dashboard
# 📋 Projektbeschreibung

# Interaktives Dashboard zur Visualisierung und Analyse von Verkehrsunfällen im Kanton Zürich mit erweiterten Filter- und Analysemöglichkeiten.


# 🚀 Schnellstart


1. Datenvorbereitung


# Rohdaten bereinigen
python clean_data.py

# Strassennamen hinzufügen
python add_streetnames.py
2. Dashboard starten

# Lokalen Server starten
python -m http.server 8000

# Im Browser öffnen: http://localhost:8000



3. Daten laden

Dashboard öffnen
unfaelle_mit_strassen.json hochladen
Daten werden automatisch visualisiert

##########################################################################################


# Datenfluss:

strassenverkehrsunfallorte.json
         ↓
clean_data.py
         ↓
strassenverkehrsunfallorte_cleaned.json  
         ↓
add_streetnames.py
         ↓
unfaelle_mit_strassen.json  ← Finale Datei für das Dashboard

##########################################################################################


# 📁 Projektstruktur

zuerich-accident-analytics/
├── index.html                          # Haupt-Dashboard
├── unfaelle_mit_strassen.json          # Finale Unfalldaten (generiert)
├── clean_data.py                       # Datenbereinigung-Skript
├── add_streetnames.py                  # Strassennamen-Skript
├── SWISSTLM3D_2025.gpkg               # Schweizer Strassennetz (extern)
└── README.md

##########################################################################################


# 🎯 Hauptfunktionen

🗺️ Interaktive Karte mit Heatmap & Clustering
📊 Echtzeit-Diagramme für Unfallanalysen
🔍 Erweiterte Filterung nach Gemeinde, Strasse, Zeit, Unfalltyp
💾 CSV-Export der gefilterten Daten
⚙️ Technische Voraussetzungen

##########################################################################################


# Python Abhängigkeiten
pip install geopandas pandas pyproj shapely
Fertig! Das Dashboard läuft auf http://localhost:8000
