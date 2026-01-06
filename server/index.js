import express from 'express';
import cors from 'cors';
import sqlite3 from 'sqlite3';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { mkdirSync, existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Database dizinini oluştur
const dbDir = join(__dirname, 'database');
if (!existsSync(dbDir)) {
  mkdirSync(dbDir, { recursive: true });
}

// Veritabanı bağlantısı
const db = new sqlite3.Database(join(dbDir, 'osos.db'), (err) => {
  if (err) {
    console.error('❌ Veritabanı bağlantı hatası:', err);
  } else {
    console.log('✅ Veritabanına bağlanıldı');
    initDatabase();
  }
});

// Veritabanı tablolarını oluştur
function initDatabase() {
  db.serialize(() => {
    db.run(`
      CREATE TABLE IF NOT EXISTS cihazlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cihaz_adi TEXT NOT NULL,
        seri_no TEXT UNIQUE NOT NULL,
        lokasyon TEXT,
        durum TEXT DEFAULT 'aktif',
        olusturma_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    db.run(`
      CREATE TABLE IF NOT EXISTS olcumler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cihaz_id INTEGER NOT NULL,
        aktif_guc REAL NOT NULL,
        reaktif_guc REAL,
        kapasitif_guc REAL,
        gerilim REAL,
        akim REAL,
        guc_faktoru REAL,
        enerji REAL,
        frekans REAL DEFAULT 50.0,
        zaman DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cihaz_id) REFERENCES cihazlar(id)
      )
    `);

    db.run(`
      CREATE TABLE IF NOT EXISTS raporlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cihaz_id INTEGER,
        rapor_tipi TEXT,
        baslangic_tarihi DATE,
        bitis_tarihi DATE,
        toplam_tuketim REAL,
        ortalama_guc REAL,
        maliyet REAL,
        olusturma_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cihaz_id) REFERENCES cihazlar(id)
      )
    `);

    db.run(`CREATE INDEX IF NOT EXISTS idx_olcumler_cihaz_zaman ON olcumler(cihaz_id, zaman)`);
    db.run(`CREATE INDEX IF NOT EXISTS idx_raporlar_tarih ON raporlar(baslangic_tarihi, bitis_tarihi)`);

    // Örnek cihaz ekle
    db.get('SELECT COUNT(*) as count FROM cihazlar', (err, row) => {
      if (!err && row.count === 0) {
        db.run(`INSERT INTO cihazlar (cihaz_adi, seri_no, lokasyon) VALUES (?, ?, ?)`, 
          ['Ana Bina Sayacı', 'OSOS-2024-001', 'Ana Bina - Giriş Katı']);
        console.log('✅ Örnek cihaz eklendi');
        addSampleData();
      }
    });
  });

  console.log('✅ Veritabanı tabloları oluşturuldu');
}

// Örnek veriler ekle
function addSampleData() {
  const now = new Date();
  for (let i = 0; i < 50; i++) {
    const zaman = new Date(now.getTime() - (i * 5 * 60 * 1000));
    db.run(`
      INSERT INTO olcumler (cihaz_id, aktif_guc, reaktif_guc, kapasitif_guc, gerilim, akim, guc_faktoru, enerji, frekans, zaman)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `, [
      1,
      50 + Math.random() * 100,
      10 + Math.random() * 20,
      5 + Math.random() * 10,
      220 + Math.random() * 10,
      100 + Math.random() * 50,
      0.85 + Math.random() * 0.1,
      (50 + Math.random() * 100) * 0.083,
      49.9 + Math.random() * 0.2,
      zaman.toISOString()
    ]);
  }
  console.log('✅ Örnek veriler eklendi');
}

// ==================== CİHAZLAR API ====================

// Tüm cihazları listele
app.get('/api/cihazlar', (req, res) => {
  db.all('SELECT * FROM cihazlar ORDER BY id DESC', (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// Yeni cihaz ekle
app.post('/api/cihazlar', (req, res) => {
  const { cihaz_adi, seri_no, lokasyon } = req.body;
  db.run('INSERT INTO cihazlar (cihaz_adi, seri_no, lokasyon) VALUES (?, ?, ?)',
    [cihaz_adi, seri_no, lokasyon],
    function(err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ id: this.lastID, message: 'Cihaz eklendi' });
    }
  );
});

// Cihaz detayı
app.get('/api/cihazlar/:id', (req, res) => {
  db.get('SELECT * FROM cihazlar WHERE id = ?', [req.params.id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!row) return res.status(404).json({ error: 'Cihaz bulunamadı' });
    res.json(row);
  });
});

// ==================== ÖLÇÜMLER API ====================

// Yeni ölçüm verisi ekle (OSOS'tan gelecek)
app.post('/api/olcumler', (req, res) => {
  const { cihaz_id, aktif_guc, reaktif_guc, kapasitif_guc, gerilim, akim, guc_faktoru, enerji, frekans } = req.body;
  
  db.run(`
    INSERT INTO olcumler (cihaz_id, aktif_guc, reaktif_guc, kapasitif_guc, gerilim, akim, guc_faktoru, enerji, frekans)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  `, [cihaz_id, aktif_guc, reaktif_guc || 0, kapasitif_guc || 0, gerilim, akim, guc_faktoru, enerji, frekans || 50.0],
    function(err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ id: this.lastID, message: 'Ölçüm kaydedildi' });
    }
  );
});

// Tüm ölçümleri getir (sayfalama ile)
app.get('/api/olcumler', (req, res) => {
  const { limit = 100, offset = 0, cihaz_id } = req.query;
  
  let query = `
    SELECT o.*, c.cihaz_adi, c.lokasyon 
    FROM olcumler o
    LEFT JOIN cihazlar c ON o.cihaz_id = c.id
  `;
  
  const params = [];
  if (cihaz_id) {
    query += ` WHERE o.cihaz_id = ?`;
    params.push(cihaz_id);
  }
  
  query += ` ORDER BY o.zaman DESC LIMIT ? OFFSET ?`;
  params.push(limit, offset);
  
  db.all(query, params, (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// Cihaza göre son ölçüm
app.get('/api/olcumler/son/:cihaz_id', (req, res) => {
  db.get(`
    SELECT o.*, c.cihaz_adi, c.lokasyon 
    FROM olcumler o
    LEFT JOIN cihazlar c ON o.cihaz_id = c.id
    WHERE o.cihaz_id = ?
    ORDER BY o.zaman DESC
    LIMIT 1
  `, [req.params.cihaz_id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(row || {});
  });
});

// Tarih aralığına göre ölçümler
app.get('/api/olcumler/tarih/:cihaz_id', (req, res) => {
  const { baslangic, bitis } = req.query;
  db.all(`
    SELECT * FROM olcumler
    WHERE cihaz_id = ? AND zaman BETWEEN ? AND ?
    ORDER BY zaman ASC
  `, [req.params.cihaz_id, baslangic, bitis], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// ==================== RAPORLAR API ====================

// Günlük rapor
app.get('/api/raporlar/gunluk/:cihaz_id', (req, res) => {
  const { tarih } = req.query;
  const gun = tarih || new Date().toISOString().split('T')[0];
  
  db.get(`
    SELECT 
      COUNT(*) as olcum_sayisi,
      AVG(aktif_guc) as ort_aktif_guc,
      MAX(aktif_guc) as max_aktif_guc,
      MIN(aktif_guc) as min_aktif_guc,
      AVG(gerilim) as ort_gerilim,
      AVG(akim) as ort_akim,
      AVG(guc_faktoru) as ort_guc_faktoru,
      SUM(enerji) as toplam_enerji
    FROM olcumler
    WHERE cihaz_id = ? AND DATE(zaman) = ?
  `, [req.params.cihaz_id, gun], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(row);
  });
});

// Haftalık rapor
app.get('/api/raporlar/haftalik/:cihaz_id', (req, res) => {
  db.all(`
    SELECT 
      DATE(zaman) as gun,
      COUNT(*) as olcum_sayisi,
      AVG(aktif_guc) as ort_guc,
      SUM(enerji) as gunluk_tuketim
    FROM olcumler
    WHERE cihaz_id = ? AND zaman >= datetime('now', '-7 days')
    GROUP BY DATE(zaman)
    ORDER BY gun DESC
  `, [req.params.cihaz_id], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// Aylık rapor
app.get('/api/raporlar/aylik/:cihaz_id', (req, res) => {
  const { yil, ay } = req.query;
  const yilAy = `${yil || new Date().getFullYear()}-${(ay || new Date().getMonth() + 1).toString().padStart(2, '0')}`;
  
  db.all(`
    SELECT 
      DATE(zaman) as gun,
      AVG(aktif_guc) as ort_guc,
      MAX(aktif_guc) as max_guc,
      SUM(enerji) as gunluk_tuketim
    FROM olcumler
    WHERE cihaz_id = ? AND strftime('%Y-%m', zaman) = ?
    GROUP BY DATE(zaman)
    ORDER BY gun ASC
  `, [req.params.cihaz_id, yilAy], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// Dashboard özet istatistikleri
app.get('/api/dashboard/:cihaz_id', (req, res) => {
  db.get(`
    SELECT 
      (SELECT aktif_guc FROM olcumler WHERE cihaz_id = ? ORDER BY zaman DESC LIMIT 1) as anlik_guc,
      (SELECT AVG(aktif_guc) FROM olcumler WHERE cihaz_id = ? AND zaman >= datetime('now', '-1 day')) as gunluk_ort,
      (SELECT SUM(enerji) FROM olcumler WHERE cihaz_id = ? AND zaman >= datetime('now', '-1 day')) as gunluk_tuketim,
      (SELECT AVG(guc_faktoru) FROM olcumler WHERE cihaz_id = ? AND zaman >= datetime('now', '-1 day')) as gunluk_verimlilik
  `, [req.params.cihaz_id, req.params.cihaz_id, req.params.cihaz_id, req.params.cihaz_id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(row);
  });
});

// ==================== SERVER ====================

app.listen(PORT, () => {
  console.log(`🚀 OSOS API Server çalışıyor: http://localhost:${PORT}`);
  console.log(`📊 Veritabanı: ${join(__dirname, 'database', 'osos.db')}`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  db.close((err) => {
    if (err) console.error(err.message);
    console.log('\n✅ Veritabanı bağlantısı kapatıldı');
    process.exit(0);
  });
});
