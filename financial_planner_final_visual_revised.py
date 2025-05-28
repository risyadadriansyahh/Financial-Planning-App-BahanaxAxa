
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Financial Planning Calculator", layout="wide")
st.markdown("<h1 style='text-align: center; color: darkred;'>💼 Financial Planning & Retirement Calculator</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Expense Input", "🎯 Retirement Need", "📊 Investment Strategy"])

# ----------------------
# Tab 1: Expense Inputs
# ----------------------
with tab1:
    st.markdown("### 📌 Input Rincian Pengeluaran Bulanan dan Take Home Pay")
    take_home = st.number_input("💰 Take Home Pay Bulanan (IDR)", value=40_000_000, step=100_000)

    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.subheader("📂 List Kebutuhan")
        kebutuhan_data = {
            "No": list(range(1, 15)),
            "List Kebutuhan": [
                "Sewa rumah atau cicilan KPR", "Listrik, air, dan gas", "Makanan pokok dan kebutuhan dapur",
                "Gaji PRT/ Baby Sitter/ Driver/ Satpam", "Transportasi (bensin, ongkos, servis kendaraan)",
                "Asuransi kesehatan dan jiwa", "Biaya pendidikan anak/ sendiri", "Biaya Les anak",
                "Jajan anak", "Tagihan telepon dan internet (untuk keperluan kerja/sekolah)",
                "Obat-obatan dan perawatan kesehatan dasar", "Cicilan kartu kredit atau pinjaman",
                "Iuran lingkungan", "Perlengkapan rumah tangga dasar (sabun, deterjen, dll.)"
            ],
            "Nominal (IDR)": [
                8000000, 800000, 3000000, 2000000, 1500000, 500000, 400000, 500000,
                600000, 200000, 0, 0, 0, 3000000
            ]
        }
        df_kebutuhan = st.data_editor(pd.DataFrame(kebutuhan_data), num_rows="fixed")

        st.subheader("🎈 List Keinginan")
        keinginan_data = {
            "No": list(range(1, 12)),
            "List Keinginan": [
                "Makan di luar atau pesan makanan online", "Langganan hiburan (Netflix, Spotify, dll.)",
                "Liburan dan jalan-jalan", "Belanja pakaian, sepatu dan aksesoris non-esensial",
                "Gadget terbaru atau upgrade perangkat", "Hobi (game, alat musik, koleksi, dll.)",
                "Keanggotaan gym atau kelas olahraga", "Dekorasi rumah", "Tiket konser, bioskop, atau event lainnya",
                "Arisan", "Nongkrong di kafe"
            ],
            "Nominal (IDR)": [
                800000, 250000, 0, 0, 100000, 0, 600000, 500000, 1000000, 2000000, 1000000
            ]
        }
        df_keinginan = st.data_editor(pd.DataFrame(keinginan_data), num_rows="fixed")

        st.subheader("💾 List Saving")
        saving_data = {
            "No": [1, 2, 3],
            "List Saving": ["Tabung/Cicil Emas", "Reksadana, Obligasi, Saham", "Dana pensiun"],
            "Nominal (IDR)": [3000000, 0, 0]
        }
        df_saving = st.data_editor(pd.DataFrame(saving_data), num_rows="fixed")

    with right_col:
        total_kebutuhan = df_kebutuhan["Nominal (IDR)"].sum()
        total_keinginan = df_keinginan["Nominal (IDR)"].sum()
        total_saving = df_saving["Nominal (IDR)"].sum()
        total_outflow = total_kebutuhan + total_keinginan + total_saving
        surplus = take_home - total_outflow

        st.markdown("### 🔢 Ringkasan Alokasi")
        st.metric("Total Kebutuhan", f"Rp{total_kebutuhan:,.0f}")
        st.metric("Total Keinginan", f"Rp{total_keinginan:,.0f}")
        st.metric("Total Saving", f"Rp{total_saving:,.0f}")
        st.metric("Surplus / Defisit", f"Rp{surplus:,.0f}", delta_color="inverse")

        st.markdown("### 📊 Diagram Alokasi")
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie(
            [total_kebutuhan, total_keinginan, total_saving],
            labels=["Kebutuhan", "Keinginan", "Saving"],
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )
        ax.set_title("Proporsi Alokasi Bulanan", fontsize=10)
        st.pyplot(fig)

