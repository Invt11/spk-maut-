import os
import pandas as pd


def load_ranking(csv_path):
    df = pd.read_csv(csv_path)
    # ensure ordering by Score desc
    df = df.sort_values('Score', ascending=False).reset_index(drop=True)
    df['Rank'] = df.index + 1
    return df[['Alternative', 'Rank']]


def main():
    base = os.path.join(os.path.dirname(__file__), '..', 'results', 'tuning')
    presets = ['price-focused', 'duration-focused', 'balanced']
    ranking_tables = {}

    for p in presets:
        csv_path = os.path.join(base, p, f'result_{p}.csv')
        if not os.path.exists(csv_path):
            print('Missing', csv_path)
            return
        ranking_tables[p] = load_ranking(csv_path)

    # build combined table
    all_alts = pd.Index(sorted(set().union(*[set(t['Alternative']) for t in ranking_tables.values()])))
    comp = pd.DataFrame({'Alternative': all_alts})

    for p, df in ranking_tables.items():
        comp = comp.merge(df, on='Alternative', how='left')
        comp = comp.rename(columns={'Rank': p})

    # reorder columns
    comp = comp[['Alternative'] + presets]

    out_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'tuning')
    out_csv = os.path.join(out_dir, 'comparison_ranks.csv')
    comp.to_csv(out_csv, index=False)

    print('\nPerbandingan posisi paket antar preset:\n')
    print(comp.to_string(index=False))
    print('\nSaved to', out_csv)


if __name__ == '__main__':
    main()
