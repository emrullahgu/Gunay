import { useState, useEffect } from 'react';
import axios from 'axios';
import { Calendar, Download, TrendingUp } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { config } from '../config';
import { generateMockData } from '../mockData';

const Raporlar = () => {
  const [raporTipi, setRaporTipi] = useState('haftalik');
  const [raporData, setRaporData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [cihazId] = useState(1);

  useEffect(() => {
    fetchRapor();
  }, [raporTipi]);

  const fetchRapor = async () => {
    setLoading(true);
    try {
      if (config.useMockData) {
        setRaporData(generateMockData());
      } else {
        const response = await axios.get(`/api/raporlar/${raporTipi}/${cihazId}`);
        setRaporData(response.data);
      }
      setLoading(false);
    } catch (error) {
      console.error('Rapor alınamadı:', error);
      setRaporData(generateMockData());
      setLoading(false);
    }
  };

  const exportToExcel = () => {
    // Excel export fonksiyonu (basit CSV)
    const csvContent = [
      ['Tarih', 'Ortalama Güç (kW)', 'Günlük Tüketim (kWh)'],
      ...raporData.map(item => [
        item.gun,
        item.ort_guc?.toFixed(2) || '0',
        item.gunluk_tuketim?.toFixed(2) || '0'
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `osos_rapor_${raporTipi}_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  const toplamTuketim = raporData.reduce((sum, item) => sum + (item.gunluk_tuketim || 0), 0);
  const ortalamaGuc = raporData.length > 0 
    ? raporData.reduce((sum, item) => sum + (item.ort_guc || 0), 0) / raporData.length 
    : 0;
  const maxGuc = Math.max(...raporData.map(item => item.max_guc || item.ort_guc || 0));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-800">Raporlar</h1>
        <button 
          onClick={exportToExcel}
          disabled={raporData.length === 0}
          className="btn-primary flex items-center space-x-2"
        >
          <Download className="w-5 h-5" />
          <span>Excel'e Aktar</span>
        </button>
      </div>

      {/* Rapor Tipi Seçimi */}
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <Calendar className="w-5 h-5 text-gray-600" />
          <h2 className="text-lg font-semibold">Rapor Dönemi</h2>
        </div>
        <div className="flex space-x-3">
          {['gunluk', 'haftalik', 'aylik'].map((tip) => (
            <button
              key={tip}
              onClick={() => setRaporTipi(tip)}
              className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                raporTipi === tip
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {tip === 'gunluk' ? 'Günlük' : tip === 'haftalik' ? 'Haftalık' : 'Aylık'}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-xl text-gray-600">Rapor hazırlanıyor...</div>
        </div>
      ) : raporData.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-gray-600 text-lg">Bu dönem için veri bulunmuyor</p>
        </div>
      ) : (
        <>
          {/* Özet İstatistikler */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Toplam Tüketim</h3>
              <div className="flex items-baseline space-x-2">
                <span className="text-3xl font-bold text-blue-600">
                  {toplamTuketim.toFixed(2)}
                </span>
                <span className="text-lg text-gray-500">kWh</span>
              </div>
            </div>

            <div className="card">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Ortalama Güç</h3>
              <div className="flex items-baseline space-x-2">
                <span className="text-3xl font-bold text-green-600">
                  {ortalamaGuc.toFixed(2)}
                </span>
                <span className="text-lg text-gray-500">kW</span>
              </div>
            </div>

            <div className="card">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Maksimum Güç</h3>
              <div className="flex items-baseline space-x-2">
                <span className="text-3xl font-bold text-red-600">
                  {maxGuc.toFixed(2)}
                </span>
                <span className="text-lg text-gray-500">kW</span>
              </div>
            </div>
          </div>

          {/* Günlük Tüketim Grafiği */}
          <div className="card">
            <h2 className="text-xl font-bold mb-4">Günlük Tüketim (kWh)</h2>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={raporData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="gun" 
                  tickFormatter={(value) => new Date(value).toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit' })}
                />
                <YAxis />
                <Tooltip 
                  labelFormatter={(value) => new Date(value).toLocaleDateString('tr-TR')}
                  formatter={(value) => [value.toFixed(2), 'kWh']}
                />
                <Legend />
                <Bar dataKey="gunluk_tuketim" fill="#0ea5e9" name="Tüketim" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Ortalama Güç Grafiği */}
          <div className="card">
            <h2 className="text-xl font-bold mb-4">Ortalama Güç (kW)</h2>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={raporData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="gun" 
                  tickFormatter={(value) => new Date(value).toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit' })}
                />
                <YAxis />
                <Tooltip 
                  labelFormatter={(value) => new Date(value).toLocaleDateString('tr-TR')}
                  formatter={(value) => [value?.toFixed(2) || '0', 'kW']}
                />
                <Legend />
                <Line type="monotone" dataKey="ort_guc" stroke="#10b981" strokeWidth={2} name="Ortalama Güç" />
                {raporData[0]?.max_guc !== undefined && (
                  <Line type="monotone" dataKey="max_guc" stroke="#ef4444" strokeWidth={2} name="Maksimum Güç" />
                )}
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Tablo */}
          <div className="card">
            <h2 className="text-xl font-bold mb-4">Detaylı Veriler</h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Tarih</th>
                    <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Ölçüm Sayısı</th>
                    <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Ort. Güç (kW)</th>
                    <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Tüketim (kWh)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {raporData.map((item, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm text-gray-800">
                        {new Date(item.gun).toLocaleDateString('tr-TR')}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-800 text-right">
                        {item.olcum_sayisi || '-'}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-800 text-right">
                        {item.ort_guc?.toFixed(2) || '0.00'}
                      </td>
                      <td className="px-4 py-3 text-sm font-semibold text-gray-900 text-right">
                        {item.gunluk_tuketim?.toFixed(2) || '0.00'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Raporlar;
