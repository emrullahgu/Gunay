import { useEffect, useState } from 'react';
import axios from 'axios';
import { Zap, TrendingUp, Activity, DollarSign } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [recentData, setRecentData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cihazId] = useState(1); // Varsayılan cihaz ID

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Her 5 saniyede bir güncelle
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, dataRes] = await Promise.all([
        axios.get(`/api/dashboard/${cihazId}`),
        axios.get(`/api/olcumler?limit=20&cihaz_id=${cihazId}`)
      ]);
      
      setStats(statsRes.data);
      setRecentData(dataRes.data.reverse());
      setLoading(false);
    } catch (error) {
      console.error('Veri alınamadı:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-xl text-gray-600">Yükleniyor...</div>
      </div>
    );
  }

  const statCards = [
    {
      title: 'Anlık Güç',
      value: `${(stats?.anlik_guc || 0).toFixed(2)} kW`,
      icon: Zap,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50',
    },
    {
      title: 'Günlük Ortalama',
      value: `${(stats?.gunluk_ort || 0).toFixed(2)} kW`,
      icon: TrendingUp,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Günlük Tüketim',
      value: `${(stats?.gunluk_tuketim || 0).toFixed(2)} kWh`,
      icon: Activity,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      title: 'Verimlilik',
      value: `${((stats?.gunluk_verimlilik || 0) * 100).toFixed(1)}%`,
      icon: DollarSign,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
        <div className="text-sm text-gray-500">
          Son güncelleme: {new Date().toLocaleTimeString('tr-TR')}
        </div>
      </div>

      {/* İstatistik Kartları */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
                </div>
                <div className={`${stat.bgColor} ${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Grafikler */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Güç Grafiği */}
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Aktif Güç (kW)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={recentData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="zaman" 
                tickFormatter={(value) => new Date(value).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })}
              />
              <YAxis />
              <Tooltip 
                labelFormatter={(value) => new Date(value).toLocaleTimeString('tr-TR')}
              />
              <Legend />
              <Line type="monotone" dataKey="aktif_guc" stroke="#0ea5e9" name="Aktif Güç" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Gerilim ve Akım */}
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Gerilim & Akım</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={recentData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="zaman" 
                tickFormatter={(value) => new Date(value).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })}
              />
              <YAxis />
              <Tooltip 
                labelFormatter={(value) => new Date(value).toLocaleTimeString('tr-TR')}
              />
              <Legend />
              <Line type="monotone" dataKey="gerilim" stroke="#10b981" name="Gerilim (V)" />
              <Line type="monotone" dataKey="akim" stroke="#f59e0b" name="Akım (A)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Güç Faktörü */}
      <div className="card">
        <h2 className="text-xl font-bold mb-4">Güç Faktörü (cos φ)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={recentData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="zaman" 
              tickFormatter={(value) => new Date(value).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })}
            />
            <YAxis domain={[0, 1]} />
            <Tooltip 
              labelFormatter={(value) => new Date(value).toLocaleTimeString('tr-TR')}
            />
            <Legend />
            <Bar dataKey="guc_faktoru" fill="#8b5cf6" name="Güç Faktörü" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Dashboard;
