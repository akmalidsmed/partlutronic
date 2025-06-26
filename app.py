import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sparepart's Lutronic", layout="wide")

# Judul Aplikasi
st.title("🔧 Sparepart's Lutronic")

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("Combined_Spare_Part_List.xlsx")

df = load_data()

st.markdown("### 🔍 Pencarian Umum")

# Input pencarian utama (seluruh kolom)
search_all = st.text_input("Cari di semua kolom")

# Filter berdasarkan pencarian umum
if search_all:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_all, case=False, na=False).any(), axis=1)]
else:
    filtered_df = df

st.markdown("### 🔎 Filter Berdasarkan Kolom Tertentu")

# Pilih kolom dan input kata kunci khusus
col1, col2 = st.columns([2, 5])
with col1:
    selected_column = st.selectbox("Pilih Kolom", df.columns.tolist())

with col2:
    search_text = st.text_input("Masukkan kata kunci (khusus kolom terpilih)")

# Filter lanjutan (khusus kolom)
if search_text:
    filtered_df = filtered_df[filtered_df[selected_column].astype(str).str.contains(search_text, case=False, na=False)]

# Tampilkan hasil
st.dataframe(filtered_df, use_container_width=True)
