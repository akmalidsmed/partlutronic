# Streamlit app: Sparepart's Lutronic
# File: streamlit_spareparts_lutronic_with_password.py
# Petunjuk: simpan file ini di folder yang sama dengan "Combined_Spare_Part_List.xlsx"
# Jalankan: streamlit run streamlit_spareparts_lutronic_with_password.py

import streamlit as st
import pandas as pd
import hashlib

# --------- Konfigurasi halaman ----------
st.set_page_config(page_title="Sparepart's Lutronic", layout="wide")

# --------- Password (disimpan sebagai hash) ----------
# Password plain: idsMED11!
_PASSWORD_HASH = hashlib.sha256("idsMED11!".encode("utf-8")).hexdigest()

def check_password(password: str) -> bool:
    """True jika password cocok (SHA-256)."""
    if not password:
        return False
    return hashlib.sha256(password.encode("utf-8")).hexdigest() == _PASSWORD_HASH

# --------- Inisialisasi session state ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "login_error" not in st.session_state:
    st.session_state.login_error = False

# --------- Halaman login ----------
if not st.session_state.authenticated:
    st.markdown("# 🔐 Masuk untuk melihat aplikasi")
    st.write("Masukkan password untuk membuka seluruh tampilan aplikasi.")

    cols = st.columns([3, 1])
    with cols[0]:
        pwd = st.text_input("Password", type="password")
    with cols[1]:
        enter = st.button("Masuk")

    if enter:
        if check_password(pwd):
            st.session_state.authenticated = True
            st.session_state.login_error = False
            st.experimental_rerun()
        else:
            st.session_state.login_error = True

    if st.session_state.login_error:
        st.error("Password salah — coba lagi.")

    st.caption("Hubungi administrator jika Anda lupa password.")

else:
    # --------- Konten utama ----------
    st.sidebar.markdown("## 🔓 Status: Terautentikasi")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()

    st.title("🔧 Sparepart's Lutronic")

    @st.cache_data
    def load_data():
        return pd.read_excel("Combined_Spare_Part_List.xlsx")

    with st.spinner("Memuat data..."):
        df = load_data()

    st.markdown("### 🔍 Pencarian Umum")
    search_all = st.text_input("Cari di semua kolom")

    if search_all:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_all, case=False, na=False).any(), axis=1)]
    else:
        filtered_df = df

    st.markdown("### 🔎 Filter Berdasarkan Kolom Tertentu")
    col1, col2 = st.columns([2, 5])
    with col1:
        selected_column = st.selectbox("Pilih Kolom", df.columns.tolist())
    with col2:
        search_text = st.text_input("Masukkan kata kunci (khusus kolom terpilih)")

    if search_text:
        filtered_df = filtered_df[filtered_df[selected_column].astype(str).str.contains(search_text, case=False, na=False)]

    st.dataframe(filtered_df, use_container_width=True)

    # Tombol unduh hasil
    def to_excel(df_input: pd.DataFrame) -> bytes:
        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df_input.to_excel(writer, index=False, sheet_name="Results")
            writer.save()
        return buffer.getvalue()

    if not filtered_df.empty:
        excel_bytes = to_excel(filtered_df)
        st.download_button("⬇️ Unduh hasil (Excel)", data=excel_bytes,
                           file_name="search_results.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.caption("Aplikasi dikunci dengan password. Pastikan file 'Combined_Spare_Part_List.xlsx' tersedia di direktori yang sama.")
