import { useState, useEffect } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import PortfolioTable from './PortfolioTable';
import RiskPieChart from './RiskPieChart';
import SectorChart from './SectorChart';
import RecommendationCards from './RecommendationCards';
import AddHoldingModal from './AddHoldingModal';
import { getHoldings, getDistribution, getRecommendations } from '../services/api';

function Dashboard({ onLogout }) {
  const [holdings, setHoldings] = useState([]);
  const [distribution, setDistribution] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const location = useLocation();

  const fetchData = async () => {
    setLoading(true);
    try {
      const [holdingsData, distData, recData] = await Promise.all([
        getHoldings(),
        getDistribution(),
        getRecommendations()
      ]);
      setHoldings(holdingsData);
      setDistribution(distData);
      setRecommendations(recData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleHoldingAdded = () => {
    setShowAddModal(false);
    fetchData();
  };

  const navItems = [
    { path: '/', label: 'Overview', icon: '📊' },
    { path: '/holdings', label: 'Holdings', icon: '💼' },
    { path: '/recommendations', label: 'Recommendations', icon: '💡' },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">Smart Folio</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowAddModal(true)}
                className="btn-primary flex items-center"
              >
                <span className="mr-1">+</span> Add Stock
              </button>
              <button
                onClick={onLogout}
                className="text-gray-600 hover:text-gray-800 font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  location.pathname === item.path
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{item.icon}</span>
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <Routes>
            <Route
              path="/"
              element={
                <OverviewPage
                  holdings={holdings}
                  distribution={distribution}
                  recommendations={recommendations}
                />
              }
            />
            <Route
              path="/holdings"
              element={
                <PortfolioTable
                  holdings={holdings}
                  onUpdate={fetchData}
                />
              }
            />
            <Route
              path="/recommendations"
              element={
                <RecommendationCards recommendations={recommendations} />
              }
            />
          </Routes>
        )}
      </main>

      {/* Add Holding Modal */}
      {showAddModal && (
        <AddHoldingModal
          onClose={() => setShowAddModal(false)}
          onAdd={handleHoldingAdded}
        />
      )}
    </div>
  );
}

function OverviewPage({ holdings, distribution, recommendations }) {
  const totalValue = distribution?.total_value || 0;
  const totalGainLoss = holdings.reduce((sum, h) => sum + (h.gain_loss || 0), 0);
  const totalGainLossPercent = holdings.length > 0
    ? holdings.reduce((sum, h) => sum + (h.gain_loss_percent || 0), 0) / holdings.length
    : 0;

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="text-sm font-medium text-gray-500 uppercase">Total Value</h3>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            ${totalValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
        </div>
        <div className="card">
          <h3 className="text-sm font-medium text-gray-500 uppercase">Total Gain/Loss</h3>
          <p className={`text-3xl font-bold mt-2 ${totalGainLoss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {totalGainLoss >= 0 ? '+' : ''}${totalGainLoss.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
        </div>
        <div className="card">
          <h3 className="text-sm font-medium text-gray-500 uppercase">Holdings</h3>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            {holdings.length} <span className="text-lg font-normal text-gray-500">stocks</span>
          </p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Risk Distribution</h3>
          <RiskPieChart distribution={distribution} />
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Sector Allocation</h3>
          <SectorChart distribution={distribution} />
        </div>
      </div>

      {/* Gap Analysis */}
      {distribution && distribution.risk_distribution.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Target vs Current Allocation</h3>
          <div className="grid grid-cols-3 gap-4">
            {['High', 'Medium', 'Low'].map((level) => {
              const current = distribution.risk_distribution.find(r => r.risk_level === level)?.percentage || 0;
              const target = distribution.target_allocation[level];
              const diff = current - target;
              return (
                <div key={level} className="text-center p-4 bg-gray-50 rounded-lg">
                  <h4 className={`font-medium ${
                    level === 'High' ? 'text-red-600' : level === 'Medium' ? 'text-yellow-600' : 'text-green-600'
                  }`}>
                    {level} Risk
                  </h4>
                  <div className="mt-2 text-2xl font-bold text-gray-800">
                    {current.toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-500">
                    Target: {target}%
                  </div>
                  <div className={`text-sm font-medium ${diff > 0 ? 'text-red-500' : diff < 0 ? 'text-blue-500' : 'text-green-500'}`}>
                    {diff > 0 ? '+' : ''}{diff.toFixed(1)}%
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Quick Recommendations Preview */}
      {recommendations && recommendations.strategies.length > 0 && (
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Strategy Recommendations</h3>
            <Link to="/recommendations" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
              View All →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {recommendations.strategies.map((strategy) => (
              <div
                key={strategy.name}
                className={`p-4 rounded-lg border-2 ${
                  strategy.risk_level === 'High'
                    ? 'border-red-200 bg-red-50'
                    : strategy.risk_level === 'Medium'
                    ? 'border-yellow-200 bg-yellow-50'
                    : 'border-green-200 bg-green-50'
                }`}
              >
                <h4 className="font-semibold text-gray-800">{strategy.name}</h4>
                <p className="text-sm text-gray-600 mt-1">{strategy.expected_return}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
