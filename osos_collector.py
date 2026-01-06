"""
OSOS Veri Toplama Script'i
Bu script OSOS sisteminden verileri okuyup GUNAY backend'ine gönderir
"""

import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# .env dosyasından ayarları yükle
load_dotenv()

# GUNAY Backend URL'i
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:3001/api")

# OSOS Portal Ayarları
DAGITIM_SIRKETI = os.getenv("OSOS_DAGITIM_SIRKETI", "toroslar")  # toroslar, baskent, ayedas, gedas, sedas
OSOS_KULLANICI = os.getenv("OSOS_KULLANICI_ADI", "")
OSOS_SIFRE = os.getenv("OSOS_SIFRE", "")
SAYAC_NO = os.getenv("OSOS_SAYAC_NO", "")

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

def read_osos_data_portal():
    """OSOS Web Portal'dan veri çek (Önerilen Yöntem)"""
    try:
        from osos_portal_client import OSOSPortalClient
        
        if not OSOS_KULLANICI or not OSOS_SIFRE:
            print("⚠️  OSOS kullanıcı adı/şifre .env dosyasında tanımlanmamış!")
            return None
        
        # Portal client oluştur
        client = OSOSPortalClient(DAGITIM_SIRKETI, OSOS_KULLANICI, OSOS_SIFRE)
        
        # Giriş yap ve veri çek
        if client.login():
            veri = client.get_anlik_veri(SAYAC_NO)
            if veri:
                print(f"✓ OSOS Portal'dan veri çekildi")
                return veri
        
        return None
        
    except ImportError:
        print("❌ osos_portal_client.py bulunamadı!")
        return None
    except Exception as e:
        print(f"❌ Portal okuma hatası: {e}")
        return None

def read_osos_data_modbus(ip="192.168.1.100", port=502):
    """MODBUS TCP ile OSOS'tan veri oku"""
    from pymodbus.client import ModbusTcpClient
    
    client = ModbusTcpClient(ip, port=port)
    client.connect()
    
    try:
        # Register adreslerini OSOS cihazınıza göre ayarlayın
        # Örnek register adresleri (her cihaz farklı olabilir):
        aktif_guc = client.read_holding_registers(0, 2).registers  # 2 register = float
        reaktif_guc = client.read_holding_registers(2, 2).registers
        gerilim = client.read_holding_registers(4, 2).registers
        akim = client.read_holding_registers(6, 2).registers
        
        # Float dönüşümü (IEEE 754)
        import struct
        aktif_guc_val = struct.unpack('!f', struct.pack('!HH', *aktif_guc))[0]
        
        data = {
            "cihaz_id": 1,
            "aktif_guc": aktif_guc_val,
            "reaktif_guc": struct.unpack('!f', struct.pack('!HH', *reaktif_guc))[0],
            "kapasitif_guc": 25.8,
            "gerilim": struct.unpack('!f', struct.pack('!HH', *gerilim))[0],
            "akim": struct.unpack('!f', struct.pack('!HH', *akim))[0],
            "guc_faktoru": 0.92,
            "frekans": 50.0,
            "enerji": 1250.75
        }
        
        client.close()
        return data
    except Exception as e:
        print(f"Modbus okuma hatası: {e}")
        client.close()
        return None

def read_osos_data_mqtt():
    """MQTT ile OSOS'tan veri oku"""
    import paho.mqtt.client as mqtt
    import json
    
    received_data = {}
    
    def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode())
        received_data.update(data)
    
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("MQTT_BROKER_IP", 1883, 60)
    client.subscribe("osos/measurements/#")
    
    # Bir mesaj bekle
    client.loop_start()
    time.sleep(2)
    client.loop_stop()
    client.disconnect()
    
    return received_data if received_data else None

