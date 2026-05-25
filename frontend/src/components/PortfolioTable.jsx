import { useState } from 'react';
import { deleteHolding, updateHolding } from '../services/api';

function PortfolioTable({ holdings, onUpdate }) {
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [loading, setLoading] = useState(false);

  const handleEdit = (holding) => {
    setEditingId(holding.id);
    setEditForm({
      quantity: holding.quantity,
      purchase_price: holding.purchase_price,
      risk_level: holding.risk_level,
    });
  };

  const handleSave = async (id) => {
    setLoading(true);
    try {
      await updateHolding(id, editForm);
      setEditingId(null);
      onUpdate();
    } catch (error) {
      console.error('Error updating holding:', error);
      alert('Failed to update holding');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, symbol) => {
    if (!confirm(`Are you sure you want to delete ${symbol}?`)) return;

    setLoading(true);
    try {
      await deleteHolding(id);
      onUpdate();
    } catch (error) {
      console.error('Error deleting holding:', error);
      alert('Failed to delete holding');
    } finally {
      setLoading(false);
    }
  };

  const getRiskBadgeColor = (risk) => {
    switch (risk) {
      case 'High':
        return 'bg-red-100 text-red-800';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'Low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (holdings.length === 0) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-500 text-lg">No holdings yet. Add your first stock to get started!</p>
      </div>
    );
  }

  return (
    <div className="card overflow-hidden p-0">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Symbol
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Quantity
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Purchase Price
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Current Price
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Value
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Gain/Loss
              </th>
              <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Risk
              </th>
              <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {holdings.map((holding) => (
              <tr key={holding.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="font-semibold text-gray-900">{holding.symbol}</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right">
                  {editingId === holding.id ? (
                    <input
                      type="number"
                      value={editForm.quantity}
                      onChange={(e) => setEditForm({ ...editForm, quantity: parseFloat(e.target.value) })}
                      className="w-24 px-2 py-1 border rounded text-right"
                      step="0.01"
                    />
                  ) : (
                    <span className="text-gray-900">{holding.quantity}</span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right">
                  {editingId === holding.id ? (
                    <input
                      type="number"
                      value={editForm.purchase_price}
                      onChange={(e) => setEditForm({ ...editForm, purchase_price: parseFloat(e.target.value) })}
                      className="w-24 px-2 py-1 border rounded text-right"
                      step="0.01"
                    />
                  ) : (
                    <span className="text-gray-900">${holding.purchase_price.toFixed(2)}</span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-gray-900">
                  ${holding.current_price?.toFixed(2) || 'N/A'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right font-medium text-gray-900">
                  ${holding.current_value?.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) || 'N/A'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right">
                  {holding.gain_loss !== null ? (
                    <div>
                      <span className={`font-medium ${holding.gain_loss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {holding.gain_loss >= 0 ? '+' : ''}${holding.gain_loss.toFixed(2)}
                      </span>
                      <br />
                      <span className={`text-sm ${holding.gain_loss_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        ({holding.gain_loss_percent >= 0 ? '+' : ''}{holding.gain_loss_percent.toFixed(2)}%)
                      </span>
                    </div>
                  ) : (
                    'N/A'
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-center">
                  {editingId === holding.id ? (
                    <select
                      value={editForm.risk_level}
                      onChange={(e) => setEditForm({ ...editForm, risk_level: e.target.value })}
                      className="px-2 py-1 border rounded"
                    >
                      <option value="High">High</option>
                      <option value="Medium">Medium</option>
                      <option value="Low">Low</option>
                    </select>
                  ) : (
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getRiskBadgeColor(holding.risk_level)}`}>
                      {holding.risk_level}
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-center">
                  {editingId === holding.id ? (
                    <div className="flex justify-center space-x-2">
                      <button
                        onClick={() => handleSave(holding.id)}
                        disabled={loading}
                        className="text-green-600 hover:text-green-800 font-medium text-sm"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => setEditingId(null)}
                        className="text-gray-600 hover:text-gray-800 font-medium text-sm"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <div className="flex justify-center space-x-2">
                      <button
                        onClick={() => handleEdit(holding)}
                        className="text-primary-600 hover:text-primary-800 font-medium text-sm"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(holding.id, holding.symbol)}
                        disabled={loading}
                        className="text-red-600 hover:text-red-800 font-medium text-sm"
                      >
                        Delete
                      </button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PortfolioTable;
