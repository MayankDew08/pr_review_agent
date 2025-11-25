# AI-Powered GitHub PR Review Agent

A high-performance FastAPI backend that automatically analyzes GitHub Pull Requests using a single multi-task LLM agent. Built for the **Lyzr.ai Backend + GenAI Engineering Challenge**.

## 🎯 Project Overview

This PR Review Agent processes GitHub pull requests through an intelligent backend system that extracts code changes, analyzes them across multiple dimensions, and provides comprehensive feedback—all through a single optimized LLM call.

### Key Features

- **Single Multi-Task LLM Architecture**: Analyzes logic, security, performance, and readability in one API call
- **Async-First Design**: Fully asynchronous FastAPI backend handles multiple concurrent users without blocking
- **GitHub Integration**: Automated extraction of PR details and code diffs via GitHub REST API
- **Intelligent Analysis**: 
  - Logic error detection
  - Security vulnerability scanning
  - Performance bottleneck identification
  - Code readability assessment
- **Structured Output**: JSON responses with severity levels, line-specific issues, auto-fix suggestions, and risk scoring
- **Optimized Performance**: ~78% faster than multi-agent approach (15s vs 67s for identical PR analysis)

## 🏗️ Architecture

### Backend Stack
- **FastAPI**: Modern async web framework for high-performance APIs
- **Pydantic**: Data validation and schema management
- **Google Gemini 1.5 Flash**: Multi-task LLM for comprehensive code analysis
- **GitHub REST API**: Unauthenticated PR data retrieval

### Design Decisions

**Single-Agent vs Multi-Agent Approach**

The initial design used separate specialized agents (logic, security, performance, readability), requiring ~20+ LLM calls per PR analysis. This resulted in:
- High latency (~67 seconds)
- Increased API quota consumption
- Sequential processing bottlenecks

The redesigned **batched single-call architecture** combines all analysis dimensions into one comprehensive prompt, achieving:
- **78% latency reduction** (67s → 15s)
- **95% fewer API calls** (20+ → 1)
- Parallel processing capability
- Improved quota efficiency

### System Flow

```
GitHub PR URL → Validation → GitHub API (PR + Diffs) → Single LLM Agent → Structured Analysis → JSON Response
```

## 🚀 API Endpoints

### Core Endpoints

#### `POST /comprehensive_review/`
Single-call comprehensive PR analysis with multi-dimensional insights.

**Request:**
```json
{
  "url": "https://github.com/owner/repo/pull/123"
}
```

**Response:**
```json
{
  "success": true,
  "pr_summary": "Brief description of changes",
  "risk_score": 3,
  "overall_summary": {
    "total_files_reviewed": 5,
    "total_issues_found": 12,
    "breakdown": {
      "logic_issues": 3,
      "security_issues": 2,
      "readability_issues": 4,
      "performance_issues": 3
    },
    "severity_breakdown": {
      "critical": 0,
      "high": 2,
      "medium": 6,
      "low": 4
    }
  },
  "logic_review": { ... },
  "security_review": { ... },
  "readability_review": { ... },
  "performance_review": { ... },
  "recommendation": "⚠️ WARNING: This PR has high-severity issues.",
  "review_time_seconds": 15.2
}
```

### Additional Endpoints

- `POST /full_review/` - Multi-agent review (4 separate calls)
- `POST /review_logic/` - Logic-focused analysis
- `POST /review_security/` - Security-focused analysis
- `POST /review_readability/` - Readability-focused analysis
- `POST /review_performance/` - Performance-focused analysis
- `POST /get_pr_details/` - Fetch PR metadata
- `POST /get_pr_diffs/` - Retrieve code diffs

## 📊 Performance Metrics

