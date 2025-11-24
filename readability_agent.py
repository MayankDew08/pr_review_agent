from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY_READABILITY"))


def analyze_file_readability(filename: str, patch: str) -> list:
    """
    Analyze readability and maintainability of a single file's code changes.
    
    Args:
        filename: Name of the file being reviewed
        patch: The diff patch content
    
    Returns:
        List of readability issues in JSON format
    """
    prompt = f"""You are a Readability Review Agent for GitHub Pull Requests.

Your task is to analyze ONLY the READABILITY and MAINTAINABILITY aspects of the code changes in the PATCH below.

Identify issues related to:
- unclear or confusing variable names
- overly complex expressions
- long nested blocks that reduce clarity
- inconsistent indentation or spacing
- missing comments where needed
- poor function or class structure
- magic numbers or unclear constants
- duplicated code
- unclear control flow
- ambiguous or misleading naming
- too much logic inside one line

Input:
File: {filename}

Patch:
{patch}

Rules:
1. Consider ONLY changed lines (lines starting with + or -).
2. Ignore logic bugs, security issues, and performance problems.
3. Focus strictly on readability, clarity, maintainability, naming, structure.
4. Reference the corresponding line number.
5. If no readability issues exist, return [].

Return STRICT JSON ONLY, in this exact format:

[
  {{
    "line": <line number or null>,
    "severity": "<low|medium|high>",
    "issue": "<readability problem>",
    "suggestion": "<how to improve clarity>",
    "fixed_code": "<optional improved code or null>"
  }}
]

Important:
- Do NOT include markdown.
- Do NOT give explanations outside JSON.
- Keep issue and suggestion short, clear, and actionable."""
    
    response = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json"
        )
    )
    
    return response.text



