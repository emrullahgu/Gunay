import { useEffect, useState } from 'react';
import axios from 'axios';
import { Plus, Power, MapPin } from 'lucide-react';
import { config } from '../config';
import { mockCihazlar } from '../mockData';

const Cihazlar = () => {
  const [cihazlar, setCihazlar] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    cihaz_adi: '',
    seri_no: '',
    lokasyon: ''
  });

  useEffect(() => {
    fetchCihazlar();
  }, []);

  const fetchCihazlar = async () => {
    try {
      if (config.useMockData) {
        setCihazlar(mockCihazlar);
      } else {
        const response = await axios.get('/api/cihazlar');
        setCihazlar(response.data);
      }
      setLoading(false);
    } catch (error) {
      console.error('Cihazlar alınamadı:', error);
      setCihazlar(mockCihazlar);
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/cihazlar', formData);
      setShowModal(false);
      setFormData({ cihaz_adi: '', seri_no: '', lokasyon: '' });
      fetchCihazlar();
    } catch (error) {
      console.error('Cihaz eklenemedi:', error);
      alert('Cihaz eklenirken bir hata oluştu!');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-xl text-gray-600">Yükleniyor...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-800">Cihazlar</h1>
        <button 
          onClick={() => setShowModal(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Yeni Cihaz</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cihazlar.map((cihaz) => (
          <div key={cihaz.id} className="card hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-xl font-bold text-gray-800">{cihaz.cihaz_adi}</h3>
                <p className="text-sm text-gray-500">Seri No: {cihaz.seri_no}</p>
              </div>
              <div className={`px-2 py-1 rounded text-xs font-semibold ${
                cihaz.durum === 'aktif' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}>
                {cihaz.durum === 'aktif' ? 'Aktif' : 'Pasif'}
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center space-x-2 text-gray-600">
                <MapPin className="w-4 h-4" />
                <span className="text-sm">{cihaz.lokasyon}</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-600">
                <Power className="w-4 h-4" />
                <span className="text-sm">
                  Eklenme: {new Date(cihaz.olusturma_tarihi).toLocaleDateString('tr-TR')}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {cihazlar.length === 0 && (
        <div className="card text-center py-12">
          <p className="text-gray-600 text-lg mb-4">Henüz kayıtlı cihaz yok</p>
          <button 
            onClick={() => setShowModal(true)}
            className="btn-primary inline-flex items-center space-x-2"
          >
            <Plus className="w-5 h-5" />
            <span>İlk Cihazı Ekle</span>
          </button>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">Yeni Cihaz Ekle</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cihaz Adı
                </label>
                <input
                  type="text"
                  required
                  value={formData.cihaz_adi}
                  onChange={(e) => setFormData({ ...formData, cihaz_adi: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Örn: Ana Bina Sayacı"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Seri Numarası
                </label>
                <input
                  type="text"
                  required
                  value={formData.seri_no}
                  onChange={(e) => setFormData({ ...formData, seri_no: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Örn: OSOS-2024-001"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Lokasyon
                </label>
                <input
                  type="text"
                  required
                  value={formData.lokasyon}
                  onChange={(e) => setFormData({ ...formData, lokasyon: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Örn: Ana Bina - Giriş Katı"
                />
              </div>

              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="btn-secondary flex-1"
                >
                  İptal
                </button>
                <button
                  type="submit"
                  className="btn-primary flex-1"
                >
                  Kaydet
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Cihazlar;
