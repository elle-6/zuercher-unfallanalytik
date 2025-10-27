# Zürcher Unfallanalytik - Erweitertes Dashboard

## 📋 Projektbeschreibung

Ein interaktives Web-Dashboard zur Visualisierung und Analyse von Unfalldaten **im Kanton Zürich**. Die Anwendung ermöglicht die Darstellung von Unfällen auf einer Karte, Filterung nach verschiedenen Kriterien und die Generierung von Statistiken und Diagrammen speziell für den Kanton Zürich.

## 🗂️ Datenvorbereitung

### Vorverarbeitung der Daten

Das Projekt verwendet zwei Python-Skripte zur Datenaufbereitung:

#### 1. **Datenbereinigung** (`clean_data.py`)
```python
# Bereinigt die Rohdaten und reduziert die Dateigröße
python clean_data.py

#### 2. **Datenfluss** 

strassenverkehrsunfallorte.json
         ↓
clean_data.py
         ↓
strassenverkehrsunfallorte_cleaned.json  
         ↓
add_streetnames.py
         ↓
unfaelle_mit_strassen.json  ← Finale Datei für das Dashboard
