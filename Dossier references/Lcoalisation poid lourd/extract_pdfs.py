import pdfplumber
import os
import sys

# Dossier contenant les PDFs
pdf_dir = r"c:\Users\Administrator\Desktop\Systeme de Geolocalisation\Dossier references\Lcoalisation poid lourd"

# Liste des fichiers PDF
pdf_files = [
    "ATHMO_Informatique_embarquee_generale_fr_MEDIUM.pdf",
    "VG34_datasheet_FR.pdf",
    "ttb-link510-doc.pdf",
    "LINK.pdf",
    "livre-blanc-gestion-de-flotte-de-vehicules-corrige.pdf",
    "La-geolocalisation-des-vehicules-mis-a-disposition-des-salaries.pdf",
    "these_Maan_E_El_Najjar-1.pdf",
    "Telechargez-la-brochure-'Technologie-a-bord_2019_compressed.pdf",
    "files.pdf",
    "mode-demploi-1489844-gps-pour-poids-lourd-becker-transit-7sl-eu-178-cm-7-pouces-europe.pdf"
]

output_dir = os.path.join(pdf_dir, "extracted_text")
os.makedirs(output_dir, exist_ok=True)

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    if not os.path.exists(pdf_path):
        print(f"[SKIP] {pdf_file} - fichier non trouvé")
        continue
    
    print(f"[PROCESSING] {pdf_file}")
    output_file = os.path.join(output_dir, pdf_file.replace(".pdf", ".txt"))
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_content = []
            for i, page in enumerate(pdf.pages[:20]):  # Limiter à 20 pages
                text = page.extract_text()
                if text:
                    text_content.append(f"=== PAGE {i+1} ===\n{text}\n")
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(text_content))
            
            print(f"  -> Extrait {len(text_content)} pages vers {os.path.basename(output_file)}")
    except Exception as e:
        print(f"  [ERROR] {e}")

print("\n[DONE] Extraction terminée")
