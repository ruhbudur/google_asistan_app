import streamlit as st
import random

st.set_page_config(page_title="Adam Asmaca", page_icon="🎯", layout="centered")
st.title("🎯 Adam Asmaca Oyunu")

# --- Kelime listesi ---
kelimeler = ["python", "bilgisayar", "programlama", "oyun", "asistan", "veri", "yapayzeka"]
secilen_kelime = st.session_state.get("secilen_kelime", random.choice(kelimeler))
dogru_harfler = st.session_state.get("dogru_harfler", [])
yanlis_harfler = st.session_state.get("yanlis_harfler", [])

# --- Kullanıcı harf girişi ---
harf = st.text_input("Bir harf girin:", max_chars=1).lower()

if st.button("Tahmin Et"):
    if harf:
        if harf in secilen_kelime:
            if harf not in dogru_harfler:
                dogru_harfler.append(harf)
                st.success(f"Doğru! '{harf}' kelimede var.")
            else:
                st.info(f"'{harf}' zaten buldun.")
        else:
            if harf not in yanlis_harfler:
                yanlis_harfler.append(harf)
                st.error(f"'{harf}' kelimede yok!")
            else:
                st.warning(f"'{harf}' harfini zaten denedin.")
    else:
        st.warning("Lütfen bir harf gir.")

st.session_state.dogru_harfler = dogru_harfler
st.session_state.yanlis_harfler = yanlis_harfler
st.session_state.secilen_kelime = secilen_kelime

# --- Kelime durumu ---
gosterim = " ".join([h if h in dogru_harfler else "_" for h in secilen_kelime])
st.subheader(f"Kelime: {gosterim}")

# --- Durum bilgisi ---
st.write(f"Yanlış harfler: {', '.join(yanlis_harfler)}")
st.write(f"Kalan hak: {6 - len(yanlis_harfler)}")

# --- Oyun sonucu ---
if "_" not in gosterim:
    st.success("🎉 Tebrikler! Kelimeyi buldun!")
    if st.button("Tekrar Oyna"):
        st.session_state.clear()
elif len(yanlis_harfler) >= 6:
    st.error(f"😢 Kaybettin! Kelime '{secilen_kelime}' idi.")
    if st.button("Yeniden Dene"):
        st.session_state.clear()

