"""
OSOS Web Portal Entegrasyon Modülü
Dağıtım şirketlerinin OSOS Web Portalından veri çeker
"""

import requests
import json
from datetime import datetime, timedelta

class OSOSPortalClient:
    """OSOS Web Portal API Client"""
    
    # Dağıtım şirketi portal URL'leri
    PORTAL_URLS = {
        'toroslar': 'https://osostoroslaredas.com.tr',
        'baskent': 'https://osostuketici.cedas.com.tr',
        'ayedas': 'https://identity.enerjisa.com.tr/auth/realms/OsosWeb',
        'gedas': 'https://ososgedas.com.tr',
        'sedas': 'https://osossedas.com.tr',
    }
    
    def __init__(self, dagitim_sirketi, kullanici_adi, sifre):
        """
        OSOS Portal Client başlat
        
        Args:
            dagitim_sirketi: 'toroslar', 'baskent', 'ayedas', 'gedas', 'sedas'
            kullanici_adi: OSOS portal kullanıcı adı
            sifre: OSOS portal şifresi
        """
        self.dagitim_sirketi = dagitim_sirketi
        self.base_url = self.PORTAL_URLS.get(dagitim_sirketi)
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre
        self.session = requests.Session()
        self.token = None
        
    def login(self):
        """OSOS Portal'a giriş yap"""
        try:
            # Her dağıtım şirketi farklı API endpoint'i kullanabilir
            # Bu örnek genel bir yapı - gerçek API'ye göre düzenlenmelidir
            
            login_url = f"{self.base_url}/api/auth/login"
            
            payload = {
                "username": self.kullanici_adi,
                "password": self.sifre
            }
            
            response = self.session.post(login_url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token') or data.get('access_token')
                print(f"✅ OSOS Portal'a giriş başarılı: {self.dagitim_sirketi}")
                return True
            else:
                print(f"❌ Giriş başarısız: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Giriş hatası: {e}")
            return False
    
    def get_sayac_verileri(self, sayac_no, baslangic_tarih=None, bitis_tarih=None):
        """
        Sayaç verilerini çek
        
        Args:
            sayac_no: Sayaç numarası
            baslangic_tarih: Başlangıç tarihi (datetime)
            bitis_tarih: Bitiş tarihi (datetime)
        """
        if not self.token:
            if not self.login():
                return None
        
        # Tarih aralığı ayarla
        if not baslangic_tarih:
            baslangic_tarih = datetime.now() - timedelta(days=1)
        if not bitis_tarih:
            bitis_tarih = datetime.now()
        
        try:
            # API endpoint (dağıtım şirketine göre değişebilir)
            api_url = f"{self.base_url}/api/olcum/saatlik"
            
            params = {
                "sayacNo": sayac_no,
                "baslangicTarihi": baslangic_tarih.strftime("%Y-%m-%d"),
                "bitisTarihi": bitis_tarih.strftime("%Y-%m-%d")
            }
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(api_url, params=params, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Veri çekme hatası: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Veri çekme hatası: {e}")
            return None
    
    def get_anlik_veri(self, sayac_no):
        """
        Anlık sayaç verisini çek (son ölçüm)
        """
        veriler = self.get_sayac_verileri(sayac_no)
        
        if veriler and len(veriler) > 0:
            # En son veriyi al
            son_veri = veriler[-1]
            
            # GUNAY formatına dönüştür
            gunay_data = {
                "cihaz_id": 1,
                "aktif_guc": son_veri.get('aktifGuc', 0),
                "reaktif_guc": son_veri.get('reaktifGuc', 0),
                "kapasitif_guc": son_veri.get('kapasitifGuc', 0),
                "gerilim": son_veri.get('gerilim', 0),
                "akim": son_veri.get('akim', 0),
                "guc_faktoru": son_veri.get('gucFaktoru', 0),
                "frekans": son_veri.get('frekans', 50.0),
                "enerji": son_veri.get('toplam', 0),
                "zaman": son_veri.get('zaman', datetime.now().isoformat())
            }
            
            return gunay_data
        
        return None

# Web Scraping ile OSOS Portal verisi çekme (API yoksa)
def osos_portal_web_scraping(dagitim_sirketi, kullanici_adi, sifre, sayac_no):
    """
    OSOS Portal'dan web scraping ile veri çek
    Not: API tercih edilir, ancak API yoksa bu yöntem kullanılabilir
    """
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Chrome driver başlat (headless mode)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        
        # Portal URL'lerinden uygun olanı seç
        portal_urls = {
            'toroslar': 'https://osostoroslaredas.com.tr',
            'baskent': 'https://osostuketici.cedas.com.tr',
            'ayedas': 'https://identity.enerjisa.com.tr/auth/realms/OsosWeb',
        }
        
        url = portal_urls.get(dagitim_sirketi)
        driver.get(url)
        
        # Login
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.send_keys(kullanici_adi)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(sifre)
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Sayfa yüklenmesini bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard"))
        )
        
        # Veri çek (sayfa yapısına göre düzenlenmelidir)
        aktif_guc_element = driver.find_element(By.ID, "aktif-guc")
        aktif_guc = float(aktif_guc_element.text.replace(',', '.'))
        
        driver.quit()
        
        return {
            "cihaz_id": 1,
            "aktif_guc": aktif_guc,
            # ... diğer veriler
        }
        
    except Exception as e:
        print(f"Web scraping hatası: {e}")
        if 'driver' in locals():
            driver.quit()
        return None

# Örnek kullanım
if __name__ == "__main__":
    print("🔌 OSOS Portal Test")
    print("=" * 50)
    
    # Portal bilgileri
    DAGITIM_SIRKETI = "toroslar"  # toroslar, baskent, ayedas, vb.
    KULLANICI_ADI = "your_username"
    SIFRE = "your_password"
    SAYAC_NO = "12345678"
    
    # Client oluştur
    client = OSOSPortalClient(DAGITIM_SIRKETI, KULLANICI_ADI, SIFRE)
    
    # Giriş yap
    if client.login():
        # Anlık veri çek
        veri = client.get_anlik_veri(SAYAC_NO)
        
        if veri:
            print("\n✅ Veri başarıyla çekildi:")
            print(json.dumps(veri, indent=2, ensure_ascii=False))
        else:
            print("\n❌ Veri çekilemedi")
    else:
        print("\n❌ Portal'a giriş yapılamadı")
