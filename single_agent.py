from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_pr_full(all_patches: str) -> str:
    """
    Analyze complete PR with all file patches using a single comprehensive prompt.
    Performs multi-dimensional analysis: logic, security, readability, and performance.
    
    Args:
        all_patches: Combined string of all file patches with filenames
    
    Returns:
        Complete PR review in JSON format with detailed categorized analysis
    """
    prompt = f"""You are a single autonomous PR review agent responsible for analyzing a pull request across multiple dimensions.

Perform a complete multi-category analysis of the given PR including:
1. **PR Summary**
2. **Risk Scoring** (0–10)
3. **Logic Review**
4. **Security Review**
5. **Readability Review**
6. **Performance Review**
7. **Overall Summary and Recommendation**

==========================
ANALYSIS REQUIREMENTS
==========================

For each file in the PR, analyze ONLY the changed lines in the PATCH and categorize issues into:

**LOGIC REVIEW:**
- Algorithmic errors or incorrect logic
- Edge case handling issues
- Control flow problems
- Incorrect conditions or loops
- Missing validations
- Type mismatches
- Undefined behavior

**SECURITY REVIEW:**
- Authentication/authorization issues
- Input validation vulnerabilities
- SQL injection risks
- XSS vulnerabilities
- Sensitive data exposure
- Insecure cryptography
- Path traversal risks
- API security issues
- Token/credential exposure

**READABILITY REVIEW:**
- Poor naming conventions
- Missing documentation
- Complex nested structures
- Unclear variable names
- Missing comments for complex logic
- Code duplication
- Inconsistent formatting
- Magic numbers/strings

**PERFORMANCE REVIEW:**
- Inefficient algorithms (O(n²) where O(n) possible)
- Unnecessary loops or iterations
- Memory leaks or excessive allocations
- Missing indexes or caching
- Blocking operations
- Inefficient data structures
- Redundant computations

==========================
SEVERITY LEVELS
==========================

- **critical**: Security vulnerabilities, data loss risks, breaking bugs
- **high**: Major logic errors, performance bottlenecks, significant issues
- **medium**: Code quality issues, minor bugs, moderate improvements
- **low**: Style issues, suggestions, minor optimizations

==========================
REQUIRED JSON OUTPUT FORMAT
==========================

Return ONLY valid JSON in this EXACT structure:

{{
  "pr_summary": "<2-3 sentence summary of what this PR changes>",
  "risk_score": <number 0-10>,
  "logic_review": {{
    "summary": {{
      "total_files": <int>,
      "files_with_issues": <int>,
      "total_issues": <int>,
      "critical_issues": <int>,
      "high_issues": <int>,
      "medium_issues": <int>,
      "low_issues": <int>
    }},
    "files": [
      {{
        "filename": "<string>",
        "status": "<added|modified|deleted|renamed>",
        "issues": [
          {{
            "line": <line number or null>,
            "severity": "<critical|high|medium|low>",
            "issue": "<clear issue description>",
            "suggestion": "<actionable fix suggestion>",
            "fixed_code": "<corrected code or null>"
          }}
        ],
        "issue_count": <int>
      }}
    ]
  }},
  "security_review": {{
    "summary": {{
      "total_files": <int>,
      "files_with_issues": <int>,
      "total_issues": <int>,
      "critical_issues": <int>,
      "high_issues": <int>,
      "medium_issues": <int>,
      "low_issues": <int>
    }},
    "files": [
      {{
        "filename": "<string>",
        "status": "<added|modified|deleted|renamed>",
        "issues": [
          {{
            "line": <line number or null>,
            "severity": "<critical|high|medium|low>",
            "issue": "<clear issue description>",
            "suggestion": "<actionable fix suggestion>",
            "fixed_code": "<corrected code or null>"
          }}
        ],
        "issue_count": <int>
      }}
    ]
  }},
  "readability_review": {{
    "summary": {{
      "total_files": <int>,
      "files_with_issues": <int>,
      "total_issues": <int>,
      "critical_issues": <int>,
      "high_issues": <int>,
      "medium_issues": <int>,
      "low_issues": <int>
    }},
    "files": [
      {{
        "filename": "<string>",
        "status": "<added|modified|deleted|renamed>",
        "issues": [
          {{
            "line": <line number or null>,
            "severity": "<critical|high|medium|low>",
            "issue": "<clear issue description>",
            "suggestion": "<actionable fix suggestion>",
            "fixed_code": "<corrected code or null>"
          }}
        ],
        "issue_count": <int>
      }}
    ]
  }},
  "performance_review": {{
    "summary": {{
      "total_files": <int>,
      "files_with_issues": <int>,
      "total_issues": <int>,
      "critical_issues": <int>,
      "high_issues": <int>,
      "medium_issues": <int>,
      "low_issues": <int>
    }},
    "files": [
      {{
        "filename": "<string>",
        "status": "<added|modified|deleted|renamed>",
        "issues": [
          {{
            "line": <line number or null>,
            "severity": "<critical|high|medium|low>",
            "issue": "<clear issue description>",
            "suggestion": "<actionable fix suggestion>",
            "fixed_code": "<corrected code or null>"
          }}
        ],
        "issue_count": <int>
      }}
    ]
  }},
  "overall_summary": {{
    "total_files_reviewed": <int>,
    "total_issues_found": <int>,
    "breakdown": {{
      "logic_issues": <int>,
      "security_issues": <int>,
      "readability_issues": <int>,
      "performance_issues": <int>
    }},
    "severity_breakdown": {{
      "critical": <int>,
      "high": <int>,
      "medium": <int>,
      "low": <int>
    }}
  }},
  "recommendation": "<✅ APPROVED: No issues found. This PR looks good! | ✓ ACCEPTABLE: Minor issues found. Review and address if needed. | ⚠️ CAUTION: Multiple issues found. Consider addressing them before merging. | ⚠️ WARNING: This PR has high-severity issues. Review and fix before merging. | ❌ CRITICAL: This PR has critical security issues. DO NOT MERGE until resolved.>"
}}

==========================
CRITICAL RULES
==========================

1. ONLY analyze changed lines in the patches (lines starting with + or -)
2. Each file must appear in ALL four review categories (logic, security, readability, performance)
3. If a file has no issues in a category, set "issues": [] and "issue_count": 0
4. DO NOT include markdown code blocks or explanations outside JSON
5. Keep descriptions concise and actionable
6. Calculate all summary counts accurately
7. Ensure recommendation matches severity breakdown:
   - critical > 0 → ❌ CRITICAL
   - high > 0 → ⚠️ WARNING
   - total > 10 → ⚠️ CAUTION
   - total > 0 → ✓ ACCEPTABLE
   - total = 0 → ✅ APPROVED

==========================
PR FILE PATCHES START HERE
==========================

{all_patches}
"""
    
    response = client.models.generate_content(
        model="models/gemini-1.5-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json"
        )
    )
    
    return response.text



