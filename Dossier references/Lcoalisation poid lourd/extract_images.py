import fitz  # PyMuPDF
import os

# Dossier contenant les PDFs
pdf_dir = r"c:\Users\Administrator\Desktop\Systeme de Geolocalisation\Dossier references\Lcoalisation poid lourd"

# Liste des fichiers PDF à traiter avec pages clés à extraire
pdf_configs = [
    {"file": "VG34_datasheet_FR.pdf", "pages": [0, 1, 2, 3], "prefix": "VG34"},
    {"file": "ttb-link510-doc.pdf", "pages": [0, 1], "prefix": "TomTom_LINK510"},
    {"file": "ATHMO_Informatique_embarquee_generale_fr_MEDIUM.pdf", "pages": [0, 1, 2, 3, 4, 5, 6, 7], "prefix": "ATHMO"},
    {"file": "LINK.pdf", "pages": [0, 1, 2], "prefix": "LINK"},
    {"file": "livre-blanc-gestion-de-flotte-de-vehicules-corrige.pdf", "pages": [0, 1, 2, 3], "prefix": "LivreBlanc"},
    {"file": "La-geolocalisation-des-vehicules-mis-a-disposition-des-salaries.pdf", "pages": [0, 1, 2], "prefix": "CNIL_Geoloc"},
    {"file": "mode-demploi-1489844-gps-pour-poids-lourd-becker-transit-7sl-eu-178-cm-7-pouces-europe.pdf", "pages": [0, 10, 11, 70, 71], "prefix": "Becker_GPS"},
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
