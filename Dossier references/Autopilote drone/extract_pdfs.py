import pdfplumber
import os

# Dossier contenant les PDFs
pdf_dir = r"c:\Users\Administrator\Desktop\Systeme de Geolocalisation\Dossier references\Autopilote drone"

# Créer le dossier de sortie
output_dir = os.path.join(pdf_dir, "extracted_text")
os.makedirs(output_dir, exist_ok=True)

# Liste des fichiers PDF
pdf_files = [
    "000819608.pdf",
    "1901.0063v1.pdf",
    "2020_AlexandreDuperre.pdf",
    "2023ESMA0014_kamni.pdf",
    "Autopilot Quad copter Drone.pdf",
    "Autoplaneur-poster-final.pdf",
    "Dossier-technique-AR-Drone.pdf",
    "EP17182759NWA1.pdf",
    "GuideUtilisateur_OceanREPERV2.pdf",
    "Heliplane-LRS-Spécifications-techniques.pdf",
    "Presentation_Fi3E.pdf",
    "StarDice_Drone V3.pdf",
    "marchandn.pdf",
    "patelli16model.pdf",
    "td20_pc_maelforestal_controlealtitude.pdf",
    "tesi.pdf",
    "whitepaper-logistic-uav-en.pdf"
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
