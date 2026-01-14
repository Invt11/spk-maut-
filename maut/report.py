from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
import pandas as pd
import maut as maut_mod


def build_pdf(output_path, df_result, criteria, weights, benefit):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    y = height - margin

    c.setFont('Helvetica-Bold', 14)
    c.drawString(margin, y, 'Laporan Hasil Perankingan MAUT - Rodex Tours & Travel')
    y -= 10 * mm

    c.setFont('Helvetica', 10)
    c.drawString(margin, y, 'Kriteria dan bobot:')
    y -= 6 * mm
    for k in criteria:
        c.drawString(margin + 6 * mm, y, f'- {k}: weight={weights[k]:.2f}, type={"Benefit" if benefit[k] else "Cost"}')
        y -= 5 * mm

    y -= 4 * mm
    c.drawString(margin, y, 'Hasil Perankingan:')
    y -= 6 * mm

    # Table header
    col_x = [margin, margin + 60 * mm, margin + 95 * mm, margin + 120 * mm, margin + 145 * mm, margin + 170 * mm]
    c.setFont('Helvetica-Bold', 9)
    headers = ['No', 'Alternative', 'Price', 'Duration', 'Rating', 'Score']
    for i, h in enumerate(headers):
        c.drawString(col_x[i], y, h)
    y -= 6 * mm
    c.setFont('Helvetica', 9)

    for idx, row in df_result.iterrows():
        if y < margin + 30 * mm:
            c.showPage()
            y = height - margin
        c.drawString(col_x[0], y, str(idx + 1))
        c.drawString(col_x[1], y, str(row['Alternative']))
        c.drawRightString(col_x[2] + 20 * mm, y, f"{int(row['Price']):,}")
        c.drawRightString(col_x[3] + 8 * mm, y, str(int(row['Duration'])))
        c.drawRightString(col_x[4] + 8 * mm, y, f"{row.get('Rating',0):.1f}")
        c.drawRightString(col_x[5] + 8 * mm, y, f"{row['Score']:.6f}")
        y -= 6 * mm

    c.showPage()
    c.save()


def main():
    here = os.path.dirname(__file__)
    data_path = os.path.join(here, '..', 'data', 'alternatives.csv')
    df = pd.read_csv(data_path)

    criteria = ['Price', 'Duration', 'Facilities', 'Destination', 'Rating']
    weights = {
        'Price': 0.25,
        'Duration': 0.15,
        'Facilities': 0.2,
        'Destination': 0.2,
        'Rating': 0.2,
    }
    benefit = {
        'Price': False,
        'Duration': False,
        'Facilities': True,
        'Destination': True,
        'Rating': True,
    }

    result = maut_mod.maut(df, criteria, weights, benefit)

    out_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, 'report.pdf')
    build_pdf(out_pdf, result, criteria, weights, benefit)
    print('PDF report generated:', out_pdf)


if __name__ == '__main__':
    main()
