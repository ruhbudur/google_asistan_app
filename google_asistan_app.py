# google_asistan_app.py
import streamlit as st

st.set_page_config(page_title="Google Uygulama Asistanı", page_icon="🧭", layout="centered")

def aciklama(app):
    metinler = {
        "Docs":      "Metin yazma, ödev, rapor, ortak düzenleme.",
        "Sheets":    "Tablo, hesaplama, grafik, bütçe/puan/izin çizelgesi.",
        "Slides":    "Sunum hazırlama, şablonlar, birlikte çalışma.",
        "Forms":     "Anket, kayıt formu, quiz; sonuçlar Sheets'e düşer.",
        "Drive":     "Bulut depolama, paylaşım, dosya yedekleme.",
        "Photos":    "Foto/video yedekleme, albüm, arama.",
        "Keep":      "Hızlı notlar, kontrol listeleri, hatırlatıcılar.",
        "Gmail":     "E-posta gönder/al, etiketler, filtreler.",
        "Calendar":  "Randevu/etkinlik, hatırlatma, davet, program.",
        "Meet":      "Görüntülü toplantı, ekran paylaşımı, kayıt.",
        "Maps":      "Rotalar, trafik, toplu taşıma, yerler.",
        "Translate": "Metin/ses/görüntü çevirisi, 100+ dil.",
    }
    return metinler.get(app, "")

def akilli_oneri(cumle: str) -> str:
    t = cumle.lower()
    kurallar = [
        (("sunum", "slayt", "slide", "slides"), "Slides"),
        (("tablo", "excel", "hesap", "bütçe", "puan", "grafik"), "Sheets"),
        (("anket", "form", "kayıt", "quiz"), "Forms"),
        (("metin", "ödev", "rapor", "döküman", "belge", "yazı"), "Docs"),
        (("dosya", "paylaş", "yükle", "yedek", "bulut"), "Drive"),
        (("foto", "resim", "galeri", "görüntü"), "Photos"),
        (("not", "todo", "yapılacak", "hatırlat"), "Keep"),
        (("mail", "e-posta", "gmail", "posta"), "Gmail"),
        (("takvim", "randevu", "etkinlik", "toplantı saati"), "Calendar"),
        (("toplantı", "görüntülü", "meet", "zoom"), "Meet"),
        (("harita", "rota", "navigasyon", "adres", "konum"), "Maps"),
        (("çeviri", "translate", "çevir"), "Translate"),
    ]
    for anahtarlar, app in kurallar:
        if any(k in t for k in anahtarlar):
            return app
    return "Drive"  # varsayılan

st.title("🧭 Google Uygulama Asistanı")
st.caption("Ne yapmak istediğini söyle; sana uygun Google uygulamasını önereyim.")

secenek = st.radio(
    "Birini seç ya da alttaki kutuya ihtiyacını yaz:",
    ["Docs", "Sheets", "Slides", "Forms", "Drive", "Photos",
     "Keep", "Gmail", "Calendar", "Meet", "Maps", "Translate", "Serbest yaz (otomatik öner)"],
    horizontal=False
)

serbest = ""
if secenek == "Serbest yaz (otomatik öner)":
    serbest = st.text_input("İhtiyacını yaz (örn: *sınıf yoklaması toplamak istiyorum*)")

buton = st.button("Öneriyi Göster")

if buton:
    if secenek == "Serbest yaz (otomatik öner)":
        if not serbest.strip():
            st.warning("Önce yukarıya ne yapmak istediğini yaz 😇")
        else:
            app = akilli_oneri(serbest)
            st.success(f"👉 Öneri: **{app}**")
            st.write("•", aciklama(app))
    else:
        st.success(f"👉 Öneri: **{secenek}**")
        st.write("•", aciklama(secenek))

st.divider()
st.info("Bu uygulama **senin bilgisayarında** çalışır. İstersen sonra internete de yayınlarız (Render, PythonAnywhere vb.).")
