
import streamlit as st
import pandas as pd
import joblib
import json
import matplotlib.pyplot as plt

from pathlib import Path
from datetime import datetime

# ==================================================
# 1. KONFIGURASI
# ==================================================

st.set_page_config(
    page_title="AquaCheck",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "model_aquacheck.pkl"
METRICS_PATH = BASE_DIR / "model" / "evaluation_metrics.json"
DATASET_PATH = BASE_DIR / "dataset" / "water_potability.csv"

try:
    model = joblib.load(MODEL_PATH)
    data = pd.read_csv(DATASET_PATH)
    with open(METRICS_PATH, "r", encoding="utf-8") as file:
        evaluation = json.load(file)
except Exception as e:
    st.error(f"Gagal memuat model atau dataset: {e}")
    st.stop()

# ==================================================
# 2. SESSION STATE
# ==================================================

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# ==================================================
# 3. WARNA
# ==================================================

PLUM = "#59294D"
DARK = "#30212D"
CREAM = "#F5F1E9"
PINK = "#D8B8CF"
MUTED = "#887984"
WHITE = "#FFFFFF"

# ==================================================
# 4. CSS DESAIN
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700;800&display=swap');

:root {
  --sage: #BBD394;
  --sage-dark: #9FBD73;
  --paper: #FFFDF7;
  --ink: #252321;
  --pink: #F4B8CB;
  --blue: #B9E1E7;
  --line: #E8E4D8;
  --muted: #77716B;
  --plum: #59294D;
}
.stApp {
  background: var(--sage);
  color: var(--ink);
  font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }
.main .block-container {
  max-width: 1440px;
  padding: 1.15rem 2rem 2.5rem;
}
h1,h2,h3,h4 {
  color: var(--ink) !important;
  font-family: 'Playfair Display', Georgia, serif !important;
  letter-spacing: -0.6px;
}
p, label, .stCaption { color: #625D57; }
.eyebrow {
  color: #82786F; font-size: 9px; font-weight: 700;
  letter-spacing: 2px; margin: 0 0 7px; text-transform: uppercase;
}
.main-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(34px, 4vw, 54px); font-weight: 800;
  color: var(--ink); line-height: 1.04; letter-spacing: -1.8px;
}
.subtitle { color: #746D66; font-size: 13px; margin: 8px 0 22px; }
.brand {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 28px; color: var(--ink); font-weight: 800;
  letter-spacing: -1.5px;
}
.topnav {
  background: var(--paper); border: 1px solid #D9D4C7;
  border-radius: 13px; padding: 10px 16px; margin-bottom: 20px;
}
.hero-paper {
  background-color: var(--paper);
  background-image:
    linear-gradient(rgba(90,82,70,.075) 1px, transparent 1px),
    linear-gradient(90deg, rgba(90,82,70,.075) 1px, transparent 1px);
  background-size: 22px 22px;
  border: 1px solid #D9D4C7; border-radius: 15px;
  padding: clamp(24px, 5vw, 66px) 24px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center; margin: 4px 0 20px;
}
.hero-kicker {
  font-size: 9px; letter-spacing: 2px; font-weight: 700;
  color: #82786F; text-transform: uppercase;
}
.hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(36px, 5.5vw, 68px); font-weight: 800;
  letter-spacing: -2.4px; line-height: .98; color: var(--ink);
  margin: 12px auto; max-width: 850px; width: 100%; text-align: center;
}
.hero-title span { background: linear-gradient(transparent 62%, #F4B8CB 62%); }
.hero-sub {
  font-size: 12px; color: #6F6962; max-width: 520px;
  margin: 15px auto 0; line-height: 1.7;
}
.paper-info-card {
  background-color: var(--paper);
  background-image:
    linear-gradient(rgba(90,82,70,.075) 1px, transparent 1px),
    linear-gradient(90deg, rgba(90,82,70,.075) 1px, transparent 1px);
  background-size: 22px 22px;
  border: 1px solid #D9D4C7;
  border-radius: 15px;
  padding: 25px 27px;
  height: 100%;
  box-sizing: border-box;
  color: var(--ink);
}
.paper-info-card p {
  color: #625D57;
  font-size: 12px;
  line-height: 1.75;
  margin: 10px 0 0;
}
.paper-info-card .panel-title {
  margin: 5px 0 9px;
  line-height: 1.2;
}
.pink-highlight {
  display: inline;
  padding: 0 .12em .04em;
  background: linear-gradient(transparent 56%, var(--pink) 56%);
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
.ticker {
  background: var(--sage-dark); color: #293020;
  border-top: 1px solid #91AE68; border-bottom: 1px solid #91AE68;
  padding: 8px 12px; margin: 16px -2rem 22px;
  font-size: 9px; font-weight: 700; letter-spacing: 1.8px;
  text-align: center; text-transform: uppercase;
}
.stat-card, .stat-card-dark {
  border-radius: 13px; padding: 18px 19px; min-height: 126px;
  box-sizing: border-box; border: 1px solid #E8E1D5;
}
.stat-card { background: #fff; }
.stat-card-dark { background: var(--pink); border-color: #E9A8BE; }
.stat-label { font-size: 10px; color: #746B65; font-weight: 700; letter-spacing: .8px; }
.stat-value {
  font-family: 'Playfair Display', Georgia, serif; font-size: 39px;
  font-weight: 800; letter-spacing: -1.8px; color: var(--ink);
  margin-top: 9px; line-height: 1.1;
}
.stat-note { font-size: 10px; color: #746B65; margin-top: 8px; }
.stat-card-dark .stat-label, .stat-card-dark .stat-note { color: #57434A; }
.panel-title {
  font-family: 'Playfair Display', Georgia, serif; font-size: 22px;
  font-weight: 700; color: var(--ink);
}
.panel-description { color: #817970; font-size: 11px; margin: 4px 0 14px; }
div[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--paper); border: 1px solid #E5DFD2;
  border-radius: 14px; padding: 10px;
}
div[data-testid="stForm"] {
  background: var(--paper); border: 1px solid #E5DFD2;
  border-radius: 14px; padding: 24px;
}
.stButton > button {
  background: #fff; color: #39332F; border: 1px solid #DCD6C9;
  border-radius: 999px; text-align: center; font-size: 11px;
  font-weight: 700; min-height: 37px; padding: 7px 13px;
  transition: all .18s ease;
}
.stButton > button:hover {
  background: var(--pink); color: var(--ink); border-color: var(--pink);
}
.stButton > button[kind="primary"] {
  background: var(--ink); color: #fff !important; border-color: var(--ink);
  box-shadow: none;
}
.stButton > button[kind="primary"] *,
.stButton > button[aria-pressed="true"],
.stButton > button:focus,
.stButton > button:focus-visible {
  color: #fff !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[aria-pressed="true"]:hover {
  color: #fff !important;
}
.stButton > button[kind="primary"]:hover {
  background: var(--plum); color: #fff; border-color: var(--plum);
}
.stFormSubmitButton > button, .stDownloadButton > button {
  background: var(--ink); color: #fff; border: 0;
  border-radius: 999px; min-height: 43px; font-weight: 700;
  font-family: 'DM Sans', sans-serif; font-size: 11px;
  letter-spacing: 0; text-transform: none;
}
.stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
  background: var(--plum); color: #fff; border: 0;
}
div[data-testid="stMetric"] {
  background: #fff; border: 1px solid var(--line);
  border-radius: 13px; padding: 15px;
}
div[data-testid="stMetricValue"] { color: var(--ink); }
div[data-testid="stMetricLabel"] { color: #746B65; }
[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 11px; }
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"] {
  border-radius: 9px;
}
.stAlert { border-radius: 12px; }
hr { border-color: #D9D4C7; }
footer, #MainMenu { visibility: hidden; }
@media (max-width: 800px) {
  .main .block-container { padding: .7rem .8rem 2rem; }
  .ticker { margin-left: -.8rem; margin-right: -.8rem; }
}
</style>
""", unsafe_allow_html=True)



# ==================================================
# 5. FUNGSI UMUM
# ==================================================

def header(kategori, judul, deskripsi):
    st.markdown(
        f'<div class="eyebrow">{kategori}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="main-title">{judul}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="subtitle">{deskripsi}</div>',
        unsafe_allow_html=True
    )


def stat_card(label, value, note, dark=False):
    class_name = "stat-card-dark" if dark else "stat-card"

    st.markdown(f"""
    <div class="{class_name}">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def buat_pie_chart():
    jumlah = data["Potability"].value_counts().reindex(
        [0, 1], fill_value=0
    )

    fig, ax = plt.subplots(figsize=(5, 3.5))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    wedges, texts, autotexts = ax.pie(
        jumlah.values,
        labels=["Tidak Layak", "Layak"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#59294D", "#D8B8CF"],
        wedgeprops={
            "width": 0.42,
            "edgecolor": "#FFFFFF",
            "linewidth": 3
        },
        pctdistance=0.78,
        textprops={"fontsize": 9}
    )

    for text in autotexts:
        text.set_color("#30212D")
        text.set_fontweight("bold")

    ax.set_title(
        "Water Potability Distribution",
        fontsize=12,
        color="#30212D",
        pad=15
    )

    fig.tight_layout()
    return fig, jumlah


def buat_histogram(parameter):
    nilai = data[parameter].dropna()
    nama_parameter = "Organic Carbon" if parameter == "Organic_carbon" else parameter

    fig, ax = plt.subplots(figsize=(5, 3.5))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    ax.hist(
        nilai,
        bins=25,
        color="#8C527D",
        edgecolor="#FFFFFF",
        linewidth=1
    )

    ax.set_title(
        f"Distribution of {nama_parameter}",
        fontsize=12,
        color="#30212D",
        pad=15
    )
    ax.set_xlabel(nama_parameter, fontsize=9)
    ax.set_ylabel("Number of Samples", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#EAE3D9")
    ax.spines["bottom"].set_color("#EAE3D9")
    ax.tick_params(labelsize=8, colors="#887984")
    ax.grid(axis="y", alpha=0.15)
    fig.tight_layout()
    return fig


# ==================================================
# 6. NAVIGASI UTAMA
# ==================================================

nav_cols = st.columns([1.35, 1, 1.25, 1.15, 1.05], gap="small")
with nav_cols[0]:
    st.markdown('<div class="brand">aqua<span style="color:#8DAE62">check.</span></div><div style="font-size:8px;letter-spacing:1.7px;color:#81786E;font-weight:700">WATER QUALITY LAB</div>', unsafe_allow_html=True)

menu_items = [
    ("Dashboard", "Overview"),
    ("Prediksi Kualitas Air", "New test"),
    ("Riwayat Prediksi", "History"),
    ("Tentang Model", "Our model")
]
for i, (nama_menu, label_menu) in enumerate(menu_items, start=1):
    with nav_cols[i]:
        if st.button(label_menu, key=f"nav_{nama_menu}", use_container_width=True,
                     type="primary" if st.session_state.menu == nama_menu else "secondary"):
            st.session_state.menu = nama_menu
            st.rerun()

# ==================================================
# 7. DASHBOARD
# ==================================================

if st.session_state.menu == "Dashboard":

    total_data = len(data)
    total_parameter = len(data.columns) - 1
    total_prediksi = len(st.session_state.riwayat)
    jumlah = data["Potability"].value_counts().reindex([0, 1], fill_value=0)

    st.markdown("""
    <section class="hero-paper">
      <div class="hero-kicker">AQUACHECK · WATER QUALITY MONITORING</div>
      <div class="hero-title">Know your water.<br><span>Understand its quality.</span></div>
    </section>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ticker">MONITOR WATER QUALITY ✳  EXPLORE DATA ✳  PREDICT WITH MACHINE LEARNING ✳  MONITOR WATER QUALITY</div>', unsafe_allow_html=True)

    # AQUACHECK AT A GLANCE
    st.markdown('<div class="eyebrow">AQUACHECK AT A GLANCE</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-title" style="font-size:27px;margin-bottom:14px">A little insight goes a long way.</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        stat_card("TOTAL DATASET", f"{total_data:,}".replace(",", "."), "Sampel kualitas air", dark=True)
    with col2:
        stat_card("WATER PARAMETERS", f"{total_parameter:02d}", "Fitur untuk klasifikasi")
    with col3:
        stat_card("MODEL ACCURACY", f"{evaluation['accuracy'] * 100:.2f}%".replace(".", ","), "Evaluasi data pengujian")
    with col4:
        stat_card("TOTAL PREDICTIONS", str(total_prediksi), "Prediksi pada sesi ini")

    # GET TO KNOW AQUACHECK
    st.write("")
    st.write("")
    st.markdown('<div class="eyebrow">GET TO KNOW AQUACHECK</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-title" style="font-size:27px;margin-bottom:14px">A little more about the water we use.</div>', unsafe_allow_html=True)

    st.markdown("""
    <section class="paper-info-card" style="margin-bottom:16px">
      <div class="panel-title"><span class="pink-highlight">A clearer way to understand water quality.</span></div>
      <p>AquaCheck adalah aplikasi berbasis Machine Learning yang membantu menganalisis potabilitas atau kelayakan air melalui sembilan parameter kualitas air. Aplikasi ini menyajikan data dataset, visualisasi distribusi parameter, serta hasil klasifikasi dari data yang dimasukkan pengguna.</p>
      <p>Dengan tampilan yang terintegrasi, pengguna dapat mengenali karakteristik data kualitas air, mencoba prediksi berdasarkan nilai parameter, dan meninjau kembali hasil prediksi melalui halaman riwayat.</p>
    </section>
    """, unsafe_allow_html=True)

    info1, info2, info3 = st.columns(3, gap="medium")
    with info1:
        st.markdown("""
        <section class="paper-info-card">
          <div class="eyebrow">01 · EXPLORE</div>
          <div class="panel-title"><span class="pink-highlight">Explore the dataset</span></div>
          <p>Dataset Water Potability menjadi sumber data untuk melihat distribusi sampel air dalam kategori layak dan tidak layak.</p>
        </section>
        """, unsafe_allow_html=True)
    with info2:
        st.markdown("""
        <section class="paper-info-card">
          <div class="eyebrow">02 · ANALYZE</div>
          <div class="panel-title"><span class="pink-highlight">Analyze 9 parameters</span></div>
          <p>Sembilan indikator yang dianalisis meliputi pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic Carbon, Trihalomethanes, dan Turbidity.</p>
        </section>
        """, unsafe_allow_html=True)
    with info3:
        st.markdown("""
        <section class="paper-info-card">
          <div class="eyebrow">03 · PREDICT</div>
          <div class="panel-title"><span class="pink-highlight">Understand the result</span></div>
          <p>Model klasifikasi terpilih mengolah sembilan parameter kualitas air dan menghasilkan prediksi air layak atau tidak layak minum.</p>
        </section>
        """, unsafe_allow_html=True)

    # EXPLORE THE DATA
    st.write("")
    st.write("")
    st.markdown('<div class="eyebrow">EXPLORE THE DATA</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-title" style="font-size:27px;margin-bottom:14px">What does the dataset tell us?</div>', unsafe_allow_html=True)

    left, right = st.columns([1.05, 1.45], gap="medium")
    with left:
        with st.container(border=True):
            st.markdown('<div class="eyebrow">POTABILITY OVERVIEW</div><div class="panel-title">Water potability</div><div class="panel-description">Komposisi sampel berdasarkan kategori kelayakan air.</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(5, 3.4))
            fig.patch.set_facecolor("#FFFDF7")
            ax.set_facecolor("#FFFDF7")
            _, _, autotexts = ax.pie(
                jumlah.values,
                labels=["Tidak Layak", "Layak"],
                autopct="%1.1f%%",
                startangle=90,
                colors=["#F4B8CB", "#BBD394"],
                wedgeprops={"width": 0.40, "edgecolor": "#FFFDF7", "linewidth": 3},
                pctdistance=0.78,
                textprops={"fontsize": 9, "color": "#514A43"}
            )
            for t in autotexts:
                t.set_color("#252321")
                t.set_fontweight("bold")
            ax.text(0, 0, f"{total_data:,}".replace(",", "."), ha="center", va="center", fontsize=19, fontweight="bold", color="#252321")
            ax.text(0, -0.16, "TOTAL SAMPLES", ha="center", va="center", fontsize=7, color="#817970")
            ax.axis("equal")
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            c1, c2 = st.columns(2)
            c1.caption(f"● Tidak layak: {jumlah[0]:,}".replace(",", "."))
            c2.caption(f"● Layak: {jumlah[1]:,}".replace(",", "."))

    with right:
        with st.container(border=True):
            st.markdown('<div class="eyebrow">PARAMETER DISTRIBUTION</div><div class="panel-title">Explore water indicators</div><div class="panel-description">Pilih salah satu dari sembilan parameter untuk melihat persebaran nilainya.</div>', unsafe_allow_html=True)
            parameter_chart = st.selectbox(
                "Pilih parameter kualitas air",
                ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"],
                format_func=lambda x: "Organic Carbon" if x == "Organic_carbon" else x,
                key="pilihan_chart"
            )
            fig = buat_histogram(parameter_chart)
            fig.set_facecolor("#FFFDF7")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    # START WATER PREDICTION
    st.write("")
    st.write("")
    st.write("")
    if st.button("Start Water Prediction  →", key="mulai_prediksi", type="primary", use_container_width=True):
        st.session_state.menu = "Prediksi Kualitas Air"
        st.rerun()

elif st.session_state.menu == "Prediksi Kualitas Air":

    header(
        "PREDICTION / NEW TEST",
        "Prediksi Kualitas Air",
        "Lengkapi data responden dan parameter untuk melakukan prediksi."
    )

    with st.form("form_prediksi"):

        st.markdown("### 01. Data Responden")
        st.caption("Informasi identitas pengisi formulir.")

        nama = st.text_input(
            "Nama Lengkap *",
            placeholder="Masukkan nama lengkap"
        )

        col1, col2 = st.columns(2)

        with col1:
            tahun = st.number_input(
                "Tahun Kelahiran *",
                min_value=1900,
                max_value=datetime.now().year,
                value=2003,
                step=1
            )

        with col2:
            gender = st.selectbox(
                "Jenis Kelamin *",
                [
                    "Pilih jenis kelamin",
                    "Laki-laki",
                    "Perempuan"
                ]
            )

        username_x = st.text_input(
            "Username X (Opsional)",
            placeholder="@username"
        )

        st.divider()

        st.markdown("### 02. Parameter Kualitas Air")
        st.caption(
            "Masukkan nilai dari sembilan parameter kualitas air."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            ph = st.number_input(
                "pH",
                min_value=0.0,
                max_value=14.0,
                value=7.04,
                step=0.01
            )

            hardness = st.number_input(
                "Hardness",
                min_value=0.0,
                value=196.97,
                step=0.01
            )

            solids = st.number_input(
                "Solids",
                min_value=0.0,
                value=22014.09,
                step=0.01
            )

        with col2:
            chloramines = st.number_input(
                "Chloramines",
                min_value=0.0,
                value=7.13,
                step=0.01
            )

            sulfate = st.number_input(
                "Sulfate",
                min_value=0.0,
                value=333.07,
                step=0.01
            )

            conductivity = st.number_input(
                "Conductivity",
                min_value=0.0,
                value=421.88,
                step=0.01
            )

        with col3:
            organic_carbon = st.number_input(
                "Organic Carbon",
                min_value=0.0,
                value=14.28,
                step=0.01
            )

            trihalomethanes = st.number_input(
                "Trihalomethanes",
                min_value=0.0,
                value=66.62,
                step=0.01
            )

            turbidity = st.number_input(
                "Turbidity",
                min_value=0.0,
                value=3.95,
                step=0.01
            )

        st.write("")

        submit = st.form_submit_button(
            "Prediksi Kualitas Air",
            use_container_width=True
        )

    if submit:

        if not nama.strip():
            st.error("Nama lengkap wajib diisi.")

        elif gender == "Pilih jenis kelamin":
            st.error("Silakan pilih jenis kelamin.")

        else:

            input_data = pd.DataFrame([{
                "ph": ph,
                "Hardness": hardness,
                "Solids": solids,
                "Chloramines": chloramines,
                "Sulfate": sulfate,
                "Conductivity": conductivity,
                "Organic_carbon": organic_carbon,
                "Trihalomethanes": trihalomethanes,
                "Turbidity": turbidity
            }])

            try:

                hasil = int(model.predict(input_data)[0])

                kategori = (
                    "Air Layak Minum"
                    if hasil == 1
                    else "Air Tidak Layak Minum"
                )

                waktu = datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )

                st.session_state.riwayat.insert(0, {
                    "Waktu": waktu,
                    "Nama": nama.strip(),
                    "Tahun Kelahiran": int(tahun),
                    "Jenis Kelamin": gender,
                    "Username X": username_x.strip(),
                    "Hasil Prediksi": kategori
                })

                st.divider()
                st.markdown("### 03. Hasil Prediksi")

                st.write(f"Responden: **{nama.strip()}**")

                if hasil == 1:
                    st.success("HASIL PREDIKSI: AIR LAYAK MINUM")
                    st.write(
                        "Model mengklasifikasikan sampel air "
                        "ke dalam kategori layak minum."
                    )

                else:
                    st.error("HASIL PREDIKSI: AIR TIDAK LAYAK MINUM")
                    st.write(
                        "Model mengklasifikasikan sampel air "
                        "ke dalam kategori tidak layak minum."
                    )

                st.caption(
                    "Hasil ini merupakan prediksi model untuk "
                    "keperluan pembelajaran, bukan sertifikasi "
                    "keamanan air minum. Pengujian laboratorium "
                    "tetap diperlukan."
                )

            except Exception as e:
                st.error(f"Terjadi kesalahan saat prediksi: {e}")


# ==================================================
# 9. HALAMAN RIWAYAT
# ==================================================

elif st.session_state.menu == "Riwayat Prediksi":

    header(
        "PREDICTION / HISTORY",
        "Riwayat Prediksi",
        "Daftar hasil prediksi yang dilakukan selama sesi aplikasi."
    )

    if st.session_state.riwayat:

        riwayat = pd.DataFrame(st.session_state.riwayat)

        st.metric(
            "Total Prediksi",
            len(riwayat)
        )

        with st.container(border=True):

            st.markdown("### Prediction History")

            st.dataframe(
                riwayat,
                use_container_width=True,
                hide_index=True
            )

            csv = riwayat.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "Unduh Riwayat CSV",
                data=csv,
                file_name="riwayat_aquacheck.csv",
                mime="text/csv"
            )

        if st.button("Hapus Semua Riwayat"):
            st.session_state.riwayat = []
            st.rerun()

    else:

        with st.container(border=True):
            st.markdown("### Belum Ada Riwayat")
            st.info(
                "Silakan lakukan prediksi terlebih dahulu. "
                "Hasil prediksi akan ditampilkan di halaman ini."
            )


# ==================================================
# 10. HALAMAN TENTANG MODEL
# ==================================================

elif st.session_state.menu == "Tentang Model":

    header(
        "INFORMATION / MACHINE LEARNING",
        "Tentang Model",
        "Informasi algoritma dan evaluasi model AquaCheck."
    )

    algorithm_name = evaluation["selected_algorithm"]
    classifier = model.named_steps["classifier"]

    with st.container(border=True):
        st.markdown(f"### {algorithm_name}")
        st.write(
            "Model terbaik dipilih setelah membandingkan lima algoritma klasifikasi "
            "pada pembagian data training dan testing yang sama. Pemilihan model "
            "memprioritaskan Macro F1-Score agar performa pada kedua kelas ikut "
            "dipertimbangkan, bukan hanya akurasi. Nilai kosong pada dataset "
            "ditangani menggunakan median melalui SimpleImputer."
        )

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Accuracy", f"{evaluation['accuracy'] * 100:.2f}%")
    metric2.metric("Macro F1-Score", f"{evaluation['macro_f1'] * 100:.2f}%")
    metric3.metric("Macro Precision", f"{evaluation['precision_macro'] * 100:.2f}%")

    left_eval, right_eval = st.columns(2, gap="medium")
    with left_eval:
        with st.container(border=True):
            st.markdown("### Perbandingan Algoritma")
            comparison = pd.DataFrame(evaluation["comparison"])
            comparison["Accuracy (%)"] = comparison["accuracy"] * 100
            comparison["Macro F1 (%)"] = comparison["macro_f1"] * 100
            comparison_view = comparison[["algorithm", "Accuracy (%)", "Macro F1 (%)"]].rename(columns={"algorithm": "Algoritma"})
            st.dataframe(
                comparison_view.style.format({"Accuracy (%)": "{:.2f}", "Macro F1 (%)": "{:.2f}"}),
                use_container_width=True, hide_index=True
            )
            st.caption("Semua algoritma diuji pada data testing yang sama (20%).")

    with right_eval:
        with st.container(border=True):
            st.markdown("### Confusion Matrix")
            cm = evaluation["confusion_matrix"]
            cm_df = pd.DataFrame(
                cm,
                index=["Aktual: Tidak Layak", "Aktual: Layak"],
                columns=["Prediksi: Tidak Layak", "Prediksi: Layak"]
            )
            st.dataframe(cm_df, use_container_width=True)
            st.caption("Baris menunjukkan kelas aktual, kolom menunjukkan hasil prediksi.")

    with st.container(border=True):
        st.markdown("### Konfigurasi dan Data Pengujian")
        st.write(f"**Algoritma terpilih:** {algorithm_name}")
        st.write(f"**Dataset:** Water Potability ({evaluation['dataset_rows']:,} data)".replace(",", "."))
        st.write("**Pembagian Data:** 80% training / 20% testing")
        st.write(f"**Jumlah data training:** {evaluation['training_rows']:,}".replace(",", "."))
        st.write(f"**Jumlah data testing:** {evaluation['testing_rows']:,}".replace(",", "."))
        st.write(f"**Random State:** {evaluation['random_state']}")
        st.write("**Preprocessing:** Median Imputation")

    st.caption(
        "Metrik dihitung dari data testing yang tidak digunakan saat pelatihan "
        "awal (stratified split 80:20). Setelah evaluasi, model terpilih dilatih "
        "ulang menggunakan seluruh dataset untuk digunakan pada aplikasi. "
        "Hasil prediksi AquaCheck merupakan estimasi berbasis dataset, bukan "
        "pengganti pengujian laboratorium kualitas air."
    )

# ==================================================
# 11. FOOTER
# ==================================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#625D57;
    font-size:12px;
    padding:12px;">
    AquaCheck · Water Quality Lab<br>
    Explore · Analyze · Predict
</div>
""", unsafe_allow_html=True)
