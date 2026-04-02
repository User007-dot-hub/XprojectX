import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import './PriceChart.css';

export default function PriceChart({ data, ticker }) {
  if (!data || data.length === 0) {
    return (
      <div className="price-chart-empty glass-panel fade-in">
        <p>No chart data available.</p>
      </div>
    );
  }

  // Format data
  const chartData = data.map(item => ({
    ...item,
    date: new Date(item.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
  }));

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip glass-panel">
          <p className="label">{label}</p>
          <p className="price">${payload[0].value.toFixed(2)}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="price-chart-container glass-panel fade-in">
      <h3>{ticker} Price History</h3>
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorClose" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--accent-color)" stopOpacity={0.4} />
                <stop offset="95%" stopColor="var(--accent-color)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis 
              dataKey="date" 
              stroke="var(--text-secondary)" 
              axisLine={false}
              tickLine={false}
              minTickGap={20}
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              domain={['auto', 'auto']} 
              stroke="var(--text-secondary)" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `$${value}`}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'rgba(255,255,255,0.2)', strokeWidth: 1 }} />
            <Area 
              type="monotone" 
              dataKey="close" 
              stroke="var(--accent-color)" 
              strokeWidth={2}
              fillOpacity={1} 
              fill="url(#colorClose)" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