| Metric | Multi-Agent | Single-Agent | Improvement |
|--------|------------|--------------|-------------|
| **Response Time** | ~67s | ~15s | **78% faster** |
| **API Calls** | 20+ | 1 | **95% reduction** |
| **Concurrent Users** | Sequential blocking | Async non-blocking | **Unlimited** |
| **Quota Efficiency** | Low | High | **20x better** |

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- Conda (recommended) or virtualenv
- Gemini API key ([Get one here](https://ai.google.dev/))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/MayankDew08/pr_review_agent.git
cd pr_review_agent
```

2. **Create and activate environment**
```bash
conda create -n pr-agent python=3.12
conda activate pr-agent
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
GEMINI_API_KEY_LOGIC=your_api_key_here
GEMINI_API_KEY_SECURITY=your_api_key_here
GEMINI_API_KEY_READABILITY=your_api_key_here
GEMINI_API_KEY_PERFORMANCE=your_api_key_here
```

5. **Run the server**
```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation
Interactive API docs: `http://127.0.0.1:8000/docs`

## 🌐 Frontend

A minimal frontend is included in the `Frontend/` directory for visual interaction with the API.

**Features:**
- Clean, modern UI with gradient design
- Real-time PR analysis
- Tabbed interface for different review categories
- Color-coded severity indicators
- Auto-fix code suggestions display

**Usage:**
Open `Frontend/index.html` in a browser (ensure backend is running).

## 🔧 Technical Implementation

### URL Validation
```python
- HTTPS-only GitHub URLs
- Domain verification (github.com)
- Path structure validation (/owner/repo/pull/number)
- GitHub naming convention compliance
- PR number format validation
```

### LLM Prompt Engineering

The single-agent prompt includes:
- **Role Definition**: Autonomous PR review agent
- **Analysis Categories**: Logic, Security, Readability, Performance
- **Severity Levels**: Critical, High, Medium, Low
- **Output Schema**: Structured JSON with file-level granularity
- **Rules Enforcement**: Only analyze changed lines, accurate counts, proper recommendations

### Error Handling
- Comprehensive try-catch blocks
- HTTP status codes (400 for validation, 500 for server errors)
- Detailed error messages
- Automatic retry logic for API calls

## 📁 Project Structure

```
pr_review_agent/
├── main.py                    # FastAPI application with async endpoints
├── schemas.py                 # Pydantic models for validation
├── single_agent.py            # Single multi-task LLM agent
├── logic_agent.py             # Individual logic analysis agent
├── security_agent.py          # Individual security analysis agent
├── readability_agent.py       # Individual readability analysis agent
├── performance_agent.py       # Individual performance analysis agent
├── get_repo_details.py        # GitHub API integration
├── response_models.py         # Response formatting utilities
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration (not in repo)
├── .gitignore                 # Git ignore rules
└── Frontend/
    └── index.html             # Minimal web interface
```

## 🎥 Demonstrations

### Final Demo Video
*[Video placeholder - Full system demonstration]*

---

### Backend API Demo
*[Video placeholder - API endpoints and response structure]*

---

## 🔑 Key Achievements

✅ **Single-call architecture** reducing latency by 78%  
✅ **Async backend** supporting unlimited concurrent users  
✅ **Comprehensive analysis** across 4 code quality dimensions  
✅ **Structured JSON output** with actionable insights  
✅ **Production-ready** error handling and validation  
✅ **Clean API design** following RESTful principles  

## 📝 About This Project

Built as part of the **Lyzr.ai Backend + GenAI Engineering Challenge**, this project demonstrates proficiency in:
- Backend architecture and API design
- GenAI integration and prompt engineering
- Performance optimization
- Async programming patterns
- Production-grade error handling

The focus was on building a robust, scalable backend system that leverages LLMs efficiently while maintaining fast response times and clean code architecture.

## 🔗 Links

- **Live Demo**: [Netlify Deployment](https://pr-review-ai.netlify.app/)
- **Lyzr.ai**: [Visit Website](https://www.lyzr.ai/)

## 📄 License

MIT License - See LICENSE file for details

---

**Built with** ⚡ FastAPI • 🤖 Google Gemini • 🐙 GitHub API
