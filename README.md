# Resume Analyzer

A powerful AI-driven resume analysis tool that provides comprehensive insights, improvement suggestions, and automatically generates structured resumes with professional formatting.

## 🚀 Features

### 📊 Advanced Resume Analysis
- **Skill Detection**: Automatically identifies technical skills, soft skills, and categorizes them
- **Section Analysis**: Detects missing resume sections and provides recommendations
- **ATS Optimization**: Analyzes Applicant Tracking System compatibility and provides scores
- **Content Quality**: Evaluates word count, action verbs, quantifiable results, and keyword density
- **Completeness Score**: Overall resume completeness assessment

### 📄 Resume Generation
- **Structured Resume Creation**: Automatically generates professionally formatted resumes
- **ATS-Friendly Formatting**: Optimized for Applicant Tracking Systems
- **Skill Integration**: Incorporates detected skills into appropriate sections
- **Professional Layout**: Clean, modern design with proper sections

### 🔍 Multiple Analysis Modes
- **Single Resume Analysis**: Detailed analysis of individual resumes
- **Resume Comparison**: Compare multiple resumes side-by-side
- **Export Functionality**: Export analysis results in JSON format

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python**: Core programming language
- **PDF Processing**: pdfplumber for PDF text extraction
- **Document Processing**: python-docx for DOCX file handling
- **PDF Generation**: ReportLab for creating professional PDFs
- **AI Analysis**: Custom algorithms for skill detection and content analysis

### Frontend
- **React**: Modern JavaScript library for building user interfaces
- **Axios**: HTTP client for API communication
- **CSS3**: Advanced styling with gradients, animations, and responsive design

## 📁 Project Structure

```
Resume Analyzer/
├── resume-analyzer/
│   ├── backend/
│   │   ├── main.py              # FastAPI application with all endpoints
│   │   ├── analyzer.py          # Core analysis algorithms and functions
│   │   └── improved_resume.pdf   # Generated resume output
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── App.js           # Main React component
│   │   │   ├── App.css          # Styling and animations
│   │   │   └── index.js         # React entry point
│   │   ├── package.json         # Frontend dependencies
│   │   └── public/              # Static assets
│   └── venv/                    # Python virtual environment
└── RESUME.pdf                   # Sample resume for testing
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Resume-Analyzer
   ```

2. **Backend Setup**
   ```bash
   cd resume-analyzer/backend
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install fastapi uvicorn pdfplumber python-docx reportlab
   
   # Start the backend server
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

3. **Frontend Setup**
   ```bash
   cd resume-analyzer/frontend
   
   # Install dependencies
   npm install
   
   # Start the development server
   npm start
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📖 API Endpoints

### Core Analysis
- `POST /analyze` - Comprehensive resume analysis
- `POST /generate_resume` - Generate analysis report PDF
- `GET /analysis/health` - Health check endpoint

### Advanced Features
- `POST /analysis/compare` - Compare multiple resumes
- `POST /analysis/export` - Export analysis data

## 🎯 How to Use

### Single Resume Analysis
1. **Upload Resume**: Select a PDF or DOCX file
2. **Analyze**: Click "Analyze Resume" to get comprehensive insights
3. **Review Results**: Explore different tabs for detailed analysis
4. **Download**: Get analysis report or structured resume

### Resume Comparison
1. **Switch Mode**: Click "Compare Resumes" tab
2. **Select Files**: Choose 2 or more resume files
3. **Compare**: Click "Compare Resumes" to see side-by-side analysis

## 📊 Analysis Features

### Skills Analysis
- **Programming Languages**: Python, Java, JavaScript, C++, C#, Go, Rust, PHP, Ruby
- **Frameworks & Libraries**: React, Angular, Vue, Django, Flask, Spring, Express
- **Cloud & DevOps**: AWS, Azure, GCP, Docker, Kubernetes, Terraform, Jenkins
- **Data & AI**: Machine Learning, Data Science, SQL, TensorFlow, PyTorch, Pandas, NumPy
- **Soft Skills**: Leadership, Communication, Project Management, Problem Solving

### ATS Optimization
- Contact information detection
- Summary section analysis
- Skills section verification
- Experience section validation
- Education section check
- Quantifiable results identification
- Action verbs analysis
- Proper formatting verification

### Content Quality Metrics
- Word count analysis
- Action verb usage
- Quantifiable achievements
- Keyword density
- Section completeness
- Professional formatting

## 🎨 UI Features

### Modern Design
- **Gradient Backgrounds**: Beautiful color schemes
- **Card-Based Layout**: Clean, organized information display
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Elements**: Hover effects, animations, and transitions

### User Experience
- **Drag & Drop**: Easy file upload interface
- **Progress Indicators**: Loading states and progress bars
- **Tab Navigation**: Organized analysis results
- **Export Options**: Multiple download formats

## 🔧 Configuration

### Backend Configuration
- **CORS Settings**: Configured for React frontend
- **File Upload**: Supports PDF and DOCX formats
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed request/response logging

### Frontend Configuration
- **API Endpoints**: Configurable backend URLs
- **File Validation**: Client-side file type checking
- **State Management**: React hooks for state management

## 📈 Performance

### Backend Performance
- **Fast Processing**: Optimized text extraction and analysis
- **Memory Efficient**: Stream processing for large files
- **Concurrent Requests**: Handles multiple simultaneous analyses

### Frontend Performance
- **Lazy Loading**: Components load as needed
- **Optimized Bundles**: Efficient JavaScript and CSS
- **Caching**: Smart caching for better performance

## 🛡️ Security

### Data Protection
- **File Validation**: Server-side file validation
- **CORS Configuration**: Secure cross-origin requests
- **Error Handling**: No sensitive data in error messages

### Privacy
- **Local Processing**: Files processed locally, not uploaded to external services
- **Temporary Storage**: Generated files are temporary and can be cleaned up
- **No Data Persistence**: No permanent storage of uploaded files

## 🚀 Deployment

### Production Deployment
1. **Backend**: Deploy FastAPI with Gunicorn or similar WSGI server
2. **Frontend**: Build React app and serve with Nginx or Apache
3. **Environment Variables**: Configure production settings
4. **SSL**: Enable HTTPS for secure file uploads

### Docker Deployment
```dockerfile
# Backend Dockerfile
FROM python:3.9
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **React** for the powerful frontend library
- **ReportLab** for PDF generation capabilities
- **pdfplumber** for PDF text extraction
- **python-docx** for DOCX file processing

## 📞 Support

For support, email support@resumeanalyzer.com or create an issue in the repository.

---

**Made with ❤️ for better resumes and career success!**
