

// import React from 'react';
// import './HistoricalData.css';

// function HistoricalData({
//   company,
//   period,
//   onPeriodChange,
//   historicalData,
//   loading,
//   error,
//   financialData,
//   financialLoading,
//   financialError,
//   onBack,
//   onRiskAnalysis
// }) {

//   // Format financial values
//   const formatValue = (value) => {

//     if (value === null || value === undefined || value === '') {
//       return 'N/A';
//     }

//     if (typeof value === 'number') {
//       return value.toLocaleString('en-IN', {
//         maximumFractionDigits: 2
//       });
//     }

//     return String(value);
//   };

//   // Display financial statements
//   const renderStatement = (title, statement) => {

//     if (!statement || !statement.success || !statement.data) {
//       return (
//         <div className="historical-table-section">
//           <h3>{title}</h3>
//           <p>
//             {statement?.message ||
//               'Financial information is unavailable.'}
//           </p>
//         </div>
//       );
//     }

//     const periods = [
//       ...new Set(
//         statement.data.flatMap((item) =>
//           Object.keys(item.values || {})
//         )
//       )
//     ];

//     return (
//       <div className="historical-table-section">

//         <h3>{title}</h3>

//         <p>Total metrics: {statement.total_metrics}</p>

//         {statement.data.length > 0 ? (

//           <div className="historical-table-wrapper">

//             <table>
//               <thead>
//                 <tr>
//                   <th>Financial Metric</th>

//                   {periods.map((period) => (
//                     <th key={period}>{period}</th>
//                   ))}
//                 </tr>
//               </thead>

//               <tbody>
//                 {statement.data.map((item, index) => (
//                   <tr key={index}>
//                     <td>{item.metric}</td>

//                     {periods.map((period) => (
//                       <td key={period}>
//                         {formatValue(item.values?.[period])}
//                       </td>
//                     ))}
//                   </tr>
//                 ))}
//               </tbody>
//             </table>

//           </div>

//         ) : (
//           <p>No financial metrics available.</p>
//         )}

//       </div>
//     );
//   };

//   const profile = financialData?.company_profile?.data;

//   const stockRecords = Array.isArray(historicalData)
//     ? historicalData
//     : [];

//   return (

//     <div className="historical-container">

//       {/* TOP ACTIONS */}

//       <div
//         style={{
//           display: 'flex',
//           justifyContent: 'space-between',
//           alignItems: 'center',
//           flexWrap: 'wrap',
//           gap: '12px',
//           marginBottom: '20px'
//         }}
//       >

//         <button className="back-button" onClick={onBack}>
//           ← Back to Search
//         </button>

//         <button
//           onClick={onRiskAnalysis}
//           disabled={!company?.symbol}
//           style={{
//             background: '#2563eb',
//             color: '#ffffff',
//             border: 'none',
//             padding: '11px 20px',
//             borderRadius: '7px',
//             fontWeight: '600',
//             cursor: 'pointer'
//           }}
//         >
//           Analyze Risk →
//         </button>

//       </div>

//       {/* COMPANY HEADER */}

//       <div className="historical-header">

//         <h2>{company?.name || 'Company'}</h2>

//         <p>
//           {company?.exchange || 'N/A'} ·{' '}
//           {company?.symbol || company?.yahooTicker || 'N/A'}
//         </p>

//       </div>

//       {/* PERIOD SELECTION */}

//       <div className="period-selection">

//         <label>Select Historical Period</label>

//         <select
//           value={period}
//           onChange={(e) => onPeriodChange(e.target.value)}
//         >
//           <option value="1mo">1 Month</option>
//           <option value="3mo">3 Months</option>
//           <option value="6mo">6 Months</option>
//           <option value="1y">1 Year</option>
//           <option value="2y">2 Years</option>
//           <option value="5y">5 Years</option>
//         </select>

//       </div>

//       {/* HISTORICAL STOCK DATA */}

//       {loading && (
//         <p>Loading historical stock data...</p>
//       )}

//       {error && (
//         <p className="historical-error">{error}</p>
//       )}

//       {!loading && !error && stockRecords.length > 0 && (

//         <div className="historical-table-section">

//           <h3>Historical OHLCV & Technical Indicators</h3>

//           <p>Total records: {stockRecords.length}</p>

//           <p>
//             Displaying latest {Math.min(stockRecords.length, 7)} records
//           </p>

//           <div className="historical-table-wrapper">

//             <table>
//               <thead>
//                 <tr>
//                   <th>Date</th>
//                   <th>Open</th>
//                   <th>High</th>
//                   <th>Low</th>
//                   <th>Close</th>
//                   <th>Volume</th>
//                   <th>SMA 20</th>
//                   <th>EMA 12</th>
//                   <th>RSI 14</th>
//                   <th>MACD</th>
//                 </tr>
//               </thead>

