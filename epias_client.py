"""
EPİAŞ (Enerji Piyasaları İşletme A.Ş.) Şeffaflık Platformu Entegrasyonu
Türkiye elektrik piyasası verilerini çeker
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class EPIASClient:
    """EPİAŞ Şeffaflık Platformu API Client"""
    
    BASE_URL = "https://seffaflik.epias.com.tr/transparency/service"
    
    def __init__(self, username=None, password=None):
        """
        EPİAŞ Client başlat
        
        Not: Bazı veriler kayıt gerektirmez (halka açık)
             API Key gerektiren veriler için kayıt gerekir
        """
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.token = None
        
        if username and password:
            self.login()
    
    def login(self):
        """EPİAŞ'a giriş yap (API Key gerektiren veriler için)"""
        try:
            login_url = f"{self.BASE_URL}/oauth/token"
            
            payload = {
                "username": self.username,
                "password": self.password,
                "grant_type": "password"
            }
            
            response = self.session.post(login_url, data=payload)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access_token')
                print("✅ EPİAŞ API'ye giriş başarılı")
                return True
            else:
                print(f"❌ EPİAŞ giriş başarısız: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ EPİAŞ giriş hatası: {e}")
            return False
    
    def get_headers(self):
        """API headers"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def get_realtime_generation(self):
        """
        Gerçek Zamanlı Üretim Verileri
        Kaynak bazlı (termik, hidrolik, rüzgar, güneş vb.) anlık üretim
        """
        try:
            endpoint = f"{self.BASE_URL}/production/realtime-generation"
            
            params = {
                "startDate": datetime.now().strftime("%Y-%m-%d"),
                "endDate": datetime.now().strftime("%Y-%m-%d")
            }
            
            response = self.session.get(endpoint, params=params, headers=self.get_headers())
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Veri çekme hatası: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ API hatası: {e}")
            return None
    
    def get_consumption_data(self, start_date=None, end_date=None):
        """
        Türkiye Toplam Tüketim Verisi
        Saatlik elektrik tüketimi
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=1)
        if not end_date:
            end_date = datetime.now()
        
        try:
            endpoint = f"{self.BASE_URL}/consumption/real-time-consumption"
            
            params = {
                "startDate": start_date.strftime("%Y-%m-%d"),
                "endDate": end_date.strftime("%Y-%m-%d")
            }
            
            response = self.session.get(endpoint, params=params, headers=self.get_headers())
            
            if response.status_code == 200:
                data = response.json()
                return data.get('body', {}).get('hourlyConsumptions', [])
            else:
                return None
        except Exception as e:
            print(f"❌ Tüketim verisi hatası: {e}")
            return None
    
    def get_market_price(self, date=None):
        """
        Piyasa Takas Fiyatı (PTF)
        Saatlik elektrik fiyatları (TL/MWh)
        """
        if not date:
            date = datetime.now()
        
        try:
            endpoint = f"{self.BASE_URL}/market/mcp"
            
            params = {
                "startDate": date.strftime("%Y-%m-%d"),
                "endDate": date.strftime("%Y-%m-%d")
            }
            
            response = self.session.get(endpoint, params=params, headers=self.get_headers())
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"❌ Fiyat verisi hatası: {e}")
            return None
    
    def get_renewable_generation(self):
        """
        Yenilenebilir Enerji Üretimi
        Rüzgar, güneş, hidrolik toplam üretim
        """
        try:
            endpoint = f"{self.BASE_URL}/production/renewable-sm"
            
            params = {
                "startDate": datetime.now().strftime("%Y-%m-%d"),
                "endDate": datetime.now().strftime("%Y-%m-%d")
            }
            
            response = self.session.get(endpoint, params=params, headers=self.get_headers())
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"❌ Yenilenebilir enerji verisi hatası: {e}")
            return None

# GUNAY için veri dönüştürücü
def epias_to_gunay_format(epias_data):
    """
    EPİAŞ verisini GUNAY formatına dönüştür
    Not: EPİAŞ Türkiye geneli verisi, GUNAY'daki sayaç verisi farklı
    Bu fonksiyon karşılaştırma ve benchmark için kullanılabilir
    """
    if not epias_data:
        return None
    
    try:
        # Örnek: Tüketim verisini dönüştür
        latest = epias_data[-1] if isinstance(epias_data, list) else epias_data
        
        gunay_data = {
            "cihaz_id": 0,  # 0 = EPİAŞ (Türkiye Geneli)
            "aktif_guc": latest.get('consumption', 0),  # MW cinsinden
            "reaktif_guc": 0,
            "kapasitif_guc": 0,
            "gerilim": 380,  # OG/AG için varsayılan
            "akim": 0,
            "guc_faktoru": 0.95,  # Türkiye ortalaması
            "frekans": 50.0,
            "enerji": latest.get('consumption', 0),
            "zaman": latest.get('date', datetime.now().isoformat()),
            "kaynak": "EPİAŞ",
            "aciklama": "Türkiye Geneli Tüketim"
        }
        
        return gunay_data
    except Exception as e:
        print(f"❌ Veri dönüştürme hatası: {e}")
        return None

# Web Scraping yöntemi (API gerektirmez)
def scrape_epias_public_data():
    """
    EPİAŞ Şeffaflık Platformundan halka açık veriyi çek
    API Key gerektirmez
    """
    try:
        from bs4 import BeautifulSoup
        
        # Gerçek zamanlı üretim sayfası
        url = "https://seffaflik.epias.com.tr/transparency/uretim/gercek-zamanli-uretim.xhtml"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Veriyi parse et (sayfa yapısına göre düzenlenmelidir)
        # Bu kısım EPİAŞ'ın sayfa yapısına göre özelleştirilmelidir
        
        print("✅ EPİAŞ verisi web'den çekildi")
        return soup
        
    except Exception as e:
        print(f"❌ Web scraping hatası: {e}")
        return None

# Örnek kullanım
if __name__ == "__main__":
    print("⚡ EPİAŞ Şeffaflık Platformu Test")
    print("=" * 60)
    
    # Client oluştur (halka açık veriler için username/password gerekmez)
    client = EPIASClient()
    
    # 1. Gerçek zamanlı üretim
    print("\n📊 Gerçek Zamanlı Üretim:")
    generation = client.get_realtime_generation()
    if generation:
        print(json.dumps(generation, indent=2, ensure_ascii=False))
    
    # 2. Tüketim verisi
    print("\n📈 Türkiye Toplam Tüketim:")
    consumption = client.get_consumption_data()
    if consumption:
        print(f"Son tüketim: {consumption[-1] if consumption else 'Veri yok'}")
    
    # 3. Piyasa fiyatı
    print("\n💰 Piyasa Takas Fiyatı (PTF):")
    price = client.get_market_price()
    if price:
        print(json.dumps(price, indent=2, ensure_ascii=False))
    
    # 4. Yenilenebilir enerji
    print("\n🌱 Yenilenebilir Enerji Üretimi:")
    renewable = client.get_renewable_generation()
    if renewable:
        print(json.dumps(renewable, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("💡 EPİAŞ verileri Türkiye geneli içindir")
    print("   Tesisinize özel veriler için OSOS kullanın")
