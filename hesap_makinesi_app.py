import streamlit as st

st.set_page_config(page_title="Hesap Makinesi", page_icon="🧮", layout="centered")

st.title("🧮 Basit Hesap Makinesi")

st.write("Toplama, çıkarma, çarpma ve bölme işlemleri yapabilirsiniz.")

# Sayı girişleri
sayi1 = st.number_input("Birinci sayıyı girin:", step=1.0)
sayi2 = st.number_input("İkinci sayıyı girin:", step=1.0)

# İşlem seçimi
islem = st.selectbox("İşlem seçin:", ["Toplama", "Çıkarma", "Çarpma", "Bölme"])

# Hesaplama butonu
if st.button("Hesapla"):
    if islem == "Toplama":
        sonuc = sayi1 + sayi2
    elif islem == "Çıkarma":
        sonuc = sayi1 - sayi2
    elif islem == "Çarpma":
        sonuc = sayi1 * sayi2
    elif islem == "Bölme":
        if sayi2 != 0:
            sonuc = sayi1 / sayi2
        else:
            st.error("⚠️ Sıfıra bölme hatası!")
            sonuc = None

    if sonuc is not None:
        st.success(f"Sonuç: {sonuc}")

