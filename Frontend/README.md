# PR Review Agent - Frontend

A clean, modern web interface for the AI-Powered GitHub PR Review Agent.

## 🎨 Overview

This frontend provides a user-friendly interface to interact with the PR Review Agent backend. Simply paste a GitHub PR link and get comprehensive code analysis across logic, security, performance, and readability dimensions.

## ✨ Features

- **Minimal Input**: Just paste a GitHub PR URL and click analyze
- **Responsive Design**: Modern gradient UI that works on all devices
- **Tabbed Interface**: Organized views for different review categories
- **Severity Indicators**: Color-coded badges (Critical, High, Medium, Low)
- **Risk Scoring**: Visual 1-5 scale for overall PR risk assessment
- **Auto-fix Suggestions**: Line-specific code improvements
- **Real-time Analysis**: Live feedback with loading states

## 🚀 Live Demo

**Deployed URL**: [https://pr-review-ai.netlify.app/](https://pr-review-ai.netlify.app/)

## 📸 Screenshot

![PR Review Agent Frontend](screenshot.png)

## 🛠️ Technology

- **Pure HTML/CSS/JavaScript** - No framework dependencies
- **Responsive CSS Grid** - Modern layout system
- **Fetch API** - Async backend communication
- **Netlify** - Deployment platform

## 🔧 Configuration

The frontend currently requires a **local backend** to function:

- Backend must be running on `http://127.0.0.1:8000`
- Frontend automatically detects local environment
- Backend deployment coming soon

The deployed frontend at Netlify serves as a preview of the UI. To use full functionality, run the backend locally and open `index.html` in your browser.

## 📦 Local Usage

1. Ensure the backend is running:
```bash
cd ..
conda activate pr-agent
python -m uvicorn main:app --reload
```

2. Open `index.html` in your browser:
```bash
# Windows
start index.html

# Or simply double-click the file
```

3. Paste a GitHub PR URL and click "Analyze PR"

## 🎯 Example PR URLs to Try

```
https://github.com/facebook/react/pull/28476
https://github.com/microsoft/vscode/pull/198234
https://github.com/pytorch/pytorch/pull/115678
```

## 📋 Response Categories

The frontend displays analysis across four tabs:

1. **Logic Review** - Code correctness, edge cases, error handling
2. **Security Review** - Vulnerabilities, data exposure, authentication issues
3. **Readability Review** - Code clarity, naming conventions, documentation
4. **Performance Review** - Efficiency, scalability, resource usage

Each category includes:
- File-level breakdown
- Line-specific issues
- Severity levels
- Suggested fixes

## 🎨 UI Components

### Color Scheme
- **Background**: Purple gradient (`#667eea` to `#764ba2`)
- **Cards**: White with subtle shadows
- **Severity Badges**:
  - 🔴 Critical (Dark red)
  - 🟠 High (Orange)
  - 🟡 Medium (Yellow)
  - 🟢 Low (Green)

### Layout
- Centered container (max-width: 1200px)
- Responsive tabs for category navigation
- Collapsible file sections
- Formatted code blocks for suggestions

## 🔗 Related

- **Backend Repository**: [pr_review_agent](https://github.com/MayankDew08/pr_review_agent)
- **API Documentation**: `http://127.0.0.1:8000/docs` (when running locally)

## 📄 License

MIT License - See parent directory LICENSE file

---

**Built for the Lyzr.ai Backend + GenAI Engineering Challenge**
