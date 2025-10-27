import json
import sys

def clean_accident_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_data = []
    
    for accident in data:
        cleaned_accident = {
            "accidentuid": accident.get("accidentuid"),
            "cantoncode": accident.get("cantoncode"),
            "municipalitycode": accident.get("municipalitycode"),
            "gem_name": accident.get("gem_name"),
            "accidentyear": accident.get("accidentyear"),
            "accidentmonth_de": accident.get("accidentmonth_de"),
            "accidentweekday_de": accident.get("accidentweekday_de"),
            "accidenthour": accident.get("accidenthour"),
            "accidenttype_de": accident.get("accidenttype_de"),
            "accidentseveritycategory_de": accident.get("accidentseveritycategory_de"),
            "roadtype_de": accident.get("roadtype_de")
        }
        
        # Koordinaten - bevorzuge location falls vorhanden
        if accident.get("location"):
            cleaned_accident["location"] = accident["location"]
        elif accident.get("accidentlocation_chlv95_e") and accident.get("accidentlocation_chlv95_n"):
            cleaned_accident["accidentlocation_chlv95_e"] = accident["accidentlocation_chlv95_e"]
            cleaned_accident["accidentlocation_chlv95_n"] = accident["accidentlocation_chlv95_n"]
        
        cleaned_data.append(cleaned_accident)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    
    original_size = sys.getsizeof(json.dumps(data, ensure_ascii=False))
    cleaned_size = sys.getsizeof(json.dumps(cleaned_data, ensure_ascii=False))
    
    print(f"Original: {len(data)} Unfälle, {original_size / 1024 / 1024:.1f} MB")
    print(f"Bereinigt: {len(cleaned_data)} Unfälle, {cleaned_size / 1024 / 1024:.1f} MB")
    print(f"Reduktion: {(1 - cleaned_size/original_size) * 100:.1f}%")

# Verwendung
clean_accident_data("strassenverkehrsunfallorte.json", "strassenverkehrsunfallorte_cleaned.json")