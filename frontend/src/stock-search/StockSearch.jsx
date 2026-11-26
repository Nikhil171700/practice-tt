

// import React, { useState } from 'react';
// import './StockSearch.css';

// import HistoricalData from './HistoricalData';
// import RiskAnalysis from './RiskAnalysis';

// function StockSearch() {

//   const [query, setQuery] = useState('');
//   const [results, setResults] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState('');

//   // Selected company
//   const [selectedCompany, setSelectedCompany] = useState(null);

//   // Page navigation
//   const [showRiskAnalysis, setShowRiskAnalysis] = useState(false);

//   // Historical data states
//   const [historicalData, setHistoricalData] = useState([]);
//   const [historyLoading, setHistoryLoading] = useState(false);
//   const [historyError, setHistoryError] = useState('');
//   const [period, setPeriod] = useState('6mo');

//   // Financial information states
//   const [financialData, setFinancialData] = useState(null);
//   const [financialLoading, setFinancialLoading] = useState(false);
//   const [financialError, setFinancialError] = useState('');

//   // Convert Alpha Vantage symbol to Yahoo Finance ticker
//   const getYahooTicker = (company) => {

//     const symbol = company.symbol;

//     if (
//       company.region === 'India/Bombay' &&
//       symbol.endsWith('.BSE')
//     ) {
//       return symbol.replace('.BSE', '.NS');
//     }

//     if (company.region === 'United States') {
//       return symbol;
//     }

//     return null;
//   };

//   // Search companies
//   const handleSearch = async (e) => {

//     e.preventDefault();

//     if (!query.trim()) {
//       setError('Please enter a company name or ticker symbol.');
//       setResults([]);
//       return;
//     }

//     setLoading(true);
//     setError('');
//     setResults([]);

//     setSelectedCompany(null);
//     setShowRiskAnalysis(false);

//     try {

//       const response = await fetch(
//         `http://127.0.0.1:8000/companies/search?q=${encodeURIComponent(query.trim())}`
//       );

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(data.detail || 'Unable to search companies.');
//       }

//       if (!data.success || !data.results || data.results.length === 0) {
//         setError('No matching companies found.');
//         return;
//       }

//       const supportedResults = data.results.filter(
//         (company) => getYahooTicker(company) !== null
//       );

//       if (supportedResults.length === 0) {
//         setError('No supported exchange listings found.');
//         return;
//       }

//       setResults(supportedResults);

//     } catch (err) {

//       setError(err.message || 'Unable to connect to backend.');

//     } finally {

//       setLoading(false);

//     }
//   };

//   // Select a company
//   const handleCompanySelect = async (company) => {

//     const yahooTicker = getYahooTicker(company);

//     if (!yahooTicker) {
//       return;
//     }

//     setSelectedCompany({
//       name: company.name,

//       // Original Alpha Vantage symbol
//       symbol: company.symbol,

//       // Yahoo Finance symbol used by existing data requests
//       yahooTicker: yahooTicker,

//       exchange:
//         company.region === 'India/Bombay'
//           ? 'India - NSE'
//           : company.region,

//       currency: company.currency
//     });

//     setShowRiskAnalysis(false);

//     setHistoricalData([]);
//     setHistoryError('');
//     setHistoryLoading(true);

//     setFinancialData(null);
//     setFinancialError('');
//     setFinancialLoading(true);

//     // Fetch historical data
//     try {

