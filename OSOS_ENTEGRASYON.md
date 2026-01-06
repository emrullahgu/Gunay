# 🔌 OSOS & EPİAŞ Entegrasyon Kılavuzu

Bu rehber, elektrik verilerini GUNAY uygulamasına aktarmak için tüm yöntemleri açıklar.

## ⚡ VERİ KAYNAKLARI

### 1️⃣ OSOS (Otomatik Sayaç Okuma Sistemi)
**Tesis özel** elektrik tüketim verileri - Sayaç bazlı

### 2️⃣ EPİAŞ (Enerji Piyasaları İşletme A.Ş.)
**Türkiye geneli** elektrik piyasası verileri - Benchmark için

### 3️⃣ TEİAŞ (Türkiye Elektrik İletim A.Ş.)
Şebeke yük ve üretim bilgileri

---

## 📋 OSOS NEDİR?

**Otomatik Sayaç Okuma Sistemi (OSOS)**; elektrik dağıtım şirketlerinin (GEDAŞ, AYEDAŞ, Toroslar EDAŞ, vb.) sayaçlara taktıkları modemler ile uzaktan veri okuyan sistemdir.

OSOS şu verileri toplar:
- ⚡ Aktif/Reaktif enerji endeksleri
- 📊 Saatlik/Günlük yük profili (15 dakikalık)
- 📈 Anlık güç değerleri
- 🔋 Sayaç durum bilgileri

## 🎯 OSOS - İKİ FARKLI VERİ ALMA YÖNTEMİ

### Yöntem Karşılaştırması

| Özellik | Web Portal (Resmi) | Yerel Okuma (Mühendislik) |
|---------|-------------------|--------------------------|
| **Amaç** | Fatura ve hak ediş | Anlık izleme ve analiz |
| **Veri Frekansı** | 15 dakika / 1 saat | Anlık (saniye/dakika) |
| **Gecikme** | 1 gün gecikme | Gerçek zamanlı |
| **İzin Gereksinimi** | EDAŞ başvurusu | Optik port: İzin yok / RS-485: Mühür iznine dikkat |
| **Uygun Olduğu Durumlar** | Fatura analizi, uzlaştırma | Enerji kalitesi, kompanzasyon, harmonik analiz |
| **Maliyet** | Ücretsiz | Donanım maliyeti (~500-2000₺) |

---

## 📊 OSOS YÖNTEM 1: EDAŞ WEB PORTAL (RESMİ VERİ - ÖNERİLEN)

### Avantajlar:
✅ Faturalandırmaya esas resmi veri  
✅ Ücretsiz  
✅ Geçmişe dönük 1 yıllık veri  
✅ Excel/CSV export  

### Dezavantajlar:
❌ 1 gün gecikme  
❌ 15 dakikalık veri (anlık değil)  
❌ EDAŞ onayı gerekli  

### Uygun Olduğu Durumlar:
- 📋 Fatura analizi ve doğrulama
- 📊 Aylık/yıllık tüketim raporları
- 💰 Reaktif ceza takibi
- 📈 Baz yük (base load) analizi

#### 📝 Başvuru Süreci:

1. **Dağıtım Şirketinizi Belirleyin:**
   - Toroslar EDAŞ: Adana, Gaziantep, Hatay, Mersin, Osmaniye, Kilis
   - Başkent EDAŞ: Ankara, Bartın, Çankırı, Karabük, Kastamonu, Kırıkkale, Zonguldak
   - AYEDAŞ: İstanbul Anadolu Yakası
   - GEDAŞ: Gaziantep bölgesi
   - SEDAŞ: Konya, Karaman

2. **Başvuru Formunu İndirin:**
   - Dağıtım şirketi web sitesinden "OSOS Kullanıcı Hesap Başvuru Formu"nu indirin
   - Örnek: https://toroslaredas.com.tr/osos

3. **Gerekli Belgeleri Hazırlayın:**
   - [ ] OSOS Kullanıcı Hesap Başvuru Formu (imzalı)
   - [ ] Vekâletname/Yetki Belgesi
   - [ ] İmza Sirküleri
   - [ ] Tüm belgeleri tek PDF'e tarayın

