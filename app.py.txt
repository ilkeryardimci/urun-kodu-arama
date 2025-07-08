import streamlit as st
import pandas as pd

@st.cache_resource
def load_data():
    # Google Drive linkinden paylaşılabilir dosya URL'sini raw linke çevir
    url = "https://drive.google.com/uc?id=1Wzq9sw3zxM5LXsIe5s4DuYOHXhanff0W"
    # Tüm sheet'leri oku
    xls = pd.ExcelFile(url, engine='pyxlsb')
    all_data = pd.DataFrame()
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, dtype=str, engine='pyxlsb')
        df["Sheet"] = sheet
        all_data = pd.concat([all_data, df])
    all_data.fillna("", inplace=True)
    return all_data

# Veriyi yükle
data = load_data()

# Kod ve açıklama kolon isimleri
code_col = data.columns[0]
desc_col = data.columns[1]

st.title("Ürün Kodu Arama Uygulaması")

query = st.text_input("Ürün kodunu veya parçasını girin:")

if query:
    query_lower = query.lower()
    results = data[data[code_col].str.lower().str.contains(query_lower)]

    st.write(f"Toplam {len(results)} sonuç bulundu.")

    if not results.empty:
        st.dataframe(results[[code_col, desc_col, "Sheet"]])

        # Excel indirme butonu
        excel = results.to_excel(index=False, engine="xlsxwriter")
        st.download_button(
            label="Sonuçları Excel Olarak İndir",
            data=excel,
            file_name="arama_sonuclari.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.warning("Hiç sonuç bulunamadı.")
else:
    st.info("Arama yapmak için ürün kodu girin.")
