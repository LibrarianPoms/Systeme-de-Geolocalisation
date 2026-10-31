import pdfplumber
import os

# Dossier contenant les PDFs
pdf_dir = r"c:\Users\Administrator\Desktop\Systeme de Geolocalisation\Dossier references\Ground control station\Documentation"

# Créer le dossier de sortie
output_dir = os.path.join(pdf_dir, "extracted_text")
os.makedirs(output_dir, exist_ok=True)

# Liste des fichiers PDF
pdf_files = [
    "1-s2.0-S2590123024007539-main.pdf",
    "126020094.pdf",
    "18-VasilePRISACARIU,MirceaBOSCOIANU,DanutBALOS,CatalinCIOACA,SebastianPOP,LuigeVLADAREANU,VictorVLADAREANU,AnaMariaTRAVEDIN.pdf",
    "2013-1-04-Imre_Makkay.pdf",
    "61fd7e7b742af1644002939.pdf",
    "92055.pdf",
    "Asseco_AGCS_A4_EN.pdf",
    "CT2014_GPS_art18.pdf",
    "Design-Development-and-Validation-of-a-Ground-Control-Station-for-Aerial-Manipulators.pdf",
    "Drone-Ground-Control-Station-GCS.pdf",
    "Flight_controller_and_GCS.pdf",
    "GCS.A-1.pdf",
    "T50 GCS Specification.pdf",
    "TS US UGCS Universal Ground Control Station Datasheet 2up.pdf",
    "generic_control_station_gcs.pdf",
    "hon-aero-ground-control-station-drone-operations.pdf",
    "layout+-+1710+-+Paramita.pdf",
    "mjlefevre,+Directeur+de+la+revue,+13_new_Airinov.pdf",
    "sUAS_Sim_Final.pdf"
]

# Limite de pages par PDF
MAX_PAGES = 25

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    
    if not os.path.exists(pdf_path):
        print(f"[SKIP] {pdf_file} - fichier non trouvé")
        continue
    
    print(f"[PROCESSING] {pdf_file}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_content = []
            pages_to_extract = min(len(pdf.pages), MAX_PAGES)
            
            for i, page in enumerate(pdf.pages[:pages_to_extract]):
                text = page.extract_text()
                if text:
                    text_content.append(f"=== PAGE {i+1} ===\n{text}\n")
            
            # Sauvegarder le texte extrait
            output_file = os.path.join(output_dir, pdf_file.replace(".pdf", ".txt"))
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(text_content))
            
            print(f"  -> Extrait {pages_to_extract} pages vers {os.path.basename(output_file)}")
    
    except Exception as e:
        print(f"  [ERROR] {e}")

print("\n[DONE] Extraction terminée")
