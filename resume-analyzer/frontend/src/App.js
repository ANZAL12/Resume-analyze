import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");
  const [comparisonMode, setComparisonMode] = useState(false);
  const [comparisonFiles, setComparisonFiles] = useState([]);
  const [comparisonResult, setComparisonResult] = useState(null);

  const upload = async () => {
    setLoading(true);
    const fd = new FormData();
    fd.append("file", file);
    try {
      const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
      const r = await axios.post(`${API_URL}/analyze`, fd);
      setResult(r.data);
    } catch (err) {
      alert("Error connecting to backend");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const downloadResume = async () => {
    setDownloading(true);
    const fd = new FormData();
    fd.append("file", file);
    try {
      const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
      const response = await axios.post(
        `${API_URL}/generate_resume`,
        fd,
        { responseType: "blob" }
      );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "improved_resume.pdf");
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error(err);
      alert("Error generating resume PDF");
    } finally {
      setDownloading(false);
    }
  };

  const exportAnalysis = async () => {
    try {
      const fd = new FormData();
      fd.append("file", file);
      const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
      const response = await axios.post(`${API_URL}/analysis/export`, fd);
      
      const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "resume_analysis.json");
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error(err);
      alert("Error exporting analysis");
    }
  };

  const compareResumes = async () => {
    if (comparisonFiles.length < 2) {
      alert("Please select at least 2 files for comparison");
      return;
    }
    
    setLoading(true);
    const fd = new FormData();
    comparisonFiles.forEach(file => fd.append("files", file));
    
    try {
      const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
      const response = await axios.post(`${API_URL}/analysis/compare`, fd);
      setComparisonResult(response.data);
    } catch (err) {
      console.error(err);
      alert("Error comparing resumes");
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "#10b981";
    if (score >= 60) return "#f59e0b";
    return "#ef4444";
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return "Excellent";
    if (score >= 60) return "Good";
    if (score >= 40) return "Fair";
    return "Needs Improvement";
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <div className="logo">
            <span className="logo-icon">📄</span>
            <h1>AI Resume Analyzer</h1>
          </div>
          <p className="subtitle">Upload your resume and get intelligent analysis with improvement suggestions</p>
        </header>

        <div className="upload-section">
          <div className="mode-toggle">
            <button 
              className={`mode-btn ${!comparisonMode ? 'active' : ''}`}
              onClick={() => setComparisonMode(false)}
            >
              📄 Single Analysis
            </button>
            <button 
              className={`mode-btn ${comparisonMode ? 'active' : ''}`}
              onClick={() => setComparisonMode(true)}
            >
              📊 Compare Resumes
            </button>
          </div>

          {!comparisonMode ? (
            <>
              <div className="file-upload">
                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={(e) => setFile(e.target.files[0])}
                  id="file-input"
                  className="file-input"
                />
                <label htmlFor="file-input" className="file-label">
                  <div className="upload-icon">📁</div>
                  <div className="upload-text">
                    <strong>Choose Resume File</strong>
                    <span>PDF or DOCX format</span>
                  </div>
                </label>
              </div>

              {file && (
                <div className="file-selected">
                  <span className="file-icon">📄</span>
                  <span className="file-name">{file.name}</span>
                </div>
              )}

              <div className="action-buttons">
                <button 
                  onClick={upload} 
                  disabled={!file || loading} 
                  className="btn btn-primary"
                >
                  {loading ? (
                    <>
                      <span className="spinner"></span>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <span>🔍</span>
                      Analyze Resume
                    </>
                  )}
                </button>
                
                <button 
                  onClick={downloadResume} 
                  disabled={!file || downloading} 
                  className="btn btn-secondary"
                >
                  {downloading ? (
                    <>
                      <span className="spinner"></span>
                      Generating...
                    </>
                  ) : (
                    <>
                      <span>📥</span>
                      Download Improved Resume
                    </>
                  )}
                </button>

                {result && (
                  <button 
                    onClick={exportAnalysis} 
                    className="btn btn-export"
                  >
                    <span>📊</span>
                    Export Analysis
                  </button>
                )}
              </div>
            </>
          ) : (
            <>
              <div className="comparison-upload">
                <input
                  type="file"
                  accept=".pdf,.docx"
                  multiple
                  onChange={(e) => setComparisonFiles(Array.from(e.target.files))}
                  id="comparison-input"
                  className="file-input"
                />
                <label htmlFor="comparison-input" className="file-label">
                  <div className="upload-icon">📁</div>
                  <div className="upload-text">
                    <strong>Choose Multiple Resumes</strong>
                    <span>Select 2 or more PDF/DOCX files</span>
                  </div>
                </label>
              </div>

              {comparisonFiles.length > 0 && (
                <div className="comparison-files">
                  <h4>Selected Files ({comparisonFiles.length}):</h4>
                  {comparisonFiles.map((file, index) => (
                    <div key={index} className="comparison-file">
                      <span className="file-icon">📄</span>
                      <span className="file-name">{file.name}</span>
                    </div>
                  ))}
                </div>
              )}

              <div className="action-buttons">
                <button 
                  onClick={compareResumes} 
                  disabled={comparisonFiles.length < 2 || loading} 
                  className="btn btn-primary"
                >
                  {loading ? (
                    <>
                      <span className="spinner"></span>
                      Comparing...
                    </>
                  ) : (
                    <>
                      <span>📊</span>
                      Compare Resumes
                    </>
                  )}
                </button>
              </div>
            </>
          )}
        </div>

        {result && !comparisonMode && (
          <div className="results-section">
            <div className="results-header">
              <h2>Analysis Results</h2>
              <div className="score-dashboard">
                <div className="score-item">
                  <span className="score-label">Overall Score</span>
                  <div className="score-circle" style={{background: `linear-gradient(135deg, ${getScoreColor(result.completeness)} 0%, ${getScoreColor(result.completeness)}80 100%)`}}>
                    <span className="score-number">{result.completeness}%</span>
                  </div>
                  <span className="score-description">{getScoreLabel(result.completeness)}</span>
                </div>
                <div className="score-item">
                  <span className="score-label">ATS Score</span>
                  <div className="score-circle" style={{background: `linear-gradient(135deg, ${getScoreColor(result.ats_score)} 0%, ${getScoreColor(result.ats_score)}80 100%)`}}>
                    <span className="score-number">{result.ats_score}%</span>
                  </div>
                  <span className="score-description">{getScoreLabel(result.ats_score)}</span>
                </div>
              </div>
            </div>

            <div className="tabs">
              <button 
                className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                📊 Overview
              </button>
              <button 
                className={`tab ${activeTab === 'skills' ? 'active' : ''}`}
                onClick={() => setActiveTab('skills')}
              >
                🛠️ Skills Analysis
              </button>
              <button 
                className={`tab ${activeTab === 'ats' ? 'active' : ''}`}
                onClick={() => setActiveTab('ats')}
              >
                🎯 ATS Optimization
              </button>
              <button 
                className={`tab ${activeTab === 'content' ? 'active' : ''}`}
                onClick={() => setActiveTab('content')}
              >
                📝 Content Quality
              </button>
            </div>

            <div className="tab-content">
              {activeTab === 'overview' && (
                <div className="overview-grid">
                  <div className="result-card">
                    <div className="card-header">
                      <span className="card-icon">📝</span>
                      <h3>Text Preview</h3>
                    </div>
                    <div className="text-preview">
                      {result.text_snippet}
                    </div>
                  </div>

                  <div className="result-card">
                    <div className="card-header">
                      <span className="card-icon">📋</span>
                      <h3>Sections Analysis</h3>
                    </div>
                    <div className="sections-analysis">
                      <div className="sections-found">
                        <h4>Found Sections ({result.found_sections?.length || 0})</h4>
                        <div className="sections-list">
                          {result.found_sections?.map((section, index) => (
                            <span key={index} className="section-tag found">
                              ✓ {section}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div className="sections-missing">
                        <h4>Missing Sections ({result.missing_sections?.length || 0})</h4>
                        <div className="sections-list">
                          {result.missing_sections?.map((section, index) => (
                            <span key={index} className="section-tag missing">
                              ✗ {section}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="result-card suggestions-card">
                    <div className="card-header">
                      <span className="card-icon">💡</span>
                      <h3>Improvement Suggestions</h3>
                    </div>
                    <div className="suggestions-list">
                      {result.suggestions?.map((suggestion, index) => (
                        <div key={index} className="suggestion-item">
                          <span className="suggestion-icon">✨</span>
                          <span className="suggestion-text">{suggestion}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'skills' && (
                <div className="skills-analysis">
                  {result.skills_by_category && Object.entries(result.skills_by_category).map(([category, skills]) => (
                    <div key={category} className="skill-category">
                      <h3>{category}</h3>
                      <div className="skills-grid">
                        {skills.map((skill, index) => (
                          <div key={index} className="skill-card">
                            <span className="skill-name">{skill.skill}</span>
                            <div className="skill-confidence">
                              <span className="confidence-score">{skill.confidence}</span>
                              <div className="confidence-bar">
                                <div 
                                  className="confidence-fill" 
                                  style={{width: `${skill.confidence * 100}%`}}
                                ></div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'ats' && (
                <div className="ats-analysis">
                  <div className="ats-score-card">
                    <h3>ATS Optimization Score: {result.ats_score}%</h3>
                    <div className="ats-checks">
                      {result.ats_checks && Object.entries(result.ats_checks).map(([check, passed]) => (
                        <div key={check} className={`ats-check ${passed ? 'passed' : 'failed'}`}>
                          <span className="check-icon">{passed ? '✓' : '✗'}</span>
                          <span className="check-label">{check.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="keyword-analysis">
                    <h3>Keyword Density Analysis</h3>
                    {result.keyword_analysis && Object.entries(result.keyword_analysis).map(([keyword, data]) => (
                      <div key={keyword} className="keyword-item">
                        <span className="keyword-name">{keyword}</span>
                        <div className="keyword-metrics">
                          <span>Count: {data.count}</span>
                          <span>Density: {data.density}%</span>
                          <span>Score: {data.score}/100</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'content' && (
                <div className="content-analysis">
                  <div className="content-stats">
                    <div className="stat-card">
                      <span className="stat-value">{result.content_analysis?.word_count || 0}</span>
                      <span className="stat-label">Word Count</span>
                    </div>
                    <div className="stat-card">
                      <span className="stat-value">{result.content_analysis?.action_verb_count || 0}</span>
                      <span className="stat-label">Action Verbs</span>
                    </div>
                    <div className="stat-card">
                      <span className="stat-value">{result.content_analysis?.number_count || 0}</span>
                      <span className="stat-label">Quantifiable Results</span>
                    </div>
                  </div>
                  
                  <div className="content-issues">
                    <h3>Content Issues</h3>
                    {result.content_analysis?.issues?.map((issue, index) => (
                      <div key={index} className="issue-item">
                        <span className="issue-icon">⚠️</span>
                        <span className="issue-text">{issue}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {comparisonResult && comparisonMode && (
          <div className="comparison-results">
            <h2>Resume Comparison Results</h2>
            <div className="comparison-grid">
              {comparisonResult.comparison_results?.map((resume, index) => (
                <div key={index} className="comparison-card">
                  <h3>{resume.filename}</h3>
                  <div className="comparison-metrics">
                    <div className="metric">
                      <span className="metric-label">Skills Count</span>
                      <span className="metric-value">{resume.skills_count}</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">Sections</span>
                      <span className="metric-value">{resume.sections_count}</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">ATS Score</span>
                      <span className="metric-value" style={{color: getScoreColor(resume.ats_score)}}>
                        {resume.ats_score}%
                      </span>
                    </div>
                  </div>
                  <div className="skills-preview">
                    <h4>Top Skills:</h4>
                    <div className="skills-list">
                      {resume.skills?.slice(0, 5).map((skill, skillIndex) => (
                        <span key={skillIndex} className="skill-tag">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
