# AquaCheck FINAL

Aplikasi klasifikasi kualitas air menggunakan algoritma **Decision Tree** dan dataset 7.999 baris.

## Parameter input
- pH
- TDS (ppm)
- Turbidity (NTU)
- Temperature (°C)

## Struktur folder
- `app.py` — dashboard Streamlit
- `train_model.py` — script pelatihan dan evaluasi Decision Tree
- `dataset/AquaCheck_Dataset_7999.csv` — dataset yang digunakan
- `model/model_aquacheck.pkl` — model final yang telah dilatih
- `model/evaluation_metrics.json` — hasil evaluasi

## Menjalankan aplikasi di Windows (Anaconda Prompt)

Buka Anaconda Prompt, lalu masuk ke folder `AquaCheck`:

```bash
cd /d "LOKASI_FOLDER_AquaCheck"
pip install -r requirements.txt
python -m streamlit run app.py
```

## Melatih ulang model

Jika dataset atau konfigurasi model diubah, jalankan:

```bash
python train_model.py
```

## Hasil evaluasi saat ini
- Stratified train-test split: 80% training dan 20% testing
- Test Accuracy: 99,88%
- Macro F1-Score: 99,85%
- 5-fold CV Accuracy: 99,92%

Angka evaluasi merupakan hasil dari dataset yang digunakan, bukan jaminan performa pada sumber air baru. Dataset tidak menyediakan identitas sumber air atau waktu pengambilan pada file ini. Label Safe/Unsafe mengikuti definisi dataset. Hasil prediksi bukan sertifikasi keamanan air dan tidak menggantikan pengujian laboratorium.
