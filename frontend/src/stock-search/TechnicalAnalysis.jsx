
// import React, { useEffect, useState } from 'react';
// import './TechnicalAnalysis.css'
// function TechnicalAnalysis({ company, period, onBack }) {

//   const [analysis, setAnalysis] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState('');

//   useEffect(() => {

//     const fetchTechnicalAnalysis = async () => {

//       setLoading(true);
//       setError('');
//       setAnalysis(null);

//       try {

//         const ticker = company.yahooTicker;

//         const response = await fetch(
//           `http://127.0.0.1:8000/technical-analysis/${encodeURIComponent(ticker)}?period=${period}`
//         );

//         const data = await response.json();

//         if (!response.ok) {
//           throw new Error(
//             data.detail || 'Unable to retrieve technical analysis.'
//           );
//         }

//         if (!data.success || !data.technical_analysis) {
//           throw new Error('Technical analysis report is unavailable.');
//         }

//         setAnalysis(data.technical_analysis);

//       } catch (err) {

//         setError(
//           err.message || 'Unable to retrieve technical analysis.'
//         );

//       } finally {

//         setLoading(false);

//       }
//     };

//     if (company?.yahooTicker) {
//       fetchTechnicalAnalysis();
//     }

//   }, [company, period]);

//   return (

//     <div style={{ padding: '20px' }}>

//       <button className="back-button" onClick={onBack}>
//         ← Back to Company Details
//       </button>

//       <h2>Technical Analysis</h2>

//       <h3>
//         {company?.name} ({company?.yahooTicker})
//       </h3>

//       <p>Analysis Period: {period}</p>

//       {loading && (
//         <p>Generating technical analysis. Please wait...</p>
//       )}

//       {error && (
//         <p style={{ color: 'red' }}>{error}</p>
//       )}

//       {!loading && !error && analysis && (

//         <div style={{ marginTop: '20px' }}>

//           {Object.entries(analysis).map(([key, value]) => (

//             <div
//               key={key}
//               style={{
//                 padding: '15px',
//                 marginBottom: '12px',
//                 border: '1px solid #ddd',
//                 borderRadius: '8px'
//               }}
//             >

//               <h3>
//                 {key.replaceAll('_', ' ').toUpperCase()}
//               </h3>

//               <p>
//                 {typeof value === 'object' && value !== null
//                   ? JSON.stringify(value, null, 2)
//                   : String(value ?? 'N/A')}
//               </p>

//             </div>

//           ))}

//         </div>

//       )}

//     </div>
//   );
// }

// export default TechnicalAnalysis;

import React, { useEffect, useState } from 'react';
import './TechnicalAnalysis.css'

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
  BarChart,
  Bar
} from 'recharts';

function TechnicalAnalysis({ company, period, onBack }) {

  const [analysis, setAnalysis] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {

    const fetchTechnicalAnalysis = async () => {

      setLoading(true);
      setError('');
      setAnalysis(null);
      setHistoricalData([]);

      try {

        const ticker = company.yahooTicker;

        const response = await fetch(
          `http://127.0.0.1:8000/technical-analysis/${encodeURIComponent(ticker)}?period=${period}`
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail || 'Unable to retrieve technical analysis.'
          );
        }

        if (!data.success || !data.technical_analysis) {
          throw new Error('Technical analysis report is unavailable.');
        }

        setAnalysis(data.technical_analysis);
        setHistoricalData(data.historical_data || []);

      } catch (err) {

        setError(
          err.message || 'Unable to retrieve technical analysis.'
        );

      } finally {

        setLoading(false);

      }
    };

    if (company?.yahooTicker) {
      fetchTechnicalAnalysis();
    }

  }, [company, period]);

  return (

    <div style={{ padding: '20px' }}>

      <button className="back-button" onClick={onBack}>
        ← Back to Company Details
      </button>

      <h2>Technical Analysis</h2>

      <h3>
        {company?.name} ({company?.yahooTicker})
      </h3>

      <p>Analysis Period: {period}</p>

      {loading && (
        <p>Generating technical analysis. Please wait...</p>
      )}

      {error && (
        <p style={{ color: 'red' }}>{error}</p>
      )}

      {!loading && !error && analysis && (

        <div style={{ marginTop: '20px' }}>

          <h2>Technical Analysis Results</h2>

          {Object.entries(analysis).map(([key, value]) => (

            <div
              key={key}
              style={{
                padding: '15px',
                marginBottom: '12px',
                border: '1px solid #ddd',
                borderRadius: '8px'
              }}
            >

              <h3>
                {key.replaceAll('_', ' ').toUpperCase()}
              </h3>

              <p>
                {typeof value === 'object' && value !== null
                  ? JSON.stringify(value, null, 2)
                  : String(value ?? 'N/A')}
              </p>

            </div>

          ))}

          {historicalData.length > 0 && (

            <div style={{ marginTop: '35px' }}>

              <h2>1. Stock Price & Moving Averages</h2>

              <div style={{ width: '100%', height: 400 }}>
                <ResponsiveContainer>
                  <LineChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="Date" />
                    <YAxis domain={['auto', 'auto']} />
                    <Tooltip />
                    <Legend />

                    <Line dataKey="Close" stroke="#2563eb" dot={false} />
                    <Line dataKey="SMA_5" stroke="#16a34a" dot={false} />
                    <Line dataKey="SMA_20" stroke="#f59e0b" dot={false} />
                    <Line dataKey="SMA_50" stroke="#dc2626" dot={false} />
                    <Line dataKey="EMA_12" stroke="#9333ea" dot={false} />
                    <Line dataKey="EMA_26" stroke="#0891b2" dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <h2>2. Relative Strength Index (RSI)</h2>

              <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                  <LineChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="Date" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Legend />
                    <ReferenceLine y={70} stroke="red" strokeDasharray="5 5" />
                    <ReferenceLine y={30} stroke="green" strokeDasharray="5 5" />
                    <Line dataKey="RSI_14" stroke="#7c3aed" dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <h2>3. MACD Analysis</h2>

              <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                  <BarChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="Date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <ReferenceLine y={0} stroke="#666" />
                    <Bar dataKey="MACD_Histogram" fill="#8884d8" />
                    <Line dataKey="MACD" stroke="#2563eb" dot={false} />
                    <Line dataKey="Signal_Line" stroke="#dc2626" dot={false} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <h2>4. Historical Volatility</h2>

              <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                  <LineChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="Date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line
                      dataKey="Historical_Volatility"
                      stroke="#ea580c"
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

            </div>

          )}

        </div>

      )}

    </div>
  );
}

export default TechnicalAnalysis;