//       const response = await fetch(
//         `http://127.0.0.1:8000/historical/${encodeURIComponent(yahooTicker)}?period=${period}`
//       );

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(
//           data.detail || 'Unable to retrieve historical data.'
//         );
//       }

//       setHistoricalData(data.data || []);

//     } catch (err) {

//       setHistoryError(
//         err.message || 'Unable to retrieve historical data.'
//       );

//     } finally {

//       setHistoryLoading(false);

//     }

//     // Existing delay before financial information request
//     await new Promise((resolve) => setTimeout(resolve, 15000));

//     // Fetch financial information
//     try {

//       const response = await fetch(
//         `http://127.0.0.1:8000/financials/${encodeURIComponent(yahooTicker)}`
//       );

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(
//           data.detail || 'Unable to retrieve financial information.'
//         );
//       }

//       setFinancialData(data);

//     } catch (err) {

//       setFinancialError(
//         err.message || 'Unable to retrieve financial information.'
//       );

//     } finally {

//       setFinancialLoading(false);

//     }
//   };

//   // Change historical period
//   const handlePeriodChange = async (newPeriod) => {

//     setPeriod(newPeriod);

//     if (!selectedCompany) return;

//     setHistoryLoading(true);
//     setHistoricalData([]);
//     setHistoryError('');

//     try {

//       const response = await fetch(
//         `http://127.0.0.1:8000/historical/${encodeURIComponent(selectedCompany.yahooTicker)}?period=${newPeriod}`
//       );

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(
//           data.detail || 'Unable to retrieve historical data.'
//         );
//       }

//       setHistoricalData(data.data || []);

//     } catch (err) {

//       setHistoryError(
//         err.message || 'Unable to retrieve historical data.'
//       );

//     } finally {

//       setHistoryLoading(false);

//     }
//   };

//   // Open Risk Analysis page
//   const handleOpenRiskAnalysis = () => {
//     setShowRiskAnalysis(true);
//   };

//   // Return from Risk Analysis to Company Details
//   const handleRiskBack = () => {
//     setShowRiskAnalysis(false);
//   };

//   // Back to company search
//   const handleBack = () => {
//     setSelectedCompany(null);
//     setShowRiskAnalysis(false);
//   };

//   // Display Risk Analysis page
//   if (selectedCompany && showRiskAnalysis) {

//     return (
//       <RiskAnalysis
//         company={selectedCompany}
//         period={period}
//         onBack={handleRiskBack}
//       />
//     );
//   }

//   // Display Company Details page
//   if (selectedCompany) {

//     return (
//       <HistoricalData
//         company={selectedCompany}
//         period={period}
//         onPeriodChange={handlePeriodChange}
//         historicalData={historicalData}
//         loading={historyLoading}
//         error={historyError}
//         financialData={financialData}
//         financialLoading={financialLoading}
//         financialError={financialError}
//         onBack={handleBack}
//         onRiskAnalysis={handleOpenRiskAnalysis}
//       />
//     );
//   }

//   // Display company search page
//   return (

//     <div className="stock-search-container">

//       <h2>Search Stocks</h2>

//       <p className="stock-search-description">
//         Search for companies using their name or ticker symbol.
//       </p>

//       <form onSubmit={handleSearch} className="stock-search-form">

//         <input
//           type="text"
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//           placeholder="Example: INFY or Infosys"
//         />

//         <button type="submit" disabled={loading}>
//           {loading ? 'Searching...' : 'Search'}
//         </button>

//       </form>

//       {error && (
//         <p className="stock-search-error">{error}</p>
//       )}

//       {results.length > 0 && (

//         <div className="stock-results">

//           <h3>Search Results</h3>

//           {results.map((company, index) => (

//             <div
//               className="stock-result-card"
//               key={`${company.symbol}-${index}`}
//               onClick={() => handleCompanySelect(company)}
//               role="button"
//               tabIndex={0}
//               onKeyDown={(e) => {
//                 if (e.key === 'Enter' || e.key === ' ') {
//                   e.preventDefault();
//                   handleCompanySelect(company);
//                 }
//               }}
//             >

//               <div>
//                 <h3>{company.name}</h3>
//                 <p>Symbol: {company.symbol}</p>
//               </div>

//               <div className="stock-result-details">
//                 <p>Exchange / Region: {company.region}</p>
//                 <p>Currency: {company.currency}</p>
//                 <p>Type: {company.type}</p>
//               </div>

//               <p>
//                 Click to view historical and financial data →
//               </p>

//             </div>

//           ))}

//         </div>
//       )}

//     </div>
//   );
// }

// export default StockSearch;

















// import React, { useState } from 'react';
// import './StockSearch.css';

// import HistoricalData from './HistoricalData';
// import RiskAnalysis from './RiskAnalysis';
// import TechnicalAnalysis from './TechnicalAnalysis';

// function StockSearch() {

//   const [query, setQuery] = useState('');
//   const [results, setResults] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState('');

//   // Selected company
//   const [selectedCompany, setSelectedCompany] = useState(null);

//   // Page navigation
//   const [showRiskAnalysis, setShowRiskAnalysis] = useState(false);
//   const [showTechnicalAnalysis, setShowTechnicalAnalysis] = useState(false);

//   // Historical data states
//   const [historicalData, setHistoricalData] = useState([]);
//   const [historyLoading, setHistoryLoading] = useState(false);
//   const [historyError, setHistoryError] = useState('');
//   const [period, setPeriod] = useState('6mo');

//   // Financial information states
//   const [financialData, setFinancialData] = useState(null);
//   const [financialLoading, setFinancialLoading] = useState(false);
//   const [financialError, setFinancialError] = useState('');

//   // Convert Alpha Vantage symbol to Yahoo Finance ticker
//   const getYahooTicker = (company) => {

//     const symbol = company.symbol;

//     if (
//       company.region === 'India/Bombay' &&
//       symbol.endsWith('.BSE')
//     ) {
//       return symbol.replace('.BSE', '.NS');
//     }

//     if (company.region === 'United States') {
//       return symbol;
//     }

//     return null;
//   };

//   // Search companies
//   const handleSearch = async (e) => {

//     e.preventDefault();

//     if (!query.trim()) {
//       setError('Please enter a company name or ticker symbol.');
//       setResults([]);
//       return;
//     }

//     setLoading(true);
//     setError('');
//     setResults([]);

//     setSelectedCompany(null);
//     setShowRiskAnalysis(false);
//     setShowTechnicalAnalysis(false);

//     try {

//       const response = await fetch(
//         `http://127.0.0.1:8000/companies/search?q=${encodeURIComponent(query.trim())}`
//       );

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(data.detail || 'Unable to search companies.');
//       }

//       if (!data.success || !data.results || data.results.length === 0) {
//         setError('No matching companies found.');
//         return;
//       }

//       const supportedResults = data.results.filter(
//         (company) => getYahooTicker(company) !== null
//       );

//       if (supportedResults.length === 0) {
//         setError('No supported exchange listings found.');
//         return;
//       }

//       setResults(supportedResults);

//     } catch (err) {

//       setError(err.message || 'Unable to connect to backend.');

//     } finally {

//       setLoading(false);

//     }
//   };

//   // Select a company
//   const handleCompanySelect = async (company) => {

//     const yahooTicker = getYahooTicker(company);

//     if (!yahooTicker) {
//       return;
//     }

//     setSelectedCompany({
//       name: company.name,

//       // Original Alpha Vantage symbol
//       symbol: company.symbol,

//       // Yahoo Finance symbol used by existing data requests
//       yahooTicker: yahooTicker,

//       exchange:
//         company.region === 'India/Bombay'
//           ? 'India - NSE'
//           : company.region,

//       currency: company.currency
//     });

//     setShowRiskAnalysis(false);
//     setShowTechnicalAnalysis(false);

//     setHistoricalData([]);
//     setHistoryError('');
//     setHistoryLoading(true);

//     setFinancialData(null);
//     setFinancialError('');
//     setFinancialLoading(true);

//     // Fetch historical data
//     try {

//       const response = await fetch(
//         `http://127.0.0.1:8000/historical/${encodeURIComponent(yahooTicker)}?period=${period}`
//       );

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(
//           data.detail || 'Unable to retrieve historical data.'
//         );
//       }

//       setHistoricalData(data.data || []);

//     } catch (err) {

//       setHistoryError(
//         err.message || 'Unable to retrieve historical data.'
//       );

//     } finally {

//       setHistoryLoading(false);

//     }

//     // Existing delay before financial information request
//     await new Promise((resolve) => setTimeout(resolve, 15000));

//     // Fetch financial information
//     try {

//       const response = await fetch(
//         `http://127.0.0.1:8000/financials/${encodeURIComponent(yahooTicker)}`
//       );

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(
//           data.detail || 'Unable to retrieve financial information.'
//         );
//       }

//       setFinancialData(data);

//     } catch (err) {

//       setFinancialError(
//         err.message || 'Unable to retrieve financial information.'
//       );

//     } finally {

//       setFinancialLoading(false);

//     }
//   };

//   // Change historical period
//   const handlePeriodChange = async (newPeriod) => {

//     setPeriod(newPeriod);

//     if (!selectedCompany) return;

//     setHistoryLoading(true);
//     setHistoricalData([]);
//     setHistoryError('');

//     try {

//       const response = await fetch(
//         `http://127.0.0.1:8000/historical/${encodeURIComponent(selectedCompany.yahooTicker)}?period=${newPeriod}`
//       );

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(
//           data.detail || 'Unable to retrieve historical data.'
//         );
//       }

//       setHistoricalData(data.data || []);

//     } catch (err) {

//       setHistoryError(
//         err.message || 'Unable to retrieve historical data.'
//       );

//     } finally {

//       setHistoryLoading(false);

//     }
//   };

//   // Open Risk Analysis page
//   const handleOpenRiskAnalysis = () => {
//     setShowTechnicalAnalysis(false);
//     setShowRiskAnalysis(true);
//   };

//   // Return from Risk Analysis to Company Details
//   const handleRiskBack = () => {
//     setShowRiskAnalysis(false);
//   };

//   // Open Technical Analysis page
//   const handleOpenTechnicalAnalysis = () => {
//     setShowRiskAnalysis(false);
//     setShowTechnicalAnalysis(true);
//   };

//   // Return from Technical Analysis to Company Details
//   const handleTechnicalBack = () => {
//     setShowTechnicalAnalysis(false);
//   };

//   // Back to company search
//   const handleBack = () => {
//     setSelectedCompany(null);
//     setShowRiskAnalysis(false);
//     setShowTechnicalAnalysis(false);
//   };

//   // Display Risk Analysis page
//   if (selectedCompany && showRiskAnalysis) {

//     return (
//       <RiskAnalysis
//         company={selectedCompany}
//         period={period}
//         onBack={handleRiskBack}
//       />
//     );
//   }

//   // Display Technical Analysis page
//   if (selectedCompany && showTechnicalAnalysis) {

//     return (
//       <TechnicalAnalysis
//         company={selectedCompany}
//         period={period}
//         onBack={handleTechnicalBack}
//       />
//     );
//   }

//   // Display Company Details page
//   if (selectedCompany) {

//     return (
//       <HistoricalData
//         company={selectedCompany}
//         period={period}
//         onPeriodChange={handlePeriodChange}
//         historicalData={historicalData}
//         loading={historyLoading}
//         error={historyError}
//         financialData={financialData}
//         financialLoading={financialLoading}
//         financialError={financialError}
//         onBack={handleBack}
//         onRiskAnalysis={handleOpenRiskAnalysis}
//         onTechnicalAnalysis={handleOpenTechnicalAnalysis}
//       />
//     );
//   }

//   // Display company search page
//   return (

//     <div className="stock-search-container">

//       <h2>Search Stocks</h2>

//       <p className="stock-search-description">
//         Search for companies using their name or ticker symbol.
//       </p>

//       <form onSubmit={handleSearch} className="stock-search-form">

//         <input
//           type="text"
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//           placeholder="Example: INFY or Infosys"
//         />

//         <button type="submit" disabled={loading}>
//           {loading ? 'Searching...' : 'Search'}
//         </button>

//       </form>

//       {error && (
//         <p className="stock-search-error">{error}</p>
//       )}

//       {results.length > 0 && (

//         <div className="stock-results">

//           <h3>Search Results</h3>

//           {results.map((company, index) => (

//             <div
//               className="stock-result-card"
//               key={`${company.symbol}-${index}`}
//               onClick={() => handleCompanySelect(company)}
//               role="button"
//               tabIndex={0}
//               onKeyDown={(e) => {
//                 if (e.key === 'Enter' || e.key === ' ') {
//                   e.preventDefault();
//                   handleCompanySelect(company);
//                 }
//               }}
//             >

//               <div>
//                 <h3>{company.name}</h3>
//                 <p>Symbol: {company.symbol}</p>
//               </div>

//               <div className="stock-result-details">
//                 <p>Exchange / Region: {company.region}</p>
//                 <p>Currency: {company.currency}</p>
//                 <p>Type: {company.type}</p>
//               </div>

//               <p>
//                 Click to view historical and financial data →
//               </p>

//             </div>

//           ))}

//         </div>
//       )}

//     </div>
//   );
// }

// export default StockSearch;












import React, { useState } from 'react';
import './StockSearch.css';

import HistoricalData from './HistoricalData';
import RiskAnalysis from './RiskAnalysis';
import TechnicalAnalysis from './TechnicalAnalysis';

function StockSearch() {

  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Selected company
  const [selectedCompany, setSelectedCompany] = useState(null);

  // Page navigation
  const [showRiskAnalysis, setShowRiskAnalysis] = useState(false);
  const [showTechnicalAnalysis, setShowTechnicalAnalysis] = useState(false);

  // Historical data states
  const [historicalData, setHistoricalData] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState('');
  const [period, setPeriod] = useState('6mo');

  // Financial information states
  const [financialData, setFinancialData] = useState(null);
  const [financialLoading, setFinancialLoading] = useState(false);
  const [financialError, setFinancialError] = useState('');

  // Convert Alpha Vantage symbol to Yahoo Finance ticker
  const getYahooTicker = (company) => {

    const symbol = company.symbol;

    if (
      company.region === 'India/Bombay' &&
      symbol.endsWith('.BSE')
    ) {
      return symbol.replace('.BSE', '.NS');
    }

    if (company.region === 'United States') {
      return symbol;
    }

    return null;
  };

  // Search companies
  const handleSearch = async (e) => {

    e.preventDefault();

    if (!query.trim()) {
      setError('Please enter a company name or ticker symbol.');
      setResults([]);
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);

    setSelectedCompany(null);
    setShowRiskAnalysis(false);
    setShowTechnicalAnalysis(false);

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/companies/search?q=${encodeURIComponent(query.trim())}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Unable to search companies.');
      }

      if (!data.success || !data.results || data.results.length === 0) {
        setError('No matching companies found.');
        return;
      }

      const supportedResults = data.results.filter(
        (company) => getYahooTicker(company) !== null
      );

      if (supportedResults.length === 0) {
        setError('No supported exchange listings found.');
        return;
      }

      setResults(supportedResults);

    } catch (err) {

      setError(err.message || 'Unable to connect to backend.');

    } finally {

      setLoading(false);

    }
  };

  // Select a company
  const handleCompanySelect = async (company) => {

    const yahooTicker = getYahooTicker(company);

    if (!yahooTicker) {
      return;
    }

    setSelectedCompany({
      name: company.name,
      symbol: company.symbol,
      yahooTicker: yahooTicker,

      exchange:
        company.region === 'India/Bombay'
          ? 'India - NSE'
          : company.region,

      currency: company.currency
    });

    setShowRiskAnalysis(false);
    setShowTechnicalAnalysis(false);

    setHistoricalData([]);
    setHistoryError('');
    setHistoryLoading(true);

    setFinancialData(null);
    setFinancialError('');
    setFinancialLoading(true);

    // Fetch historical data
    try {

      const response = await fetch(
        `http://127.0.0.1:8000/historical/${encodeURIComponent(yahooTicker)}?period=${period}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || 'Unable to retrieve historical data.'
        );
      }

      setHistoricalData(data.data || []);

    } catch (err) {

      setHistoryError(
        err.message || 'Unable to retrieve historical data.'
      );

    } finally {

      setHistoryLoading(false);

    }

    // Existing delay before financial information request
    await new Promise((resolve) => setTimeout(resolve, 15000));

    // Fetch financial information
    try {

      const response = await fetch(
        `http://127.0.0.1:8000/financials/${encodeURIComponent(yahooTicker)}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || 'Unable to retrieve financial information.'
        );
      }

      setFinancialData(data);

    } catch (err) {

      setFinancialError(
        err.message || 'Unable to retrieve financial information.'
      );

    } finally {

      setFinancialLoading(false);

    }
  };

  // Change historical period
  const handlePeriodChange = async (newPeriod) => {

    setPeriod(newPeriod);

    if (!selectedCompany) return;

    setHistoryLoading(true);
    setHistoricalData([]);
    setHistoryError('');

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/historical/${encodeURIComponent(selectedCompany.yahooTicker)}?period=${newPeriod}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || 'Unable to retrieve historical data.'
        );
      }

      setHistoricalData(data.data || []);

    } catch (err) {

      setHistoryError(
        err.message || 'Unable to retrieve historical data.'
      );

    } finally {

      setHistoryLoading(false);

    }
  };

  // Open Risk Analysis page
  const handleOpenRiskAnalysis = () => {
    setShowTechnicalAnalysis(false);
    setShowRiskAnalysis(true);
  };

  // Return from Risk Analysis
  const handleRiskBack = () => {
    setShowRiskAnalysis(false);
  };

  // Open Technical Analysis page
  const handleOpenTechnicalAnalysis = () => {
    setShowRiskAnalysis(false);
    setShowTechnicalAnalysis(true);
  };

  // Return from Technical Analysis
  const handleTechnicalBack = () => {
    setShowTechnicalAnalysis(false);
  };

  // Back to company search
  const handleBack = () => {
    setSelectedCompany(null);
    setShowRiskAnalysis(false);
    setShowTechnicalAnalysis(false);
  };

  // Display Risk Analysis page
  if (selectedCompany && showRiskAnalysis) {

    return (
      <RiskAnalysis
        company={selectedCompany}
        period={period}
        onBack={handleRiskBack}
      />
    );
  }

  // Display Technical Analysis page
  if (selectedCompany && showTechnicalAnalysis) {

    return (
      <TechnicalAnalysis
        company={selectedCompany}
        period={period}
        onBack={handleTechnicalBack}
      />
    );
  }

  // Display Company Details page
  if (selectedCompany) {

    return (
      <HistoricalData
        company={selectedCompany}
        period={period}
        onPeriodChange={handlePeriodChange}
        historicalData={historicalData}
        loading={historyLoading}
        error={historyError}
        financialData={financialData}
        financialLoading={financialLoading}
        financialError={financialError}
        onBack={handleBack}
        onRiskAnalysis={handleOpenRiskAnalysis}
        onTechnicalAnalysis={handleOpenTechnicalAnalysis}
      />
    );
  }

  // Display company search page
  return (

    <div className="stock-search-container">

      <h2>Search Stocks</h2>

      <p className="stock-search-description">
        Search for companies using their name or ticker symbol.
      </p>

      <form onSubmit={handleSearch} className="stock-search-form">

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Example: INFY or Infosys"
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>

      </form>

      {error && (
        <p className="stock-search-error">{error}</p>
      )}

      {results.length > 0 && (

        <div className="stock-results">

          <h3>Search Results</h3>

          {results.map((company, index) => (

            <div
              className="stock-result-card"
              key={`${company.symbol}-${index}`}
              onClick={() => handleCompanySelect(company)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  handleCompanySelect(company);
                }
              }}
            >

              <div>
                <h3>{company.name}</h3>
                <p>Symbol: {company.symbol}</p>
              </div>

              <div className="stock-result-details">
                <p>Exchange / Region: {company.region}</p>
                <p>Currency: {company.currency}</p>
                <p>Type: {company.type}</p>
              </div>

              <p>
                Click to view historical and financial data →
              </p>

            </div>

          ))}

        </div>
      )}

    </div>
  );
}

export default StockSearch;
