import geopandas as gpd
import pandas as pd
import json
from shapely.geometry import Point
from pyproj import Transformer
import time

def setup_coordinate_transformer():
    """
    Setup für Koordinatentransformation WGS84 → LV95
    """
    # Transformer für WGS84 (EPSG:4326) zu LV95 (EPSG:2056)
    return Transformer.from_crs("EPSG:4326", "EPSG:2056", always_xy=True)

def add_streetnames_with_projection(json_file, output_json, max_distance_meters=50):
    """
    Fügt Strassennamen hinzu mit korrekter Koordinatentransformation
    """
    print("🚗 Füge Strassennamen mit Koordinatentransformation hinzu...")
    
    # 1. Koordinatentransformer setup
    transformer = setup_coordinate_transformer()
    print("✅ Koordinatentransformer initialisiert (WGS84 → LV95)")
    
    # 2. Unfalldaten laden
    with open(json_file, 'r', encoding='utf-8') as f:
        accidents = json.load(f)
    
    print(f"✅ {len(accidents)} Unfälle geladen")
    
    # 3. Strassennetz laden
    print("🗺️ Lade Strassennetz...")
    streets = gpd.read_file("SWISSTLM3D_2025.gpkg", layer="tlm_strassen_strasse")
    
    # Prüfe Koordinatensystem der Strassen
    print(f"📊 Strassen-CRS: {streets.crs}")
    
    # Nur Strassen mit Namen
    streets_with_names = streets[
        (streets['strassenname'].notna()) | 
        (streets['name'].notna())
    ].copy()
    
    print(f"✅ {len(streets_with_names)} Strassen mit Namen geladen")
    
    # Spatial Index für Performance
    print("⚡ Erstelle Spatial Index...")
    sindex = streets_with_names.sindex
    
    # 4. Strassennamen zu Unfällen hinzufügen
    print("🔍 Finde Strassennamen...")
    
    matches_found = 0
    start_time = time.time()
    
    for i, accident in enumerate(accidents):
        if i % 1000 == 0:
            elapsed = time.time() - start_time
            print(f"   Fortschritt: {i}/{len(accidents)} - {matches_found} Matches")
        
        if (accident.get('location') and 
            accident['location'].get('lon') is not None and 
            accident['location'].get('lat') is not None):
            
            lon = accident['location']['lon']
            lat = accident['location']['lat']
            
            # WGS84 zu LV95 transformieren
            lv95_e, lv95_n = transformer.transform(lon, lat)
            accident_point = Point(lv95_e, lv95_n)
            
            # Mit Spatial Index suchen (in METERN)
            possible_indices = list(sindex.intersection(accident_point.buffer(max_distance_meters).bounds))
            
            if possible_indices:
                candidates = streets_with_names.iloc[possible_indices]
                candidates['distance'] = candidates.geometry.distance(accident_point)
                nearest = candidates.loc[candidates['distance'].idxmin()]
                
                if nearest['distance'] <= max_distance_meters:
                    street_name = nearest.get('strassenname') or nearest.get('name')
                    if street_name:
                        accident['strassenname'] = str(street_name)
                        accident['strassen_distanz'] = round(nearest['distance'], 2)
                        matches_found += 1
    
    total_time = time.time() - start_time
    
    # 5. JSON speichern
    print("💾 Speichere JSON...")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(accidents, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Fertig! {output_json} erstellt")
    print(f"📊 {matches_found}/{len(accidents)} Unfälle mit Strassennamen")
    print(f"⏱️  Zeit: {total_time:.1f}s")
    
    return accidents, matches_found

def test_coordinate_transformation():
    """
    Testet die Koordinatentransformation
    """
    print("\n🧪 Teste Koordinatentransformation...")
    
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2056", always_xy=True)
    
    test_points = [
        ("Zürich HB", 8.539182, 47.378177),
        ("Oerlikon", 8.544268, 47.408430),
        ("Winterthur", 8.728000, 47.499000),
    ]
    
    for name, lon, lat in test_points:
        lv95_e, lv95_n = transformer.transform(lon, lat)
        print(f"   {name}:")
        print(f"      WGS84:  ({lon:.6f}, {lat:.6f})")
        print(f"      LV95:   ({lv95_e:.1f}, {lv95_n:.1f})")

def check_streets_coordinates():
    """
    Prüft die Koordinaten der Strassen
    """
    print("\n🔍 Prüfe Strassen-Koordinaten...")
    
    streets = gpd.read_file("SWISSTLM3D_2025.gpkg", layer="tlm_strassen_strasse")
    
    print(f"📊 Strassen-CRS: {streets.crs}")
    print(f"📈 Koordinatenbereich:")
    print(f"   E: {streets.bounds.minx.min():.0f} - {streets.bounds.maxx.max():.0f}")
    print(f"   N: {streets.bounds.miny.min():.0f} - {streets.bounds.maxy.max():.0f}")
    
    # Zürich Bereich in LV95
    zurich_streets = streets[
        (streets.bounds.minx >= 2680000) & (streets.bounds.maxx <= 2740000) &
        (streets.bounds.miny >= 1220000) & (streets.bounds.maxy <= 1280000)
    ]
    
    print(f"🏙️  Strassen in Zürich Bereich: {len(zurich_streets)}")
    
    if len(zurich_streets) > 0:
        sample = zurich_streets.head(3)
        for idx, street in sample.iterrows():
            name = street.get('strassenname') or street.get('name') or 'Unbenannt'
            centroid = street.geometry.centroid
            print(f"   📍 {name}: LV95 ({centroid.x:.0f}, {centroid.y:.0f})")

if __name__ == "__main__":
    # Zuerst Diagnose
    test_coordinate_transformation()
    check_streets_coordinates()
    
    # Dann Strassennamen hinzufügen
    result, matches = add_streetnames_with_projection(
        "strassenverkehrsunfallorte_cleaned.json", 
        "unfaelle_mit_strassen.json",
        max_distance_meters=50
    )
    
    if matches > 0:
        samples = [acc for acc in result if 'strassenname' in acc][:5]
        print(f"\n✅ Beispiele mit Strassennamen:")
        for i, acc in enumerate(samples):
            print(f"   {i+1}. {acc.get('gem_name', '?')}: {acc['strassenname']} ({acc.get('strassen_distanz', '?')}m)")
    
    print(f"\n🎉 FERTIG! {matches} Unfälle haben jetzt Strassennamen!")