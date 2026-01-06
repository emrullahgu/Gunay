"""
OSOS Yerel Okuma Modülü - Optik Port ve RS-485
Sayaçtan doğrudan anlık veri okuma için
"""

import serial
import time
from datetime import datetime

class OptikPortOkuyucu:
    """
    IEC 62056-21 (IEC 1107) Optik Port Okuyucu
    
    Donanım: USB Optik Okuyucu (Mıknatıslı prob)
    Protokol: IEC 62056-21 (DLMS/COSEM)
    Baud Rate: 300, 9600 (sayaca bağlı)
    """
    
    def __init__(self, port='COM3', baudrate=300):
        """
        Args:
            port: Seri port (Windows: COM3, Linux: /dev/ttyUSB0)
            baudrate: Başlangıç baud rate (genellikle 300)
        """
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        
    def baglan(self):
        """Optik porta bağlan"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.SEVENBITS,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE,
                timeout=2
            )
            print(f"✅ Optik port açıldı: {self.port}")
            return True
        except Exception as e:
            print(f"❌ Port açma hatası: {e}")
            return False
    
    def handshake(self):
        """IEC 62056-21 handshake protokolü"""
        try:
            # 1. İstek mesajı gönder
            self.serial.write(b'/?!\r\n')
            time.sleep(0.5)
            
            # 2. Sayaç kimliğini oku
            response = self.serial.readline().decode('ascii')
            print(f"Sayaç ID: {response}")
            
            # 3. ACK gönder ve veri moduna geç
            # Baud rate değişimi burada yapılabilir (Mode C)
            self.serial.write(b'\x06000\r\n')
            time.sleep(0.5)
            
            return True
            
        except Exception as e:
            print(f"❌ Handshake hatası: {e}")
            return False
    
    def veri_oku(self):
        """Sayaçtan veri setini oku"""
        try:
            veri_seti = {}
            
            while True:
                line = self.serial.readline().decode('ascii').strip()
                
                if line == '!' or not line:  # Veri sonu
                    break
                
                # OBIS kodları ile veri parse et
                # Örnek: 1.8.0(001234.56*kWh) -> Aktif Enerji
                if '(' in line:
                    obis_code, value = line.split('(')
                    value = value.rstrip(')')
                    veri_seti[obis_code] = value
            
            return self._obis_to_gunay_format(veri_seti)
            
        except Exception as e:
            print(f"❌ Veri okuma hatası: {e}")
            return None
    
    def _obis_to_gunay_format(self, obis_data):
        """OBIS kodlarını GUNAY formatına dönüştür"""
        
        # OBIS Kod Referansları (IEC 62056-21)
        # 1.8.0 = Toplam Aktif Enerji (Import)
        # 2.8.0 = Toplam Aktif Enerji (Export)
        # 3.8.0 = Toplam Reaktif Enerji (Import)
        # 4.8.0 = Toplam Reaktif Enerji (Export)
        # 1.7.0 = Anlık Aktif Güç
        # 3.7.0 = Anlık Reaktif Güç
        # 32.7.0 = Gerilim L1
        # 52.7.0 = Gerilim L2
        # 72.7.0 = Gerilim L3
        # 31.7.0 = Akım L1
        
        def parse_value(val):
            """Değeri sayıya çevir (1234.56*kWh -> 1234.56)"""
            return float(val.split('*')[0]) if val else 0.0
        
        gunay_data = {
            "cihaz_id": 1,
            "aktif_guc": parse_value(obis_data.get('1.7.0', '0')),
            "reaktif_guc": parse_value(obis_data.get('3.7.0', '0')),
            "kapasitif_guc": parse_value(obis_data.get('4.7.0', '0')),
            "gerilim": parse_value(obis_data.get('32.7.0', '0')),
            "akim": parse_value(obis_data.get('31.7.0', '0')),
            "guc_faktoru": parse_value(obis_data.get('13.7.0', '0.9')),
            "frekans": 50.0,  # Genellikle OBIS kodunda yok
            "enerji": parse_value(obis_data.get('1.8.0', '0')),
            "zaman": datetime.now().isoformat()
        }
        
        return gunay_data
    
    def kapat(self):
        """Seri portu kapat"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("✅ Optik port kapatıldı")


