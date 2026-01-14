import os
import pandas as pd
import maut as maut_mod
import importlib.util
import os

# helper to import maut.report module from file
def import_report_module():
    report_path = os.path.join(os.path.dirname(__file__), 'report.py')
    spec = importlib.util.spec_from_file_location('maut_report', report_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

report_mod = import_report_module()
build_pdf = report_mod.build_pdf


def main():
    here = os.path.dirname(__file__)
    data_path = os.path.join(here, '..', 'data', 'alternatives.csv')
    df = pd.read_csv(data_path)

    # Default weights added as requested
    weights = {
        'Price': 0.25,
        'Duration': 0.15,
        'Facilities': 0.20,
        'Destination': 0.20,
        'Rating': 0.20,
    }

    benefit = {
        'Price': False,
        'Duration': False,
        'Facilities': True,
        'Destination': True,
        'Rating': True,
    }

    criteria = ['Price', 'Duration', 'Facilities', 'Destination', 'Rating']

    result = maut_mod.maut(df, criteria, weights, benefit)

    out_dir = os.path.join(here, '..', 'results')
    os.makedirs(out_dir, exist_ok=True)

    txt_path = os.path.join(out_dir, 'report_with_weights.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write('Hasil perankingan (dengan bobot default):\n\n')
        f.write(result[['Alternative'] + criteria + ['Score']].to_string(index=False))

    csv_path = os.path.join(out_dir, 'report_with_weights.csv')
    result.to_csv(csv_path, index=False)

    pdf_path = os.path.join(out_dir, 'report_with_weights.pdf')
    build_pdf(pdf_path, result, criteria, weights, benefit)

    print('Wrote:', txt_path, csv_path, pdf_path)


if __name__ == '__main__':
    main()