4. **Başvurunuzu Gönderin:**
   
   **Seçenek A - KEP ile (Önerilen):**
   ```
   Toroslar EDAŞ: toroslar.edas@hs03.kep.tr
   Başkent EDAŞ: baskent.edas@hs03.kep.tr
   AYEDAŞ: istanbul.ayedas@hs03.kep.tr
   ```
   - PDF'i e-imza ile imzalayın
   - KEP adresine gönderin
   
   **Seçenek B - Fiziki Teslimat:**
   - Belgeleri "Gelen Evrak" birimine teslim edin
   - Merkez ofis adresleri web sitesinde

5. **Kullanıcı Adı/Şifre Alın:**
   - Başvuru onaylandıktan sonra kullanıcı bilgileri size gönderilir
   - Genellikle 3-5 iş günü sürer

#### 📞 Destek İletişim:

| Dağıtım Şirketi | Çağrı Merkezi | OSOS E-posta |
|-----------------|---------------|--------------|
| Toroslar EDAŞ   | 186           | toroslar_osos_mth@eedas.com.tr |
| Başkent EDAŞ    | 186           | baskent_osos@cedas.com.tr |
| AYEDAŞ          | 186           | ayedas_osos@enerjisa.com.tr |

### Adım 2: GUNAY'a OSOS Portal Bilgilerini Girin

1. `.env.example` dosyasını `.env` olarak kopyalayın:
   ```bash
   copy .env.example .env
   ```

2. `.env` dosyasını düzenleyin:
   ```env
   # Dağıtım şirketinizi seçin
   OSOS_DAGITIM_SIRKETI=toroslar
   # Seçenekler: toroslar, baskent, ayedas, gedas, sedas
   
   # Portal bilgilerinizi girin
   OSOS_KULLANICI_ADI=sizin_kullanici_adiniz
   OSOS_SIFRE=sizin_sifreniz
   OSOS_SAYAC_NO=12345678
   ```

### Adım 3: Veri Toplamayı Başlatın

```bash
# Gereksinimleri yükle
pip install -r requirements.txt

# Veri toplama scriptini çalıştır
python osos_collector.py
```

**Otomatik Çalışma:**
```bash
# Windows'ta görev zamanlayıcı ile
# Linux'ta crontab ile
```

---

## ⚡ YÖNTEM 2: YEREL OKUMA (MÜHENDİSLİK ANALİZİ - ANLIK VERİ)

### Avantajlar:
✅ **Anlık veri** (saniye/dakika bazlı)  
✅ Gerçek zamanlı  
✅ Enerji kalitesi analizi  
✅ Harmonik analiz  
✅ Kompanzasyon takibi  
✅ Bağımsız izleme  

### Dezavantajlar:
❌ Donanım maliyeti (500-2000₺)  
❌ Teknik bilgi gerekli  
❌ RS-485 için mühür iznine dikkat  

### Uygun Olduğu Durumlar:
- 🔬 Enerji kalitesi ölçümü
- ⚡ Reaktif güç kompanzasyonu
- 📊 Harmonik analizi
- 🎯 Yük profili detaylı analiz
- 💡 Enerji verimliliği projeleri
- 🏭 SCADA entegrasyonu

### A) Optik Port Okuma (ÖNERİLEN - Mühürsüz, Yasal)

#### Gerekli Donanım:
- 🔌 **USB Optik Okuyucu** (~500-1000₺)
  - IEC 62056-21 uyumlu
  - Mıknatıslı prob (sayaca yapışır)
  - Marka önerileri: GIGA, SONEL, CEC

#### Protokol:
- **IEC 62056-21** (IEC 1107)
- **DLMS/COSEM**
- **OBIS Kodları**

#### Kurulum:

1. **Optik okuyucuyu sayaca yerleştirin:**
   - Sayacın ön panelindeki optik port üzerine
   - Mıknatıs ile sabitlenir
   - Mühür gerektirmez ✅

2. **USB'yi bilgisayara takın:**
   - Windows: COM port olarak görünür (COM3, COM4, vb.)
   - Linux: /dev/ttyUSB0

3. **GUNAY'ı yapılandırın:**
   ```bash
   # requirements.txt yükle
   pip install pyserial requests python-dotenv
   
   # Test et
   python osos_yerel_okuma.py
   # Seçim: 1 (Optik Port)
   # Port: COM3
   ```

4. **Otomatik veri toplama:**
   ```python
   # osos_collector.py içinde aktif edin:
   # Optik port okumasını açın
   ```

#### Desteklenen Sayaçlar:
- ✅ Tüm OSOS uyumlu sayaçlar
- ✅ Makel, Luna, Köhler
- ✅ ABB, Schneider, Siemens
- ✅ EDMI, Landis+Gyr

