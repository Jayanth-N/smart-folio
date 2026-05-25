import { useState } from 'react';

function RecommendationCards({ recommendations }) {
  const [expandedStrategy, setExpandedStrategy] = useState(null);

  if (!recommendations || !recommendations.strategies || recommendations.strategies.length === 0) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-500 text-lg">
          Add holdings to your portfolio to see personalized recommendations.
        </p>
      </div>
    );
  }

  const getStrategyColor = (riskLevel) => {
    switch (riskLevel) {
      case 'High':
        return {
          bg: 'bg-red-50',
          border: 'border-red-200',
          header: 'bg-red-500',
          badge: 'bg-red-100 text-red-800',
        };
      case 'Medium':
        return {
          bg: 'bg-yellow-50',
          border: 'border-yellow-200',
          header: 'bg-yellow-500',
          badge: 'bg-yellow-100 text-yellow-800',
        };
      case 'Low':
        return {
          bg: 'bg-green-50',
          border: 'border-green-200',
          header: 'bg-green-500',
          badge: 'bg-green-100 text-green-800',
        };
      default:
        return {
          bg: 'bg-gray-50',
          border: 'border-gray-200',
          header: 'bg-gray-500',
          badge: 'bg-gray-100 text-gray-800',
        };
    }
  };

  const getActionColor = (action) => {
    switch (action) {
      case 'buy':
        return 'text-green-600 bg-green-50';
      case 'sell':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="space-y-6">
      {/* Current Distribution Summary */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Your Current Allocation</h3>
        <div className="flex justify-center space-x-8">
          {Object.entries(recommendations.current_distribution).map(([level, percentage]) => (
            <div key={level} className="text-center">
              <div className={`text-2xl font-bold ${
                level === 'High' ? 'text-red-600' : level === 'Medium' ? 'text-yellow-600' : 'text-green-600'
              }`}>
                {percentage.toFixed(1)}%
              </div>
              <div className="text-sm text-gray-500">{level} Risk</div>
            </div>
          ))}
        </div>
      </div>

      {/* Strategy Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {recommendations.strategies.map((strategy) => {
          const colors = getStrategyColor(strategy.risk_level);
          const isExpanded = expandedStrategy === strategy.name;

          return (
            <div
              key={strategy.name}
              className={`rounded-xl overflow-hidden border-2 ${colors.border} ${colors.bg}`}
            >
              {/* Header */}
              <div className={`${colors.header} text-white p-4`}>
                <h3 className="text-xl font-bold">{strategy.name}</h3>
                <span className={`inline-block mt-2 px-2 py-1 rounded text-xs font-semibold ${colors.badge}`}>
                  {strategy.risk_level} Risk
                </span>
              </div>

              {/* Content */}
              <div className="p-4 space-y-4">
                {/* Expected Return */}
                <div>
                  <div className="text-sm text-gray-600">Expected Return</div>
                  <div className="text-lg font-semibold text-gray-800">{strategy.expected_return}</div>
                </div>

                {/* Description */}
                <p className="text-sm text-gray-600">{strategy.description}</p>

                {/* Suggested Allocation */}
                <div>
                  <div className="text-sm font-medium text-gray-700 mb-2">Target Allocation</div>
                  <div className="space-y-2">
                    {Object.entries(strategy.suggested_allocation).map(([level, pct]) => (
                      <div key={level} className="flex items-center">
                        <span className="w-20 text-sm text-gray-600">{level}</span>
                        <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                          <div
                            className={`h-2 rounded-full ${
                              level === 'High' ? 'bg-red-500' : level === 'Medium' ? 'bg-yellow-500' : 'bg-green-500'
                            }`}
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium">{pct}%</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Rationale */}
                <div className="bg-white rounded-lg p-3">
                  <div className="text-sm font-medium text-gray-700 mb-1">Rationale</div>
                  <p className="text-sm text-gray-600">{strategy.rationale}</p>
                </div>

                {/* Expand/Collapse Actions */}
                <button
                  onClick={() => setExpandedStrategy(isExpanded ? null : strategy.name)}
                  className="w-full text-center text-sm font-medium text-primary-600 hover:text-primary-700 py-2"
                >
                  {isExpanded ? 'Hide Actions ↑' : 'Show Rebalancing Actions ↓'}
                </button>

                {/* Rebalancing Actions */}
                {isExpanded && strategy.rebalance_actions.length > 0 && (
                  <div className="space-y-2 mt-2">
                    <div className="text-sm font-medium text-gray-700">Suggested Actions</div>
                    {strategy.rebalance_actions.map((action, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between bg-white rounded-lg p-3"
                      >
                        <div>
                          <div className="flex items-center space-x-2">
                            <span className="font-semibold">{action.symbol}</span>
                            <span className={`px-2 py-0.5 rounded text-xs font-medium ${getActionColor(action.action)}`}>
                              {action.action.toUpperCase()}
                            </span>
                          </div>
                          <div className="text-xs text-gray-500 mt-1">{action.rationale}</div>
                        </div>
                        <div className="text-right text-sm">
                          <div className="text-gray-500">{action.current_allocation}%</div>
                          <div className="text-gray-400">→ {action.target_allocation}%</div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default RecommendationCards;