# ----------------------
# Tab 2: Retirement Needs Projection
# ----------------------
with tab2:
    st.markdown("<h3 style='color: darkred;'>🧮 Kalkulasi Dana Pensiun</h3>", unsafe_allow_html=True)
    st.markdown("### 🎯 Target: Waktu pensiun nanti mau punya **life-style yang sama dengan saat ini**")

    st.subheader("🧾 Profil")
    col1, col2, col3, col4 = st.columns(4)
    usia_skrg = col1.number_input("Usia saat ini", value=34)
    usia_pensiun = col2.number_input("Usia pensiun yang diinginkan", value=55)
    usia_meninggal = col3.number_input("Harapan hidup", value=75)
    masa_pensiun = usia_meninggal - usia_pensiun
    col4.markdown(f"### 🧓 Masa pensiun: **{masa_pensiun} tahun**")

    st.divider()
    monthly_lifestyle = total_keinginan  # Linked to "List Keinginan"
    yearly_lifestyle = monthly_lifestyle * 12
    st.write(f"📌 Pengeluaran bulanan saat ini (dari List Keinginan): **Rp{monthly_lifestyle:,.0f}**")
    st.write(f"📌 Pengeluaran tahunan saat ini: **Rp{yearly_lifestyle:,.0f}**")

    st.divider()
    target_pengeluaran = st.number_input("Persentase pengeluaran saat pensiun (%)", value=70) / 100
    pengeluaran_pensiun_pv = yearly_lifestyle * target_pengeluaran
    st.write(f"➡️ Pengeluaran tahunan yang diinginkan saat pensiun: **Rp{pengeluaran_pensiun_pv:,.0f}**")

    tahun_sisa = usia_pensiun - usia_skrg
    inflasi = st.number_input("Asumsi tingkat inflasi tahunan (%)", value=5.0) / 100
    pengeluaran_pensiun_fv = pengeluaran_pensiun_pv * ((1 + inflasi) ** tahun_sisa)
    st.write(f"📈 Nilai masa depan pengeluaran pensiun (FV): **Rp{pengeluaran_pensiun_fv:,.0f}**")

    st.divider()
    col1, col2 = st.columns(2)
    inflasi_pensiun = col1.number_input("Asumsi inflasi saat pensiun (%)", value=5.0) / 100
    return_pensiun = col2.number_input("Asumsi return investasi saat pensiun (%)", value=0.0) / 100
    real_return = ((1 + return_pensiun) / (1 + inflasi_pensiun)) - 1

    st.markdown(f"📉 Tingkat pengembalian riil selama pensiun: **{real_return*100:.2f}%**")

    st.write(f"PMT (pengeluaran tahun pertama pensiun): **Rp{pengeluaran_pensiun_fv:,.0f}**")
    if real_return == 0:
        pvad = pengeluaran_pensiun_fv * masa_pensiun
    else:
        pvad = pengeluaran_pensiun_fv * (((1 - (1 + real_return) ** -masa_pensiun) / real_return) * (1 + real_return))

    st.markdown(f'''
    <div style="padding: 15px; border: 2px solid #c0392b; border-radius: 10px; background-color: #fef6f5;">
        <h4 style="color:#c0392b;">📦 Jumlah total kapital yang dibutuhkan saat pensiun:</h4>
        <p style="font-size: 20px; font-weight: bold; color: #000;">Rp{pvad:,.0f}</p>
        <p style="font-style: italic; color: #555;">Arti dari angka ini adalah: di masa pensiun, Anda harus memiliki uang sebanyak <b>Rp{pvad:,.0f}</b> untuk hidup nyaman sesuai target lifestyle saat ini.</p>
    </div>
    ''', unsafe_allow_html=True)

# ----------------------
# Tab 3: Investment Strategy
# ----------------------
with tab3:
    st.markdown("## 💰 Saat ini udah punya tabungan apa aja nih?")
    st.markdown("#### (Dikurangi semua dana yang dimiliki)")

    asset_data = {
        "Aset Investasi": [
            "Tabungan", "Tabungan/Deposito", "Reksadana Pasar Uang",
            "Reksadana Pendapatan Tetap", "Reksadana Saham", "Emas"
        ],
        "Asumsi Imbal Hasil (p.a)": [0.5, 2.0, 5.0, 6.0, 9.0, 8.0],
        "Nominal (PV)": [100_000_000, 0, 0, 50_000_000, 0, 100_000_000]
    }

    df_assets = st.data_editor(pd.DataFrame(asset_data), num_rows="fixed")

    df_assets["Nominal (FV)"] = df_assets.apply(
        lambda row: row["Nominal (PV)"] * ((1 + row["Asumsi Imbal Hasil (p.a)"] / 100) ** (usia_pensiun - usia_skrg)),
        axis=1
    )

    st.dataframe(df_assets.style.format({
        "Nominal (PV)": "Rp{:,.0f}",
        "Nominal (FV)": "Rp{:,.0f}",
        "Asumsi Imbal Hasil (p.a)": "{:.1f}%"
    }))

    total_fv = df_assets["Nominal (FV)"].sum()
    st.write(f"### ✅ Total harta yang dimiliki saat pensiun: **Rp{total_fv:,.0f}**")

    deficit = max(pvad - total_fv, 0)
    st.warning(f"❗ Defisit yang harus dialokasikan: **Rp{deficit:,.0f}**")

    st.markdown("## 💡 Simulasi cicilan investasi bulanan untuk tutup defisit")
    st.markdown("Masukkan alokasi aset (%) yang direncanakan, total harus 100%.")

    alloc_data = {
        "Aset": ["Tabungan/Deposito", "RDPU", "RDPD", "RDS", "Emas"],
        "Imbal Hasil (%)": [2.0, 5.0, 6.0, 9.0, 8.0],
        "Alokasi (%)": [20, 20, 20, 20, 20]
    }

    df_alloc = st.data_editor(pd.DataFrame(alloc_data), num_rows="fixed")

    alloc_total = df_alloc["Alokasi (%)"].sum()
    if alloc_total != 100:
        st.error("❌ Total alokasi tidak sama dengan 100%!")
    else:
        weighted_return = np.dot(df_alloc["Imbal Hasil (%)"], df_alloc["Alokasi (%)"]) / 100
        r_monthly = weighted_return / 100 / 12
        n_months = (usia_pensiun - usia_skrg) * 12
        if r_monthly == 0:
            pmt = deficit / n_months
        else:
            pmt = (deficit * r_monthly) / (((1 + r_monthly) ** n_months - 1) * (1 + r_monthly))
        st.success(f"✅ Dengan return gabungan {weighted_return:.2f}%, Anda perlu menabung **Rp{pmt:,.0f}/bulan**.")