### B) RS-485 Modbus RTU (Direkt Sayaç Erişimi)

#### ⚠️ ÖNEMLİ UYARI:
- **Mühür altındaki uçlara müdahale yasaktır!**
- Sadece "tesis içi süzme sayaç" için kullanın
- Dağıtım şirketi sayacı ise EDAŞ'tan izin alın

#### Gerekli Donanım:
- 🔌 **USB-RS485 Dönüştürücü** (~200-500₺)
  - CH340 chip önerilen
  - A, B terminallerine bağlanır

#### Protokol:
- **Modbus RTU**
- **DLMS/COSEM**
- **Baud Rate**: Genellikle 9600, 19200

#### Kurulum:

1. **Kablo Bağlantısı:**
   ```
   Sayaç       USB-RS485
   -------     ----------
   A (+)   →      A
   B (-)   →      B
   GND     →      GND
   ```

2. **Modbus Slave ID'yi öğrenin:**
   - Sayaç dokümantasyonu
   - Genellikle 1

3. **GUNAY yapılandırması:**
   ```bash
   # .env dosyasında
   OSOS_MODBUS_PORT=COM4
   OSOS_MODBUS_SLAVE_ID=1
   
   # Test
   python osos_yerel_okuma.py
   # Seçim: 2 (Modbus RTU)
   ```

#### Register Haritası:
Her sayaç farklı! Sayaç dokümantasyonuna bakın:

**Örnek (Genel):**
| Parametre | Register | Format |
|-----------|----------|--------|
| Aktif Güç | 0-1 | Float |
| Reaktif Güç | 2-3 | Float |
| Gerilim L1 | 4-5 | Float |
| Akım L1 | 6-7 | Float |

### C) Donanım Önerileri

#### Optik Okuyucular:
1. **GIGA Optik Okuyucu** - 800₺
   - USB
   - IEC 62056-21
   - Türkiye'de yaygın

2. **SONEL CIR-e3** - 1200₺
   - Profesyonel
   - Bluetooth + USB
   - Android uygulama

3. **CEC Optical Probe** - 600₺
   - Ekonomik
   - Temel özellikler

#### USB-RS485 Dönüştürücüler:
1. **FTDI Chipli** - 400₺ (En kaliteli)
2. **CH340 Chipli** - 200₺ (Uygun fiyat)

## 📋 Ön Hazırlık (Diğer Alternatif Yöntemler)

### 1. Bilgi Toplama
OSOS sisteminiz hakkında şu bilgileri toplayın:

- [ ] **IP Adresi**: _________________ (Örn: 192.168.1.100)
- [ ] **Port**: _____________________ (Örn: 502, 80, 1883)
- [ ] **Marka/Model**: ______________ (Örn: ABB, Siemens, Schneider)
- [ ] **Protokol**: _________________ (Modbus TCP / MQTT / REST API)
- [ ] **Kullanıcı Adı/Şifre**: _______ (Varsa)

### 2. Nereden Öğrenebilirsiniz?

#### A) Cihaz Etiketi
- Cihazın üzerindeki etiket/plakette model numarası
- Google'da "[Model Numarası] communication protocol" araması

#### B) Web Arayüzü
```
http://OSOS_IP_ADRESI
```
- Tarayıcıdan cihaz IP'sine gidin
- Genellikle bir web arayüzü vardır
- System Info / Communication / Settings bölümlerine bakın

#### C) IT Departmanı
- Ağ yöneticinize sorun
- SCADA sistemini yöneten ekiple görüşün

#### D) Elektrik Dağıtım Şirketi
- GEDAŞ, AYEDAŞ, vb. teknik destek
- Sistemi kuran firma/teknisyen

## 🔬 Adım 1: Protokol Tespiti

### Otomatik Tespit Aracını Çalıştırın

```bash
# Gereksinimleri yükle
pip install -r requirements_detector.txt

# Protokol tespit aracını çalıştır
python osos_protocol_detector.py
```

**Örnek Çıktı:**
```
🔬 GUNAY - OSOS Protokol Tespit Aracı
IP Adresi: 192.168.1.100

✅ Modbus TCP portu AÇIK! (Port 502)
   → OSOS cihazınız Modbus TCP kullanıyor olabilir

📊 SONUÇ ÖZETİ
✅ Modbus TCP protokolü tespit edildi!
```

## 🔧 Adım 2: Konfigürasyon

### Tespit edilen protokole göre yapılandırma:

---

## 📘 SENARYO 1: Modbus TCP

