import React, { useState } from 'react';
import '../dashboard.css';

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [runStatus, setRunStatus] = useState('');
  const [metrics, setMetrics] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus('Please select a file first.');
      return;
    }
    
    setUploadStatus('Uploading...');
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Upload failed');
      const data = await response.json();
      setUploadStatus(`File uploaded successfully: ${data.filename}`);
    } catch (error) {
      setUploadStatus(`Error: ${error.message}`);
    }
  };

  const handleRunPipeline = async () => {
    if (!file) {
      setRunStatus('Please upload a file first.');
      return;
    }
    
    setRunStatus('Running phase mapping pipeline (this might take a minute)...');
    try {
      const response = await fetch(`http://localhost:8000/api/run-phase-mapping?filename=${file.name}`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error('Pipeline failed');
      const data = await response.json();
      setMetrics(data);
      setRunStatus('Pipeline completed successfully!');
    } catch (error) {
      setRunStatus(`Error: ${error.message}`);
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Phase Mapping Dashboard</h1>
        <p>A complete full-stack solution for voltage-based phase identification</p>
      </header>
      
      <main className="dashboard-content">
        <section className="card upload-section">
          <h2>1. Upload Data</h2>
          <div className="upload-controls">
            <input type="file" accept=".xlsx" onChange={handleFileChange} />
            <button className="primary-btn" onClick={handleUpload}>Upload Excel</button>
          </div>
          {uploadStatus && <p className="status-msg">{uploadStatus}</p>}
        </section>
        
        <section className="card run-section">
          <h2>2. Process Data</h2>
          <button className="run-btn" onClick={handleRunPipeline} disabled={!file || !uploadStatus.includes('successfully')}>
            Run Phase Mapping Pipeline
          </button>
          {runStatus && <p className="status-msg">{runStatus}</p>}
        </section>

        {metrics && (
          <section className="metrics-section">
            <div className="card summary-card">
              <h2>Processing Summary</h2>
              <ul className="metrics-list">
                <li><strong>Consumers Processed:</strong> {metrics.consumers_processed}</li>
                <li><strong>Features Engineered:</strong> {metrics.features_engineered}</li>
                <li><strong>PCA Retained:</strong> {metrics.pca_components}</li>
              </ul>
            </div>
            
            <div className="card metrics-card">
              <h2>Clustering Metrics</h2>
              <ul className="metrics-list">
                <li><strong>Silhouette Score:</strong> {metrics.silhouette_score.toFixed(4)}</li>
                <li><strong>Davies-Bouldin:</strong> {metrics.davies_bouldin.toFixed(4)}</li>
              </ul>
            </div>
            
            <div className="card results-card">
              <h2>Phase Distribution</h2>
              <ul className="metrics-list">
                {Object.entries(metrics.phase_counts).map(([phase, count]) => (
                  <li key={phase}><strong>Phase {phase}:</strong> {count}</li>
                ))}
              </ul>
            </div>

            <div className="card plots-card">
               <h2>Visualizations</h2>
               <div className="plots-grid">
                 <div className="plot-item">
                   <p>PCA Scatter Clusters</p>
                   <img src={`http://localhost:8000/api/results/download/pca_scatter_clusters.png`} alt="PCA Clusters" />
                 </div>
                 <div className="plot-item">
                   <p>Final Phase Distribution</p>
                   <img src={`http://localhost:8000/api/results/download/final_phase_distribution.png`} alt="Phase Distribution" />
                 </div>
               </div>
            </div>

            <div className="card outputs-card">
              <h2>Download Results</h2>
              <a href="http://localhost:8000/api/results/download/final_phase_mapping.csv" className="download-btn" download>Download Final Mapping</a>
              <a href="http://localhost:8000/api/results/download/engineered_features.csv" className="download-btn" download>Download Engineered Features</a>
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
