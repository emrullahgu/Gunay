import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Cihazlar from './pages/Cihazlar';
import Raporlar from './pages/Raporlar';
import Canli from './pages/Canli';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/canli" element={<Canli />} />
            <Route path="/cihazlar" element={<Cihazlar />} />
            <Route path="/raporlar" element={<Raporlar />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
