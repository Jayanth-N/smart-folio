import { useState, useEffect } from 'react';
import { addHolding, getRiskSuggestion } from '../services/api';

function AddHoldingModal({ onClose, onAdd }) {
  const [formData, setFormData] = useState({
    symbol: '',
    quantity: '',
    purchase_price: '',
    purchase_date: new Date().toISOString().split('T')[0],
    risk_level: 'Medium',
  });
  const [riskSuggestion, setRiskSuggestion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetchingRisk, setFetchingRisk] = useState(false);
  const [error, setError] = useState('');

  // Fetch risk suggestion when symbol changes
  useEffect(() => {
    const fetchRisk = async () => {
      if (formData.symbol.length < 1) {
        setRiskSuggestion(null);
        return;
      }

      setFetchingRisk(true);
      try {
        const suggestion = await getRiskSuggestion(formData.symbol);
        setRiskSuggestion(suggestion);
      } catch (err) {
        setRiskSuggestion(null);
      } finally {
        setFetchingRisk(false);
      }
    };

    const debounce = setTimeout(fetchRisk, 500);
    return () => clearTimeout(debounce);
  }, [formData.symbol]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await addHolding({
        ...formData,
        symbol: formData.symbol.toUpperCase(),
        quantity: parseFloat(formData.quantity),
        purchase_price: parseFloat(formData.purchase_price),
      });
      onAdd();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add holding');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const applySuggestedRisk = () => {
    if (riskSuggestion) {
      setFormData((prev) => ({ ...prev, risk_level: riskSuggestion.suggested_risk }));
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-gray-800">Add Stock</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          {/* Symbol */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Stock Symbol
            </label>
            <input
              type="text"
              name="symbol"
              value={formData.symbol}
              onChange={handleChange}
              placeholder="e.g., AAPL"
              className="input-field uppercase"
              required
            />
          </div>

          {/* Risk Suggestion */}
          {riskSuggestion && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <div className="flex justify-between items-center">
                <div>
                  <div className="text-sm font-medium text-blue-800">
                    Suggested Risk: {riskSuggestion.suggested_risk}
                  </div>
                  <div className="text-xs text-blue-600 mt-1">
                    {riskSuggestion.rationale}
                  </div>
                </div>
                <button
                  type="button"
                  onClick={applySuggestedRisk}
                  className="text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700"
                >
                  Apply
                </button>
              </div>
            </div>
          )}
          {fetchingRisk && (
            <div className="text-sm text-gray-500">Fetching risk suggestion...</div>
          )}

          {/* Quantity */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Quantity (Shares)
            </label>
            <input
              type="number"
              name="quantity"
              value={formData.quantity}
              onChange={handleChange}
              placeholder="e.g., 50"
              className="input-field"
              min="0.01"
              step="0.01"
              required
            />
          </div>

          {/* Purchase Price */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Purchase Price ($)
            </label>
            <input
              type="number"
              name="purchase_price"
              value={formData.purchase_price}
              onChange={handleChange}
              placeholder="e.g., 150.00"
              className="input-field"
              min="0.01"
              step="0.01"
              required
            />
          </div>

          {/* Purchase Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Purchase Date
            </label>
            <input
              type="date"
              name="purchase_date"
              value={formData.purchase_date}
              onChange={handleChange}
              className="input-field"
              required
            />
          </div>

          {/* Risk Level */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Risk Level (Your Assessment)
            </label>
            <select
              name="risk_level"
              value={formData.risk_level}
              onChange={handleChange}
              className="input-field"
              required
            >
              <option value="High">High Risk</option>
              <option value="Medium">Medium Risk</option>
              <option value="Low">Low Risk</option>
            </select>
            <p className="text-xs text-gray-500 mt-1">
              You decide the final risk level for your portfolio.
            </p>
          </div>

          {/* Buttons */}
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 btn-primary disabled:opacity-50"
            >
              {loading ? 'Adding...' : 'Add Stock'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddHoldingModal;