def read_osos_data_rest_api(ip="192.168.1.100", port=80):
    """REST API ile OSOS'tan veri oku"""
    try:
        # API endpoint'inizi buraya yazın
        url = f"http://{ip}:{port}/api/measurements"
        # veya
        # url = f"http://{ip}:{port}/api/instant-data"
        
        response = requests.get(url, timeout=5)
        
        if reönceliği:
    1. OSOS Web Portal (Dağıtım şirketi portalı - ÖNERİLEN)
    2. Modbus TCP (Direkt sayaç okuma)
    3. REST API (Varsa)
    4. MQTT (Varsa)
    5. Test/Demo verisi
    """
    
    # Öncelik 1: OSOS Web Portal (Toroslar EDAŞ, Başkent EDAŞ, AYEDAŞ vb.)
    veri = read_osos_data_portal()
    if veri:
        return veri
    
    # Öncelik 2: Modbus TCP (Direkt sayaç erişimi varsa)
    # veri = read_osos_data_modbus(ip="192.168.1.100", port=502)
    # if veri:
    #     return veri
    
    # Öncelik 3: REST API
    # veri = read_osos_data_rest_api(ip="192.168.1.100", port=80)
    # if veri:
    #     return veri
    
    # Öncelik 4: MQTT
    # veri = read_osos_data_mqtt()
    # if veri:
    #     return veri
    
    # Test/Demo verisi (Gerçek OSOS yoksa):
    print("⚠️  OSOS kaynağı bulunamadı, demo verisi kullanılıyor")
            print(f"API hatası: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"REST API okuma hatası: {e}")
        return None

def read_osos_data():
    """
    OSOS sisteminden veri oku - Protokol seçimi
    
    Kullanım önceliği:
    1. Yerel Okuma (Optik Port / RS-485) - ANLIK VERİ ⭐
    2. OSOS Web Portal (Dağıtım şirketi) - 15 DAKİKALIK VERİ
    3. Modbus TCP (Ağ üzerinden)
    4. REST API / MQTT
    5. Test/Demo verisi
    """
    
    # Öncelik 1: Yerel Okuma (Anlık veri için - mühendislik analizi)
    try:
        from osos_yerel_okuma import OptikPortOkuyucu, ModbusRTUOkuyucu
        
        # Optik Port (Mühürsüz, yasal, anlık veri)
        okuyucu = OptikPortOkuyucu(port='COM3')
        if okuyucu.baglan() and okuyucu.handshake():
            veri = okuyucu.veri_oku()
            okuyucu.kapat()
            if veri:
                print("✓ Yerel okuma (Optik Port) - Anlık veri")
                return veri
        
        # veya RS-485 Modbus RTU (Mühür iznine dikkat!)
        # okuyucu = ModbusRTUOkuyucu(port='COM4', slave_id=1)
        # if okuyucu.baglan():
        #     veri = okuyucu.veri_oku()
        #     okuyucu.kapat()
        #     if veri:
        #         return veri
    except:
        pass
    
    # Öncelik 2: OSOS Web Portal (Resmi veri - 15 dakikalık)
    veri = read_osos_data_portal()
    if veri:
        return veri
    
    # Öncelik 3: Modbus TCP (Ağ üzerinden)
    # veri = read_osos_data_modbus(ip="192.168.1.100", port=502)
    # if veri:
    #     return veri
    
    # Öncelik 4: REST API / MQTT
    # veri = read_osos_data_rest_api(ip="192.168.1.100", port=80)
    # if veri:
    #     return veri
    
    # Test/Demo verisi (Gerçek OSOS yoksa):
    print("⚠️  OSOS kaynağı bulunamadı, demo verisi kullanılıyor")
    import random
    data = {
        "cihaz_id": 1,
        "aktif_guc": round(random.uniform(150, 200), 2),
        "reaktif_guc": round(random.uniform(30, 50), 2),
        "kapasitif_guc": round(random.uniform(20, 30), 2),
        "gerilim": round(random.uniform(220, 230), 2),
        "akim": round(random.uniform(10, 15), 2),
        "guc_faktoru": round(random.uniform(0.85, 0.95), 2),
        "frekans": round(random.uniform(49.8, 50.2), 2),
        "enerji": round(random.uniform(1000, 1500), 2)
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
