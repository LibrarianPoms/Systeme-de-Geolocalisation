#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplifié pour générer un PDF de présentation depuis un fichier Markdown
Utilise ReportLab pour une conversion plus simple et robuste
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import markdown
import re

class PresentationPDF:
    def __init__(self, output_file="PRESENTATION_COMPLETE.pdf"):
        self.output_file = output_file
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        self.story = []
        
    def setup_custom_styles(self):
        """Configure les styles personnalisés pour la présentation"""
        # Style pour les titres de slides
        self.styles.add(ParagraphStyle(
            name='SlideTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1a73e8'),
            borderWidth=0,
            borderColor=colors.HexColor('#1a73e8'),
            borderPadding=10,
            leading=24
        ))
        
        # Style pour les titres de sections
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#1a73e8'),
            borderWidth=0,
            borderColor=colors.HexColor('#1a73e8'),
            leading=20
        ))
        
        # Style pour les sous-titres
        self.styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.HexColor('#2c3e50'),
            leading=16
        ))
        
        # Style pour le contenu normal
        self.styles.add(ParagraphStyle(
            name='Content',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            leading=14
        ))
        
        # Style pour le code
        self.styles.add(ParagraphStyle(
            name='CodeBlock',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=6,
            fontName='Courier',
            backgroundColor=colors.HexColor('#f1f3f4'),
            leading=12
        ))
        
        # Style pour les listes
        self.styles.add(ParagraphStyle(
            name='ListItem',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            leftIndent=20,
            leading=14
        ))

    def add_slide_break(self):
        """Ajoute un saut de page pour un nouveau slide"""
        self.story.append(PageBreak())

    def add_title(self, text):
        """Ajoute un titre de slide"""
        self.story.append(Paragraph(text, self.styles['SlideTitle']))
        self.story.append(Spacer(1, 0.2*inch))

    def add_section_title(self, text):
        """Ajoute un titre de section"""
        self.story.append(Paragraph(text, self.styles['SectionTitle']))
        self.story.append(Spacer(1, 0.1*inch))

    def add_subtitle(self, text):
        """Ajoute un sous-titre"""
        self.story.append(Paragraph(text, self.styles['SubTitle']))
        self.story.append(Spacer(1, 0.05*inch))

    def add_content(self, text):
        """Ajoute du contenu normal"""
        # Nettoyer le texte
        text = text.replace('**', '<b>').replace('**', '</b>')
        text = text.replace('*', '<i>').replace('*', '</i>')
        text = text.replace('•', '• ')
        text = text.replace('✅', '✅ ')
        text = text.replace('⚡', '⚡ ')
        text = text.replace('📊', '📊 ')
        text = text.replace('🎯', '🎯 ')
        text = text.replace('🚀', '🚀 ')
        
        self.story.append(Paragraph(text, self.styles['Content']))

    def add_code_block(self, code):
        """Ajoute un bloc de code"""
        self.story.append(Paragraph(code, self.styles['CodeBlock']))
        self.story.append(Spacer(1, 0.1*inch))

    def add_table(self, headers, data):
        """Ajoute un tableau"""
        table_data = [headers] + data
        table = Table(table_data, repeatRows=1)
        
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        # Alternance des lignes
        for i in range(1, len(data) + 1):
            if i % 2 == 0:
                style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8f9fa'))
        
        table.setStyle(style)
        self.story.append(table)
        self.story.append(Spacer(1, 0.1*inch))

    def add_separator(self):
        """Ajoute un séparateur"""
        self.story.append(Spacer(1, 0.3*inch))

    def process_markdown_line(self, line):
        """Traite une ligne Markdown"""
        line = line.strip()
        
        if not line:
            return
        
        # Titres de slides
        if line.startswith('#### Slide'):
            self.add_slide_break()
            title = line.replace('#### Slide', '').strip()
            self.add_title(title)
            
        # Titres de sections
        elif line.startswith('### PARTIE'):
            self.add_slide_break()
            self.add_section_title(line)
            
        # Sous-titres
        elif line.startswith('#### '):
            title = line.replace('#### ', '').strip()
            self.add_subtitle(title)
            
        elif line.startswith('### '):
            title = line.replace('### ', '').strip()
            self.add_subtitle(title)
            
        elif line.startswith('## '):
            title = line.replace('## ', '').strip()
            self.add_section_title(title)
            
        # Tableaux
        elif line.startswith('|') and '|' in line[1:]:
            # Collecter les lignes du tableau
            # Cette méthode est simplifiée - pour des tableaux complexes, 
            # une analyse plus approfondie serait nécessaire
            pass
            
        # Blocs de code
        elif line.startswith('```'):
            pass  # Ignorer pour l'instant
            
        # Listes
        elif line.startswith('-') or line.startswith('*'):
            content = line.lstrip('-* ').strip()
            self.story.append(Paragraph(f"• {content}", self.styles['ListItem']))
            
        # Contenu normal
        else:
            self.add_content(line)

    def process_markdown_content(self, content):
        """Traite tout le contenu Markdown"""
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Gérer les tableaux
            if line.startswith('|') and i + 2 < len(lines) and lines[i+1].startswith('|-'):
                # Extraire les en-têtes
                headers = [h.strip() for h in line.split('|')[1:-1]]
                i += 2  # Sauter la ligne de séparation
                
                # Extraire les données
                data = []
                while i < len(lines) and lines[i].startswith('|'):
                    row = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                    if row:  # Ignorer les lignes vides
                        data.append(row)
                    i += 1
                
                if headers and data:
                    self.add_table(headers, data)
                i -= 1  # Ajuster pour la boucle
                
            # Gérer les blocs de code
            elif line.startswith('```'):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                
                if code_lines:
                    self.add_code_block('\n'.join(code_lines))
                    
            else:
                self.process_markdown_line(line)
            
            i += 1

    def add_footer(self):
        """Ajoute un pied de page"""
        self.story.append(PageBreak())
        footer_text = f"""
        <br/><br/><br/><br/><br/><br/><br/>
        <center>
        <b>Présentation - Solution de Géolocalisation Avancée pour Poids Lourds</b><br/>
        Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}<br/>
        <br/>
        Pour plus d'informations : contact@company.com
        </center>
        """
        self.story.append(Paragraph(footer_text, self.styles['Content']))

    def generate_pdf(self, input_file):
        """Génère le PDF à partir du fichier Markdown"""
        try:
            # Lire le fichier Markdown
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Créer le document PDF
            doc = SimpleDocTemplate(
                self.output_file,
                pagesize=landscape(A4),
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Traiter le contenu
            self.process_markdown_content(content)
            
            # Ajouter le pied de page
            self.add_footer()
            
            # Générer le PDF
            doc.build(self.story)
            
            print(f"✅ PDF généré avec succès: {self.output_file}")
            
            # Afficher la taille du fichier
            if os.path.exists(self.output_file):
                file_size = os.path.getsize(self.output_file) / (1024 * 1024)  # MB
                print(f"📊 Taille du fichier: {file_size:.2f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération du PDF: {e}")
            return False

def main():
    """Fonction principale"""
    print("🚀 Génération du PDF de présentation (version simplifiée)")
    print("=" * 60)
    
    input_file = "PRESENTATION_STRUCTURE_COMPLETE.md"
    output_file = "PRESENTATION_COMPLETE.pdf"
    
    # Vérifier si le fichier d'entrée existe
    if not os.path.exists(input_file):
        print(f"❌ Erreur: Le fichier {input_file} n'existe pas")
        return False
    
    # Créer le générateur PDF
    pdf_generator = PresentationPDF(output_file)
    
    # Générer le PDF
    success = pdf_generator.generate_pdf(input_file)
    
    if success:
        print("\n🎉 Génération terminée avec succès!")
        print(f"📄 Fichier PDF disponible: {output_file}")
        print("\n📋 Caractéristiques:")
        print("   • Format: A4 paysage")
        print("   • Pages: Automatique selon contenu")
        print("   • Styles: Professionnels avec couleurs")
        print("   • Tableaux: Formatés automatiquement")
        print("   • Code: Blocs de code préservés")
    else:
        print("\n❌ Échec de la génération du PDF")
    
    return success

if __name__ == "__main__":
    main()
