import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="Financial Planning Calculator", layout="wide")
st.markdown("<h1 style='text-align: center; color: darkred;'>💼 Financial Planning & Retirement Calculator</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Expense Input", "🎯 Retirement Need", "📊 Investment Strategy"])

# ----------------------
# Tab 1: Expense Inputs
# ----------------------
with tab1:
    st.markdown("### 📌 Input Rincian Pengeluaran Bulanan dan Take Home Pay")

    # Integer-based input (no format string needed)
    take_home = st.number_input(
        "💰 Take Home Pay Bulanan (IDR)",
        value=40_000_000,
        step=100_000
    )

    st.markdown(f"""
    <div style='padding: 10px 0 20px 0;'>
    <p style='color:#0d47a1; font-size: 18px; margin: 0;'><strong>Take Home Pay Bulanan</strong></p>
    <h2 style='color:#0d47a1; font-size: 28px;'>Rp{take_home:,}</h2>
    </div>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([2, 1])

    st.markdown(f"""
    <div style='font-size: 24px; color: #0d47a1; margin-top: -10px; margin-bottom: 30px;'>
        <strong>Rp{take_home:,}</strong>
    </div>
    """, unsafe_allow_html=True)

    with left_col:
        st.subheader("📂 List Kebutuhan")
        kebutuhan_data = {
            "No": list(range(1, 15)),
            "List Kebutuhan": [
                "Sewa rumah atau cicilan KPR", "Listrik, air, dan gas", "Makanan pokok dan kebutuhan dapur",
                "Gaji PRT/ Baby Sitter/ Driver/ Satpam", "Transportasi (bensin, ongkos, servis kendaraan)",
                "Asuransi kesehatan dan jiwa", "Biaya pendidikan anak/ sendiri", "Biaya Les anak",
                "Jajan anak", "Tagihan telepon dan internet", "Obat-obatan", "Cicilan kartu kredit",
                "Iuran lingkungan", "Perlengkapan rumah tangga"
            ],
            "Nominal (IDR)": [
                8_000_000, 800_000, 3_000_000, 2_000_000, 1_500_000, 500_000,
                400_000, 500_000, 600_000, 200_000, 0, 0, 0, 3_000_000
            ]
        }
        df_kebutuhan = st.data_editor(pd.DataFrame(kebutuhan_data), num_rows="dynamic")

        st.subheader("🎈 List Keinginan")
        keinginan_data = {
            "No": list(range(1, 12)),
            "List Keinginan": [
                "Makan di luar", "Langganan hiburan", "Liburan", "Belanja non-esensial", "Gadget",
                "Hobi", "Gym", "Dekorasi rumah", "Tiket event", "Arisan", "Nongkrong"
            ],
            "Nominal (IDR)": [
                800_000, 250_000, 0, 0, 100_000, 0, 600_000, 500_000, 1_000_000, 2_000_000, 1_000_000
            ]
        }
        df_keinginan = st.data_editor(pd.DataFrame(keinginan_data), num_rows="dynamic")

    with right_col:
        total_kebutuhan = df_kebutuhan["Nominal (IDR)"].sum()
        total_keinginan = df_keinginan["Nominal (IDR)"].sum()
        pengeluaran_bulanan_input = total_kebutuhan + total_keinginan
        pengeluaran_tahunan_input = pengeluaran_bulanan_input * 12
        total_saving = 3_000_000
        total_outflow = pengeluaran_bulanan_input + total_saving
        surplus = take_home - total_outflow

        st.markdown(f"""
        <div style='border: 3px solid #1976d2; border-radius: 10px; padding: 20px; background-color: #e3f2fd; margin-bottom: 10px;'>
            <h3 style='color: #0d47a1;'>📌 Total Pengeluaran Bulanan: Rp{pengeluaran_bulanan_input:,.0f}</h3>
            <h3 style='color: #0d47a1;'>📌 Total Pengeluaran Tahunan: Rp{pengeluaran_tahunan_input:,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Total Kebutuhan", f"Rp{total_kebutuhan:,.0f}")
        st.metric("Total Keinginan", f"Rp{total_keinginan:,.0f}")
        st.metric("Total Saving", f"Rp{total_saving:,.0f}")
        st.metric("Surplus / Defisit", f"Rp{surplus:,.0f}", delta_color="inverse")

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie([total_kebutuhan, total_keinginan, total_saving],
               labels=["Kebutuhan", "Keinginan", "Saving"],
               autopct="%1.1f%%", startangle=90,
               wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
        ax.set_title("Proporsi Alokasi Bulanan", fontsize=10)
        st.pyplot(fig)

# ----------------------
# ----------------------
# Tab 2: Retirement Needs Projection
# ----------------------
with tab2:
    st.markdown("## 🎯 Target Dana Pensiun")

    # 1️⃣ Age inputs
    col1, col2, col3 = st.columns(3)
    usia_skrg    = col1.number_input("Usia saat ini", value=34,   min_value=18,  max_value=100)
    usia_pensiun = col2.number_input("Usia pensiun",   value=55,   min_value=usia_skrg+1, max_value=120)
    usia_meninggal = col3.number_input("Harapan hidup", value=75,  min_value=usia_pensiun+1, max_value=120)

    # Calculate periods
    masa_akumulasi = usia_pensiun - usia_skrg
    masa_pensiun   = usia_meninggal - usia_pensiun

    # Display them
    col4, col5 = st.columns(2)
    col4.markdown(f"🧓 Masa pensiun: **{masa_pensiun} tahun**")
    col5.markdown(f"📈 Masa akumulasi: **{masa_akumulasi} tahun**")

    st.markdown("---")

    # 2️⃣ Expense & PV/FV
    pengeluaran_bulanan = st.number_input(
        "Pengeluaran Lifestyle Bulanan Saat Ini (IDR)",
        value=6_250_000,
        step=100_000
    )
    pengeluaran_tahunan = pengeluaran_bulanan * 12
    st.markdown(f"📌 Pengeluaran Tahunan Saat Ini: **Rp{pengeluaran_tahunan:,.0f}**")

    persentase_pensiun = st.number_input(
        "Persentase Pengeluaran Saat Pensiun (%)",
        value=70, min_value=0, max_value=100
    ) / 100
    inflasi = st.number_input("Asumsi Inflasi hingga Pensiun (p.a)", value=5.0) / 100

    pengeluaran_pensiun_pv = pengeluaran_tahunan * persentase_pensiun
    pengeluaran_pensiun_fv = pengeluaran_pensiun_pv * ((1 + inflasi) ** masa_akumulasi)

    st.markdown(f"📌 Pengeluaran Tahunan di Masa Pensiun (PV): **Rp{pengeluaran_pensiun_pv:,.0f}**")
    st.markdown(f"📈 Nilai Masa Depan Pengeluaran (FV): **Rp{pengeluaran_pensiun_fv:,.0f}**")

    st.markdown("---")

    # 3️⃣ Draw‐down & PVAD (inflation only)
    inflasi_pensiun = st.number_input(
        "Asumsi Inflasi Saat Pensiun (% p.a)",
        value=5.0,
        step=0.1
    ) / 100

    # use inflation as the only “discount” rate
    discount_rate = -inflasi_pensiun
    st.markdown(f"📉 Tingkat diskon (inflasi) saat pensiun: **{discount_rate*100:.2f}%**")

    # compute PVAD
    if discount_rate == 0:
        pvad = pengeluaran_pensiun_fv * masa_pensiun
    else:
        annuity_due_factor = (
            (1 - (1 + discount_rate) ** -masa_pensiun)
            / discount_rate
        ) * (1 + discount_rate)
        pvad = pengeluaran_pensiun_fv * annuity_due_factor

    st.markdown(
        f"<div style='border:3px solid #d32f2f; padding:20px; "
        f"border-radius:8px; background-color:#ffecec; margin-top:20px;'>"
        f"<h4>📦 Jumlah total kapital yang dibutuhkan di awal pensiun:</h4>"
        f"<h2 style='color:#d32f2f;'>Rp{pvad:,.0f}</h2>"
        f"</div>",
        unsafe_allow_html=True
    )

# ----------------------
# Tab 3: Investment Strategy
# ----------------------
with tab3:
    st.markdown("## 💡 Strategi Investasi untuk Tutup Defisit")

    asset_data = {
        "Aset Investasi": ["Tabungan", "Deposito", "Reksa Dana Pasar Uang", "Reksa Dana Pendapatan Tetap", "Reksa Dana Saham", "Emas"],
        "Imbal Hasil (p.a)": [0.5, 2.0, 5.0, 6.0, 9.0, 8.0],
        "Nominal Saat Ini": [100_000_000, 0, 0, 50_000_000, 0, 100_000_000]
    }
    df_assets = st.data_editor(pd.DataFrame(asset_data), num_rows="fixed")

    df_assets["Proyeksi Saat Pensiun"] = df_assets.apply(
        lambda row: row["Nominal Saat Ini"] * ((1 + row["Imbal Hasil (p.a)"] / 100) ** masa_akumulasi),
        axis=1
    )
    total_fv = df_assets["Proyeksi Saat Pensiun"].sum()

    st.dataframe(df_assets.style.format({
        "Nominal Saat Ini": "Rp{:,.0f}",
        "Proyeksi Saat Pensiun": "Rp{:,.0f}"
    }))

    deficit = max(pvad - total_fv, 0)
    st.markdown(
        f"<div style='border:3px solid #f57c00;padding:20px;border-radius:10px;margin:20px 0;background-color:#fff3e0;'>"
        f"<h4>❗ Defisit yang harus dialokasikan:</h4>"
        f"<h2 style='color:#f57c00;'>Rp{deficit:,.0f}</h2>"
        f"</div>",
        unsafe_allow_html=True
    )

    st.markdown("### 📊 Simulasi Alokasi Investasi Bulanan")

    alloc_data = {
        "Aset": ["Deposito", "Reksa Dana Pasar Uang", "Reksa Dana Pendapatan Tetap", "Reksa Dana Saham", "Emas"],
        "Imbal Hasil (%)": [2.0, 5.0, 6.0, 9.0, 8.0],
        "Alokasi (%)": [20, 20, 20, 20, 20]
    }
    df_alloc = st.data_editor(pd.DataFrame(alloc_data), num_rows="fixed")

    if df_alloc["Alokasi (%)"].sum() != 100:
        st.error("❌ Total alokasi harus 100%")
    else:
        weighted_return = np.dot(df_alloc["Imbal Hasil (%)"], df_alloc["Alokasi (%)"]) / 100
        r_monthly = weighted_return / 100 / 12
        n_months = masa_akumulasi * 12
        pmt = deficit / n_months if r_monthly == 0 else (deficit * r_monthly) / (((1 + r_monthly) ** n_months - 1) * (1 + r_monthly))

        st.markdown(
            f"<div style='border:3px solid #388e3c;padding:20px;border-radius:10px;margin:20px 0;background-color:#e8f5e9;'>"
            f"<h4>✅ Dengan return gabungan {weighted_return:.2f}%, Anda perlu menabung:</h4>"
            f"<h2 style='color:#388e3c;'>Rp{pmt:,.0f} / bulan</h2>"
            f"</div>",
            unsafe_allow_html=True
        )
