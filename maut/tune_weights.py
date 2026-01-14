import os
import pandas as pd
import importlib.util
import maut as maut_mod


def import_report_module():
    report_path = os.path.join(os.path.dirname(__file__), 'report.py')
    spec = importlib.util.spec_from_file_location('maut_report', report_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_preset(name, weights, benefit, df, criteria, report_mod, out_dir):
    result = maut_mod.maut(df, criteria, weights, benefit)
    base = os.path.join(out_dir, name)
    os.makedirs(base, exist_ok=True)

    txt = os.path.join(base, f'result_{name}.txt')
    csv = os.path.join(base, f'result_{name}.csv')
    pdf = os.path.join(base, f'result_{name}.pdf')

    with open(txt, 'w', encoding='utf-8') as f:
        f.write(f'Preset: {name}\n')
        f.write('Weights:\n')
        for k, v in weights.items():
            f.write(f' - {k}: {v}\n')
        f.write('\n')
        f.write(result[['Alternative'] + criteria + ['Score']].to_string(index=False))

    result.to_csv(csv, index=False)
    report_mod.build_pdf(pdf, result, criteria, weights, benefit)
    return txt, csv, pdf


def main():
    here = os.path.dirname(__file__)
    data_path = os.path.join(here, '..', 'data', 'alternatives.csv')
    df = pd.read_csv(data_path)

    criteria = ['Price', 'Duration', 'Facilities', 'Destination', 'Rating']
    benefit = {
        'Price': False,
        'Duration': False,
        'Facilities': True,
        'Destination': True,
        'Rating': True,
    }

    presets = {
        'price-focused': {
            'weights': {'Price': 0.4, 'Duration': 0.1, 'Facilities': 0.2, 'Destination': 0.15, 'Rating': 0.15}
        },
        'duration-focused': {
            'weights': {'Price': 0.2, 'Duration': 0.4, 'Facilities': 0.15, 'Destination': 0.15, 'Rating': 0.1}
        },
        'balanced': {
            'weights': {'Price': 0.25, 'Duration': 0.15, 'Facilities': 0.2, 'Destination': 0.2, 'Rating': 0.2}
        }
    }

    report_mod = import_report_module()

    out_dir = os.path.join(here, '..', 'results', 'tuning')
    os.makedirs(out_dir, exist_ok=True)

    summary = []
    for name, cfg in presets.items():
        txt, csv, pdf = run_preset(name, cfg['weights'], benefit, df, criteria, report_mod, out_dir)
        summary.append((name, txt, csv, pdf))

    # write summary file
    with open(os.path.join(out_dir, 'summary.txt'), 'w', encoding='utf-8') as f:
        for name, txt, csv, pdf in summary:
            f.write(f'{name}:\n  txt: {txt}\n  csv: {csv}\n  pdf: {pdf}\n\n')

    print('Tuning complete, outputs in', out_dir)


if __name__ == '__main__':
    main()
