"""
OSOS Veri Toplama Script'i
Bu script OSOS sisteminden verileri okuyup GUNAY backend'ine gönderir
"""

import requests
import time
from datetime import datetime

# GUNAY Backend URL'i
BACKEND_URL = "http://localhost:3001/api"

def send_osos_data(data):
    """OSOS verisini backend'e gönder"""
    try:
        response = requests.post(f"{BACKEND_URL}/olcumler", json=data)
        if response.status_code == 201:
            print(f"✓ Veri gönderildi: {datetime.now()}")
        else:
            print(f"✗ Hata: {response.status_code}")
    except Exception as e:
        print(f"✗ Bağlantı hatası: {e}")

def read_osos_data():
    """
    OSOS sisteminden veri oku
    
    Burayı kendi OSOS sisteminize göre düzenleyin:
    - Modbus TCP kullanıyorsanız: pymodbus kütüphanesi
    - MQTT kullanıyorsanız: paho-mqtt kütüphanesi
    - REST API varsa: requests kütüphanesi
    """
    
    # ÖRNEK: OSOS REST API'den veri çekme
    # osos_url = "http://OSOS_IP_ADRESI/api/measurements"
    # response = requests.get(osos_url)
    # osos_data = response.json()
    
    # ÖRNEK: Modbus TCP ile veri okuma
    # from pymodbus.client import ModbusTcpClient
    # client = ModbusTcpClient('OSOS_IP_ADRESI', port=502)
    # aktif_guc = client.read_holding_registers(0, 1).registers[0]
    
    # Şimdilik test verisi dönelim
    data = {
        "cihaz_id": 1,
        "aktif_guc": 185.5,  # OSOS'tan okunan değer
        "reaktif_guc": 45.2,
        "kapasitif_guc": 25.8,
        "gerilim": 225.3,
        "akim": 12.5,
        "guc_faktoru": 0.92,
        "frekans": 50.0,
        "enerji": 1250.75
    }
    
    return data

def main():
    """Ana döngü - Her 5 saniyede bir veri topla"""
    print("GUNAY - OSOS Veri Toplama Servisi Başlatıldı")
    print("=" * 50)
    
    while True:
        try:
            # OSOS'tan veri oku
            data = read_osos_data()
            
            # Backend'e gönder
            send_osos_data(data)
            
            # 5 saniye bekle
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n\nServis durduruldu.")
            break
        except Exception as e:
            print(f"Hata: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
