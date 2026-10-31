import fitz  # PyMuPDF
import os

# Dossier contenant les PDFs
pdf_dir = r"c:\Users\Administrator\Desktop\Systeme de Geolocalisation\Dossier references\Autopilote drone"

# Liste des fichiers PDF à traiter avec pages clés à extraire
pdf_configs = [
    {"file": "Autopilot Quad copter Drone.pdf", "pages": [0, 1, 2, 3, 4], "prefix": "Autopilot_Quadcopter"},
    {"file": "Dossier-technique-AR-Drone.pdf", "pages": [0, 1, 2, 3, 4, 5, 6], "prefix": "AR_Drone"},
    {"file": "GuideUtilisateur_OceanREPERV2.pdf", "pages": [0, 1, 2, 3, 4, 5], "prefix": "OceanREPER"},
    {"file": "Heliplane-LRS-Spécifications-techniques.pdf", "pages": [0, 1], "prefix": "Heliplane_LRS"},
    {"file": "StarDice_Drone V3.pdf", "pages": [0, 1, 2, 3, 4], "prefix": "StarDice_Drone"},
    {"file": "whitepaper-logistic-uav-en.pdf", "pages": [0, 1, 2, 3, 4], "prefix": "Logistic_UAV"},
    {"file": "Presentation_Fi3E.pdf", "pages": [0, 1, 2, 3], "prefix": "Fi3E"},
    {"file": "Autoplaneur-poster-final.pdf", "pages": [0], "prefix": "Autoplaneur"},
    {"file": "2020_AlexandreDuperre.pdf", "pages": [0, 1, 2, 3], "prefix": "Duperre_Thesis"},
    {"file": "2023ESMA0014_kamni.pdf", "pages": [0, 1, 2, 3], "prefix": "Kamni_Thesis"},
    {"file": "EP17182759NWA1.pdf", "pages": [0, 1, 2], "prefix": "Patent_EP"},
    {"file": "marchandn.pdf", "pages": [0, 1, 2], "prefix": "Marchand"},
    {"file": "patelli16model.pdf", "pages": [0, 1, 2], "prefix": "Patelli_Model"},
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
