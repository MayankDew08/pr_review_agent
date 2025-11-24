from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY_SECURITY"))

def analyze_file_security(filename: str, patch: str) -> list:
    """
    Analyze security aspects of a single file's code changes.
    
    Args:
        filename: Name of the file being reviewed
        patch: The diff patch content
    
    Returns:
        List of security issues in JSON format
    """
    prompt = f"""You are a Security Review Agent for GitHub Pull Requests.

Your job is to analyze ONLY the SECURITY aspects of the code changes shown in the PATCH below.

Detect vulnerabilities such as:
- SQL injection
- No input validation / unsanitized user input
- Hardcoded secrets (tokens, passwords, keys)
- Command injection
- Insecure API usage
- Missing authentication / authorization
- Insecure cryptography
- Sensitive data exposure (logging PII)
- Path traversal
- Weak password handling
- Unvalidated redirects
- Insecure file handling

Input:
File: {filename}

Patch:
{patch}

Rules:
1. Consider ONLY the modified lines in the patch.
2. Ignore formatting, readability, or performance issues.
3. Identify ONLY genuine security risks.
4. Reference the correct line numbers.
5. If no issues exist, return [].

Return STRICT JSON in the following format:

[
  {{
    "line": <line number or null>,
    "severity": "<critical|high|medium|low>",
    "issue": "<short security vulnerability>",
    "suggestion": "<how to fix it>",
    "fixed_code": "<minimal corrected code or null>"
  }}
]

Important:
- NO markdown.
- NO comments outside JSON.
- Keep responses short and actionable."""
    
    response = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json"
        )
    )
    
    return response.text



