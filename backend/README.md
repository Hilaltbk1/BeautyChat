# BeautyChat 💄✨

![WhatsApp Image 2025-10-25 at 21 38 58](https://github.com/user-attachments/assets/10ae1e91-a883-43fb-a6b7-6ee57106002e)


BeautyChat, güzellik, makyaj ve cilt bakımı hakkında sorular sorabileceğiniz ve yapay zeka (veya bir backend servisi) tarafından desteklenen cevaplar alabileceğiniz basit bir React tabanlı sohbet arayüzüdür.

 ## 🚀 Özellikler

## Bu projenin mevcut  özellikleri:

Kullanıcı Adı ve Soru Girişi: API isteği göndermek için bir kullanıcı adı ve soru girişi.

Gerçek Zamanlı API İsteği: Soruları axios kullanarak bir backend sunucusuna gönderme.

Cevap Görüntüleme: API'den gelen cevapları doğrudan arayüzde gösterme.

Yükleme ve Hata Durumları: API cevabı beklenirken "Cevap hazırlanıyor..." mesajı ve bir hata oluşursa "Bir hata oluştu..." uyarısı gösterilir.

Geçmiş Arayüzü: Geçmiş konuşmaları listelemek için tasarlanmış bir kenar çubuğu (sidebar).

# 🛠️ Kullanılan Teknolojiler

Bu projenin çalışması için iki bölüm gereklidir:

## 1. Frontend:

React: Kullanıcı arayüzü için.

Vite: Geliştirme sunucusu ve derleyici.

axios: Backend API'sine HTTP istekleri göndermek için.

Özel CSS: App.css dosyasında tanımlanan .appInput, .wallpaper, .sidebar gibi özel sınıflar (class'lar).

## 2. Backend :

Bu frontend projesi, http://localhost:8000 adresinde çalışan bir backend sunucusuna ihtiyaç duyar.

Backend'in (Python/FastAPI ile yazılmış) Pydantic modellerine uygun olarak query (soru) ve name (kullanıcı adı) alanlarını beklemesi gerekmektedir.

# 🏁 Kurulum ve Çalıştırma

Bu projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

## 1. Backend Sunucusu (Ön Koşul)

Bu frontend'i çalıştırmadan önce, BeautyChat'in backend sunucusunun çalışır durumda olduğundan emin olun.

Backend sunucunuzun http://localhost:8000 adresinde çalıştığından emin olun.

Backend'in, aşağıda detayları verilen /search endpoint'ini (uç nokta) sağladığından emin olun.

## 2. Frontend (Bu Proje)

Projeyi klonlayın:

```
git clone [PROJE_GIT_ADRESINIZ]
cd MyFrontend 
```

Gerekli paketleri yükleyin:
```
npm install
```

Not: axios kütüphanesinin yüklü olduğundan emin olun:
```
npm install axios
```

Geliştirme sunucusunu başlatın:
```
npm run dev
```

Tarayıcınızda http://localhost:5173 (veya Vite'in size verdiği adresi) açın.

#🔌 API Detayları

Frontend'in backend'den cevap alabilmesi için backend'in aşağıdaki yapıya uyması gerekir:

Endpoint: POST /search

Adres: http://localhost:8000/search

İstek (Request) Body (JSON):
Backend, query ve name adında iki anahtar beklemektedir.
```
{
  "query": "Kullanıcının girdiği soru metni",
  "name": "Kullanıcının girdiği kullanıcı adı"
}
```

Başarılı Cevap (Response) Body (JSON):
Frontend, cevap adında bir anahtar beklemektedir.
```
{
  "cevap": "Yapay zeka veya servis tarafından üretilen cevap metni."
}
```


