import streamlit as st
import pandas as pd
import io
import requests

@st.cache_data
def load_data():
    # Google Drive paylaşım linkinden file ID
    file_id = "1wRPhcSVpmdTiAUb9YDEZCMLt01YYR3_8"
    # Raw download URL
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Dosyayı indir
    response = requests.get(url)
    response.raise_for_status()

    # Excel dosyasını belleğe yükle
    xls_data = io.BytesIO(response.content)

    # Tüm sayfaları oku
    xls = pd.ExcelFile(xls_data)
    all_data = pd.DataFrame()
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, dtype=str)
        df["Sheet"] = sheet
        all_data = pd.concat([all_data, df], ignore_index=True)

    all_data.fillna("", inplace=True)
    return all_data

# Veri yükle
data = load_data()

# Kod ve açıklama kolonları
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

        # Excel indirme
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            results.to_excel(writer, index=False)
        st.download_button(
            label="Sonuçları Excel Olarak İndir",
            data=output.getvalue(),
            file_name="arama_sonuclari.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.warning("Hiç sonuç bulunamadı.")
else:
    st.info("Arama yapmak için ürün kodu girin.")
