import { useState } from 'react';
import { Search } from 'lucide-react';
import './PredictionForm.css';

export default function PredictionForm({ onSubmit, isLoading }) {
  const [ticker, setTicker] = useState('AAPL');
  const [timeframe, setTimeframe] = useState('1d');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (ticker) {
      onSubmit(ticker.toUpperCase(), timeframe);
    }
  };

  return (
    <div className="prediction-form-container glass-panel fade-in">
      <h2>Analyze Stock</h2>
      <form onSubmit={handleSubmit} className="prediction-form">
        <div className="input-group">
          <label htmlFor="ticker">Stock Ticker</label>
          <div className="input-wrapper">
            <Search className="input-icon" size={18} />
            <input
              id="ticker"
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              placeholder="e.g. AAPL"
              required
            />
          </div>
        </div>
        
        <div className="input-group">
          <label htmlFor="timeframe">Timeframe</label>
          <select 
            id="timeframe" 
            value={timeframe} 
            onChange={(e) => setTimeframe(e.target.value)}
          >
            <option value="1d">1 Day</option>
            <option value="1w">1 Week</option>
          </select>
        </div>

        <button type="submit" disabled={isLoading} className="predict-btn">
          {isLoading ? <span className="spinner"></span> : 'Predict'}
        </button>
      </form>
    </div>
  );
}
