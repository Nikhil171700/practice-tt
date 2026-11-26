
import React, { useEffect, useState } from 'react';
import './RiskAnalysis.css';

function RiskAnalysis({ company, period, onBack }) {

  const [riskReport, setRiskReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch Risk Agent report
  const fetchRiskAnalysis = async () => {

    setLoading(true);
    setError('');
    setRiskReport(null);

    try {

      const response = await fetch(
        'http://127.0.0.1:8000/risk/analyze',
        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify({
            symbol: company.symbol,
            period: period
          })
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || 'Unable to generate risk analysis.'
        );
      }

      if (!data.success || !data.risk_report) {
        throw new Error('Risk Analysis Agent returned an invalid response.');
      }

      setRiskReport(data.risk_report);

    } catch (err) {

      setError(
        err.message || 'Unable to connect to Risk Analysis Agent.'
      );

    } finally {

      setLoading(false);

    }
  };

  // Automatically run analysis when page opens
  useEffect(() => {
    fetchRiskAnalysis();
  }, [company.symbol, period]);

  // Reset analysis
  const handleReset = () => {
    fetchRiskAnalysis();
  };

  // Format numbers
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

  // Risk level styling
  const getRiskClass = (level) => {

    if (!level) return 'risk-neutral';

    switch (level.toLowerCase()) {

      case 'low':
        return 'risk-low';

      case 'moderate':
        return 'risk-moderate';

      case 'high':
        return 'risk-high';

      case 'critical':
      case 'very high':
        return 'risk-critical';

      default:
        return 'risk-neutral';
    }
  };

  // Display list of financial risks
  const renderFinancialRisks = (risks) => {

    if (!risks || risks.length === 0) {
      return <p>No financial risks were identified from the available data.</p>;
    }

    return risks.map((risk, index) => (

      <div className="risk-item" key={index}>

        <div className="risk-item-header">

          <h4>{risk.risk_name}</h4>

          <span className={getRiskClass(risk.severity)}>
            {risk.severity}
          </span>

        </div>

        <p>{risk.description}</p>

        {risk.evidence && (
          <p className="risk-evidence">
            Evidence: {risk.evidence}
          </p>
        )}

      </div>

    ));
  };

  // Display text lists
  const renderTextList = (items, emptyMessage) => {

    if (!items || items.length === 0) {
      return <p>{emptyMessage}</p>;
    }

    return (
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    );
  };

  // Display alternative scenarios
  const renderScenarios = (scenarios) => {

    if (!scenarios || scenarios.length === 0) {
      return <p>No alternative scenarios are available.</p>;
    }

    return scenarios.map((scenario, index) => (

      <div className="risk-item" key={index}>

        <div className="risk-item-header">

          <h4>{scenario.scenario} Scenario</h4>

        </div>

        <p>{scenario.description}</p>

        <p>
          <strong>Possible impact:</strong>{' '}
          {scenario.possible_impact}
        </p>

      </div>

    ));
  };

  return (

    <div className="risk-analysis-container">

      {/* HEADER */}

      <div className="risk-page-header">

        <div>
          <h2>Risk Analysis Report</h2>

          <p>
            {company.name} ({company.symbol})
          </p>

          <p>
            Analysis Period: {period}
          </p>
        </div>

        <div className="risk-header-buttons">

          <button
            className="risk-reset-button"
            onClick={handleReset}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : '↻ Reset'}
          </button>

          <button
            className="risk-back-button"
            onClick={onBack}
          >
            ← Back
          </button>

        </div>

      </div>

      {/* LOADING */}

      {loading && (

        <div className="risk-loading">

          <div className="risk-spinner"></div>

          <h3>Risk Analysis in Progress</h3>

          <p>
            The Risk Analysis Agent is processing historical
            and financial information.
          </p>

          <p>Please wait...</p>

        </div>

      )}

      {/* ERROR */}

      {error && !loading && (

        <div className="risk-error">

          <h3>Unable to Generate Risk Report</h3>

          <p>{error}</p>

          <button onClick={handleReset}>
            Try Again
          </button>

        </div>

      )}

      {/* RISK REPORT */}

      {riskReport && !loading && (

        <div className="risk-report">

          {/* OVERALL RISK */}

          <div className="risk-overview-card">

            <h3>Overall Risk Assessment</h3>

            <span
              className={`overall-risk-badge ${getRiskClass(
                riskReport.overall_risk
              )}`}
            >
              {riskReport.overall_risk}
            </span>

            <p>{riskReport.risk_summary}</p>

          </div>

          {/* KEY METRICS */}

          <div className="risk-metrics-grid">

            <div className="risk-metric-card">

              <h3>Historical Volatility</h3>

              <h2>
                {formatValue(riskReport.historical_volatility?.value)}
                {riskReport.historical_volatility?.value !== null &&
                riskReport.historical_volatility?.value !== undefined
                  ? '%'
                  : ''}
              </h2>

              <span
                className={getRiskClass(
                  riskReport.historical_volatility?.risk_level
                )}
              >
                {riskReport.historical_volatility?.risk_level || 'N/A'}
              </span>

              <p>
                {riskReport.historical_volatility?.method}
              </p>

            </div>

            <div className="risk-metric-card">

              <h3>Maximum Drawdown</h3>

              <h2>
                {formatValue(
                  riskReport.maximum_drawdown?.maximum_drawdown
                )}
                {riskReport.maximum_drawdown?.maximum_drawdown !== null &&
                riskReport.maximum_drawdown?.maximum_drawdown !== undefined
                  ? '%'
                  : ''}
              </h2>

              <span
                className={getRiskClass(
                  riskReport.maximum_drawdown?.risk_level
                )}
              >
                {riskReport.maximum_drawdown?.risk_level || 'N/A'}
              </span>

              <p>
                Peak: {formatValue(
                  riskReport.maximum_drawdown?.peak_price
                )}
              </p>

              <p>
                Trough: {formatValue(
                  riskReport.maximum_drawdown?.trough_price
                )}
              </p>

              <p>
                Peak Date: {formatValue(
                  riskReport.maximum_drawdown?.peak_date
                )}
              </p>

              <p>
                Trough Date: {formatValue(
                  riskReport.maximum_drawdown?.trough_date
                )}
              </p>

            </div>

          </div>

          {/* FINANCIAL RISKS */}

          <section className="risk-section">

            <h3>Financial Risks</h3>

            {renderFinancialRisks(riskReport.financial_risks)}

          </section>

          {/* SECTOR RISKS */}

          <section className="risk-section">

            <h3>Sector Risks</h3>

            {renderFinancialRisks(riskReport.sector_risks)}

          </section>

          {/* ALTERNATIVE SCENARIOS */}

          <section className="risk-section">

            <h3>Alternative Scenarios</h3>

            {renderScenarios(riskReport.alternative_scenarios)}

          </section>

          {/* CONFLICTING FINDINGS */}

          <section className="risk-section">

            <h3>Conflicting Findings</h3>

            {renderTextList(
              riskReport.conflicting_findings,
              'No conflicting findings are currently available.'
            )}

          </section>

          {/* MISSING INFORMATION */}

          <section className="risk-section">

            <h3>Missing Information</h3>

            {renderTextList(
              riskReport.missing_information,
              'No missing information was reported.'
            )}

          </section>

          {/* UNCERTAINTIES */}

          <section className="risk-section">

            <h3>Uncertainties and Limitations</h3>

            {renderTextList(
              riskReport.uncertainties_and_limitations,
              'No additional limitations were reported.'
            )}

          </section>

        </div>

      )}

    </div>

  );
}

export default RiskAnalysis;
