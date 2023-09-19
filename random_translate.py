from googletrans import Translator, LANGUAGES
import sys
import PyPDF2
import os
import random
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet



translator = Translator(service_urls=['translate.google.com'])
langkeys = list(LANGUAGES.keys())
filename = sys.argv[1]
outputname = sys.argv[2]
doc = SimpleDocTemplate(outputname, pagesize=letter)
style = getSampleStyleSheet()

n = int(input('how many iterations of translation? '))


origin_lang = ""


text_pages = []
translated = []

if ".pdf" in filename:
    with open(filename, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for pg_nm in range(len(reader.pages)):
            pg = reader._get_page(pg_nm)
            text = pg.extract_text()
            text_pages.append(text)
           
else:
    raise TypeError(f'Wrong filetype, file {filename} not a pdf')

origin_lang = translator.detect(text_pages[0]).lang
for i in range(n):
    lg = langkeys[random.randint(0, len(langkeys))]
    print(f'language is {lg}')
    for i in range(len(text_pages)):
        print(f'translating page {i}')
        untranslated = text_pages[i]
        text_pages[i] = translator.translate(untranslated, dest=lg).text
    print(text_pages)
print("exiting multiple translation")
final = []
for i in text_pages:
    t = translator.translate(i, dest=origin_lang).text
    final.append(Paragraph(t))
print("BUILDING DOCUMENT")


doc.build(final)

