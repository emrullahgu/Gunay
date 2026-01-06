// Mock/Demo Data Generator
export const generateMockData = () => {
  const now = new Date();
  const data = [];
  
  for (let i = 19; i >= 0; i--) {
    const time = new Date(now - i * 60000); // Her dakika
    data.push({
      id: 20 - i,
      cihaz_id: 1,
      aktif_guc: (Math.random() * 50 + 150).toFixed(2),
      reaktif_guc: (Math.random() * 20 + 30).toFixed(2),
      kapasitif_guc: (Math.random() * 15 + 20).toFixed(2),
      gerilim: (Math.random() * 10 + 220).toFixed(2),
      akim: (Math.random() * 5 + 10).toFixed(2),
      guc_faktoru: (Math.random() * 0.1 + 0.85).toFixed(2),
      frekans: (Math.random() * 0.2 + 49.9).toFixed(2),
      enerji: (Math.random() * 100 + 1000).toFixed(2),
      zaman: time.toISOString()
    });
  }
  
  return data;
};

export const mockStats = {
  total_enerji: 1234.56,
  ortalama_guc: 185.4,
  max_guc: 245.8,
  min_guc: 125.3,
  guc_faktoru: 0.92,
  toplam_kayit: 1542
};

export const mockCihazlar = [
  {
    id: 1,
    ad: "Ana Elektrik Panosu",
    konum: "Bina A - Zemin Kat",
    durum: "aktif",
    son_olcum: new Date().toISOString()
  },
  {
    id: 2,
    ad: "Üretim Hattı 1",
    konum: "Üretim Binası",
    durum: "aktif",
    son_olcum: new Date().toISOString()
  }
];

// API çağrılarını simüle et
export const mockAPI = {
  getOlcumler: () => Promise.resolve({ data: generateMockData() }),
  getDashboard: () => Promise.resolve({ data: mockStats }),
  getCihazlar: () => Promise.resolve({ data: mockCihazlar }),
  getRaporlar: (params) => Promise.resolve({ 
    data: {
      records: generateMockData(),
      summary: mockStats
    }
  })
};

export default mockAPI;
