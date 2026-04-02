import { useState } from 'react';
import PredictionForm from './components/PredictionForm';
import PredictionResult from './components/PredictionResult';
import PriceChart from './components/PriceChart';
import { AlertCircle } from 'lucide-react';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [chartData, setChartData] = useState(null);

  const handlePredict = async (ticker, timeframe) => {
    setLoading(true);
    setError(null);
    setPredictionData(null);
    setChartData(null);

    try {
      const res = await fetch(`http://localhost:8000/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, timeframe })
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to fetch prediction');
      }

      const data = await res.json();
      
      setPredictionData({
        ticker,
        prediction: data.prediction,
        probability: data.probability,
        timestamp: new Date().toISOString()
      });

      if (data.history && data.history.length > 0) {
        setChartData(data.history);
      } else {
        // Fallback mock history if backend doesn't send it yet
        const mockHistory = Array.from({ length: 30 }, (_, i) => {
          const date = new Date();
          date.setDate(date.getDate() - (30 - i));
          return {
            date: date.toISOString().split('T')[0],
            close: 100 + Math.random() * 50 + (i * 0.5)
          };
        });
        setChartData(mockHistory);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header glass-panel fade-in">
        <h1>Stock AI Predictor</h1>
      </header>
      
      <main className="main-content">
        <section className="form-section">
          <PredictionForm onSubmit={handlePredict} isLoading={loading} />
          {error && (
            <div className="error-message glass-panel fade-in">
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}
        </section>

        {(predictionData || chartData) && (
          <div className="results-grid">
            {predictionData && (
              <div className="prediction-section">
                <PredictionResult result={predictionData} />
              </div>
            )}
            
            {chartData && (
              <div className="chart-section">
                <PriceChart data={chartData} ticker={predictionData?.ticker || ''} />
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
