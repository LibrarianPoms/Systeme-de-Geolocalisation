#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour convertir Markdown en LaTeX avec capture d'images des diagrammes Mermaid
Utilise Mermaid CLI pour générer des images PNG des diagrammes
"""

import os
import sys
import re
import subprocess
import tempfile
import shutil
from datetime import datetime
import base64
import json

class MarkdownToLatexConverter:
    def __init__(self, input_file="PRESENTATION_STRUCTURE_COMPLETE.md", output_dir="latex_output"):
        self.input_file = input_file
        self.output_dir = output_dir
        self.images_dir = os.path.join(output_dir, "images")
        self.diagram_counter = 0
        self.latex_content = []
        
        # Créer les répertoires
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
    def setup_latex_preamble(self):
        """Configure le préambule LaTeX"""
        preamble = r"""
\documentclass[aspectratio=169,12pt]{beamer}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}
\usepackage{colortbl}
\usepackage{xcolor}
\usepackage{fontawesome5}
\usepackage{listings}
\usepackage{adjustbox}

% Définition des couleurs
\definecolor{primaryblue}{RGB}{26,115,232}
\definecolor{darkgray}{RGB}{44,62,80}
\definecolor{lightgray}{RGB}{248,249,250}
\definecolor{bordergray}{RGB}{221,221,221}

% Configuration du thème
\usetheme{Madrid}
\usecolortheme{seahorse}
\setbeamercolor{structure}{fg=primaryblue}
\setbeamercolor{title}{fg=white,bg=primaryblue}
\setbeamercolor{frametitle}{fg=white,bg=primaryblue}

% Configuration des polices
\setbeamerfont{title}{size=\Large,series=\bfseries}
\setbeamerfont{frametitle}{size=\large,series=\bfseries}
\setbeamerfont{framesubtitle}{size=\normalsize}

% Configuration des listings pour le code
\lstset{
    basicstyle=\ttfamily\footnotesize,
    backgroundcolor=\color{lightgray},
    frame=single,
    frameround=tttt,
    framesep=2pt,
    breaklines=true,
    showstringspaces=false
}

% Suppression de la navigation
\setbeamertemplate{navigation symbols}{}

% Configuration du pied de page
\setbeamertemplate{footline}{
    \leavevmode%
    \hbox{%
    \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{author in head/foot}%
        \usebeamerfont{author in head/foot}Solution de Géolocalisation Poids Lourd
    \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{title in head/foot}%
        \usebeamerfont{title in head/foot}\insertshorttitle
    \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,right]{date in head/foot}%
        \usebeamerfont{date in head/foot}\insertshortdate{}\hspace*{2em}
        \insertframenumber{} / \inserttotalframenumber\hspace*{2ex} 
    \end{beamercolorbox}}%
    \vskip0pt%
}

% Informations du document
\title{Solution de Géolocalisation Avancée pour Poids Lourds}
\subtitle{Architecture Hybride Hardware/Logiciel/Firmware}
\author{Présentation Technique}
\date{\today}
\institute{Département R\&D}

\begin{document}

% Page de titre
\begin{frame}[plain]
    \titlepage
\end{frame}

