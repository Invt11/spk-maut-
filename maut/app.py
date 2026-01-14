import streamlit as st
import pandas as pd
import os
from maut import maut as maut_module


st.set_page_config(page_title="MAUT - Rodex Tours & Travel", layout="wide")

st.title("Sistem Pendukung Keputusan Paket Wisata (MAUT)")

st.markdown("Upload file CSV atau gunakan dataset contoh bawaan.")

uploaded = st.file_uploader("Upload CSV (kolom: Alternative, Price, Duration, Facilities, Destination, Rating)", type=["csv"]) 

if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'alternatives.csv')
    df = pd.read_csv(sample_path)

st.subheader("Dataset")
st.dataframe(df)

criteria = ['Price', 'Duration', 'Facilities', 'Destination', 'Rating']

st.sidebar.header('Bobot kriteria (harus dijumlah = 1)')
weights = {}
total = 0.0
for c in criteria:
    w = st.sidebar.number_input(c, min_value=0.0, max_value=1.0, value=0.2 if c != 'Price' else 0.25, step=0.05, format="%.2f")
    weights[c] = float(w)
    total += float(w)

st.sidebar.markdown(f"**Total bobot:** {total:.2f}")
if abs(total - 1.0) > 1e-6:
    st.sidebar.error('Jumlah bobot harus 1.0')

st.sidebar.header('Tipe kriteria')
benefit = {}
for c in criteria:
    b = st.sidebar.selectbox(f"{c}", options=['Benefit','Cost'])
    benefit[c] = True if b == 'Benefit' else False

if st.button('Jalankan MAUT'):
    if abs(total - 1.0) > 1e-6:
        st.error('Perbaiki bobot sehingga jumlahnya 1.0')
    else:
        result = maut_module.maut(df, criteria, weights, benefit)
        st.subheader('Hasil Perankingan')
        st.dataframe(result[['Alternative'] + criteria + ['Score']])
        csv = result.to_csv(index=False)
        st.download_button('Unduh hasil CSV', data=csv, file_name='maut_result.csv')
