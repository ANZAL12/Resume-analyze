import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const upload = async () => {
    const fd = new FormData();
    fd.append("file", file);
    try {
      const r = await axios.post("http://127.0.0.1:8000/analyze", fd);
      setResult(r.data);
    } catch (err) {
      alert("Error connecting to backend");
      console.error(err);
    }
  };

  const downloadResume = async () => {
    const fd = new FormData();
    fd.append("file", file);
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/generate_resume",
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
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>AI Resume Analyzer</h2>
      <input
        type="file"
        accept=".pdf,.docx"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={upload} disabled={!file} style={{ marginLeft: 10 }}>
        Analyze
      </button>
      <button onClick={downloadResume} disabled={!file} style={{ marginLeft: 10 }}>
        Download Improved Resume
      </button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Text Snippet</h3>
          <p>{result.text_snippet}</p>

          <h3>Detected Skills</h3>
          <ul>{result.skills_detected.map((s) => <li key={s}>{s}</li>)}</ul>

          <h3>Sections Found</h3>
          <ul>{result.found_sections.map((s) => <li key={s}>{s}</li>)}</ul>

          <h3>Resume Completeness</h3>
          <div style={{ width: "300px", background: "#ddd", borderRadius: 5 }}>
            <div
              style={{
                width: `${result.completeness}%`,
                background: "green",
                height: "20px",
                borderRadius: 5,
              }}
            ></div>
          </div>
          <p>{result.completeness}%</p>

          <h3>Suggestions</h3>
          <ul>{result.suggestions.map((s) => <li key={s}>{s}</li>)}</ul>
        </div>
      )}
    </div>
  );
}

export default App;
