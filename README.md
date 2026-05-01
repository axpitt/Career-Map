# � CareerMap AI

**AI-Powered Resume Analysis & Career Guidance Platform**

CareerMap AI analyzes your resume using advanced AI to provide personalized career insights, skill assessments, and targeted job recommendations. Built with FastAPI backend and modern web frontend.

## ✨ Features

- **AI Resume Analysis**: GPT-4 powered analysis of skills, experience, and career level
- **Personalized Recommendations**: Targeted company suggestions based on your location
- **Career Level Assessment**: Beginner → Intermediate → Strong progression tracking
- **Skill Gap Analysis**: Identify strengths and areas for improvement
- **Modern UI**: Beautiful, responsive interface with drag-and-drop file upload
- **Production Ready**: Secure, scalable architecture with proper error handling

## 🏗️ Architecture

```
career_map_ai/
├── backend/              # FastAPI application
│   ├── main.py          # Application entry point
│   ├── config.py        # Configuration management
│   ├── logging_config.py # Structured logging
│   ├── middleware/      # Security & rate limiting
│   ├── models/          # Pydantic response models
│   └── services/        # Business logic (AI, PDF processing)
├── frontend/            # Static web application
│   ├── index.html       # Main HTML
│   ├── script.js        # Frontend logic
│   └── styles.css       # Modern styling
├── .env.example         # Environment template
├── DEPLOYMENT.md        # Deployment guide
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key
- Git

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd career_map_ai
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

2. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Run the backend**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

4. **Open the frontend**:
   - Open `frontend/index.html` in your browser
   - Or serve with a local server: `python -m http.server 3000`

5. **Test the application**:
   - Upload a PDF resume
   - Enter your city
   - Click "Analyze My Resume"

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (with defaults)
APP_NAME=CareerMap AI
DEBUG=true
LOG_LEVEL=INFO
SECRET_KEY=your_secret_key_here
# Optional: enable backend API key auth if you are using a secure server or proxy.
# For public static frontend builds, do not expose this key in browser-side code.
API_KEY=your_api_key_here
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW_MINUTES=60
MAX_FILE_SIZE_MB=10
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 📦 API Documentation

### POST /analyze

Analyze a resume PDF and return career insights.

**Request**: `multipart/form-data`
- `file`: PDF resume file (max 10MB)
- `city`: User's city for location-based recommendations

**Response**: JSON
```json
{
  "score": 85,
  "level": "Intermediate",
  "strengths": ["Python", "FastAPI", "React"],
  "weaknesses": ["Cloud Architecture", "DevOps"],
  "companies_to_apply": ["Google", "Microsoft", "Amazon"],
  "upgrade_target_companies": ["Netflix", "Stripe"],
  "upgrade_requirements": ["AWS Certification", "Kubernetes experience"]
}
```

## 🛡️ Security Features

- **API Key Authentication**: Secure backend access
- **Rate Limiting**: Prevent abuse (10 requests/hour default)
- **File Validation**: PDF-only uploads with size limits
- **CORS Protection**: Configurable origin restrictions
- **Input Sanitization**: Comprehensive validation
- **Structured Logging**: Security event monitoring

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete production deployment instructions.

**Recommended Stack**:
- **Backend**: Render (Python hosting)
- **Frontend**: Vercel (static site hosting)
- **AI**: OpenAI GPT-4
- **File Processing**: pdfplumber

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/  # (when tests are added)
```

### Manual Testing
1. Upload various PDF formats
2. Test error scenarios (invalid files, missing API keys)
3. Verify rate limiting
4. Test CORS restrictions

## 📊 Performance

- **Response Time**: < 30 seconds for typical resumes
- **File Size Limit**: 10MB PDFs
- **Rate Limit**: 10 requests/hour (configurable)
- **Concurrent Users**: Scales with hosting provider

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **FastAPI** for the excellent web framework
- **pdfplumber** for PDF text extraction
- **Render/Vercel** for hosting platforms

---

**Built with ❤️ for developers seeking career advancement**
