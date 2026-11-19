from pathlib import Path
import argparse, ast, copy, hashlib, json, re, shutil
from xml.sax.saxutils import escape
import fitz
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether, Preformatted

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent/'assistant-rag-horizon'
FONT_DIR=PROJECT/'assets/fonts'
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Display','DejaVuSerif.ttf'),('Mono','DejaVuSansMono.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(FONT_DIR/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
INK=colors.HexColor('#15263b');BLUE=colors.HexColor('#3157c8');MUTED=colors.HexColor('#607086');PALE=colors.HexColor('#edf2fc');LINE=colors.HexColor('#dbe2ed')
S={
 'body':ParagraphStyle('Body',fontName='Body',fontSize=10.2,leading=15.2,textColor=INK,spaceAfter=9),
 'small':ParagraphStyle('Small',fontName='Body',fontSize=8.5,leading=12.2,textColor=MUTED,spaceAfter=7),
 'h1':ParagraphStyle('Title',fontName='Display',fontSize=27,leading=33,textColor=INK,spaceAfter=16),
 'h2':ParagraphStyle('Heading',fontName='Bold',fontSize=13,leading=18,textColor=BLUE,spaceBefore=14,spaceAfter=8,keepWithNext=True),
 'lead':ParagraphStyle('Lead',fontName='Body',fontSize=13,leading=19,textColor=INK,spaceAfter=15),
 'label':ParagraphStyle('Label',fontName='Bold',fontSize=8,leading=12,textColor=BLUE,spaceAfter=14),
 'cell':ParagraphStyle('Cell',fontName='Body',fontSize=9,leading=13,textColor=INK),
}

def txt(value):
 value=escape(value.replace('\u2011','-').replace('\u2014','-').replace('\u2013','-'))
 return re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',value)

def p(value,style='body'):
 return Paragraph(txt(value),S[style])

def bullets(values):
 return [p('• '+v) for v in values]

def table(headers,rows,widths):
 data=[[p(str(x),'cell') for x in headers]]+[[p(str(x),'cell') for x in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('LINEBELOW',(0,0),(-1,0),.8,BLUE),('LINEBELOW',(0,1),(-1,-1),.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
 return t

def footer(canvas,doc):
 w,h=doc.pagesize
 canvas.saveState();canvas.setFillColor(BLUE);canvas.setFont('Bold',8)
 canvas.drawString(doc.leftMargin,h-29,'KORYXA / ASSISTANTS IA')
 canvas.setStrokeColor(LINE);canvas.line(doc.leftMargin,h-37,w-doc.rightMargin,h-37)
 canvas.setFont('Body',7.5);canvas.setFillColor(MUTED)
 canvas.drawString(doc.leftMargin,24,'Dossier de lancement - 18 novembre 2026')
 canvas.drawRightString(w-doc.rightMargin,24,str(doc.page));canvas.restoreState()

def build_dossier():
 width=A4[0]-96
 story=[p('POSITIONNEMENT ET OFFRE','label'),p('Apprendre à construire.\nSavoir livrer.','h1'),p('Faire de KORYXA une référence francophone pour apprendre à construire, vérifier et livrer des assistants IA en entreprise.','lead')]
 story+=[p('La promesse du premier produit','h2'),p('Créez un assistant IA que vous savez expliquer, tester et livrer à un client.','lead'),p('Pour les développeurs et freelances francophones qui connaissent les bases de Python et veulent réaliser un assistant documentaire pour une organisation.')]
 story+=[p('Une offre de départ unique','h2'),table(['Contenu','Résultat pour le lecteur'],[
  ['Guide de 68 pages / 12 chapitres','Comprendre le parcours, les choix et les vérifications.'],
  ['Projet et code source','Suivre l’assistant Horizon Numérique, son API et son interface.'],
  ['Documents et 35 questions','Reproduire les exercices et examiner les réponses.'],
  ['Modèles client','Cadrer le besoin, présenter le travail et préparer la remise.'],
  ['Scripts et procédures','Configurer, sauvegarder, restaurer et chiffrer l’usage.']], [150,width-150])]
 story+=[p('Le tarif et le parcours d’achat seront ajoutés à l’offre retenue. Ce dossier prépare la présentation et la démonstration.','small'),p('LAMADOKOU Yayra','h2')]

 story+=[PageBreak(),p('TEXTE DE PRÉSENTATION','label'),p('Créez un assistant IA que vous savez tester et livrer.','h1'),p('Un guide pratique en français, un projet complet et son code pour passer des documents d’une entreprise à un assistant documentaire, puis préparer sa livraison à un client.','lead')]
 story+=[p('Une progression complète','h2'),p('Avec « Créer et livrer son premier assistant IA », vous suivez Horizon Numérique, un centre de formation fictif. Vous préparez les documents, construisez la recherche et la génération, examinez les réponses et organisez la remise du projet.')]
 story+=bullets(['Transformer une demande client en projet défini.','Préparer et mettre à jour des documents PDF et Markdown.','Retrouver les passages utiles et afficher leurs sources.','Relier Cohere à une API, une interface et une administration.','Évaluer le résultat et préparer le déploiement et la livraison.'])
 story+=[p('Le pack','h2'),p('Le livre, le code du projet, les documents d’exercice, les questions de référence et les modèles de cadrage, devis, réception et évaluation.'),p('Pour qui ?','h2'),p('Développeurs et freelances connaissant les bases de Python. Le projet utilise FastAPI, Next.js, PostgreSQL/pgvector, Docker et Cohere.'),p('Action proposée : lire l’extrait gratuit.','h2'),p('L’extrait présente le cadrage client et le fonctionnement du RAG. Son fichier est fourni dans le dossier de lancement.','small')]

 story+=[PageBreak(),p('DÉMONSTRATION DE RÉFÉRENCE','label'),p('Une preuve en\n90 secondes.','h1'),p('Montrer le lien entre une réponse, sa source et une mise à jour des documents. Les montants d’Horizon Numérique sont fictifs.','lead')]
 story+=[table(['Temps','À montrer','Résultat attendu'],[
  ['0-10 s','La grille tarifaire et l’assistant.','Présenter le besoin documentaire.'],
  ['10-25 s','Poser la question sur Analyse de Données.','650 euros et une source.'],
  ['25-38 s','Ouvrir le document cité.','Le passage confirme le montant.'],
  ['38-48 s','Demander seulement le prix de « la formation ».','Une précision sur la formation.'],
  ['48-65 s','Remplacer la grille dans l’administration.','Nouvelle version indexée.'],
  ['65-80 s','Reposer la question dans une nouvelle conversation.','700 euros et la nouvelle source.'],
  ['80-90 s','Présenter le guide et le code.','Inviter à découvrir l’extrait.']], [54,235,width-289])]
 story+=[p('Deux versions du même fichier sont fournies','h2'),p('Avant : 650 euros, tranches 220 + 220 + 210. Après : 700 euros, tranches 250 + 250 + 200. Le nom du PDF reste identique pour effectuer le remplacement.'),p('Répéter le scénario avec le véritable fournisseur et vérifier les résultats avant l’enregistrement. Les comportements indiqués sont des attentes à observer.','small')]

 story+=[PageBreak(),p('ORDRE DE LANCEMENT','label'),p('Une offre visible.\nDes résultats documentés.','h1')]
 for title,body in [
  ('1. Présenter','Relire l’offre, publier un extrait et conserver une promesse identique dans chaque support.'),
  ('2. Montrer','Exécuter les questions avec Cohere, vérifier le remplacement documentaire et enregistrer le parcours validé.'),
  ('3. Organiser l’achat','Fixer le tarif, choisir le paiement et vérifier l’accès aux fichiers après achat.'),
  ('4. Faire connaître','Associer la présentation, l’extrait et la démonstration. Utiliser les brouillons de publication fournis.'),
  ('5. Faire progresser','Recueillir les difficultés et les réalisations des lecteurs, puis améliorer le parcours et documenter les cas avec leur accord.')]:
  story+=[p(title,'h2'),p(body)]
 story+=[p('Ce qui est déjà vérifié','h2'),p('46 tests logiciels avec des doubles de test ; compilation de l’interface ; parcours sur ordinateur et mobile avec un fournisseur simulé. Les essais réels Cohere et Docker compléteront ces contrôles.','small'),p('Mesures à suivre','h2'),p('Consultations de la présentation, lectures de l’extrait, demandes reçues, achats après ouverture et projets réalisés par les lecteurs. Les premiers résultats seront consignés pendant le lancement.','small')]

 story+=[PageBreak(),p('PREMIERS CONTENUS','label'),p('Une même promesse,\nplusieurs formats.','h1'),p('Publication LinkedIn ou Facebook','h2')]
 md=(ROOT/'Dossier_lancement_KORYXA_Assistants_IA.md').read_text()
 publication=md.split('### Publication LinkedIn ou Facebook\n\n',1)[1].split('### Script vidéo court',1)[0].strip()
 for paragraph in publication.split('\n\n'):story.append(p(paragraph))
 story+=[p('Vidéo courte / 35 à 45 secondes','h2')]
 video=md.split('### Script vidéo court - 35 à 45 secondes\n\n',1)[1].split('## 6.',1)[0].strip()
 for paragraph in video.split('\n\n'):story.append(p(paragraph))
 story+=[p('Textes préparés pour relecture. Aucune publication ni prise de contact n’a été effectuée.','small')]
 destination=ROOT/'Dossier_lancement_KORYXA_Assistants_IA.pdf'
 SimpleDocTemplate(str(destination),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=57,bottomMargin=43,title='KORYXA - Dossier de lancement Assistants IA',author='LAMADOKOU Yayra').build(story,onFirstPage=footer,onLaterPages=footer)
 return destination

def excerpt_footer(canvas,doc):
 canvas.saveState();canvas.setFillColor(MUTED);canvas.setFont('Body',7)
 canvas.drawString(35,24,'KORYXA / EXTRAIT DÉCOUVERTE');canvas.restoreState()

def build_excerpt(source):
 current=fitz.open(source)
 first=next(i for i in range(3,len(current)) if 'Chapitre 1 -' in current[i].get_text()[:250])
 stop=next(i for i in range(first+1,len(current)) if 'Partie II -' in current[i].get_text()[:250])
 tmp=ROOT/'reference';tmp.mkdir(exist_ok=True)
 cover=tmp/'couverture_extrait.pdf'
 closing=tmp/'suite_extrait.pdf'
 styles={k:v.clone('excerpt-'+k) for k,v in S.items()}
 cover_story=[Spacer(1,35),Paragraph('KORYXA / ASSISTANTS IA',styles['label']),Spacer(1,16),Paragraph('Créer et livrer<br/>son premier<br/>assistant IA',styles['h1']),Spacer(1,25),Paragraph('Extrait découverte',styles['h2']),Paragraph('Chapitres 1 et 2 : cadrer le besoin du client et comprendre le RAG.',styles['lead']),Spacer(1,18),Paragraph('LAMADOKOU Yayra',styles['h2']),Paragraph('Édition Cohere. Projet pédagogique fictif Horizon Numérique. Les pages extraites conservent la pagination du guide complet.',styles['small'])]
 SimpleDocTemplate(str(cover),pagesize=A5,leftMargin=35,rightMargin=35,topMargin=35,bottomMargin=42,title='KORYXA - Extrait du guide Assistant IA',author='LAMADOKOU Yayra').build(cover_story,onFirstPage=excerpt_footer)
 closing_story=[p('CONTINUER LE PARCOURS','label'),p('Du besoin client\nà la livraison.','h1'),p('La suite du guide accompagne la préparation des documents, la recherche, la génération avec Cohere, l’API et l’interface.','body'),p('Vous aborderez aussi','h2')]
 closing_story+=bullets(['La vérification des réponses et de leurs sources.','Le remplacement des documents.','Le déploiement, la sauvegarde et la restauration.','Le budget et la remise du projet au client.'])
 closing_story+=[p('Le guide complet est accompagné du code, des documents d’exercice, des questions de référence et des modèles de livraison.','body'),p('KORYXA','h2'),p('Apprendre à construire. Savoir livrer.','lead')]
 SimpleDocTemplate(str(closing),pagesize=A5,leftMargin=35,rightMargin=35,topMargin=35,bottomMargin=42).build(closing_story,onFirstPage=excerpt_footer)
 writer=PdfWriter();writer.append(str(cover))
 writer.append(str(source),pages=(first,stop),import_outline=False)
 writer.append(str(closing));writer.add_metadata({'/Title':'KORYXA - Créer et livrer son premier assistant IA - Extrait','/Author':'LAMADOKOU Yayra'})
 destination=ROOT/'KORYXA_Assistant_IA_Extrait.pdf'
 with destination.open('wb') as file:writer.write(file)
 current.close()
 return destination,first+1,stop

def build_demo():
 source=PROJECT/'corpus/02_tarifs_et_financements.pdf'
 before=ROOT/'demo/avant'/source.name;before.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,before)
 ast_source=ast.parse((PROJECT/'scripts/build_corpus.py').read_text())
 assignment=next(n for n in ast_source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DOCUMENTS' for t in n.targets))
 pages=copy.deepcopy(ast.literal_eval(assignment.value)[source.name])
 after=ROOT/'demo/apres'/source.name;after.parent.mkdir(parents=True,exist_ok=True)
 rows=[]
 for index,(title,paras) in enumerate(pages):
  if index:rows.append(PageBreak())
  rows+=[p('HORIZON NUMÉRIQUE','label'),p(title,'h1')]
  for paragraph in paras:
   paragraph=paragraph.replace('650 euros','700 euros').replace('220 euros, 220 euros puis 210 euros','250 euros, 250 euros puis 200 euros')
   rows.append(p(paragraph))
 def page_footer(c,d):
  c.setFont('Body',8);c.setFillColor(MUTED);c.drawString(44,27,'Horizon Numérique - document fictif pour exercice');c.drawRightString(A4[0]-44,27,f'Page {d.page}')
 SimpleDocTemplate(str(after),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=44,bottomMargin=45,author='LAMADOKOU Yayra').build(rows,onFirstPage=page_footer,onLaterPages=page_footer)
 manifest=[]
 for path,total in [(before,'650 euros'),(after,'700 euros')]:
  text=' '.join(page.extract_text() or '' for page in PdfReader(path).pages)
  if total not in text:raise ValueError('Tarif attendu absent du document.')
  manifest.append({'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'expected_total':total})
 (ROOT/'demo/versions_documents.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 return manifest

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--book',type=Path,required=True);args=parser.parse_args()
 dossier=build_dossier();extrait,start,end=build_excerpt(args.book);manifest=build_demo()
 print(json.dumps({'dossier':str(dossier),'dossier_pages':len(PdfReader(dossier).pages),'extrait':str(extrait),'extrait_pages':len(PdfReader(extrait).pages),'source_pages_inclusive':[start,end],'demo':manifest},ensure_ascii=False))

if __name__=='__main__':main()
