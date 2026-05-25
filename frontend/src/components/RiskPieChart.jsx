import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const COLORS = {
  High: '#ef4444',
  Medium: '#f59e0b',
  Low: '#22c55e',
};

function RiskPieChart({ distribution }) {
  if (!distribution || !distribution.risk_distribution || distribution.risk_distribution.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        No data available. Add holdings to see risk distribution.
      </div>
    );
  }

  const data = distribution.risk_distribution.map((item) => ({
    name: `${item.risk_level} Risk`,
    value: item.percentage,
    amount: item.value,
    count: item.count,
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border">
          <p className="font-semibold">{data.name}</p>
          <p className="text-sm text-gray-600">
            ${data.amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
          <p className="text-sm text-gray-600">{data.value.toFixed(1)}%</p>
          <p className="text-sm text-gray-500">{data.count} stock(s)</p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, value }) => `${value.toFixed(1)}%`}
          outerRadius={100}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={COLORS[entry.name.split(' ')[0]] || '#8884d8'}
            />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export default RiskPieChart;
