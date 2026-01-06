"""
OSOS Protokol Tespit Aracı
Bu script OSOS cihazına bağlanıp protokolü tespit etmeye çalışır
"""

import socket
import requests
from datetime import datetime

def test_modbus_tcp(ip, port=502):
    """Modbus TCP protokolünü test et"""
    print(f"\n🔌 Modbus TCP test ediliyor: {ip}:{port}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Modbus TCP portu AÇIK! (Port {port})")
            print("   → OSOS cihazınız Modbus TCP kullanıyor olabilir")
            return True
        else:
            print(f"❌ Modbus TCP portu kapalı")
            return False
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_http_api(ip, ports=[80, 8080, 8081, 443]):
    """HTTP REST API test et"""
    print(f"\n🌐 HTTP/REST API test ediliyor: {ip}")
    for port in ports:
        try:
            url = f"http://{ip}:{port}"
            print(f"   Deneniyor: {url}")
            response = requests.get(url, timeout=3)
            print(f"✅ HTTP API BULUNDU! Port {port}")
            print(f"   Status: {response.status_code}")
            print(f"   → OSOS cihazınız REST API kullanıyor olabilir")
            return True, port
        except requests.exceptions.ConnectionError:
            continue
        except Exception as e:
            continue
    
    print(f"❌ HTTP API bulunamadı")
    return False, None

def test_mqtt(ip, port=1883):
    """MQTT protokolünü test et"""
    print(f"\n📡 MQTT test ediliyor: {ip}:{port}")
    try:
        import paho.mqtt.client as mqtt
        
        client = mqtt.Client()
        client.connect(ip, port, 60)
        print(f"✅ MQTT bağlantısı BAŞARILI! (Port {port})")
        print("   → OSOS cihazınız MQTT kullanıyor olabilir")
        client.disconnect()
        return True
    except ImportError:
        print("⚠️  paho-mqtt yüklü değil. Yüklemek için: pip install paho-mqtt")
        return False
    except Exception as e:
        print(f"❌ MQTT bağlantısı başarısız: {e}")
        return False

def scan_common_ports(ip):
    """Yaygın portları tara"""
    print(f"\n🔍 Port taraması yapılıyor: {ip}")
    common_ports = {
        80: "HTTP",
        443: "HTTPS",
        502: "Modbus TCP",
        1883: "MQTT",
        8080: "HTTP Alt",
        8883: "MQTT SSL",
        8081: "HTTP Alt 2",
        4840: "OPC UA",
        20000: "DNP3"
    }
    
    open_ports = []
    for port, service in common_ports.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                print(f"   ✅ Port {port} AÇIK - {service}")
                open_ports.append((port, service))
        except:
            pass
    
    if not open_ports:
        print("   ❌ Açık port bulunamadı")
    
    return open_ports

def detect_osos_protocol(ip_address):
    """OSOS protokolünü otomatik tespit et"""
    print("=" * 60)
    print("🔬 GUNAY - OSOS Protokol Tespit Aracı")
    print("=" * 60)
    print(f"📍 Hedef IP: {ip_address}")
    print(f"⏰ Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = {
        'modbus': False,
        'http': False,
        'mqtt': False,
        'open_ports': []
    }
    
    # Port taraması
    results['open_ports'] = scan_common_ports(ip_address)
    
    # Modbus TCP test
    results['modbus'] = test_modbus_tcp(ip_address)
    
    # HTTP API test
    results['http'], http_port = test_http_api(ip_address)
    
    # MQTT test
    results['mqtt'] = test_mqtt(ip_address)
    
    # Sonuç özeti
    print("\n" + "=" * 60)
    print("📊 SONUÇ ÖZETİ")
    print("=" * 60)
    
    if results['modbus']:
        print("✅ Modbus TCP protokolü tespit edildi!")
        print("   Kullanım: osos_collector.py içinde Modbus bölümünü aktif edin")
        print("   Kütüphane: pip install pymodbus")
    
    if results['http']:
        print("✅ HTTP REST API tespit edildi!")
        print("   Kullanım: osos_collector.py içinde REST API bölümünü aktif edin")
        print("   Kütüphane: pip install requests")
    
    if results['mqtt']:
        print("✅ MQTT protokolü tespit edildi!")
        print("   Kullanım: osos_collector.py içinde MQTT bölümünü aktif edin")
        print("   Kütüphane: pip install paho-mqtt")
    
    if not any([results['modbus'], results['http'], results['mqtt']]):
        print("⚠️  Bilinen protokol tespit edilemedi!")
        print("\n💡 Öneriler:")
        print("   1. OSOS cihaz dokümantasyonunu kontrol edin")
        print("   2. IT departmanınızla görüşün")
        print("   3. Cihaz IP adresini doğrulayın")
        print("   4. Firewall ayarlarını kontrol edin")
    
    print("=" * 60)
    return results

if __name__ == "__main__":
    print("\n🎯 OSOS Cihaz IP Adresini Girin:")
    print("   Örnek: 192.168.1.100")
    print("   Veya cihaz hostname'i: osos-device.local")
    print()
    
    ip = input("IP Adresi: ").strip()
    
    if ip:
        detect_osos_protocol(ip)
    else:
        print("❌ IP adresi girilmedi!")
        print("\nÖrnek kullanım:")
        print("  python osos_protocol_detector.py")
        print("  IP Adresi: 192.168.1.100")
