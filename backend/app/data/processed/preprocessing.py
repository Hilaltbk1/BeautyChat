import json
from langchain_core.documents import Document
from typing import List, Dict, Any


def preprocessing(file_name: str) -> List[Document]:
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data: List[Dict[str, Any]] = json.load(f)
    except FileNotFoundError:
        print(f"HATA: '{file_name}' adında bir dosya bulunamadı.")
        return []

    dokumanlar: List[Document] = []


    for urun in data:
        urun_adi = urun.get("name", "Bilinmeyen Ürün")
        urun_icerikleri = urun.get("ingredients")

        if urun_icerikleri:
            for icerik in urun_icerikleri:
                icerik_metni = (
                    f"İçerik Adı: {icerik.get('name', 'N/A')}\n"
                    f"Fonksiyon: {icerik.get('function', 'N/A')}\n"
                    f"Cilt Sorunları: {icerik.get('concerns', 'N/A')}\n"
                    f"Güvenlik Yorumu: {icerik.get('safety_comment', 'N/A')}"
                )

                icerik_etiketi = {
                    "kaynak_dosya": file_name,
                    "urun_adi": urun_adi,
                    "bilgi_tipi": "içerik",
                    "icerik_adi": icerik.get("name", "N/A")
                }

                doc = Document(page_content=icerik_metni, metadata=icerik_etiketi)
                dokumanlar.append(doc)

        ambalaj_bilgisi = urun.get("packaging")
        if ambalaj_bilgisi:
            ambalaj_metni = (
                f"Ürün Adı: {urun_adi}\n"
                f"Ambalaj İçerik Listesi: {ambalaj_bilgisi.get('ingredients', 'N/A')}\n"
                f"Kullanım Talimatı: {ambalaj_bilgisi.get('directions', 'N/A')}\n"
                f"Uyarılar: {ambalaj_bilgisi.get('warnings', 'N/A')}"
            )

            ambalaj_etiketi = {
                "kaynak_dosya": file_name,
                "urun_adi": urun_adi,
                "bilgi_tipi": "ürün özeti ve kullanım",
            }

            doc = Document(page_content=ambalaj_metni, metadata=ambalaj_etiketi)
            dokumanlar.append(doc)

    return dokumanlar

