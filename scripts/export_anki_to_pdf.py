from glob import glob
from os import path
import csv
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A7, landscape
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer  
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle   
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY       
from reportlab.pdfbase import pdfmetrics      
from reportlab.pdfbase.ttfonts import TTFont   
from reportlab.lib.fonts import addMapping

how_to_study_korean_dir = path.join('/Users/jlibbey/Repositories/goforbroca', 'data', 'howtostudykorean.com')

pdfmetrics.registerFont(TTFont('Arial Unicode', 'Arial Unicode.ttf'))
addMapping('Arial Unicode', 0, 0, 'ArialUnicode')

styles = getSampleStyleSheet()
styles["Title"].fontName = 'Arial Unicode'

width, height = landscape(A7)
margin = 20

def csvs_to_pdf(csv_file_paths, pdf_name):
    canvas = Canvas(f'{pdf_name}.pdf', pagesize=landscape(A7))  # 74 x 105 mm

    for csv_file_path in csv_file_paths:
        print(f'csv_to_pdf: {csv_file_path}')
        deck_name = path.basename(csv_file_path)[:-4]
        with open(csv_file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter='\t')
            for row in reader:
                back = row[0]
                front = row[1]

                p_back = Paragraph(back, styles["Title"])
                p_back.wrap(width, height)
                p_back.drawOn(canvas, 0, height/2)

                canvas.drawString(margin, margin, deck_name)
                canvas.showPage()

                p_front = Paragraph(front, styles["Title"])
                p_front.wrap(width, height)
                p_front.drawOn(canvas, 0, height/2)

                canvas.drawString(margin, margin, deck_name)
                canvas.showPage()

    canvas.save()


def csv_to_pdf(csv_file_path: str):
    print(f'csv_to_pdf: {csv_file_path}')

    deck_name = path.basename(csv_file_path)[:-4]

    canvas = Canvas(f'{deck_name}.pdf', pagesize=landscape(A7))  # 74 x 105 mm

    with open(csv_file_path) as csv_file:
        reader = csv.reader(csv_file, delimiter='\t')
        for row in reader:
            back = row[0]
            front = row[1]

            p_back = Paragraph(back, styles["Title"])
            p_back.wrap(width, height)
            p_back.drawOn(canvas, 0, height/2)

            canvas.drawString(margin, margin, deck_name)
            canvas.showPage()

            p_front = Paragraph(front, styles["Title"])
            p_front.wrap(width, height)
            p_front.drawOn(canvas, 0, height/2)

            canvas.drawString(margin, margin, deck_name)
            canvas.showPage()

    canvas.save()


def main():
    csv_file_paths = sorted(glob(path.join(how_to_study_korean_dir, '*.csv')))
    # csvs_to_pdf(csv_file_paths, 'How to Study Korean: lessons 1 - 3')
    for csv_file_path in csv_file_paths:
        csv_to_pdf(csv_file_path)


if __name__ == '__main__':
    main()