### Adım 2.1: Register Haritasını Öğrenin

Cihaz dokümantasyonundan register adresleri:

| Parametre      | Register Adresi | Veri Tipi |
|----------------|-----------------|-----------|
| Aktif Güç      | 0-1            | Float     |
| Reaktif Güç    | 2-3            | Float     |
| Gerilim        | 4-5            | Float     |
| Akım           | 6-7            | Float     |

### Adım 2.2: osos_collector.py'yi Düzenleyin

```python
def read_osos_data():
    # Modbus bölümünü aktif edin:
    return read_osos_data_modbus(ip="192.168.1.100", port=502)
```

### Adım 2.3: Test Edin

```bash
python osos_collector.py
```

---

## 🌐 SENARYO 2: REST API

### Adım 2.1: API Endpoint'lerini Keşfedin

Tarayıcıda test edin:
```
http://OSOS_IP_ADRESI/api/
http://OSOS_IP_ADRESI/api/measurements
http://OSOS_IP_ADRESI/api/instant-data
http://OSOS_IP_ADRESI/data.json
```

### Adım 2.2: API Yanıtını İnceleyin

```bash
# PowerShell'de test:
Invoke-WebRequest -Uri "http://192.168.1.100/api/measurements"

# veya curl ile:
curl http://192.168.1.100/api/measurements
```

Yanıt formatı:
```json
{
  "active_power": 185.5,
  "voltage": 225.3,
  "current": 12.5
}
```

### Adım 2.3: osos_collector.py'yi Düzenleyin

`read_osos_data_rest_api()` fonksiyonundaki alan isimlerini API yanıtınıza göre düzenleyin:

```python
data = {
    "aktif_guc": api_data.get('active_power', 0),  # API'nizdeki alan adı
    "gerilim": api_data.get('voltage', 0),
    # ...
}
```

---

## 📡 SENARYO 3: MQTT

### Adım 2.1: MQTT Broker Bilgileri

- **Broker IP**: ________________
- **Port**: ____________________ (Varsayılan: 1883)
- **Topic**: ___________________ (Örn: osos/measurements)

### Adım 2.2: Topic'i Dinleyin

```bash
# MQTT Explorer kurarak topic'leri görün
# veya
pip install paho-mqtt
python -c "import paho.mqtt.client as mqtt; client = mqtt.Client(); client.connect('BROKER_IP', 1883); client.subscribe('osos/#'); client.loop_forever()"
```

### Adım 2.3: osos_collector.py'yi Düzenleyin

```python
def read_osos_data():
    return read_osos_data_mqtt()
```

---

## ✅ Adım 3: Test ve Doğrulama

### 1. Backend'i Başlat
```bash
cd server
node index.js
```

### 2. Veri Toplayıcıyı Başlat
```bash
python osos_collector.py
```

### 3. Frontend'i Aç
```bash
cd client
npm run dev
```

Tarayıcıda: http://localhost:5173

---

## 🆘 Sorun Giderme

### Bağlantı Hatası
```
❌ Connection refused
```
**Çözüm:**
- IP adresini doğrulayın
- Firewall kurallarını kontrol edin
- Cihazın açık olduğundan emin olun

### Timeout Hatası
```
❌ Timeout error
```
**Çözüm:**
- Port numarasını doğrulayın
- Ağ bağlantısını test edin: `ping OSOS_IP_ADRESI`

### Veri Format Hatası
```
❌ Invalid data format
```
**Çözüm:**
- API yanıtını konsola yazdırın
- Alan isimlerini kontrol edin
- Veri tiplerini doğrulayın (string → float)

---

## 🌐 EPİAŞ (TÜRKİYE GENELİ VERİLER - BENCHMARK)

### EPİAŞ Şeffaflık Platformu Nedir?

**EPİAŞ (Enerji Piyasaları İşletme A.Ş.)** Türkiye elektrik piyasasının resmi veri kaynağıdır:

- ⚡ Gerçek zamanlı üretim-tüketim (Türkiye geneli)
- 💰 Piyasa Takas Fiyatları (PTF - TL/MWh)
- 📊 Kaynak bazlı üretim (Termik, Hidrolik, Rüzgar, Güneş)
- 🌱 Yenilenebilir enerji payı
- 📈 Yük tahminleri

### Kullanım Alanları

