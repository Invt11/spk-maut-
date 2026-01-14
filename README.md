# SISTEM PENDUKUNG KEPUTUSAN MAUT untuk PT. Rodex Tours & Travel

Prototipe sederhana untuk memilih paket wisata menggunakan metode Multi-Attribute Utility Theory (MAUT).

Quick start

1. Instal dependensi:

```bash
pip install -r requirements.txt
```

2. Jalankan demo:

```bash
python3 maut/maut.py
```

Files
- `maut/maut.py`: implementasi MAUT dan demo yang membaca `data/alternatives.csv`.
- `data/alternatives.csv`: contoh dataset paket wisata.
- `requirements.txt`: dependensi minimal.

Web interface (Streamlit)

1. Instal dependensi (sudah termasuk `streamlit` di `requirements.txt`):

```bash
pip install -r requirements.txt
```

2. Jalankan aplikasi Streamlit:

```bash
streamlit run maut/app.py
```

Anda dapat mengubah bobot kriteria di sidebar dan mengunggah file CSV kustom.

Selanjutnya Anda bisa:
- Mengubah bobot dan tipe kriteria di `maut/maut.py`.
- Menambahkan antarmuka (Streamlit/Flask) untuk input dinamis.
# spk-maut-