//               <tbody>
//                 {stockRecords
//                   .slice(-7)
//                   .reverse()
//                   .map((item, index) => (

//                     <tr key={item.Date || index}>
//                       <td>{item.Date}</td>

//                       <td>{formatValue(item.Open)}</td>
//                       <td>{formatValue(item.High)}</td>
//                       <td>{formatValue(item.Low)}</td>
//                       <td>{formatValue(item.Close)}</td>
//                       <td>{formatValue(item.Volume)}</td>

//                       <td>{formatValue(item.SMA_20)}</td>
//                       <td>{formatValue(item.EMA_12)}</td>
//                       <td>{formatValue(item.RSI_14)}</td>
//                       <td>{formatValue(item.MACD)}</td>
//                     </tr>

//                   ))}
//               </tbody>
//             </table>

//           </div>

//         </div>

//       )}

//       {!loading && !error && stockRecords.length === 0 && (
//         <p>No historical data available.</p>
//       )}

//       {/* COMPANY FINANCIAL INFORMATION */}

//       <div className="financial-information">

//         <h2>Company Financial Information</h2>

//         {financialLoading && (
//           <p>Loading company financial information...</p>
//         )}

//         {financialError && (
//           <p className="historical-error">
//             {financialError}
//           </p>
//         )}

//         {!financialLoading && !financialError && financialData && (

//           <>

//             {/* COMPANY PROFILE */}

//             <div className="historical-table-section">

//               <h3>Company Profile</h3>

//               {financialData.company_profile?.success && profile ? (

//                 <div className="historical-table-wrapper">

//                   <table>
//                     <tbody>
//                       {Object.entries(profile).map(([key, value]) => (

//                         <tr key={key}>
//                           <td>
//                             <strong>
//                               {key.replaceAll('_', ' ').toUpperCase()}
//                             </strong>
//                           </td>

//                           <td>{formatValue(value)}</td>
//                         </tr>

//                       ))}
//                     </tbody>
//                   </table>

//                 </div>

//               ) : (

//                 <p>
//                   {financialData.company_profile?.message ||
//                     'Company profile information is unavailable.'}
//                 </p>

//               )}

//             </div>

//             {/* INCOME STATEMENT */}

//             {renderStatement(
//               'Income Statement',
//               financialData.financial_statements?.income_statement
//             )}

//             {/* BALANCE SHEET */}

//             {renderStatement(
//               'Balance Sheet',
//               financialData.financial_statements?.balance_sheet
//             )}

//             {/* CASH FLOW STATEMENT */}

//             {renderStatement(
//               'Cash Flow Statement',
//               financialData.financial_statements?.cash_flow_statement
//             )}

//           </>

//         )}

//         {!financialLoading && !financialError && !financialData && (
//           <p>Financial information is not available.</p>
//         )}

//       </div>

//     </div>
//   );
// }

// export default HistoricalData;


import React from 'react';
import './HistoricalData.css';

