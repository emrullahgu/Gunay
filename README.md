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

## 🔌 Gerçek OSOS Verilerini Alma

### Yöntem 1: OSOS Web Portal (ÖNERİLEN) ⭐

Dağıtım şirketinizin (Toroslar EDAŞ, Başkent EDAŞ, AYEDAŞ, vb.) OSOS Web Portal'ından otomatik veri çekin:

**Adım 1: Portal Hesabı Alın**

1. Dağıtım şirketinizin web sitesinden "OSOS Kullanıcı Hesap Başvuru Formu"nu indirin
2. Formu ve gerekli belgeleri (vekâletname, imza sirküleri) doldurun
3. KEP ile gönderin veya fiziki teslim edin:
   - Toroslar EDAŞ KEP: toroslar.edas@hs03.kep.tr
   - Başkent EDAŞ KEP: baskent.edas@hs03.kep.tr  
   - AYEDAŞ KEP: istanbul.ayedas@hs03.kep.tr
   - Çağrı Merkezi: 186

**Adım 2: GUNAY Yapılandırması**

\`\`\`bash
# .env dosyası oluştur
copy .env.example .env

# Düzenle:
OSOS_DAGITIM_SIRKETI=toroslar
OSOS_KULLANICI_ADI=your_username
OSOS_SIFRE=your_password
OSOS_SAYAC_NO=12345678

# Veri toplamayı başlat
python osos_collector.py
\`\`\`

**Desteklenen Dağıtım Şirketleri:**
- ✅ Toroslar EDAŞ (Adana, Gaziantep, Hatay, Mersin)
- ✅ Başkent EDAŞ (Ankara, Bartın, Çankırı)
- ✅ AYEDAŞ (İstanbul Anadolu)
- ✅ GEDAŞ (Gaziantep)
- ✅ SEDAŞ (Konya)

📘 **Detaylı Rehber:** [OSOS_ENTEGRASYON.md](OSOS_ENTEGRASYON.md)

---

### Yöntem 2: REST API (Önceki Yöntem)

OSOS sisteminizden backend'e veri gönderin:

\`\`\`bash
curl -X POST http://localhost:3001/api/olcumler \
  -H "Content-Type: application/json" \
  -d '{
    "cihaz_id": 1,
    "aktif_guc": 185.5,
    "reaktif_guc": 45.2,
    "kapasitif_guc": 25.8,
    "gerilim": 225.3,
    "akim": 12.5,
    "guc_faktoru": 0.92,
    "frekans": 50.0,
    "enerji": 1250.75
  }'
\`\`\`

### Yöntem 2: Python Script (Otomatik)

\`\`\`bash
# Gereksinimleri yükle
pip install -r requirements.txt

# Veri toplama scriptini çalıştır
python osos_collector.py
\`\`\`

**Not:** `osos_collector.py` dosyasındaki `read_osos_data()` fonksiyonunu OSOS sisteminize göre düzenleyin:
- Modbus TCP → `pymodbus` kullanın
- MQTT → `paho-mqtt` kullanın
- REST API → `requests` kullanın

### Yöntem 3: Excel/CSV Import

1. `osos_upload.html` dosyasını tarayıcıda açın
2. CSV veya Excel dosyanızı yükleyin
3. Sistem otomatik olarak verileri backend'e gönderecek

**CSV Format Örneği:**
\`\`\`csv
cihaz_id,aktif_guc,reaktif_guc,kapasitif_guc,gerilim,akim,guc_faktoru,frekans,enerji,zaman
1,185.5,45.2,25.8,225.3,12.5,0.92,50.0,1250.75,2026-01-06 10:30:00
\`\`\`

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
