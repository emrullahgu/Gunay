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

## 🚀 Deployment (Canlıya Alma)

### Backend - Render.com (Ücretsiz)

1. [Render.com](https://render.com)'a giriş yapın
2. "New +" → "Web Service" seçin
3. GitHub repo'nuzu bağlayın: `https://github.com/emrullahgu/Gunay`
4. Ayarlar:
   - **Name:** gunay-backend
   - **Root Directory:** (boş bırakın)
   - **Build Command:** `npm install`
   - **Start Command:** `npm start`
   - **Plan:** Free
5. "Create Web Service" tıklayın
6. Backend URL'inizi kopyalayın (örn: `https://gunay-backend.onrender.com`)

### Frontend - Netlify

1. [Netlify](https://netlify.com)'a giriş yapın
2. "Add new site" → "Import an existing project"
3. GitHub repo'nuzu seçin
4. Build ayarları (otomatik gelecek):
   - **Base directory:** `client`
   - **Build command:** `npm run build`
   - **Publish directory:** `client/dist`
5. Environment Variables ekleyin:
   - `VITE_API_URL` = Backend URL'niz (Render'dan kopyaladığınız)
6. "Deploy site" tıklayın

### Manuel Deploy

\`\`\`bash
# 1. Backend'i deploy et
git push origin main

# 2. Netlify CLI ile frontend deploy (opsiyonel)
cd client
npm install -g netlify-cli
netlify deploy --prod
\`\`\`

## 🔧 Geliştirme

Proje yapısı:
\`\`\`
gunay/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # Bileşenler
│   │   ├── pages/          # Sayfalar
│   │   └── App.jsx         # Ana uygulama
├── server/                 # Express backend
│   ├── database/           # Veritabanı
│   └── index.js            # Server entry point
├── netlify.toml            # Netlify config
└── README.md
\`\`\`

## 📝 Lisans

MIT

## 👨‍💻 Geliştirici

Emrullah - GUNAY OSOS Enerji İzleme Sistemi

---

**Not**: Okula geldiğinizde daha detaylı görüşelim!
