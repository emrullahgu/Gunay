# GUNAY - OSOS Enerji İzleme ve Raporlama Sistemi

Apollo Eco tarzında, OSOS'tan gelen elektrik tüketim verilerini kaydeden ve raporlayan modern web uygulaması.

**GitHub:** https://github.com/emrullahgu/Gunay

## 🎯 Özellikler

- ⚡ **Gerçek Zamanlı İzleme**: OSOS verilerini canlı olarak görüntüleme
- 📊 **Detaylı Grafikler**: Aktif/Reaktif/Kapasitif güç, gerilim, akım grafikleri
- 📈 **Raporlama**: Günlük, haftalık, aylık enerji tüketim raporları
- 💾 **Veri Saklama**: SQLite ile güvenli veri depolama
- 🎨 **Modern Arayüz**: Tailwind CSS ile responsive tasarım
- 🇹🇷 **Türkçe**: Tam Türkçe dil desteği

## 🔧 Teknolojiler

### Backend
- Node.js & Express.js
- SQLite veritabanı
- REST API

### Frontend
- React 18
- Vite
- Tailwind CSS
- Recharts (Grafikler)
- Lucide React (İkonlar)
https://github.com/emrullahgu/Gunay
## 📦 Kurulum

### 1. Bağımlılıkları Yükle
\`\`\`bash
npm run install-all
\`\`\`

### 2. Uygulamayı Başlat
\`\`\`bash
npm run dev
\`\`\`

Backend: http://localhost:3000
Frontend: http://localhost:5173

## 📊 OSOS Veri Yapısı

Sistem aşağıdaki verileri toplar:

- **Aktif Güç** (kW) - Gerçek güç tüketimi
- **Reaktif Güç** (kVAr) - İndüktif güç
- **Kapasitif Güç** (kVAr) - Kapasitif güç
- **Gerilim** (V) - Hat gerilimi
- **Akım** (A) - Hat akımı
- **Güç Faktörü** (cos φ) - Enerji verimliliği
- **Enerji** (kWh) - Toplam tüketim
- **Frekans** (Hz) - Şebeke frekansı

## 🌐 API Endpoints

### Ölçüm Verileri
- `POST /api/olcumler` - Yeni ölçüm verisi ekle
- `GET /api/olcumler` - Tüm ölçüm verilerini getir
- `GET /api/olcumler/:cihazId` - Cihaza göre verileri getir

### Cihazlar
- `GET /api/cihazlar` - Tüm cihazları listele
- `POST /api/cihazlar` - Yeni cihaz ekle
- `GET /api/cihazlar/:id` - Cihaz detayı

### Raporlar
- `GET /api/raporlar/gunluk` - Günlük rapor
- `GET /api/raporlar/haftalik` - Haftalık rapor
- `GET /api/raporlar/aylik` - Aylık rapor

## 📱 Ekran Görüntüleri

Dashboard'da şunları görebilirsiniz:
- Anlık güç tüketimi
- Tarihsel tüketim grafikleri
- Cihaz durumları
- Enerji maliyeti hesaplamaları
- Verimlilik analizleri

## 🚀 Geliştirme

Proje yapısı:
\`\`\`
osos-enerji-izleme/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # Bileşenler
│   │   ├── pages/          # Sayfalar
│   │   ├── utils/          # Yardımcı fonksiyonlar
│   │   └── App.jsx         # Ana uygulama
├── server/                 # Express backend
│   ├── database/           # Veritabanı
│   ├── routes/             # API routes
│   └── index.js            # Server entry point
└── README.md
\`\`\`

## 📝 Lisans

MIT

## 👨‍💻 Geliştirici

Emrullah - OSOS Enerji İzleme Sistemi

---

**Not**: Okula geldiğinizde daha detaylı görüşelim!
