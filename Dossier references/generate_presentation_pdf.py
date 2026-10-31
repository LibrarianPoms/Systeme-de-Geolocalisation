#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer un PDF de présentation depuis un fichier Markdown
Utilise WeasyPrint pour une conversion haute qualité
"""

import os
import sys
import markdown
from weasyprint import HTML, CSS
from datetime import datetime

def create_presentation_css():
    """Crée le CSS pour la présentation professionnelle"""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    @page {
        size: A4 landscape;
        margin: 2cm;
        @top-center {
            content: "Solution de Géolocalisation Avancée pour Poids Lourds";
            font-size: 10pt;
            color: #666;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5pt;
        }
        @bottom-center {
            content: counter(page);
            font-size: 10pt;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 5pt;
        }
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 11pt;
        line-height: 1.4;
        color: #333;
        background: white;
    }
    
    h1 {
        font-size: 24pt;
        font-weight: 700;
        color: #1a73e8;
        text-align: center;
        margin-bottom: 20pt;
        page-break-before: always;
    }
    
    h2 {
        font-size: 18pt;
        font-weight: 600;
        color: #1a73e8;
        margin: 20pt 0 10pt 0;
        border-bottom: 2px solid #1a73e8;
        padding-bottom: 5pt;
    }
    
    h3 {
        font-size: 14pt;
        font-weight: 600;
        color: #2c3e50;
        margin: 15pt 0 8pt 0;
        page-break-after: avoid;
    }
    
    h4 {
        font-size: 12pt;
        font-weight: 600;
        color: #34495e;
        margin: 10pt 0 5pt 0;
    }
    
    h5 {
        font-size: 11pt;
        font-weight: 600;
        color: #34495e;
        margin: 8pt 0 4pt 0;
    }
    
    p {
        margin-bottom: 8pt;
        text-align: justify;
    }
    
    strong, b {
        font-weight: 600;
        color: #2c3e50;
    }
    
    em, i {
        font-style: italic;
        color: #555;
    }
    
    ul, ol {
        margin: 10pt 0 10pt 20pt;
    }
    
    li {
        margin-bottom: 4pt;
    }
    
    blockquote {
        margin: 15pt 0;
        padding: 10pt 15pt;
        background: #f8f9fa;
        border-left: 4px solid #1a73e8;
        font-style: italic;
    }
    
    code {
        font-family: 'Courier New', monospace;
        background: #f1f3f4;
        padding: 2pt 4pt;
        border-radius: 3pt;
        font-size: 10pt;
    }
    
    pre {
        background: #f8f9fa;
        border: 1px solid #e1e5e9;
        border-radius: 4pt;
        padding: 10pt;
        margin: 10pt 0;
        overflow: hidden;
        page-break-inside: avoid;
    }
    
    pre code {
        background: none;
        padding: 0;
        font-size: 9pt;
        line-height: 1.3;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15pt 0;
        font-size: 10pt;
        page-break-inside: avoid;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 6pt 8pt;
        text-align: left;
    }
    
    th {
        background: #f8f9fa;
        font-weight: 600;
        color: #2c3e50;
    }
    
    tr:nth-child(even) {
        background: #f8f9fa;
    }
    
    hr {
        border: none;
        border-top: 2px solid #1a73e8;
        margin: 20pt 0;
        page-break-after: always;
    }
    
    .slide-title {
        font-size: 20pt;
        font-weight: 700;
        color: #1a73e8;
        text-align: center;
        margin: 30pt 0 20pt 0;
        page-break-before: always;
        page-break-after: avoid;
    }
    
    .slide-content {
        min-height: 400pt;
    }
    
    .highlight-box {
        background: #e8f0fe;
        border: 1px solid #1a73e8;
        border-radius: 4pt;
        padding: 10pt;
        margin: 10pt 0;
    }
    
    .warning-box {
        background: #fef7e0;
        border: 1px solid #fbbc04;
        border-radius: 4pt;
        padding: 10pt;
        margin: 10pt 0;
    }
    
    .success-box {
        background: #e6f4ea;
        border: 1px solid #34a853;
        border-radius: 4pt;
        padding: 10pt;
        margin: 10pt 0;
    }
    
    .diagram-placeholder {
        background: #f1f3f4;
        border: 2px dashed #5f6368;
        border-radius: 4pt;
        padding: 20pt;
        text-align: center;
        margin: 15pt 0;
        color: #5f6368;
        font-style: italic;
    }
    
    .footer {
        margin-top: 30pt;
        padding-top: 10pt;
        border-top: 1px solid #ddd;
        font-size: 9pt;
        color: #666;
        text-align: center;
    }
    
    /* Page breaks for sections */
    .section-break {
        page-break-before: always;
    }
    
    /* Avoid breaking inside important elements */
    .no-break {
        page-break-inside: avoid;
    }
    
    /* Mermaid diagram styling */
    .mermaid {
        text-align: center;
        margin: 15pt 0;
        font-family: monospace;
        font-size: 9pt;
        background: #f8f9fa;
        padding: 10pt;
        border-radius: 4pt;
        page-break-inside: avoid;
    }
    """

