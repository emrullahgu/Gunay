import { useEffect, useState } from 'react';
import axios from 'axios';
import { RefreshCw } from 'lucide-react';

const Canli = () => {
  const [olcum, setOlcum] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cihazId] = useState(1);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000); // Her 2 saniyede bir güncelle
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get(`/api/olcumler/son/${cihazId}`);
      setOlcum(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Veri alınamadı:', error);
      setLoading(false);
    }
  };

  if (loading || !olcum) {
    return (
      <div className="flex items-center justify-center h-96">
        <RefreshCw className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  const measurements = [
    { label: 'Aktif Güç', value: olcum.aktif_guc, unit: 'kW', color: 'text-blue-600' },
    { label: 'Reaktif Güç', value: olcum.reaktif_guc, unit: 'kVAr', color: 'text-purple-600' },
    { label: 'Kapasitif Güç', value: olcum.kapasitif_guc, unit: 'kVAr', color: 'text-pink-600' },
    { label: 'Gerilim', value: olcum.gerilim, unit: 'V', color: 'text-green-600' },
    { label: 'Akım', value: olcum.akim, unit: 'A', color: 'text-orange-600' },
    { label: 'Güç Faktörü', value: olcum.guc_faktoru, unit: 'cos φ', color: 'text-indigo-600' },
    { label: 'Enerji', value: olcum.enerji, unit: 'kWh', color: 'text-red-600' },
    { label: 'Frekans', value: olcum.frekans, unit: 'Hz', color: 'text-yellow-600' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Canlı İzleme</h1>
          <p className="text-gray-600 mt-1">{olcum.cihaz_adi} - {olcum.lokasyon}</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <RefreshCw className="w-4 h-4 animate-spin" />
          <span>Otomatik güncelleniyor</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {measurements.map((measurement, index) => (
          <div key={index} className="card">
            <h3 className="text-sm font-medium text-gray-600 mb-2">{measurement.label}</h3>
            <div className="flex items-baseline space-x-2">
              <span className={`text-4xl font-bold ${measurement.color}`}>
                {typeof measurement.value === 'number' ? measurement.value.toFixed(2) : '-'}
              </span>
              <span className="text-lg text-gray-500">{measurement.unit}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h2 className="text-xl font-bold mb-4">Son Ölçüm Zamanı</h2>
        <p className="text-2xl font-semibold text-gray-700">
          {olcum.zaman ? new Date(olcum.zaman).toLocaleString('tr-TR') : '-'}
        </p>
      </div>

      {/* Durum Göstergeleri */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="text-sm font-medium text-gray-600 mb-2">Gerilim Durumu</h3>
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${
              olcum.gerilim >= 210 && olcum.gerilim <= 240 ? 'bg-green-500' : 'bg-red-500'
            }`} />
            <span className="text-lg font-semibold">
              {olcum.gerilim >= 210 && olcum.gerilim <= 240 ? 'Normal' : 'Anormal'}
            </span>
          </div>
        </div>

        <div className="card">
          <h3 className="text-sm font-medium text-gray-600 mb-2">Frekans Durumu</h3>
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${
              olcum.frekans >= 49.5 && olcum.frekans <= 50.5 ? 'bg-green-500' : 'bg-red-500'
            }`} />
            <span className="text-lg font-semibold">
              {olcum.frekans >= 49.5 && olcum.frekans <= 50.5 ? 'Normal' : 'Anormal'}
            </span>
          </div>
        </div>

        <div className="card">
          <h3 className="text-sm font-medium text-gray-600 mb-2">Verimlilik</h3>
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${
              olcum.guc_faktoru >= 0.9 ? 'bg-green-500' : olcum.guc_faktoru >= 0.8 ? 'bg-yellow-500' : 'bg-red-500'
            }`} />
            <span className="text-lg font-semibold">
              {olcum.guc_faktoru >= 0.9 ? 'Mükemmel' : olcum.guc_faktoru >= 0.8 ? 'İyi' : 'Düşük'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Canli;
