import fitz  # PyMuPDF
import os

# Dossier contenant les PDFs
pdf_dir = r"c:\Users\Administrator\Desktop\Systeme de Geolocalisation\Dossier references\Ground control station\Documentation"

# Liste des fichiers PDF à traiter avec pages clés à extraire
pdf_configs = [
    {"file": "Asseco_AGCS_A4_EN.pdf", "pages": [0, 1, 2, 3, 4], "prefix": "Asseco_AGCS"},
    {"file": "T50 GCS Specification.pdf", "pages": [0, 1, 2, 3, 4, 5], "prefix": "T50_GCS"},
    {"file": "TS US UGCS Universal Ground Control Station Datasheet 2up.pdf", "pages": [0, 1], "prefix": "UGCS_Universal"},
    {"file": "Drone-Ground-Control-Station-GCS.pdf", "pages": [0, 1, 2, 3], "prefix": "Drone_GCS"},
    {"file": "Flight_controller_and_GCS.pdf", "pages": [0, 1, 2, 3], "prefix": "FC_GCS"},
    {"file": "generic_control_station_gcs.pdf", "pages": [0, 1], "prefix": "Generic_GCS"},
    {"file": "hon-aero-ground-control-station-drone-operations.pdf", "pages": [0, 1, 2], "prefix": "Honeywell_GCS"},
    {"file": "Design-Development-and-Validation-of-a-Ground-Control-Station-for-Aerial-Manipulators.pdf", "pages": [0, 1, 2, 3], "prefix": "Aerial_Manipulator_GCS"},
    {"file": "GCS.A-1.pdf", "pages": [0, 1], "prefix": "GCS_A1"},
    {"file": "1-s2.0-S2590123024007539-main.pdf", "pages": [0, 1, 2, 3], "prefix": "Scientific_GCS"},
    {"file": "126020094.pdf", "pages": [0, 1, 2, 3], "prefix": "Research_GCS"},
    {"file": "sUAS_Sim_Final.pdf", "pages": [0, 1, 2, 3], "prefix": "sUAS_Sim"},
    {"file": "mjlefevre,+Directeur+de+la+revue,+13_new_Airinov.pdf", "pages": [0, 1, 2], "prefix": "Airinov"},
]

# Créer le dossier de sortie
output_dir = os.path.join(pdf_dir, "extracted_images")
os.makedirs(output_dir, exist_ok=True)

for config in pdf_configs:
    pdf_path = os.path.join(pdf_dir, config["file"])
    if not os.path.exists(pdf_path):
        print(f"[SKIP] {config['file']} - fichier non trouvé")
        continue
    
    print(f"[PROCESSING] {config['file']}")
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        for page_num in config["pages"]:
            if page_num >= total_pages:
                print(f"  [SKIP] Page {page_num+1} - dépasse le nombre de pages ({total_pages})")
                continue
            
            page = doc[page_num]
            # Zoom 2x pour meilleure qualité
            zoom = 2.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            output_file = os.path.join(output_dir, f"{config['prefix']}_page_{page_num+1:02d}.png")
            pix.save(output_file)
            print(f"  -> Page {page_num+1} extraite: {os.path.basename(output_file)}")
        
        doc.close()
    except Exception as e:
        print(f"  [ERROR] {e}")

print("\n[DONE] Extraction des images terminée")
print(f"Images sauvegardées dans: {output_dir}")