def process_markdown_content(content):
    """Traite le contenu Markdown pour l'optimiser pour PDF"""
    
    # Remplacer les titres de slides par des classes CSS
    content = content.replace('#### Slide', '<div class="slide-title">Slide')
    
    # Ajouter des sauts de page pour les parties principales
    content = content.replace('### PARTIE', '<div class="section-break">### PARTIE')
    
    # Traiter les diagrammes Mermaid
    import re
    mermaid_pattern = r'```mermaid\n(.*?)```'
    
    def replace_mermaid(match):
        mermaid_code = match.group(1)
        return f'<div class="mermaid"><pre><code>{mermaid_code}</code></pre></div><div class="diagram-placeholder">📊 Diagramme Mermaid - Voir fichier original pour version interactive</div>'
    
    content = re.sub(mermaid_pattern, replace_mermaid, content, flags=re.DOTALL)
    
    # Ajouter des classes pour les tableaux
    content = content.replace('<table>', '<table class="no-break">')
    
    # Traiter les listes avec des icônes
    content = content.replace('•', '🔹')
    content = content.replace('✅', '✅')
    content = content.replace('⚡', '⚡')
    content = content.replace('📊', '📊')
    content = content.replace('🎯', '🎯')
    content = content.replace('🚀', '🚀')
    
    return content

def generate_pdf():
    """Génère le PDF de présentation"""
    
    # Chemins des fichiers
    input_file = "PRESENTATION_STRUCTURE_COMPLETE.md"
    output_file = "PRESENTATION_COMPLETE.pdf"
    
    try:
        # Vérifier si le fichier d'entrée existe
        if not os.path.exists(input_file):
            print(f"❌ Erreur: Le fichier {input_file} n'existe pas")
            return False
        
        # Lire le contenu Markdown
        print(f"📖 Lecture du fichier {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Traiter le contenu
        print("🔄 Traitement du contenu Markdown...")
        processed_content = process_markdown_content(markdown_content)
        
        # Convertir Markdown en HTML
        print("🔄 Conversion Markdown vers HTML...")
        html_content = markdown.markdown(
            processed_content,
            extensions=['tables', 'fenced_code', 'codehilite', 'toc', 'attr_list']
        )
        
        # Créer le HTML complet
        html_template = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Présentation - Solution de Géolocalisation Poids Lourd</title>
</head>
<body>
    <div class="document">
        {html_content}
        <div class="footer">
            Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}<br>
            Solution de Géolocalisation Avancée pour Poids Lourds
        </div>
    </div>
</body>
</html>
        """
        
        # Créer le CSS
        css_content = create_presentation_css()
        
        # Générer le PDF
        print(f"📄 Génération du PDF {output_file}...")
        HTML(string=html_template).write_pdf(
            output_file,
            stylesheets=[CSS(string=css_content)]
        )
        
        print(f"✅ PDF généré avec succès: {output_file}")
        
        # Afficher la taille du fichier
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        print(f"📊 Taille du fichier: {file_size:.2f} MB")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Veuillez installer les dépendances avec:")
        print("   pip install markdown weasyprint")
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Génération du PDF de présentation")
    print("=" * 50)
    
    success = generate_pdf()
    
    if success:
        print("\n🎉 Génération terminée avec succès!")
        print("📄 Fichier PDF disponible: PRESENTATION_COMPLETE.pdf")
    else:
        print("\n❌ Échec de la génération du PDF")
        print("💡 Vérifiez les dépendances et les fichiers d'entrée")

if __name__ == "__main__":
    main()