function HistoricalData({
  company,
  period,
  onPeriodChange,
  historicalData,
  loading,
  error,
  financialData,
  financialLoading,
  financialError,
  onBack,
  onRiskAnalysis,
  onTechnicalAnalysis
}) {

  // Format financial values
  const formatValue = (value) => {

    if (value === null || value === undefined || value === '') {
      return 'N/A';
    }

    if (typeof value === 'number') {
      return value.toLocaleString('en-IN', {
        maximumFractionDigits: 2
      });
    }

    return String(value);
  };

  // Display financial statements
  const renderStatement = (title, statement) => {

    if (!statement || !statement.success || !statement.data) {
      return (
        <div className="historical-table-section">
          <h3>{title}</h3>
          <p>
            {statement?.message ||
              'Financial information is unavailable.'}
          </p>
        </div>
      );
    }

    const periods = [
      ...new Set(
        statement.data.flatMap((item) =>
          Object.keys(item.values || {})
        )
      )
    ];

    return (
      <div className="historical-table-section">

        <h3>{title}</h3>

        <p>Total metrics: {statement.total_metrics}</p>

        {statement.data.length > 0 ? (

          <div className="historical-table-wrapper">

            <table>
              <thead>
                <tr>
                  <th>Financial Metric</th>

                  {periods.map((period) => (
                    <th key={period}>{period}</th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {statement.data.map((item, index) => (
                  <tr key={index}>
                    <td>{item.metric}</td>

                    {periods.map((period) => (
                      <td key={period}>
                        {formatValue(item.values?.[period])}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>

          </div>

        ) : (
          <p>No financial metrics available.</p>
        )}

      </div>
    );
  };

  const profile = financialData?.company_profile?.data;

  const stockRecords = Array.isArray(historicalData)
    ? historicalData
    : [];

  return (

    <div className="historical-container">

      {/* TOP ACTIONS */}

      <div className="historical-top-actions">

        <button className="back-button" onClick={onBack}>
          ← Back to Search
        </button>

        <div className="historical-analysis-buttons">

          <button
            className="analyze-risk-button"
            onClick={onRiskAnalysis}
            disabled={!company?.symbol}
          >
            Analyze Risk →
          </button>

          <button
            className="analyze-technical-button"
            onClick={onTechnicalAnalysis}
            disabled={!company?.yahooTicker}
          >
            Technical Analysis →
          </button>

        </div>

      </div>

      {/* COMPANY HEADER */}

      <div className="historical-header">

        <h2>{company?.name || 'Company'}</h2>

        <p>
          {company?.exchange || 'N/A'} ·{' '}
          {company?.symbol || company?.yahooTicker || 'N/A'}
        </p>

      </div>

      {/* PERIOD SELECTION */}

      <div className="period-selection">

        <label>Select Historical Period</label>

        <select
          value={period}
          onChange={(e) => onPeriodChange(e.target.value)}
        >
          <option value="1mo">1 Month</option>
          <option value="3mo">3 Months</option>
          <option value="6mo">6 Months</option>
          <option value="1y">1 Year</option>
          <option value="2y">2 Years</option>
          <option value="5y">5 Years</option>
        </select>

      </div>

      {/* HISTORICAL STOCK DATA */}

      {loading && (
        <p>Loading historical stock data...</p>
      )}

      {error && (
        <p className="historical-error">{error}</p>
      )}

      {!loading && !error && stockRecords.length > 0 && (

        <div className="historical-table-section">

          <h3>Historical OHLCV & Technical Indicators</h3>

          <p>Total records: {stockRecords.length}</p>

          <p>
            Displaying latest {Math.min(stockRecords.length, 7)} records
          </p>

          <div className="historical-table-wrapper">

            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Open</th>
                  <th>High</th>
                  <th>Low</th>
                  <th>Close</th>
                  <th>Volume</th>
                  <th>SMA 20</th>
                  <th>EMA 12</th>
                  <th>RSI 14</th>
                  <th>MACD</th>
                </tr>
              </thead>

              <tbody>
                {stockRecords
                  .slice(-7)
                  .reverse()
                  .map((item, index) => (

                    <tr key={item.Date || index}>
                      <td>{item.Date}</td>

                      <td>{formatValue(item.Open)}</td>
                      <td>{formatValue(item.High)}</td>
                      <td>{formatValue(item.Low)}</td>
                      <td>{formatValue(item.Close)}</td>
                      <td>{formatValue(item.Volume)}</td>

                      <td>{formatValue(item.SMA_20)}</td>
                      <td>{formatValue(item.EMA_12)}</td>
                      <td>{formatValue(item.RSI_14)}</td>
                      <td>{formatValue(item.MACD)}</td>
                    </tr>

                  ))}
              </tbody>
            </table>

          </div>

        </div>

      )}

      {!loading && !error && stockRecords.length === 0 && (
        <p>No historical data available.</p>
      )}

      {/* COMPANY FINANCIAL INFORMATION */}

      <div className="financial-information">

        <h2>Company Financial Information</h2>

        {financialLoading && (
          <p>Loading company financial information...</p>
        )}

        {financialError && (
          <p className="historical-error">
            {financialError}
          </p>
        )}

        {!financialLoading && !financialError && financialData && (

          <>

            {/* COMPANY PROFILE */}

            <div className="historical-table-section">

              <h3>Company Profile</h3>

              {financialData.company_profile?.success && profile ? (

                <div className="historical-table-wrapper">

                  <table>
                    <tbody>
                      {Object.entries(profile).map(([key, value]) => (

                        <tr key={key}>
                          <td>
                            <strong>
                              {key.replaceAll('_', ' ').toUpperCase()}
                            </strong>
                          </td>

                          <td>{formatValue(value)}</td>
                        </tr>

                      ))}
                    </tbody>
                  </table>

                </div>

              ) : (

                <p>
                  {financialData.company_profile?.message ||
                    'Company profile information is unavailable.'}
                </p>

              )}

            </div>

            {/* INCOME STATEMENT */}

            {renderStatement(
              'Income Statement',
              financialData.financial_statements?.income_statement
            )}

            {/* BALANCE SHEET */}

            {renderStatement(
              'Balance Sheet',
              financialData.financial_statements?.balance_sheet
            )}

            {/* CASH FLOW STATEMENT */}

            {renderStatement(
              'Cash Flow Statement',
              financialData.financial_statements?.cash_flow_statement
            )}

          </>

        )}

        {!financialLoading && !financialError && !financialData && (
          <p>Financial information is not available.</p>
        )}

      </div>

    </div>
  );
}

export default HistoricalData;