| Veri Tipi | OSOS | EPİAŞ |
|-----------|------|-------|
| **Kapsam** | Tesisiniz | Türkiye Geneli |
| **Amaç** | Kendi tüketiminizi izleme | Benchmark, karşılaştırma |
| **Fiyat** | - | Piyasa fiyat takibi |
| **Örnek** | "Bu ay 12.500 kWh tükettik" | "Türkiye'de saat 14:00'te 45.000 MW tüketiliyor" |

### EPİAŞ Entegrasyonu

#### Adım 1: EPİAŞ Client'ı Kullan

```bash
# epias_client.py'yi çalıştır
python epias_client.py
```

**Mevcut Özellikler:**
```python
from epias_client import EPIASClient

client = EPIASClient()

# Gerçek zamanlı üretim
generation = client.get_realtime_generation()

# Türkiye tüketimi
consumption = client.get_consumption_data()

# Piyasa fiyatı (PTF)
price = client.get_market_price()

# Yenilenebilir enerji
renewable = client.get_renewable_generation()
```

#### Adım 2: GUNAY Dashboard'a Ekle

EPİAŞ verileri Dashboard'da **Türkiye Geneli** karşılaştırması için kullanılabilir:

```javascript
// Örnek: Tesisinizin tüketimini Türkiye ortalamasıyla karşılaştırın
const turkiyeOrtalama = epias_data.consumption / 1000; // MW → kW
const tesisTuketim = gunay_data.aktif_guc;
const verimlilik = (tesisTuketim / turkiyeOrtalama) * 100;
```

### EPİAŞ API Kaydı (Opsiyonel)

Bazı detaylı veriler için EPİAŞ'a kayıt gerekir:

1. https://seffaflik.epias.com.tr adresine gidin
2. "Kayıt Ol" → Kurumsal/Bireysel hesap oluşturun
3. API Key alın (bazı planlar ücretlidir)
4. `.env` dosyasına ekleyin:
   ```env
   EPIAS_USERNAME=your_username
   EPIAS_PASSWORD=your_password
   ```

### Halka Açık Veriler (Kayıt Gerektirmez)

✅ Gerçek zamanlı üretim  
✅ Toplam tüketim  
✅ Yenilenebilir enerji payı  
❌ Detaylı fiyat analizi (API Key gerekir)  
❌ İleri düzey raporlar (Ücretli)

### EPİAŞ vs TEİAŞ

| Platform | Veri Tipi | Erişim |
|----------|-----------|--------|
| **EPİAŞ** | Piyasa verileri, fiyat | API + Web |
| **TEİAŞ** | Şebeke yük, iletim | Web (gercekzamanli.teias.gov.tr) |

---

## 🔄 TÜM KAYNAKLARI BİRLİKTE KULLANMA

### Önerilen Strateji (Enerji Verimliliği Danışmanları İçin)

1. **OSOS Web Portal** → Müşterinizin geçmiş tüketim analizi (1 yıllık)
2. **OSOS Yerel Okuma** → Anlık izleme, kompanzasyon takibi
3. **EPİAŞ** → Benchmark, piyasa fiyatı takibi

### Örnek Senaryo: Bir Sanayi Tesisi

```python
# 1. OSOS'tan tesis verisi al
tesis_tuketim = osos_client.get_anlik_veri(sayac_no="123456")

# 2. EPİAŞ'tan Türkiye geneli al
turkiye_data = epias_client.get_consumption_data()

# 3. Karşılaştır ve rapora ekle
rapor = {
    "tesis": tesis_tuketim['aktif_guc'],
    "turkiye_ortalama": turkiye_data[-1]['consumption'] / 84_000,  # 84M nüfus
    "verimlilik_skoru": calculate_efficiency(tesis_tuketim)
}
```

### GUNAY Collector'a Hepsini Ekle

`osos_collector.py` zaten bu yapıdadır:

```python
def read_osos_data():
    # Öncelik 1: OSOS Portal
    veri = read_osos_data_portal()
    if veri: return veri
    
    # Öncelik 2: Yerel okuma
    veri = read_osos_data_modbus()
    if veri: return veri
    
    # Öncelik 3: EPİAŞ (benchmark)
    veri = read_epias_data()
    return veri
```

---

## 📞 Destek

Sorun yaşarsanız:

1. `osos_protocol_detector.py` çıktısını kaydedin
2. OSOS cihaz modelini not edin
3. Hata mesajlarını kopyalayın
4. GitHub Issues'da ticket açın: https://github.com/emrullahgu/Gunay/issues

veya README.md'deki iletişim bilgilerini kullanın.