"""
        return preamble

    def extract_diagram_title(self, mermaid_code):
        """Extrait le titre du diagramme depuis le code Mermaid"""
        lines = mermaid_code.split('\n')
        for line in lines:
            if 'title' in line.lower():
                title_match = re.search(r'title\s+(.+)', line, re.IGNORECASE)
                if title_match:
                    return title_match.group(1).strip()
        
        # Classification automatique
        if 'flowchart' in mermaid_code:
            return "Diagramme de Flux"
        elif 'graph' in mermaid_code:
            return "Graphe Système"
        elif 'mindmap' in mermaid_code:
            return "Carte Mentale"
        elif 'quadrantChart' in mermaid_code:
            return "Diagramme Quadrant"
        elif 'sequenceDiagram' in mermaid_code:
            return "Diagramme de Séquence"
        elif 'classDiagram' in mermaid_code:
            return "Diagramme de Classes"
        elif 'stateDiagram' in mermaid_code:
            return "Diagramme d'États"
        elif 'erDiagram' in mermaid_code:
            return "Diagramme Entité-Relation"
        elif 'journey' in mermaid_code:
            return "Diagramme de Parcours"
        elif 'gantt' in mermaid_code:
            return "Diagramme de Gantt"
        elif 'pie' in mermaid_code:
            return "Graphique Circulaire"
        elif 'architecture' in mermaid_code.lower() or 'ARCHITECTURE' in mermaid_code:
            return "Architecture Système"
        else:
            return "Diagramme Mermaid"

    def capture_mermaid_diagram(self, mermaid_code, title):
        """Capture un diagramme Mermaid comme image PNG"""
        self.diagram_counter += 1
        diagram_filename = f"diagram_{self.diagram_counter:03d}.png"
        diagram_path = os.path.join(self.images_dir, diagram_filename)
        
        # Créer un fichier Mermaid temporaire
        temp_mmd_file = os.path.join(self.images_dir, f"temp_{self.diagram_counter}.mmd")
        
        # Nettoyer et préparer le code Mermaid
        clean_code = mermaid_code.strip()
        
        # Ajouter un titre si non présent
        if 'title' not in clean_code.lower():
            clean_code = f"title: {title}\n{clean_code}"
        
        # Écrire le fichier Mermaid
        with open(temp_mmd_file, 'w', encoding='utf-8') as f:
            f.write(clean_code)
        
        try:
            # Utiliser Mermaid CLI pour générer l'image
            cmd = [
                'mmdc', 
                '--input', temp_mmd_file,
                '--output', diagram_path,
                '--theme', 'default',
                '--backgroundColor', 'transparent',
                '--width', '800',
                '--height', '600'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(diagram_path):
                print(f"✅ Diagramme #{self.diagram_counter} capturé: {title}")
                return diagram_filename
            else:
                print(f"⚠️ Échec capture diagramme #{self.diagram_counter}: {title}")
                print(f"   Erreur: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"⏱️ Timeout capture diagramme #{self.diagram_counter}")
            return None
        except FileNotFoundError:
            print("❌ Mermaid CLI (mmdc) non trouvé. Installation requise:")
            print("   npm install -g @mermaid-js/mermaid-cli")
            return None
        except Exception as e:
            print(f"❌ Erreur capture diagramme: {e}")
            return None
        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(temp_mmd_file):
                os.remove(temp_mmd_file)

    def process_mermaid_diagram(self, mermaid_code):
        """Traite un diagramme Mermaid et l'ajoute au LaTeX"""
        title = self.extract_diagram_title(mermaid_code)
        
        # Tenter de capturer l'image
        image_filename = self.capture_mermaid_diagram(mermaid_code, title)
        
        # Ajouter le code LaTeX pour le diagramme
        latex_code = r"""
\begin{frame}[fragile]
\frametitle{""" + title + r"""}
\begin{center}
"""
        
        if image_filename:
            latex_code += f"    \\includegraphics[width=0.9\\textwidth,height=0.6\\textheight,keepaspectratio]{{images/{image_filename}}}\n"
        else:
            # Fallback: afficher le code Mermaid comme fallback
            latex_code += r"""
    \begin{tikzpicture}
        \node[draw=primaryblue, fill=lightgray, rounded corners, minimum width=8cm, minimum height=3cm, text centered] {
            \begin{minipage}{7cm}
                \centering
                \textbf{""" + title + r"""}\\[0.5em]
                \textit{[Diagramme Mermaid]}\\[0.5em]
                \small Pour voir le diagramme interactif,\\consultez la version numérique
            \end{minipage}
        };
    \end{tikzpicture}
"""
        
        latex_code += r"""
\end{center}
\end{frame}

"""
        
        self.latex_content.append(latex_code)

    def process_table(self, headers, data):
        """Traite un tableau et le convertit en LaTeX"""
        latex_code = r"""
\begin{frame}
\frametitle{Tableau de Données}
\begin{center}
\resizebox{\textwidth}{!}{%
\begin{tabular}{"""
        
        # Définir les colonnes
        num_cols = len(headers)
        latex_code += 'l' * num_cols + "}\n"
        
        # En-têtes
        latex_code += "\\toprule\n"
        latex_code += " & ".join([f"\\textbf{{h}}" for h in headers]) + " \\\\\n"
        latex_code += "\\midrule\n"
        
        # Données
        for row in data:
            # Échapper les caractères spéciaux LaTeX
            clean_row = []
            for cell in row:
                cell = cell.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')
                cell = cell.replace('#', '\\#').replace('$', '\\$')
                clean_row.append(cell)
            latex_code += " & ".join(clean_row) + " \\\\\n"
        
        latex_code += "\\bottomrule\n"
        latex_code += r"""\end{tabular}%
}
\end{center}
\end{frame}

"""
        
        self.latex_content.append(latex_code)

    def process_code_block(self, code):
        """Traite un bloc de code"""
        latex_code = r"""
\begin{frame}[fragile]
\frametitle{Code Source}
\begin{lstlisting}[language=Python]
""" + code + r"""
\end{lstlisting}
\end{frame}

"""
        
        self.latex_content.append(latex_code)

    def process_content_line(self, line):
        """Traite une ligne de contenu normal"""
        if not line.strip():
            return ""
        
        # Échapper les caractères spéciaux LaTeX
        line = line.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')
        line = line.replace('#', '\\#').replace('$', '\\$').replace('{', '\\{').replace('}', '\\}')
        
        # Remplacer les emojis et icônes
        line = line.replace('•', '\\item ')
        line = line.replace('✅', '\\textcolor{green}{\\checkmark}')
        line = line.replace('⚡', '\\textcolor{yellow}{\\bolt}')
        line = line.replace('📊', '\\faChartBar')
        line = line.replace('🎯', '\\faBullseye')
        line = line.replace('🚀', '\\faRocket')
        
        return line

    def process_markdown_content(self, content):
        """Traite tout le contenu Markdown"""
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # Titres de slides
            if line.startswith('#### Slide'):
                title = line.replace('#### Slide', '').strip()
                latex_code = f"""
\\begin{{frame}}
\\frametitle{{{title}}}

"""
                self.latex_content.append(latex_code)
                
            # Sections
            elif line.startswith('### PARTIE'):
                title = line.replace('### PARTIE', '').strip()
                latex_code = f"""
\\section{{{title}}}

"""
                self.latex_content.append(latex_code)
                
            # Sous-titres
            elif line.startswith('### ') or line.startswith('## '):
                title = re.sub(r'^(#{1,3})\s+', '', line)
                latex_code = f"\\textbf{{{title}}}\\\\\n\n"
                self.latex_content.append(latex_code)
                
            # Diagrammes Mermaid
            elif line.startswith('```mermaid'):
                # Extraire le code du diagramme
                mermaid_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    mermaid_lines.append(lines[i])
                    i += 1
                
                if mermaid_lines:
                    mermaid_code = '\n'.join(mermaid_lines)
                    self.process_mermaid_diagram(mermaid_code)
                    
            # Tableaux
            elif line.startswith('|') and i + 2 < len(lines) and lines[i+1].startswith('|-'):
                # Extraire les en-têtes
                headers = [h.strip() for h in line.split('|')[1:-1]]
                i += 2  # Sauter la ligne de séparation
                
                # Extraire les données
                data = []
                while i < len(lines) and lines[i].startswith('|'):
                    row = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                    if row:
                        data.append(row)
                    i += 1
                
                if headers and data:
                    self.process_table(headers, data)
                i -= 1  # Ajuster pour la boucle
                
            # Blocs de code
            elif line.startswith('```') and not line.startswith('```mermaid'):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                
                if code_lines:
                    self.process_code_block('\n'.join(code_lines))
                    
            # Listes
            elif line.startswith('-') or line.startswith('*'):
                content = self.process_content_line(line)
                self.latex_content.append(content + "\n")
                
            # Contenu normal
            else:
                content = self.process_content_line(line)
                if content:
                    self.latex_content.append(content + "\n\n")
            
            i += 1

    def add_latex_footer(self):
        """Ajoute le pied de page LaTeX"""
        footer = r"""

% Page de conclusion
\begin{frame}[plain]
    \begin{center}
        \Large\textbf{Merci pour votre attention}\\[1em]
        \normalsize
        \textcolor{primaryblue}{Solution de Géolocalisation Avancée pour Poids Lourds}\\[0.5em]
        \small
        Généré le """ + datetime.now().strftime('%d/%m/%Y à %H:%M') + r"""\\[1em]
        \faEnvelope\ contact@company.com\\
        \faGlobe\ www.company.com
    \end{center}
\end{frame}

\end{document}
"""
        self.latex_content.append(footer)

    def generate_latex_file(self):
        """Génère le fichier LaTeX complet"""
        latex_file = os.path.join(self.output_dir, "presentation.tex")
        
        # Assembler le contenu LaTeX
        full_latex = self.setup_latex_preamble()
        full_latex += "".join(self.latex_content)
        self.add_latex_footer()
        full_latex += "".join(self.latex_content[-1:])  # Ajouter le footer
        
        # Écrire le fichier LaTeX
        with open(latex_file, 'w', encoding='utf-8') as f:
            f.write(full_latex)
        
        return latex_file

    def compile_latex_to_pdf(self, latex_file):
        """Compile le fichier LaTeX en PDF"""
        try:
            # Changer le répertoire de travail
            original_cwd = os.getcwd()
            os.chdir(self.output_dir)
            
            # Compiler avec pdflatex (2 fois pour les références)
            for i in range(2):
                cmd = ['pdflatex', '-interaction=nonstopmode', '-shell-escape', 'presentation.tex']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode != 0:
                    print(f"❌ Erreur compilation LaTeX (passage {i+1}):")
                    print(result.stderr)
                    return False
            
            pdf_file = os.path.join(self.output_dir, "presentation.pdf")
            if os.path.exists(pdf_file):
                file_size = os.path.getsize(pdf_file) / (1024 * 1024)  # MB
                print(f"✅ PDF généré avec succès: presentation.pdf ({file_size:.2f} MB)")
                return True
            else:
                print("❌ Fichier PDF non généré")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout lors de la compilation LaTeX")
            return False
        except FileNotFoundError:
            print("❌ pdflatex non trouvé. Installation LaTeX requise (MiKTeX, TeX Live, etc.)")
            return False
        except Exception as e:
            print(f"❌ Erreur compilation LaTeX: {e}")
            return False
        finally:
            os.chdir(original_cwd)

    def convert(self):
        """Effectue la conversion complète"""
        print("🚀 Conversion Markdown vers LaTeX avec diagrammes")
        print("=" * 60)
        
        # Vérifier le fichier d'entrée
        if not os.path.exists(self.input_file):
            print(f"❌ Erreur: Le fichier {self.input_file} n'existe pas")
            return False
        
        # Lire le contenu Markdown
        print(f"📖 Lecture du fichier {self.input_file}...")
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Traiter le contenu
        print("🔄 Traitement du contenu Markdown...")
        self.process_markdown_content(content)
        
        # Générer le fichier LaTeX
        print("📝 Génération du fichier LaTeX...")
        latex_file = self.generate_latex_file()
        print(f"✅ Fichier LaTeX généré: {latex_file}")
        
        # Compiler en PDF
        print("📄 Compilation LaTeX vers PDF...")
        success = self.compile_latex_to_pdf(latex_file)
        
        if success:
            print(f"\n🎉 Conversion terminée avec succès!")
            print(f"📁 Répertoire de sortie: {self.output_dir}")
            print(f"📊 Diagrammes capturés: {self.diagram_counter}")
            print(f"📄 Fichier PDF: {os.path.join(self.output_dir, 'presentation.pdf')}")
            print(f"📝 Fichier LaTeX: {latex_file}")
            print(f"🖼️ Images: {self.images_dir}")
        else:
            print(f"\n❌ Échec de la conversion")
            print(f"💡 Vérifiez l'installation de LaTeX et Mermaid CLI")
        
        return success

def main():
    """Fonction principale"""
    converter = MarkdownToLatexConverter()
    success = converter.convert()
    
    if not success:
        print("\n🔧 Instructions d'installation:")
        print("1. Installer LaTeX (MiKTeX, TeX Live, ou similar)")
        print("2. Installer Node.js")
        print("3. Installer Mermaid CLI: npm install -g @mermaid-js/mermaid-cli")
        print("4. Réexécuter le script")

if __name__ == "__main__":
    main()