class ModbusRTUOkuyucu:
    """
    RS-485 Modbus RTU ile sayaç okuma
    
    Donanım: USB-RS485 dönüştürücü
    Protokol: Modbus RTU
    Sayaçlar: Makel, Luna, Köhler, ABB, Schneider
    """
    
    def __init__(self, port='COM4', baudrate=9600, slave_id=1):
        """
        Args:
            port: Seri port
            baudrate: Genellikle 9600, 19200
            slave_id: Modbus slave adresi (sayaç ID'si)
        """
        from pymodbus.client import ModbusSerialClient
        
        self.client = ModbusSerialClient(
            method='rtu',
            port=port,
            baudrate=baudrate,
            timeout=3,
            parity='N',
            stopbits=1,
            bytesize=8
        )
        self.slave_id = slave_id
    
    def baglan(self):
        """Modbus RTU bağlantısı"""
        try:
            self.client.connect()
            print(f"✅ Modbus RTU bağlantısı kuruldu")
            return True
        except Exception as e:
            print(f"❌ Modbus bağlantı hatası: {e}")
            return False
    
    def veri_oku(self):
        """
        Modbus register'lardan veri oku
        
        Not: Register adresleri sayaç modeline göre değişir!
        Sayaç dokümantasyonuna bakın.
        """
        try:
            # Örnek register adresleri (Genel kullanım)
            # Her sayaç farklı register haritası kullanır!
            
            # 2 register = 1 float (IEEE 754)
            import struct
            
            # Aktif Güç (Register 0-1)
            aktif_guc_regs = self.client.read_holding_registers(0, 2, unit=self.slave_id)
            aktif_guc = struct.unpack('!f', struct.pack('!HH', *aktif_guc_regs.registers))[0]
            
            # Reaktif Güç (Register 2-3)
            reaktif_guc_regs = self.client.read_holding_registers(2, 2, unit=self.slave_id)
            reaktif_guc = struct.unpack('!f', struct.pack('!HH', *reaktif_guc_regs.registers))[0]
            
            # Gerilim (Register 4-5)
            gerilim_regs = self.client.read_holding_registers(4, 2, unit=self.slave_id)
            gerilim = struct.unpack('!f', struct.pack('!HH', *gerilim_regs.registers))[0]
            
            # Akım (Register 6-7)
            akim_regs = self.client.read_holding_registers(6, 2, unit=self.slave_id)
            akim = struct.unpack('!f', struct.pack('!HH', *akim_regs.registers))[0]
            
            gunay_data = {
                "cihaz_id": 1,
                "aktif_guc": round(aktif_guc, 2),
                "reaktif_guc": round(reaktif_guc, 2),
                "kapasitif_guc": 0,
                "gerilim": round(gerilim, 2),
                "akim": round(akim, 2),
                "guc_faktoru": 0.92,
                "frekans": 50.0,
                "enerji": 0,
                "zaman": datetime.now().isoformat()
            }
            
            return gunay_data
            
        except Exception as e:
            print(f"❌ Modbus okuma hatası: {e}")
            return None
    
    def kapat(self):
        """Bağlantıyı kapat"""
        self.client.close()
        print("✅ Modbus bağlantısı kapatıldı")


# Test fonksiyonu
if __name__ == "__main__":
    import sys
    
    print("🔌 OSOS Yerel Okuma Test")
    print("=" * 50)
    print("1. Optik Port (IEC 62056-21)")
    print("2. Modbus RTU (RS-485)")
    print()
    
    secim = input("Seçim (1/2): ").strip()
    
    if secim == "1":
        port = input("Seri Port (örn: COM3): ").strip() or "COM3"
        
        okuyucu = OptikPortOkuyucu(port=port)
        
        if okuyucu.baglan():
            if okuyucu.handshake():
                veri = okuyucu.veri_oku()
                if veri:
                    print("\n✅ Veri başarıyla okundu:")
                    print(veri)
            okuyucu.kapat()
    
    elif secim == "2":
        port = input("Seri Port (örn: COM4): ").strip() or "COM4"
        slave_id = int(input("Modbus Slave ID (1): ").strip() or "1")
        
        okuyucu = ModbusRTUOkuyucu(port=port, slave_id=slave_id)
        
        if okuyucu.baglan():
            veri = okuyucu.veri_oku()
            if veri:
                print("\n✅ Veri başarıyla okundu:")
                print(veri)
            okuyucu.kapat()
    
    else:
        print("❌ Geçersiz seçim!")
